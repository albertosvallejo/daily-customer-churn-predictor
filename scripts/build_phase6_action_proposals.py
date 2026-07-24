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

from evidence.phase6_integration import build_action_proposals

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Phase 6.4 action proposals from the latest eligible recommendations")
    parser.add_argument("--run-date", dest="run_date", default=None, help="Optional catalog run date in YYYYMMDD format")
    args = parser.parse_args()
    LOGGER.info("Starting Phase 6.4 approval proposal build")
    payload = build_action_proposals(project_root=PROJECT_ROOT, run_date=args.run_date)
    LOGGER.info("Phase 6.4 approval proposal build completed")
    print(json.dumps(payload, indent=2))
