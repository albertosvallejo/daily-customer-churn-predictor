-- Phase 4 / Block B traceability hardening baseline
-- Additive migration: action-traceability fields, holdout flags, and idempotent uniqueness.

ALTER TABLE retention_actions
    ADD COLUMN IF NOT EXISTS holdout BOOLEAN NOT NULL DEFAULT FALSE;

ALTER TABLE retention_actions
    ADD COLUMN IF NOT EXISTS holdout_reason TEXT;

ALTER TABLE retention_actions
    ADD COLUMN IF NOT EXISTS campaign_cycle DATE;

CREATE UNIQUE INDEX IF NOT EXISTS uq_retention_actions_customer_run_action_channel_holdout
    ON retention_actions (customer_unique_id, run_date_tag, action_type, channel, holdout);

CREATE INDEX IF NOT EXISTS idx_retention_actions_campaign_cycle
    ON retention_actions (campaign_cycle);

CREATE INDEX IF NOT EXISTS idx_retention_actions_holdout
    ON retention_actions (holdout);
