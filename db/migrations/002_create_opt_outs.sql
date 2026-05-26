-- db/migrations/002_create_opt_outs.sql
CREATE TABLE IF NOT EXISTS opt_outs (
    id                  BIGSERIAL PRIMARY KEY,
    customer_unique_id  TEXT          NOT NULL,
    channel             TEXT          NOT NULL,  -- email | push | sms | all
    suppressed_at       TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    reason              TEXT          NOT NULL,  -- unsubscribe | bounce | manual | lgpd_request
    suppressed_by       TEXT,                    -- system | operator_id
    reinstated_at       TIMESTAMPTZ              -- NULL until actively reinstated
);

-- Unique active suppression per customer per channel
CREATE UNIQUE INDEX IF NOT EXISTS uq_opt_outs_active
  ON opt_outs (customer_unique_id, channel)
  WHERE reinstated_at IS NULL;

CREATE INDEX IF NOT EXISTS idx_opt_outs_customer
  ON opt_outs (customer_unique_id);
