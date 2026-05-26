import logging
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OPS_DB_URL = os.getenv("CHURN_DB_URL", f"sqlite:///{PROJECT_ROOT / 'data' / 'raw' / 'churn_sqlite_db.sqlite'}")
DEFAULT_SOURCE_DB_URL = os.getenv("SOURCE_DB_URL", f"sqlite:///{PROJECT_ROOT / 'data' / 'raw' / 'churn_sqlite_db.sqlite'}")
CONVERSION_WINDOW_DAYS = int(os.getenv("CONVERSION_WINDOW_DAYS", "14"))


def _ensure_retention_events_table(engine) -> None:
    ddl = """
    CREATE TABLE IF NOT EXISTS retention_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_unique_id TEXT NOT NULL,
        run_date_tag TEXT NOT NULL,
        offer_code_stub TEXT,
        channel TEXT NOT NULL,
        event_type TEXT NOT NULL,
        event_ts TIMESTAMP NOT NULL,
        provider_message_id TEXT,
        coupon_redeemed BOOLEAN DEFAULT FALSE,
        order_id TEXT,
        order_value_brl REAL,
        metadata TEXT
    );
    """
    dedup = """
    CREATE UNIQUE INDEX IF NOT EXISTS uq_retention_events_conversion
      ON retention_events (customer_unique_id, run_date_tag, channel, event_type, order_id);
    """
    with engine.begin() as conn:
        conn.execute(text(ddl))
        conn.execute(text(dedup))
    logger.info("retention_events table ensured")


def _load_candidate_actions(ops_engine) -> pd.DataFrame:
    query = text(
        """
        SELECT DISTINCT customer_unique_id, run_date_tag, coupon_code, executed_at, channel
        FROM retention_actions
        WHERE executed_at IS NOT NULL
        """
    )
    with ops_engine.connect() as connection:
        return pd.read_sql(query, connection)


def _load_orders(source_engine) -> pd.DataFrame:
    query = text(
        """
        SELECT
            c.customer_unique_id,
            o.order_id,
            o.order_purchase_timestamp AS order_ts,
            op.payment_value AS order_value_brl
        FROM orders o
        JOIN customers c
          ON c.customer_id = o.customer_id
        LEFT JOIN order_payments op
          ON op.order_id = o.order_id
        WHERE o.order_purchase_timestamp IS NOT NULL
        """
    )
    with source_engine.connect() as connection:
        orders = pd.read_sql(query, connection)
    orders["order_ts"] = pd.to_datetime(orders["order_ts"], errors="coerce", utc=True)
    return orders.dropna(subset=["order_ts"]).copy()


def detect_conversions(ops_engine, source_engine) -> int:
    actions = _load_candidate_actions(ops_engine)
    if actions.empty:
        logger.info("No retention actions found; nothing to detect")
        return 0

    actions["executed_at"] = pd.to_datetime(actions["executed_at"], errors="coerce", utc=True)
    actions = actions.dropna(subset=["executed_at"]).copy()
    if actions.empty:
        logger.info("No retention actions with executed_at; nothing to detect")
        return 0

    orders = _load_orders(source_engine)
    merged = actions.merge(orders, on="customer_unique_id", how="inner")
    if merged.empty:
        logger.info("No orders match any retention action customers")
        return 0

    merged["window_end"] = merged["executed_at"] + pd.to_timedelta(CONVERSION_WINDOW_DAYS, unit="D")
    eligible = merged[(merged["order_ts"] >= merged["executed_at"]) & (merged["order_ts"] <= merged["window_end"])].copy()
    if eligible.empty:
        logger.info("No conversions found within the %s-day window", CONVERSION_WINDOW_DAYS)
        return 0

    eligible = eligible.sort_values(["customer_unique_id", "run_date_tag", "order_ts"]).drop_duplicates(
        subset=["customer_unique_id", "run_date_tag", "order_id"], keep="first"
    )
    eligible["event_ts"] = eligible["order_ts"].dt.strftime("%Y-%m-%d %H:%M:%S")
    eligible["metadata"] = eligible.apply(
        lambda row: (
            '{"conversion_window_days": %d, "coupon_code": "%s"}'
            % (CONVERSION_WINDOW_DAYS, (row["coupon_code"] or ""))
        ),
        axis=1,
    )

    records = eligible[
        [
            "customer_unique_id",
            "run_date_tag",
            "channel",
            "event_ts",
            "order_id",
            "order_value_brl",
            "metadata",
        ]
    ].copy()
    records["offer_code_stub"] = None
    records["provider_message_id"] = None
    records["coupon_redeemed"] = False
    records["event_type"] = "converted"
    records["channel"] = records["channel"].fillna("conversion_window")

    insert_sql = text(
        """
        INSERT OR IGNORE INTO retention_events (
            customer_unique_id,
            run_date_tag,
            offer_code_stub,
            channel,
            event_type,
            event_ts,
            provider_message_id,
            coupon_redeemed,
            order_id,
            order_value_brl,
            metadata
        ) VALUES (
            :customer_unique_id,
            :run_date_tag,
            :offer_code_stub,
            :channel,
            :event_type,
            :event_ts,
            :provider_message_id,
            :coupon_redeemed,
            :order_id,
            :order_value_brl,
            :metadata
        )
        """
    )

    inserted = 0
    with ops_engine.begin() as conn:
        for record in records.to_dict(orient="records"):
            result = conn.execute(insert_sql, record)
            inserted += result.rowcount or 0
    logger.info("Conversion detection inserted %s new events", inserted)
    return inserted


def main() -> None:
    ops_engine = create_engine(DEFAULT_OPS_DB_URL)
    source_engine = create_engine(DEFAULT_SOURCE_DB_URL)
    _ensure_retention_events_table(ops_engine)
    inserted = detect_conversions(ops_engine, source_engine)
    logger.info("Conversion detection completed with %s inserted rows", inserted)


if __name__ == "__main__":
    main()
