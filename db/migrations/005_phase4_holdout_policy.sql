-- Phase 4 / Block B holdout policy baseline
-- Additive migration: explicit holdout policy window fields for stable attribution.

ALTER TABLE retention_actions
    ADD COLUMN IF NOT EXISTS holdout_assignment_key TEXT;

ALTER TABLE retention_actions
    ADD COLUMN IF NOT EXISTS holdout_window_days INTEGER;

ALTER TABLE retention_actions
    ADD COLUMN IF NOT EXISTS holdout_window_end DATE;

CREATE INDEX IF NOT EXISTS idx_retention_actions_holdout_window_end
    ON retention_actions (holdout_window_end);
