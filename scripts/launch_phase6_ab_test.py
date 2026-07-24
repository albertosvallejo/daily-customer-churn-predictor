from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from evidence.phase6_integration import launch_ab_test


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Launch a simulated Phase 6.4 A/B test for an approved proposal.")
    parser.add_argument("--proposal-id", required=True, help="Proposal identifier to launch")
    parser.add_argument("--proposal-run-date", default=None, help="Optional proposal run date to disambiguate artifact")
    parser.add_argument("--launched-by", required=True, help="Operator identifier for traceability")
    return parser


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    args = build_parser().parse_args()
    logging.getLogger(__name__).info("Starting Phase 6.4 simulated A/B test launch")
    payload = launch_ab_test(
        {
            "proposal_id": args.proposal_id,
            "proposal_run_date": args.proposal_run_date,
            "launched_by": args.launched_by,
        },
        project_root=PROJECT_ROOT,
    )
    logging.getLogger(__name__).info("Phase 6.4 simulated A/B test launch completed")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
