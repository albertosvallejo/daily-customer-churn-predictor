import logging
import os
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DEFAULT_DATABASE_URL = os.getenv("CHURN_DB_URL", f"sqlite:///{PROJECT_ROOT / 'data' / 'raw' / 'churn_sqlite_db.sqlite'}")
MAX_PARQUET_AGE_HOURS = int(os.getenv("MAX_PARQUET_AGE_HOURS", "48"))
REQUIRED_COLUMNS = [
    "customer_unique_id",
    "snapshot_key",
    "snapshot_date",
    "recency_days",
    "total_orders",
    "total_payment_value",
    "orders_30d",
    "orders_90d",
    "observed_target",
    "churn_probability",
    "risk_tier",
    "selected_model",
    "version_name",
    "top_driver_group",
    "recommended_offer_type",
    "recommended_discount_pct",
    "free_shipping_flag",
    "vip_human_touch_flag",
    "ltv_segment",
    "primary_channels",
    "contact_policy",
    "message_focus",
    "control_group_flag",
    "send_action_flag",
    "offer_code_stub",
    "journey_stage_count",
]

TARGET_COLUMNS = [
    "customer_unique_id",
    "snapshot_key",
    "scored_date",
    "recency_days",
    "total_orders",
    "total_payment_value",
    "orders_30d",
    "orders_90d",
    "observed_target",
    "churn_probability",
    "risk_tier",
    "selected_model",
    "version_name",
    "top_driver_group",
    "recommended_offer_type",
    "recommended_discount_pct",
    "free_shipping_flag",
    "vip_human_touch_flag",
    "ltv_segment",
    "primary_channels",
    "contact_policy",
    "message_focus",
    "control_group_flag",
    "send_action_flag",
    "offer_code_stub",
    "journey_stage_count",
    "run_date",
]

VALID_RISK_TIERS = {"HIGH", "MEDIUM", "LOW"}


def _validate_freshness(parquet_path: Path) -> None:
    modified_at = datetime.fromtimestamp(parquet_path.stat().st_mtime, tz=timezone.utc)
    age_hours = (datetime.now(timezone.utc) - modified_at).total_seconds() / 3600
    if age_hours > MAX_PARQUET_AGE_HOURS:
        raise ValueError(
            f"Parquet file {parquet_path.name} is stale ({age_hours:.2f}h old). Max allowed age: {MAX_PARQUET_AGE_HOURS}h"
        )
    logger.info("Freshness check passed for %s (%.2fh old)", parquet_path.name, age_hours)


def _resolve_latest_retention_actions_path() -> Path:
    candidates = sorted(DATA_PROCESSED_DIR.glob("retention_actions_*.parquet"), reverse=True)
    if not candidates:
        raise FileNotFoundError(f"No retention_actions parquet found in {DATA_PROCESSED_DIR}")
    return candidates[0]


def _load_predictions(parquet_path: Path) -> pd.DataFrame:
    logger.info("Loading retention payload from %s", parquet_path)
    df = pd.read_parquet(parquet_path)
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Retention parquet is missing required columns: {missing_columns}")
    invalid_scores = df["churn_probability"].isna() | (df["churn_probability"] < 0) | (df["churn_probability"] > 1)
    if invalid_scores.any():
        raise ValueError(f"Retention parquet contains {int(invalid_scores.sum())} invalid churn_probability values")
    invalid_tiers = sorted({str(value).upper() for value in df["risk_tier"].dropna().unique()} - VALID_RISK_TIERS)
    if invalid_tiers:
        raise ValueError(f"Retention parquet contains unexpected risk_tier values: {invalid_tiers}")
    return df.copy()


def _prepare_frame(df: pd.DataFrame, parquet_path: Path) -> pd.DataFrame:
    prepared = df.copy()
    run_date_series = pd.to_datetime(prepared["snapshot_key"].astype(str), format="%Y%m%d", errors="raise")
    prepared["run_date"] = run_date_series.dt.date.astype(str)
    prepared["scored_date"] = pd.to_datetime(prepared["snapshot_date"], errors="raise").dt.strftime("%Y-%m-%d %H:%M:%S")
    return prepared[TARGET_COLUMNS].drop_duplicates(subset=["customer_unique_id", "run_date"])


def _ensure_table(engine) -> None:
    existing_columns_query = text(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = current_schema()
          AND table_name = 'churn_predictions'
        ORDER BY ordinal_position
        """
    )
    dedup_index = "CREATE UNIQUE INDEX IF NOT EXISTS uq_churn_predictions_customer_run_date ON churn_predictions (customer_unique_id, run_date);"
    with engine.begin() as connection:
        existing_columns = {
            row[0] for row in connection.execute(existing_columns_query).fetchall()
        }
        if not existing_columns:
            raise RuntimeError("Target table churn_predictions does not exist in the current Postgres schema")
        expected_columns = set(TARGET_COLUMNS + ["loaded_at"])
        missing_columns = sorted(expected_columns - existing_columns)
        if missing_columns:
            raise RuntimeError(
                f"Target table churn_predictions is missing required Postgres columns: {missing_columns}"
            )
        connection.execute(text(dedup_index))
    logger.info("Target table churn_predictions validated for Postgres")


def _ensure_opt_outs_table(engine) -> None:
    ddl = """
    CREATE TABLE IF NOT EXISTS opt_outs (
        customer_unique_id TEXT NOT NULL,
        channel TEXT NOT NULL,
        scope TEXT NOT NULL DEFAULT 'channel',
        reason TEXT,
        source TEXT NOT NULL DEFAULT 'manual',
        active BOOLEAN NOT NULL DEFAULT TRUE,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (customer_unique_id, channel)
    );
    """
    with engine.begin() as connection:
        connection.execute(text(ddl))
    logger.info("Suppression table opt_outs ensured")


def _insert_predictions(engine, df: pd.DataFrame) -> int:
    inserted = 0
    insert_sql = text(
        """
        INSERT INTO churn_predictions (
            customer_unique_id,
            snapshot_key,
            scored_date,
            recency_days,
            total_orders,
            total_payment_value,
            orders_30d,
            orders_90d,
            observed_target,
            churn_probability,
            risk_tier,
            selected_model,
            version_name,
            top_driver_group,
            recommended_offer_type,
            recommended_discount_pct,
            free_shipping_flag,
            vip_human_touch_flag,
            ltv_segment,
            primary_channels,
            contact_policy,
            message_focus,
            control_group_flag,
            send_action_flag,
            offer_code_stub,
            journey_stage_count,
            run_date,
            loaded_at
        ) VALUES (
            :customer_unique_id,
            :snapshot_key,
            :scored_date,
            :recency_days,
            :total_orders,
            :total_payment_value,
            :orders_30d,
            :orders_90d,
            :observed_target,
            :churn_probability,
            :risk_tier,
            :selected_model,
            :version_name,
            :top_driver_group,
            :recommended_offer_type,
            :recommended_discount_pct,
            :free_shipping_flag,
            :vip_human_touch_flag,
            :ltv_segment,
            :primary_channels,
            :contact_policy,
            :message_focus,
            :control_group_flag,
            :send_action_flag,
            :offer_code_stub,
            :journey_stage_count,
            :run_date,
            NOW()
        ) ON CONFLICT(customer_unique_id, snapshot_key) DO NOTHING;
        """
    )
    records = df.to_dict(orient="records")
    with engine.begin() as connection:
        for record in records:
            result = connection.execute(insert_sql, record)
            inserted += result.rowcount or 0
    logger.info("Inserted %s new rows into churn_predictions", inserted)
    return inserted


def run(parquet_path: Path | None = None, database_url: str | None = None) -> int:
    effective_path = parquet_path or Path(os.getenv("RETENTION_ACTIONS_PARQUET_PATH", _resolve_latest_retention_actions_path()))
    effective_db_url = database_url or DEFAULT_DATABASE_URL

    if not effective_path.exists():
        raise FileNotFoundError(f"Prediction parquet not found: {effective_path}")

    _validate_freshness(effective_path)
    predictions = _load_predictions(effective_path)
    prepared = _prepare_frame(predictions, effective_path)
    engine = create_engine(effective_db_url)
    _ensure_table(engine)
    _ensure_opt_outs_table(engine)
    return _insert_predictions(engine, prepared)


if __name__ == "__main__":
    try:
        inserted_rows = run()
        logger.info("load_predictions completed successfully with %s inserted rows", inserted_rows)
    except Exception as exc:
        logger.error("load_predictions failed: %s", exc)
        raise
