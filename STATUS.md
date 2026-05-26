# STATUS

## Project
Daily Customer Churn Predictor – VivaMarket Brasil

## Current state
Phase 1 / v1.0.0 has been completed and, per user confirmation, already uploaded to GitHub. Phase 2 / v2 has now progressed through `NB09` on the canonical `V2C` line, and the local publication layer has now been hardened as well. On 2026-05-12, local-only Phase 2 / Phase 3 workspace updates resumed with an upgraded NB09 Plotly dashboard, a local model card, an illustrative ROI simulation, and a README expansion that now includes `Project Evolution`. On 2026-05-18, the deferred Drive replication was resumed and the pending workspace/project files were synchronized and verified through the mounted Drive path `/data/gdrive`. Later the same day, the new n8n support API endpoints were implemented locally: `GET /explainability/latest` and `POST /coupons/generate`. After the user approved a port change, the service was standardized on port `62881` and a container-restart watchdog was added through the persistent OpenClaw cron job `ensure-churn-api-62881`. On 2026-05-19 evening, the local Phase 3 minimum-publication layer was revalidated end-to-end through real execution of `NB05`–`NB09`, and the stakeholder-facing Model Card / ROI reporting was strengthened in the canonical local workspace without depending on the current rclone incident.

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
  - `n8n/daily_churn_retention_workflow_20260506.json`
  - `reports/n8n_orchestration_20260506.html`
- `NB09` was adapted to the canonical `V2C` line and executed successfully.
- New reporting artifact produced locally:
  - `reports/churn_monitoring_dashboard_20260506.html`
- Publication-layer hardening was then completed locally:
  - `README.md` rewritten to reflect the canonical V2C candidate state instead of the old v1-only framing
  - critical narrative sections later restored into `README.md` as requested (expanded executive framing, methodology, architecture, file structure, technical stack, methodological notes, roadmap, and contact/license section)
  - `requirements.txt` aligned with actual project dependencies (`shap`, `joblib`, `pyarrow`, `jupyterlab`)
  - `Dockerfile` created for reproducible containerized notebook execution
  - `.dockerignore` created to keep the image context clean
  - lightweight contract tests added in `tests/test_churn_scoring.py`
  - `RELEASE_NOTES_v1.md` extended with a clear local post-v1 hardening note
- The requested asset replacement has now been completed:
  - `assets/images/logo.png` was removed from the project
  - `assets/images/logo.gif` was added from the approved Drive/workspace source
  - remaining branded HTML exports that still referenced `logo.png` were repointed to `logo.gif`
- Local publication validation executed successfully:
  - `python3 -m py_compile src/models/churn_scoring.py`
  - `python3 -m unittest tests.test_churn_scoring -v`
- The project workspace and Drive copy were re-synchronized and verified after the publication hardening and logo replacement updates.
- A final publication sanity pass then re-confirmed:
  - `python3 -m py_compile src/models/churn_scoring.py`
  - `python3 -m unittest tests.test_churn_scoring -v`
  - remote `assets/images/` now contains `logo.gif` and `visual_identity_guide_v1.pdf`, with `logo.png` absent both locally and in Drive.
- The short controlled benchmark artifact remains available locally as `data/processed/churn_variant_benchmark_20260506.csv`.
- New local-only Phase 2 / Phase 3 reporting artifacts were produced on 2026-05-12:
  - `reports/churn_monitoring_dashboard_20260512.html`
  - `reports/model_card_v2_20260512.md`
  - `reports/roi_simulation_20260512.html`
- `notebooks/09_reporting_dashboard.ipynb` was rewritten from the earlier 8-cell lightweight version into a richer Plotly-based stakeholder dashboard notebook and executed successfully in the local workspace.
- `README.md` was expanded again to add the missing `Project Evolution` section and to list the new reporting/model-card/ROI artifacts.
- On 2026-05-13, the project README was replaced in the local workspace with the user-supplied revised version, and the visual workflow asset `assets/images/n8n_workflow_phase2.png` was added for README embedding.
- Current canonical v2 modeling artifacts produced locally:
  - `models/churn_model_20260506.joblib`
  - `data/processed/churn_predictions_20260506.parquet`
  - `data/processed/churn_model_metrics_20260506.csv`
  - `data/processed/churn_model_comparison_20260506.csv`
- On 2026-05-19, the duplicate local project folder outside `projects/TFM/` was removed after verifying that the `projects/TFM/daily-customer-churn-predictor` path is the operational canonical root used by scripts, notebook path resolution, environment assets, and project traceability.
- On 2026-05-19, the user-provided refreshed notebooks plus the updated `README.md` and `n8n/` workflow JSON files were installed into the canonical local project tree.
- Also on 2026-05-19, Phase 2 of the improvement plan was implemented and executed successfully on the canonical local notebook chain:
  - `NB05` now exports a stronger diagnostics HTML with interactive Plotly sections for risk mix and threshold precision/recall trade-offs, plus a reporting footer with run date, model version, and pipeline tag.
  - `NB06` now exports an upgraded explainability HTML with static representative HIGH/LOW SHAP force views, adjusted report styling, and the same footer metadata.
  - `NB07` now writes `model_version` and `pipeline_tag` into the scoring package metadata.
  - `NB08` was then realigned with the updated user-provided n8n workflow JSON files and re-executed so the dated orchestration HTML / JSON snapshots now match the current two-workflow architecture.
  - `NB09` now exports a richer monitoring dashboard with KPI cards, interactive Plotly visuals for risk mix / driver mix / threshold curve, and footer metadata.
  - Real execution QA was completed for `NB05`, `NB06`, `NB07`, `NB08`, and `NB09`, producing fresh 20260519 artifacts without blocking errors.
- Still on 2026-05-19, the minimum viable Phase 3 publication layer was strengthened locally after fresh execution evidence:
  - `reports/model_card_v2_20260519.md` was generated to replace the older lighter model-card narrative with a stronger governance-oriented card tied to the latest local diagnostics and payload profile.
  - `reports/roi_simulation_20260519.html` was generated to replace the older single-scenario ROI narrative with a clearer three-scenario stakeholder view (Conservative / Base case / Upside), explicit assumption disclosure, and stronger publication framing.
  - The Phase 3 local closure decision is now evidence-based: `NB05`–`NB09` all executed successfully again on 2026-05-19, so Model Card + ROI are now backed by fresh local artifacts rather than by stale documentation only.
- On 2026-05-21, the housekeeping alignment requested by the user was applied in both the local workflow and Drive copy:
  - obsolete `reports/*20260502*` outputs were removed where present
  - `reports/churn_monitoring_dashboard_20260512.html`, `reports/model_card_v2_20260512.md`, and `reports/roi_simulation_20260512.html` were removed
  - Python `__pycache__` folders under `src/` and `tests/` were removed
  - `n8n/daily_churn_retention_workflow_20260502.json` was removed locally where present
  - Drive-side misplaced `.csv`, `.parquet`, and `.joblib` artifacts were re-homed from `reports/` into `data/processed/` and `models/`, then verified
- Also on 2026-05-21, the proposed action table was exported as a compact 4-column semicolon-separated CSV for easier review and spreadsheet import:
  - `reports/proposed_action_table_4cols_20260521.csv`
  - columns: `customer_unique_id`, `snapshot_date`, `risk_tier`, `proposed_action`
- Later on 2026-05-21, the user-reviewed workspace↔Drive discrepancy sheet was applied with the agreed clarifications:
  - Drive-canonical files such as `.dockerignore`, `.gitattributes`, `.gitignore`, `Dockerfile`, `RELEASE_NOTES_v1.md`, selected `_private/` files, `requirements.txt`, `assets/images/n8n_workflow_phase2.png`, and `n8n`/workflow support references were replicated into the workspace where requested.
  - Obsolete local-only files from older project states were removed from the workspace, including old `20260502` processed/model artifacts, local-only `_private/_agents` and `_deprecated_logos` files, `notebooks/Workflow.xlsx`, and dated `n8n` workflow snapshots.
  - Drive-only deprecated notebook files under `notebooks/_deprecated/` and lingering spreadsheet exports under `reports/` were removed from Drive where requested.
  - Workspace-canonical files including `notebooks/08_n8n_orchestration.ipynb`, `reports/model_card_v2_20260519.md`, `reports/roi_simulation_20260519.html`, `data/processed/generated_coupons.jsonl`, `data/processed/retention_actions_20260519.parquet`, `scripts/ensure_churn_api_62881.sh`, `src/api/__init__.py`, `src/api/churn_service.py`, and `tests/test_churn_service.py` were copied to Drive.
  - Runtime log files `logs/churn_api_62881.log` and `logs/churn_api_62881.pid` were intentionally kept local-only by explicit agreement and not synchronized to Drive.
  - Verification succeeded for all targeted actions except `_private/Hoja de cálculo sin título.xlsx`, which copied across but still presents a content mismatch between workspace and Drive and should be rechecked before treating it as fully aligned.
- Later on 2026-05-21, the user approved removal in both workspace and Drive of now-nonessential `20260506` processed artifacts that no longer apply to the latest notebook line:
  - `data/processed/churn_diagnostics_20260506.csv`
  - `data/processed/churn_driver_summary_20260506.csv`
- `data/processed/churn_explainability_20260506.parquet`
  - `data/processed/churn_inference_smoke_test_20260506.parquet`
  - `data/processed/retention_actions_20260506.parquet`
  - Removal was verified in both locations.
- On 2026-05-21 evening, the notebook chain was hardened against cross-run drift and non-reproducible orchestration ids:
  - `NB02` now uses the same robust project-root resolution pattern as `NB01`.
  - `NB04` now persists `run_id`, `run_date_tag`, `model_version`, `pipeline_tag`, and training timestamp inside the model package, anchored to the feature artifact tag instead of a fresh wall-clock date.
  - `NB05` and `NB06` now rebuild diagnostics/explainability outputs against the persisted `run_date_tag` from `NB04`, so downstream artifacts stay aligned with the same canonical run.
  - `NB07` now validates and packages only same-run feature / prediction / explainability artifacts, and carries the shared run metadata into the scoring bundle.
  - `NB08` now validates the scoring-bundle run tag before generating orchestration outputs and builds `offer_code_stub` from `customer_unique_id` instead of the dataframe index.
  - `README.md` now clarifies that `STATUS.md` is the operational traceability log, that `20260506` is the canonical shared artifact tag, and that the publication wording consistently uses the `canonical V2C artifact line` / `internal-pilot-first` framing.
- On 2026-05-22 early morning, the user-approved refresh from Drive was applied for `README.md` and `.gitignore` from `Portfolio/daily-customer-churn-predictor` into the canonical local project tree `projects/TFM/daily-customer-churn-predictor`, and both files were byte-verified against Drive after copy.
- On 2026-05-23, the first implementation block of `PHASE3_unified_integration_plan_v3.md` was started in the canonical local repo with the first contract-normalization pass:
  - `src/api/churn_service.py` health output now surfaces `run_id`, `run_date_tag`, `model_version`, `pipeline_tag`, and source metadata from the latest scoring bundle.
  - `src/api/churn_service.py` coupon generation now accepts the canonical Phase 3 keys `customer_unique_id` and `risk_tier` (while remaining backward compatible with legacy aliases) and returns canonical lineage metadata.
  - `tests/test_churn_service.py` was updated and revalidated against the new canonical API contract.
  - `notebooks/08_n8n_orchestration.ipynb` was normalized so HIGH-tier `primary_channels` now match the actual operational scope (`email,push`) and the outdated SMS follow-up wording was removed from the current workflow narrative.
  - `n8n/n8n_workflow_daily_churn_retention_workflow.json` was normalized away from legacy `customer_id` / `risk_level` references and now carries `customer_unique_id`, `risk_tier`, `run_id`, and `run_date_tag` in the coupon-generation and SQL-log paths.
  - `src/pipeline/load_predictions.py` was created as the first repo-aligned Phase B loader baseline with freshness validation, required-column checks, idempotent load behavior, and automatic table/index creation against the configured SQLAlchemy target.
  - The loader was then upgraded from the earlier prediction-only shape to the canonical retention-payload shape expected by the workflow (`snapshot_key`, `recommended_offer_type`, `primary_channels`, `control_group_flag`, `send_action_flag`, `offer_code_stub`, plus normalized lineage fields), including fallback inference for `run_id` / `run_date_tag` when older payload files omit them.
  - `db/migrations/001_add_run_date_dedup.sql` was created as the canonical DDL baseline for `churn_predictions` plus the unique dedup index on `(customer_unique_id, run_date)`.
  - `db/migrations/002_opt_outs_and_governance.sql` was added as the initial suppression/governance baseline with `opt_outs`, `retention_actions_skipped`, and `retention_governance_config` tables plus default send-window and daily-cap values.
  - Repo-level runtime artifacts `docker-compose.yml` and `.env.example` were added to anchor the hardened deployment shape around Postgres + the scoring API service on port `62881`.
  - Real execution validation confirmed the loader can populate a fresh SQLite target from the canonical `retention_actions_20260506.parquet` artifact with `3346` rows and the unique dedup index present; a second run remains idempotent.
- On 2026-05-24, the next Phase 3 execution block was applied locally on the canonical repo:
  - `src/pipeline/load_predictions.py` was adjusted again so the insert idempotency now targets the live primary key constraint on `(customer_unique_id, snapshot_key)`, avoiding `UniqueViolation` against historical rows already present in Postgres while preserving no-op behavior on replays.
  - `src/pipeline/load_predictions.py` now validates parquet columns against the parquet contract itself (using `snapshot_date` rather than `scored_date`) and maps `snapshot_date -> scored_date` only during the Postgres insert-preparation step.
  - `src/pipeline/load_predictions.py` was realigned to the live Postgres `churn_predictions` schema: the insert path now maps only the approved operational columns, derives `run_date` from `snapshot_key` (`YYYYMMDD`), generates `loaded_at` at insert time, removes non-schema fields such as `snapshot_date`, `model_version`, `pipeline_tag`, `run_id`, and `run_date_tag`, and validates the target table instead of attempting to add columns to it.
  - `src/pipeline/load_predictions.py` was updated so `_ensure_table()` now inspects `churn_predictions` through Postgres-compatible `information_schema.columns` instead of SQLite `PRAGMA table_info`, preserving the additive column backfill logic while keeping the loader aligned with the intended Postgres runtime.
  - `src/api/churn_service.py` now resolves `PROJECT_ROOT` from the `PROJECT_ROOT` environment variable when provided, with the previous `Path(__file__).resolve().parents[2]` logic retained as fallback for repo-local execution.
  - The migration files requested from `PHASE3_unified_integration_plan_v3.md` sections `B-1`, `B-2`, and `B-3` were aligned in the repo: `db/migrations/001_add_run_date_dedup.sql` now carries the documented `ALTER TABLE` + dedup index baseline, `db/migrations/002_create_opt_outs.sql` was added with the documented suppression-table definition, and `db/migrations/003_retention_action_logs.sql` now also includes the missing retention-events dedup index.
  - `src/pipeline/load_predictions.py` was hardened again so the canonical retention payload validates score bounds and valid `risk_tier` values, ensures the suppression table exists before load, and still backfills `run_id` / `run_date_tag` from the parquet tag when older payload artifacts do not yet carry those fields.
  - `n8n/n8n_workflow_daily_churn_retention_workflow.json` was upgraded from a documentation-only baseline into an executable Phase 3 draft with a loader node, scoring-API health check, suppression + dedup preselection query, a governance code node enforcing send-window / tier-cap filtering before coupon generation, and a skip-log query aligned with the current `retention_actions_skipped` schema.
  - `tests/test_load_predictions.py` was added to validate loader insertion, `opt_outs` bootstrap behavior, and fallback inference of missing run metadata on a fresh SQLite target.
  - `scripts/reconcile_local_phase3_sqlite.py` was added and executed successfully to rebuild the local SQLite `churn_predictions` table onto the richer Phase 3 operational shape while preserving a `churn_predictions_backup_pre_phase3` backup table.
  - `db/migrations/003_retention_action_logs.sql` was added to establish canonical `retention_actions` / `retention_events` operational tables and indexes for the hardened workflow contract.
  - `src/pipeline/detect_conversions.py` plus `n8n/n8n_workflow_conversion_detection.json` were added as the first executable Phase C baseline for conversion detection over the 14-day window.
  - `.env.example` now documents `SOURCE_DB_URL` and `CONVERSION_WINDOW_DAYS`, and `tests/test_detect_conversions.py` now validates the conversion-detection insert path on a fresh SQLite setup.
  - Real execution validation succeeded for `python3 -m py_compile src/pipeline/load_predictions.py src/api/churn_service.py scripts/reconcile_local_phase3_sqlite.py src/pipeline/detect_conversions.py`, `python3 -m unittest tests.test_churn_service tests.test_load_predictions tests.test_detect_conversions -v`, and the local SQLite reconciliation run itself.

## Current findings
- The v1 model remained extremely high-recall/high-positive under the original 90-day churn definition, which kept average precision near 0.994 but yielded a more modest ROC AUC around 0.589 on the test split.
- The canonical `V2C` base is structurally valid with `9,571` rows, `1,795` unique customers, `14` snapshots, and prevalence around `0.9748`.
- The selected adaptive horizon is now tighter than the first v2 attempt, with bounds `75-150` days and average horizon around `93.64` days.
- `NB04` selected **XGBoost** as the best model again on the canonical `V2C` line.
- On the canonical v2 test split, the selected model reached approximately:
  - `ROC AUC = 0.8016`
  - `Average Precision = 0.9937`
  - `Precision@Top 5% = 1.0000`
  - `Precision@Top 10% = 0.9970`
- `NB05` diagnostics confirm that the ranking remains very strong in aggregate, but also reinforce the same caveat seen earlier: the target is still overwhelmingly positive, so calibration and threshold interpretation must be handled cautiously.
- The quantile-threshold diagnostic remains operationally useful even under that caveat: top-ranked slices preserve very high observed churn rates, which supports the retention prioritization logic.
- `NB06` explainability shows that the current score is driven predominantly by frequency, monetary, and recency patterns in the scored sample, and the explainability layer yields action-ready segments through driver grouping, LTV quartiles, recommended offer types, discount guidance, and VIP human-touch flags.
- `NB07` now packages the canonical V2C inference logic with percentile-based risk tiers and attached retention rules instead of the legacy fixed-threshold policy.
- `NB08` translates the scored population into a concrete retention payload aligned with the confirmed retention-strategy document, including journey sequencing, control-group handling, driver-sensitive offer mapping, and channel policy.
- `NB09` consolidates diagnostics, explainability, and campaign-readiness outputs into a single monitoring dashboard for stakeholder review.
- The publication layer now reflects the current local candidate coherently instead of leaving the repository framed as a v1-only baseline.
- The main unresolved analytical caveat is unchanged: even the winning `V2C` formulation still has a very high positive prevalence, so downstream diagnostics should continue to interpret the target cautiously.

## Next pending step
1. [blocked] Validate the upgraded n8n / Postgres runtime end-to-end against the real live schema and credentials. The current container lacks `docker` and no live Postgres/n8n service is reachable from this session, so only repo/static/local-SQLite validation has been completed so far.
2. Decide whether the notebook/NB08 export should now emit `run_id` and `run_date_tag` natively so the fallback loader path can later be retired.
3. If the repository is prepared for a public push after that, execute the release packaging/publication step with the synchronized backup as support.
4. As the next analytical upgrade beyond this portfolio-ready state, replace the scenario-based ROI layer with experimentally grounded uplift / threshold optimization.

## Risks / open questions
- The core v2 risk is now confirmed empirically: even after filtering to repeat customers with 90+ days of tenure, the current adaptive label still produces a very high positive rate and may continue to limit separability.
- The refreshed ROI simulation is still intentionally illustrative and scenario-based; it is stronger for publication/storytelling, but it is not yet a causal or experimentally validated business case.
- The latest run-metadata hardening pass is now synchronized and verified in Drive, but public-release wording should still be reviewed once more before any new GitHub publication step.
- The new n8n support API now runs on port `62881` by user-approved design instead of `62880`, because `62880` is occupied in this runtime by the existing OpenClaw Node server.
- The remaining integration risk is now mostly environmental rather than repo-local: this session cannot launch/inspect the real Docker+n8n+Postgres runtime because `docker` is unavailable here and no live Postgres service credentials/endpoint have been validated from the current container.
- A watchdog script plus persistent OpenClaw cron job now re-check the API every minute so the service comes back automatically after container restarts, provided the OpenClaw gateway itself starts normally.
- There is a methodological risk of over-iterating on too many variants; the benchmark should therefore stay intentionally short (around 3-4 candidate formulations).
- NB06 explainability is still expected to rely on a robust sample rather than full-population SHAP unless runtime permits broader execution.
- n8n remains acceptable for the current orchestration baseline, but a later v3 may replace it with a more hardened automation architecture.
- Phase 2 and the minimum viable Phase 3 layer should preserve explicit comparability against v1 so the portfolio narrative remains traceable.
