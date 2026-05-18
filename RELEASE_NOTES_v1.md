# RELEASE NOTES · v1.0.0

## Summary

Version 1.0.0 is the first complete end-to-end baseline of the Daily Customer Churn Predictor for VivaMarket Brasil.

This version was developed under an **ad hoc Spec-Driven Data Science framework** supported by **OpenClaw agents**, with explicit workflow control, notebook execution QA, and operational traceability across the project lifecycle.

It includes:

- full notebook flow from NB01 to NB09;
- temporal churn modeling;
- diagnostics and explainability;
- deployment-preparation code;
- retention-action orchestration artifacts;
- reporting/dashboard outputs;
- a README positioned around the Spec-Driven/OpenClaw/human-supervision methodology;
- expanded documentation of the current modeling approach, model families, feature blocks, and diagnostic logic;
- documented project limitations and a clear path toward v2.

## Delivered scope

- Data cleaning and analytical base creation
- Exploratory churn-oriented analysis
- Snapshot-based feature engineering
- Temporal model training and benchmark comparison
- Evaluation diagnostics
- Churn explainability outputs
- Scoring package preparation
- n8n retention orchestration design
- Reporting/dashboard generation

## Known limitation in v1

The current 90-day churn definition is extremely positive-heavy because the dataset is dominated by one-time buyers. This limits business separability and should be refined in v2.

## Why the version is still valid

Despite the analytical limitation, v1 is a valid baseline because it demonstrates a complete professional workflow, explicit traceability, operational outputs, and clear awareness of the next analytical improvements required.

## Recommended next version

Target the next analytical refinement as **v2** if the churn target definition and eligible population are materially redefined.

Recommended follow-up improvements after the v1 publication baseline:

- probability calibration;
- ROI-aware threshold optimization;
- uplift / incremental-response modeling;
- uncertainty-aware predictions;
- drift and data-quality monitoring;
- model card / decision card documentation;
- experiment tracking / lightweight model registry.

## Local post-v1 hardening note

After the published v1 baseline, the repository was further hardened around the canonical **V2C** candidate line and then synchronized to Drive as a verified backup/publication-ready workspace state.

That local hardening includes:

- completed downstream notebook chain through `NB09` on the canonical V2C formulation;
- deployment packaging aligned with percentile-based V2 operational tiers;
- orchestration payloads aligned with the confirmed retention strategy;
- monitoring dashboard aligned with the canonical V2C outputs;
- dependency hardening in `requirements.txt` including `psycopg2-binary`;
- Docker support via `Dockerfile` and `.dockerignore`;
- lightweight contract tests for `src/models/churn_scoring.py`;
- brand asset cleanup with `assets/images/logo.gif` replacing the previous `logo.png` reference set;
- verified Drive replication of the current project state.

This note is intentionally kept separate from the formal v1 baseline scope so the published baseline remains historically clear while the next release can present the V2C redesign explicitly.

## Phase 2 operational completion note — 2026-05-18

After the V2C analytical hardening, Phase 2 was closed with the successful end-to-end execution of the **n8n workflow V9** in a real production environment, using a two-workflow architecture.

The workflows (`n8n/n8n_workflow_daily_churn_retention_workflow.json` and `n8n/n8n_workflow_error_handler_workflow.json`) were executed and validated on 2026-05-18 against the following production stack:

- VPS: Hostinger, Ubuntu 24.04, IP 187.127.225.147
- Containers: `openclaw-opvz-openclaw-1` (scoring API, port 62881) + `n8n` (orchestration)
- Database: Postgres, `vivamarket` DB, `churn_predictions` table (3,346 rows loaded from `retention_actions_20260506.parquet`)
- Network: n8n connected to `openclaw-opvz_default` Docker network for internal API access

**Main pipeline (Daily Churn Retention Actions - V9) — all 12 nodes executed successfully:**

> Cron Trigger → Read Predictions (10 items) → Read SHAP Explainability → Merge Data → Risk Switch → Merge Risks → Generate Coupon → Validate Pre-Send → Send Email + Send Push → Log Actions + Log Skipped → [Error Workflow via Settings]

**Error Handler (VivaMarket Error Handler) — 2 nodes:**

> Error Trigger → Send Error Email

The two-workflow architecture was adopted after resolving a known n8n issue: the single-workflow pattern with an inline Error Handler node caused the n8n canvas engine to incorrectly auto-wire error connections as main connections. The solution was to move to n8n's native Error Workflow mechanism, connecting a fully independent error handler workflow through the Settings panel of the main V9 workflow.

Key fixes implemented between V5 and V9:
- **OneSignal credentials:** migrated from unsupported `$credentials.x` syntax to n8n Variables (`ONE_SIGNAL_API_KEY`, `ONE_SIGNAL_APP_ID`)
- **Postgres bindings:** parameterized `queryReplacement` added to Log Actions and Log Skipped nodes to properly bind `$1`, `$2`... parameters
- **Error handling:** moved from inline Error Handler node to dedicated `VivaMarket Error Handler` workflow via n8n native Error Workflow setting

**n8n is the internal orchestration platform for Phase 2.** It validates end-to-end operational readiness of the retention pipeline before the customer-facing delivery layer is implemented in Phase 3. The architecture deliberately separates internal pipeline orchestration (Layer 2, n8n) from customer-facing delivery (Layer 3, Phase 3), with the retention payload as the explicit contract between them.

Infrastructure notes documented in `_private/tech_doc.md`.
