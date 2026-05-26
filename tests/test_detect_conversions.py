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

from pipeline.detect_conversions import _ensure_retention_events_table, detect_conversions


class TestDetectConversions(unittest.TestCase):
    def test_detect_conversions_inserts_window_matches(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            ops_db = tmpdir_path / "ops.sqlite"
            source_db = tmpdir_path / "source.sqlite"

            ops_engine = create_engine(f"sqlite:///{ops_db}")
            source_engine = create_engine(f"sqlite:///{source_db}")

            with ops_engine.begin() as conn:
                conn.execute(text("CREATE TABLE retention_actions (customer_unique_id TEXT, run_date_tag TEXT, coupon_code TEXT, executed_at TIMESTAMP, channel TEXT);"))
                conn.execute(text("INSERT INTO retention_actions VALUES ('cust_001','20260524','VIVA-AAAA-BBBB','2026-05-24 09:00:00','email');"))
            _ensure_retention_events_table(ops_engine)

            with source_engine.begin() as conn:
                conn.execute(text("CREATE TABLE customers (customer_id TEXT, customer_unique_id TEXT);"))
                conn.execute(text("CREATE TABLE orders (order_id TEXT, customer_id TEXT, order_purchase_timestamp TIMESTAMP);"))
                conn.execute(text("CREATE TABLE order_payments (order_id TEXT, payment_value REAL);"))
                conn.execute(text("INSERT INTO customers VALUES ('c1','cust_001');"))
                conn.execute(text("INSERT INTO orders VALUES ('o1','c1','2026-05-25 10:00:00');"))
                conn.execute(text("INSERT INTO order_payments VALUES ('o1', 123.45);"))

            inserted = detect_conversions(ops_engine, source_engine)
            self.assertEqual(inserted, 1)

            with ops_engine.begin() as conn:
                row = conn.execute(text("SELECT customer_unique_id, run_date_tag, channel, event_type, order_id FROM retention_events")).fetchone()
            self.assertEqual(tuple(row), ("cust_001", "20260524", "email", "converted", "o1"))


if __name__ == "__main__":
    unittest.main()
