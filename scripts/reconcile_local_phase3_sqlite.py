import logging
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, inspect, text

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SQLITE_PATH = PROJECT_ROOT / "data" / "raw" / "churn_sqlite_db.sqlite"
RETENTION_PATH = PROJECT_ROOT / "data" / "processed" / "retention_actions_20260519.parquet"


def load_retention_payload() -> pd.DataFrame:
    logger.info("Loading retention payload from %s", RETENTION_PATH)
    df = pd.read_parquet(RETENTION_PATH).copy()
    run_date_tag = RETENTION_PATH.stem.split("_")[-1]
    df["snapshot_date"] = pd.to_datetime(df["snapshot_date"], errors="raise")
    df["run_date"] = df["snapshot_date"].dt.date.astype(str)
    df["run_id"] = df.get("run_id", f"canonical_v2c_{run_date_tag}")
    df["run_date_tag"] = df.get("run_date_tag", run_date_tag)
    df["model_version"] = df.get("model_version", df.get("version_name", "unknown"))
    df["pipeline_tag"] = df.get("pipeline_tag", "canonical_v2c_phase3")
    df["snapshot_date"] = df["snapshot_date"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df["loaded_at"] = pd.Timestamp.now("UTC").strftime("%Y-%m-%dT%H:%M:%SZ")
    keep = [
        "customer_unique_id",
        "snapshot_key",
        "snapshot_date",
        "run_date",
        "churn_probability",
        "risk_tier",
        "recommended_offer_type",
        "primary_channels",
        "control_group_flag",
        "send_action_flag",
        "offer_code_stub",
        "run_id",
        "run_date_tag",
        "model_version",
        "pipeline_tag",
        "loaded_at",
    ]
    prepared = df[keep].drop_duplicates(subset=["customer_unique_id", "run_date"]).copy()
    logger.info("Prepared %s unique rows for reconciliation", len(prepared))
    return prepared


def ensure_phase3_tables(engine) -> None:
    ddl_predictions = """
    CREATE TABLE IF NOT EXISTS churn_predictions (
        customer_unique_id TEXT NOT NULL,
        snapshot_key TEXT NOT NULL,
        snapshot_date TIMESTAMP NOT NULL,
        run_date DATE NOT NULL,
        churn_probability REAL NOT NULL,
        risk_tier TEXT NOT NULL,
        recommended_offer_type TEXT NOT NULL,
        primary_channels TEXT NOT NULL,
        control_group_flag BOOLEAN NOT NULL,
        send_action_flag BOOLEAN NOT NULL,
        offer_code_stub TEXT NOT NULL,
        run_id TEXT NOT NULL,
        run_date_tag TEXT NOT NULL,
        model_version TEXT NOT NULL,
        pipeline_tag TEXT NOT NULL,
        loaded_at TIMESTAMP NOT NULL
    );
    """
    ddl_opt_outs = """
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
    ddl_skipped = """
    CREATE TABLE IF NOT EXISTS retention_actions_skipped (
        customer_unique_id TEXT NOT NULL,
        reason_code TEXT NOT NULL,
        evaluated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        churn_probability REAL,
        risk_tier TEXT,
        run_id TEXT,
        run_date_tag TEXT,
        details_json TEXT
    );
    """
    ddl_governance = """
    CREATE TABLE IF NOT EXISTS retention_governance_config (
        config_key TEXT PRIMARY KEY,
        config_value TEXT NOT NULL,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """
    with engine.begin() as conn:
        conn.execute(text(ddl_predictions))
        conn.execute(text(ddl_opt_outs))
        conn.execute(text(ddl_skipped))
        conn.execute(text(ddl_governance))
        conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS uq_churn_predictions_customer_run_date ON churn_predictions (customer_unique_id, run_date);"))
        existing = {c['name'] for c in inspect(engine).get_columns('churn_predictions')}
        required = {
            'snapshot_key': 'TEXT',
            'recommended_offer_type': 'TEXT',
            'primary_channels': 'TEXT',
            'control_group_flag': 'BOOLEAN',
            'send_action_flag': 'BOOLEAN',
            'offer_code_stub': 'TEXT',
        }
        for name, kind in required.items():
            if name not in existing:
                conn.execute(text(f"ALTER TABLE churn_predictions ADD COLUMN {name} {kind};"))
        conn.execute(text("INSERT OR IGNORE INTO retention_governance_config (config_key, config_value) VALUES ('SEND_WINDOW_START_BRT','09:00'),('SEND_WINDOW_END_BRT','20:00'),('DAILY_CAP_HIGH','600'),('DAILY_CAP_MEDIUM','1200'),('DAILY_CAP_LOW','2000');"))
    logger.info("Phase 3 support tables ensured")


def reconcile_predictions(engine, prepared: pd.DataFrame) -> None:
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS churn_predictions_phase3_rebuild;"))
        conn.execute(text("""
        CREATE TABLE churn_predictions_phase3_rebuild (
            customer_unique_id TEXT NOT NULL,
            snapshot_key TEXT NOT NULL,
            snapshot_date TIMESTAMP NOT NULL,
            run_date DATE NOT NULL,
            churn_probability REAL NOT NULL,
            risk_tier TEXT NOT NULL,
            recommended_offer_type TEXT NOT NULL,
            primary_channels TEXT NOT NULL,
            control_group_flag BOOLEAN NOT NULL,
            send_action_flag BOOLEAN NOT NULL,
            offer_code_stub TEXT NOT NULL,
            run_id TEXT NOT NULL,
            run_date_tag TEXT NOT NULL,
            model_version TEXT NOT NULL,
            pipeline_tag TEXT NOT NULL,
            loaded_at TIMESTAMP NOT NULL
        );
        """))
    prepared.to_sql("churn_predictions_phase3_rebuild", engine, if_exists="append", index=False)
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS churn_predictions_backup_pre_phase3;"))
        conn.execute(text("ALTER TABLE churn_predictions RENAME TO churn_predictions_backup_pre_phase3;"))
        conn.execute(text("ALTER TABLE churn_predictions_phase3_rebuild RENAME TO churn_predictions;"))
        conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS uq_churn_predictions_customer_run_date ON churn_predictions (customer_unique_id, run_date);"))
        rows = conn.execute(text("SELECT COUNT(*) FROM churn_predictions")).scalar_one()
    logger.info("Reconciled churn_predictions with %s rows", rows)


def main() -> None:
    logger.info("Starting local SQLite Phase 3 reconciliation")
    engine = create_engine(f"sqlite:///{SQLITE_PATH}")
    prepared = load_retention_payload()
    ensure_phase3_tables(engine)
    reconcile_predictions(engine, prepared)
    logger.info("Local SQLite Phase 3 reconciliation completed successfully")


if __name__ == "__main__":
    main()
