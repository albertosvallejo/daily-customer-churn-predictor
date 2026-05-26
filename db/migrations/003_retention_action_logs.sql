-- Phase 3 / v3 action logging baseline
-- Establishes canonical action-attempt and feedback tables for the hardened workflow.

CREATE TABLE IF NOT EXISTS retention_actions (
    id BIGSERIAL PRIMARY KEY,
    customer_unique_id TEXT NOT NULL,
    risk_tier TEXT NOT NULL,
    action_type TEXT NOT NULL,
    channel TEXT NOT NULL DEFAULT 'email_push',
    coupon_code TEXT,
    workflow_execution_id TEXT,
    provider_message_id TEXT,
    execution_status TEXT NOT NULL DEFAULT 'sent',
    executed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    dispatched_at TIMESTAMPTZ,
    churn_probability DOUBLE PRECISION,
    send_action_flag BOOLEAN NOT NULL DEFAULT TRUE,
    run_id TEXT NOT NULL,
    run_date_tag TEXT NOT NULL,
    metadata JSONB
);

CREATE INDEX IF NOT EXISTS idx_retention_actions_customer_run
    ON retention_actions (customer_unique_id, run_date_tag);

CREATE INDEX IF NOT EXISTS idx_retention_actions_dispatched_at
    ON retention_actions (dispatched_at);

CREATE INDEX IF NOT EXISTS idx_retention_actions_execution_status
    ON retention_actions (execution_status);

CREATE TABLE IF NOT EXISTS retention_events (
    id BIGSERIAL PRIMARY KEY,
    customer_unique_id TEXT NOT NULL,
    run_date_tag TEXT NOT NULL,
    offer_code_stub TEXT,
    channel TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_ts TIMESTAMPTZ NOT NULL,
    provider_message_id TEXT,
    coupon_redeemed BOOLEAN DEFAULT FALSE,
    order_id TEXT,
    order_value_brl NUMERIC(10,2),
    metadata JSONB
);

CREATE INDEX IF NOT EXISTS idx_re_customer_run
  ON retention_events (customer_unique_id, run_date_tag);

CREATE INDEX IF NOT EXISTS idx_re_event_type_ts
  ON retention_events (event_type, event_ts);

CREATE UNIQUE INDEX IF NOT EXISTS uq_retention_events_customer_run_type_ts
  ON retention_events (customer_unique_id, run_date_tag, event_type, event_ts);
