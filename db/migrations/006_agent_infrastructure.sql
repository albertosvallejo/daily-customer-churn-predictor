-- Phase 5 / Block G agent shadow-mode infrastructure baseline
-- SQLite-compatible additive migration for the first Block G data surface.

CREATE TABLE IF NOT EXISTS agent_decision_log (
    id TEXT PRIMARY KEY,
    decision_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    decision_type TEXT NOT NULL,
    input_snapshot TEXT,
    agent_decision TEXT NOT NULL,
    human_decision TEXT,
    match BOOLEAN,
    rationale TEXT,
    shadow_mode BOOLEAN NOT NULL DEFAULT TRUE,
    cycle_date DATE NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_adl_cycle_date
    ON agent_decision_log (cycle_date);

CREATE INDEX IF NOT EXISTS idx_adl_decision_type
    ON agent_decision_log (decision_type);
