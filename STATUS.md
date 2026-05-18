# STATUS

## Project
Daily Customer Churn Predictor – VivaMarket Brasil

## Current state
Phase 1 / v1.0.0 has been completed and uploaded to GitHub. Phase 2 is now **fully complete**: the canonical `V2C` analytical redesign has been executed through `NB09`, the n8n workflow (V5) has been executed end-to-end in a real production environment (VPS + Docker + Postgres), and the full publication layer has been hardened and synchronized to Drive. The project currently has a locally completed end-to-end flow from modeling to explainability, deployment packaging, orchestration payloads, reporting, README positioning, dependency alignment, and Docker publication support.

## Last completed step
- v1.0.0 is considered published to GitHub by the user after the README, release notes, branding, notebook normalization, and reporting refactor.
- Phase 2 / v2 was specified operationally in the project documentation as a true analytical redesign, not a silent continuation of v1.
- `NB03` was updated and executed with the selected canonical `V2C` formulation:
  - `total_orders >= 2`
  - `tenure_days >= 90`
  - adaptive horizon `1.25x` median gap bounded to `75-150` days
  - fallback horizon `75` days
- The canonical v2 feature base was regenerated locally as `data/processed/churn_features_20260506.parquet`.
- `NB04` was re-executed on that canonical `V2C` base.
- `NB05` was adapted to the canonical `V2C` line, debugged through multiple execution fixes, and executed successfully.
- New diagnostics artifacts produced locally:
  - `data/processed/churn_diagnostics_20260506.csv`
  - `reports/model_diagnostics_20260506.html`
- `NB06` was adapted to the canonical `V2C` line and executed successfully.
- New explainability artifacts produced locally:
  - `data/processed/churn_explainability_20260506.parquet`
  - `data/processed/churn_driver_summary_20260506.csv`
  - `reports/churn_explainability_20260506.html`
- `NB07` was adapted to the canonical `V2C` line and executed successfully.
- New deployment-preparation artifacts produced locally:
  - `models/churn_scoring_package_20260506.joblib`
  - `src/models/churn_scoring.py`
  - `data/processed/churn_inference_smoke_test_20260506.parquet`
- `NB08` was adapted to the canonical `V2C` line and executed successfully.
- New orchestration artifacts produced locally:
  - `data/processed/retention_actions_20260506.parquet`
  - `n8n/n8n_workflow_daily_churn_retention_workflow.json` (V9 — final validated main pipeline)
  - `n8n/n8n_workflow_error_handler_workflow.json` (VivaMarket Error Handler — separate error workflow)
  - `reports/n8n_orchestration_20260506.html`
- `NB09` was adapted to the canonical `V2C` line and executed successfully.
- New reporting artifact produced locally:
  - `reports/churn_monitoring_dashboard_20260506.html`
- Publication-layer hardening was then completed locally:
  - `README.md` rewritten to reflect the canonical V2C candidate state and Phase 2 operational completion
  - `requirements.txt` aligned with actual project dependencies including `psycopg2-binary`
  - `Dockerfile` created for reproducible containerized notebook execution
  - `.dockerignore` updated to exclude SQLite from image context
  - lightweight contract tests added in `tests/test_churn_scoring.py`
  - `RELEASE_NOTES_v1.md` extended with Phase 2 operational completion note
- Asset replacement completed:
  - `assets/images/logo.gif` confirmed as canonical brand asset
  - `assets/images/visual_identity_guide_v1.pdf` confirmed present
- Local publication validation executed successfully:
  - `python3 -m py_compile src/models/churn_scoring.py`
  - `python3 -m unittest tests.test_churn_scoring -v`
- **n8n workflow V9 executed end-to-end in production (2026-05-18) — two-workflow architecture:**
  - **Main pipeline (Daily Churn Retention Actions - V9):** Cron Trigger → Read Predictions (10 items from Postgres) → Read SHAP Explainability (scoring API port 62881) → Merge Data → Risk Switch (high / medium routing) → Merge Risks (10 items) → Generate Coupon → Validate Pre-Send → Send Email + Send Push (OneSignal via n8n Variables) → Log Actions (parameterized bindings) → [Error Workflow via Settings]
  - **Error Handler (VivaMarket Error Handler):** separate two-node workflow (Error Trigger → Send Error Email), connected to V9 through n8n native Error Workflow setting. Adopted to avoid known n8n inline error node auto-wiring issue.
  - All nodes executed successfully with green status
  - Infrastructure validated: VPS (Hostinger, Ubuntu 24.04) + Docker (openclaw-opvz-openclaw-1 + n8n containers) + Postgres (vivamarket DB) + rclone Google Drive mount
  - Docker network connectivity confirmed: n8n connected to `openclaw-opvz_default` network to reach scoring API by hostname
  - Three API endpoints validated post-restart: `/health`, `/explainability/latest`, `/coupons/generate`
  - `churn_predictions` table loaded in Postgres from `retention_actions_20260506.parquet` (3,346 rows, 3,246 with `send_action_flag = TRUE`)
  - Session issues resolved and documented in `_private/tech_doc.md`: rclone mount persistence, API startup after container restart, Docker network isolation, Postgres table creation
- Project workspace and Drive copy re-synchronized and verified after Phase 2 completion.

## Current findings
- The v1 model remained extremely high-recall/high-positive under the original 90-day churn definition.
- The canonical `V2C` base is structurally valid with `9,571` rows, `1,795` unique customers, `14` snapshots, and prevalence around `0.9748`.
- The selected adaptive horizon is now tighter than the first v2 attempt, with bounds `75-150` days and average horizon around `93.64` days.
- `NB04` selected **XGBoost** as the best model again on the canonical `V2C` line.
- On the canonical v2 test split, the selected model reached approximately:
  - `ROC AUC = 0.8016`
  - `Average Precision = 0.9937`
  - `Precision@Top 5% = 1.0000`
  - `Precision@Top 10% = 0.9970`
- `NB05` diagnostics confirm strong ranking in aggregate, with the caveat that the target is still overwhelmingly positive.
- `NB06` explainability shows the score is driven predominantly by frequency, monetary, and recency patterns, yielding action-ready segments through driver grouping, LTV quartiles, recommended offer types, and VIP human-touch flags.
- `NB07` packages the canonical V2C inference logic with percentile-based risk tiers and attached retention rules.
- `NB08` translates the scored population into a concrete retention payload aligned with the confirmed retention-strategy document.
- `NB09` consolidates diagnostics, explainability, and campaign-readiness outputs into a single monitoring dashboard.
- The n8n workflow V9 (two-workflow architecture) is operationally validated: all nodes executed end-to-end successfully in production on 2026-05-18.
- The main unresolved analytical caveat is unchanged: even the winning `V2C` formulation still has a very high positive prevalence.

## Next pending step
1. Push the updated repository to GitHub as the Phase 2 publication, including the updated README, STATUS.md, RELEASE_NOTES_v1.md, requirements.txt, .gitignore, .dockerignore, and the n8n workflow V5 JSON.
2. Consider adding calibration and ROI-aware threshold optimization if the project advances beyond the current portfolio-ready V2C candidate state.
3. Phase 3 scoping: customer-facing delivery layer (Layer 3), automated daily scoring pipeline, automated API startup on container restart.

## Risks / open questions
- The core v2 risk is confirmed empirically: even after filtering to repeat customers with 90+ days of tenure, the current adaptive label still produces a very high positive rate.
- API persistence across container restarts requires a manual rclone remount step; this is documented and acceptable for Phase 2 but should be automated in Phase 3.
- The Docker network connection between n8n and the OpenClaw container must be re-applied if the n8n container is recreated (`docker network connect openclaw-opvz_default n8n`).
- The `scored_date = CURRENT_DATE` filter in the Postgres query should be activated once the daily scoring pipeline is running and populating fresh predictions automatically.
- n8n remains the internal orchestration platform for Phase 2 using a two-workflow architecture (main V9 + VivaMarket Error Handler); a more hardened customer-facing architecture is planned for Phase 3.
- Phase 3 should preserve explicit comparability against v1 and Phase 2 so the portfolio narrative remains traceable.
