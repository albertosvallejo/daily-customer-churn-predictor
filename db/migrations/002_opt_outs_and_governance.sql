-- Phase 3 / v3 governance and suppression baseline

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

CREATE TABLE IF NOT EXISTS retention_governance_config (
    config_key TEXT PRIMARY KEY,
    config_value TEXT NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO retention_governance_config (config_key, config_value) VALUES
    ('SEND_WINDOW_START_BRT', '09:00'),
    ('SEND_WINDOW_END_BRT', '20:00'),
    ('DAILY_CAP_HIGH', '600'),
    ('DAILY_CAP_MEDIUM', '1200'),
    ('DAILY_CAP_LOW', '2000');
