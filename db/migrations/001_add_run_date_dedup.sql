-- db/migrations/001_add_run_date_dedup.sql
ALTER TABLE churn_predictions
  ADD COLUMN IF NOT EXISTS run_date     DATE,
  ADD COLUMN IF NOT EXISTS loaded_at    TIMESTAMPTZ DEFAULT NOW();

CREATE UNIQUE INDEX IF NOT EXISTS uq_predictions_customer_run
  ON churn_predictions (customer_unique_id, run_date);
