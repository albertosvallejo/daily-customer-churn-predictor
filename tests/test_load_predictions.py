import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from pipeline.load_predictions import run


class TestLoadPredictions(unittest.TestCase):
    def _build_base_rows(self):
        return [
            {
                "customer_unique_id": "cust_001",
                "snapshot_key": "20260524",
                "snapshot_date": "2026-05-24",
                "churn_probability": 0.91,
                "risk_tier": "HIGH",
                "recommended_offer_type": "reactivacion_fuerte",
                "primary_channels": "email,push",
                "control_group_flag": False,
                "send_action_flag": True,
                "offer_code_stub": "HIGH-20260524-001",
                "run_id": "canonical_v2c_20260524",
                "run_date_tag": "20260524",
            },
            {
                "customer_unique_id": "cust_002",
                "snapshot_key": "20260524",
                "snapshot_date": "2026-05-24",
                "churn_probability": 0.55,
                "risk_tier": "MEDIUM",
                "recommended_offer_type": "reactivacion_media",
                "primary_channels": "email,push",
                "control_group_flag": False,
                "send_action_flag": True,
                "offer_code_stub": "MED-20260524-002",
                "run_id": "canonical_v2c_20260524",
                "run_date_tag": "20260524",
            },
        ]

    def test_loader_inserts_rows_and_creates_opt_outs_table(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            parquet_path = tmpdir_path / "retention_actions_20260524.parquet"
            db_path = tmpdir_path / "churn.sqlite"
            df = pd.DataFrame(self._build_base_rows())
            df.to_parquet(parquet_path, index=False)

            inserted = run(parquet_path=parquet_path, database_url=f"sqlite:///{db_path}")
            self.assertEqual(inserted, 2)

            engine = create_engine(f"sqlite:///{db_path}")
            with engine.begin() as connection:
                count = connection.execute(text("SELECT COUNT(*) FROM churn_predictions")).scalar_one()
                opt_outs_exists = connection.execute(
                    text("SELECT name FROM sqlite_master WHERE type='table' AND name='opt_outs'")
                ).scalar_one()

            self.assertEqual(count, 2)
            self.assertEqual(opt_outs_exists, "opt_outs")

    def test_loader_backfills_missing_run_metadata_from_filename(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            parquet_path = tmpdir_path / "retention_actions_20260524.parquet"
            db_path = tmpdir_path / "churn.sqlite"
            rows = self._build_base_rows()
            for row in rows:
                row.pop("run_id")
                row.pop("run_date_tag")
            pd.DataFrame(rows).to_parquet(parquet_path, index=False)

            inserted = run(parquet_path=parquet_path, database_url=f"sqlite:///{db_path}")
            self.assertEqual(inserted, 2)

            engine = create_engine(f"sqlite:///{db_path}")
            with engine.begin() as connection:
                values = connection.execute(text("SELECT DISTINCT run_id, run_date_tag FROM churn_predictions")).fetchall()

            self.assertEqual(values, [("canonical_v2c_20260524", "20260524")])


if __name__ == "__main__":
    unittest.main()
