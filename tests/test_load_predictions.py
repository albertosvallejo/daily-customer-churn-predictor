import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from pipeline.load_predictions import _load_predictions, _prepare_frame


class TestLoadPredictions(unittest.TestCase):
    def _build_base_rows(self):
        return [
            {
                "customer_unique_id": "cust_001",
                "snapshot_key": "20260524",
                "snapshot_date": "2026-05-24",
                "recency_days": 120,
                "total_orders": 5,
                "total_payment_value": 420.5,
                "orders_30d": 1,
                "orders_90d": 2,
                "observed_target": 1,
                "churn_probability": 0.91,
                "risk_tier": "HIGH",
                "selected_model": "xgboost",
                "version_name": "v2",
                "top_driver_group": "recency",
                "recommended_offer_type": "reactivation_strong",
                "recommended_discount_pct": 20,
                "free_shipping_flag": True,
                "vip_human_touch_flag": False,
                "ltv_segment": "HIGH",
                "primary_channels": "email,push",
                "contact_policy": "business_hours",
                "message_focus": "urgency",
                "control_group_flag": False,
                "send_action_flag": True,
                "offer_code_stub": "HIGH-20260524-001",
                "journey_stage_count": 1,
            },
            {
                "customer_unique_id": "cust_002",
                "snapshot_key": "20260524",
                "snapshot_date": "2026-05-24",
                "recency_days": 75,
                "total_orders": 3,
                "total_payment_value": 210.0,
                "orders_30d": 0,
                "orders_90d": 1,
                "observed_target": 0,
                "churn_probability": 0.55,
                "risk_tier": "MEDIUM",
                "selected_model": "xgboost",
                "version_name": "v2",
                "top_driver_group": "frequency",
                "recommended_offer_type": "reactivation_medium",
                "recommended_discount_pct": 12,
                "free_shipping_flag": True,
                "vip_human_touch_flag": False,
                "ltv_segment": "MID",
                "primary_channels": "email,push",
                "contact_policy": "business_hours",
                "message_focus": "value",
                "control_group_flag": False,
                "send_action_flag": True,
                "offer_code_stub": "MED-20260524-002",
                "journey_stage_count": 1,
            },
        ]

    def test_load_predictions_accepts_canonical_retention_schema(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            parquet_path = Path(tmpdir) / "retention_actions_20260524.parquet"
            pd.DataFrame(self._build_base_rows()).to_parquet(parquet_path, index=False)

            loaded = _load_predictions(parquet_path)

            self.assertEqual(len(loaded), 2)
            self.assertIn("recommended_discount_pct", loaded.columns)
            self.assertEqual(set(loaded["risk_tier"]), {"HIGH", "MEDIUM"})

    def test_prepare_frame_derives_run_date_and_scored_date(self):
        rows = self._build_base_rows()
        rows.append({**rows[0]})
        df = pd.DataFrame(rows)

        prepared = _prepare_frame(df, Path("retention_actions_20260524.parquet"))

        self.assertEqual(len(prepared), 2)
        self.assertIn("run_date", prepared.columns)
        self.assertIn("scored_date", prepared.columns)
        self.assertEqual(set(prepared["run_date"]), {"2026-05-24"})

    def test_load_predictions_rejects_invalid_risk_tier(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            parquet_path = Path(tmpdir) / "retention_actions_20260524.parquet"
            rows = self._build_base_rows()
            rows[0]["risk_tier"] = "CRITICAL"
            pd.DataFrame(rows).to_parquet(parquet_path, index=False)

            with self.assertRaisesRegex(ValueError, "unexpected risk_tier"):
                _load_predictions(parquet_path)


if __name__ == "__main__":
    unittest.main()
