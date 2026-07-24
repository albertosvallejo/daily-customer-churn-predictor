import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from evidence.phase6_integration import (
    build_action_proposals,
    build_kpi_status_view,
    build_n8n_action_payload,
    launch_ab_test,
    load_action_history,
    record_action_decision,
)


class TestPhase6Integration(unittest.TestCase):
    def test_build_action_proposals_creates_only_eligible_guardrailed_candidates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "data" / "processed").mkdir(parents=True)
            catalog = [
                {
                    "intervention_id": "INT-02",
                    "source_name": "ResearchGate",
                    "ref_id": "[4]",
                    "confidence_score": "medium",
                    "actionability_score": "high",
                    "applicability_to_vivamarket": "medium",
                    "actionable_elements": {"copy": "personalized", "channel": "email", "timing": "followup", "incentive": "offer"},
                    "effect_size_text": "quasi experimental",
                    "quote_or_anchor": "anchor 2",
                },
                {
                    "intervention_id": "INT-05",
                    "source_name": "Vendor",
                    "ref_id": "[15]",
                    "confidence_score": "high",
                    "actionability_score": "high",
                    "applicability_to_vivamarket": "high",
                    "actionable_elements": {"copy": "x", "channel": "sms", "timing": "y", "incentive": "z"},
                    "effect_size_text": "vendor",
                    "quote_or_anchor": "anchor 5",
                },
                {
                    "intervention_id": "INT-01",
                    "source_name": "CXL",
                    "ref_id": "[1]",
                    "confidence_score": "low",
                    "actionability_score": "high",
                    "applicability_to_vivamarket": "high",
                    "actionable_elements": {"copy": "value_first", "channel": "email", "timing": "pre", "incentive": "coupon"},
                    "effect_size_text": "heuristic",
                    "quote_or_anchor": "anchor 1",
                },
            ]
            (root / "data" / "processed" / "evidence_catalog_20260724.json").write_text(json.dumps(catalog), encoding="utf-8")

            payload = build_action_proposals(project_root=root, run_date="20260724")

            self.assertEqual(payload["proposal_count"], 1)
            proposals = json.loads(Path(payload["proposals_path"]).read_text(encoding="utf-8"))
            self.assertEqual(proposals[0]["intervention_id"], "INT-02")
            self.assertEqual(proposals[0]["decision_status"], "pending")

    def test_record_action_decision_updates_history_and_proposal(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "data" / "processed").mkdir(parents=True)
            catalog = [
                {
                    "intervention_id": "INT-02",
                    "source_name": "ResearchGate",
                    "ref_id": "[4]",
                    "confidence_score": "medium",
                    "actionability_score": "high",
                    "applicability_to_vivamarket": "medium",
                    "actionable_elements": {"copy": "personalized", "channel": "email", "timing": "followup", "incentive": "offer"},
                    "effect_size_text": "quasi experimental",
                    "quote_or_anchor": "anchor 2",
                }
            ]
            (root / "data" / "processed" / "evidence_catalog_20260724.json").write_text(json.dumps(catalog), encoding="utf-8")
            proposal_payload = build_action_proposals(project_root=root, run_date="20260724")
            proposals = json.loads(Path(proposal_payload["proposals_path"]).read_text(encoding="utf-8"))
            proposal_id = proposals[0]["proposal_id"]

            record = record_action_decision(
                {
                    "proposal_id": proposal_id,
                    "proposal_run_date": "20260724",
                    "decision_status": "approved",
                    "decision_reason": "Approved for simulated launch",
                    "decided_by": "architect.openclaw@gmail.com",
                },
                project_root=root,
            )

            self.assertEqual(record["decision_status"], "approved")
            history = load_action_history(project_root=root)
            self.assertEqual(len(history), 1)
            self.assertEqual(history[0]["proposal_id"], proposal_id)

    def test_launch_ab_test_builds_kpi_view_and_n8n_payload(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            proposal_id = self._build_single_approved_proposal(root)

            launch_payload = launch_ab_test(
                {
                    "proposal_id": proposal_id,
                    "proposal_run_date": "20260724",
                    "launched_by": "architect.openclaw@gmail.com",
                },
                project_root=root,
            )
            self.assertEqual(launch_payload["status"], "completed")
            self.assertEqual(launch_payload["intervention_id"], "INT-02")
            self.assertIn("verdict", launch_payload)

            kpi_payload = build_kpi_status_view(project_root=root)
            self.assertEqual(kpi_payload["status"], "ok")
            self.assertEqual(kpi_payload["test_count"], 1)
            self.assertEqual(kpi_payload["records"][0]["proposal_id"], proposal_id)

            n8n_payload = build_n8n_action_payload(project_root=root, run_date="20260724")
            self.assertEqual(n8n_payload["status"], "ok")
            self.assertEqual(n8n_payload["action_count"], 1)
            self.assertEqual(n8n_payload["actions"][0]["proposal_id"], proposal_id)

            history = load_action_history(project_root=root)
            self.assertEqual(len(history), 2)
            self.assertEqual(history[0]["event_type"], "decision")
            self.assertEqual(history[1]["event_type"], "ab_test_result")

    def test_launch_ab_test_supports_internal_no_signal_scenario(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            proposal_id = self._build_single_approved_proposal(root)

            launch_payload = launch_ab_test(
                {
                    "proposal_id": proposal_id,
                    "proposal_run_date": "20260724",
                    "launched_by": "architect.openclaw@gmail.com",
                },
                project_root=root,
                test_scenario_key="no_signal",
            )

            self.assertEqual(launch_payload["scenario_key"], "no_signal")
            self.assertFalse(launch_payload["guardrail_breach"])
            self.assertEqual(launch_payload["verdict"], "no_significant_difference")

            kpi_payload = build_kpi_status_view(project_root=root)
            self.assertEqual(kpi_payload["records"][0]["verdict"], "no_significant_difference")
            n8n_payload = build_n8n_action_payload(project_root=root, run_date="20260724")
            self.assertEqual(n8n_payload["actions"][0]["latest_verdict"], "no_significant_difference")
            history = load_action_history(project_root=root)
            self.assertEqual(history[1]["scenario_key"], "no_signal")

    def test_launch_ab_test_supports_internal_guardrail_breach_scenario(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            proposal_id = self._build_single_approved_proposal(root)

            launch_payload = launch_ab_test(
                {
                    "proposal_id": proposal_id,
                    "proposal_run_date": "20260724",
                    "launched_by": "architect.openclaw@gmail.com",
                },
                project_root=root,
                test_scenario_key="guardrail_breach",
            )

            self.assertEqual(launch_payload["scenario_key"], "guardrail_breach")
            self.assertTrue(launch_payload["guardrail_breach"])
            self.assertEqual(launch_payload["verdict"], "not_recommended_guardrail")

            kpi_payload = build_kpi_status_view(project_root=root)
            self.assertEqual(kpi_payload["records"][0]["verdict"], "not_recommended_guardrail")
            n8n_payload = build_n8n_action_payload(project_root=root, run_date="20260724")
            self.assertEqual(n8n_payload["actions"][0]["latest_verdict"], "not_recommended_guardrail")
            history = load_action_history(project_root=root)
            self.assertEqual(history[1]["scenario_key"], "guardrail_breach")

    @staticmethod
    def _build_single_approved_proposal(root: Path) -> str:
        (root / "data" / "processed").mkdir(parents=True)
        catalog = [
            {
                "intervention_id": "INT-02",
                "source_name": "ResearchGate",
                "ref_id": "[4]",
                "confidence_score": "medium",
                "actionability_score": "high",
                "applicability_to_vivamarket": "medium",
                "actionable_elements": {"copy": "personalized", "channel": "email", "timing": "followup", "incentive": "offer"},
                "effect_size_text": "quasi experimental",
                "quote_or_anchor": "anchor 2",
            }
        ]
        (root / "data" / "processed" / "evidence_catalog_20260724.json").write_text(json.dumps(catalog), encoding="utf-8")
        proposal_payload = build_action_proposals(project_root=root, run_date="20260724")
        proposals = json.loads(Path(proposal_payload["proposals_path"]).read_text(encoding="utf-8"))
        proposal_id = proposals[0]["proposal_id"]
        record_action_decision(
            {
                "proposal_id": proposal_id,
                "proposal_run_date": "20260724",
                "decision_status": "approved",
                "decision_reason": "Approved for simulated launch",
                "decided_by": "architect.openclaw@gmail.com",
            },
            project_root=root,
        )
        return proposal_id
