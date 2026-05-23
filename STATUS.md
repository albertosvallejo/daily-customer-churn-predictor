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
1. Review whether the freshly pulled Drive versions of `README.md` and `.gitignore` should remain the canonical local versions or need any additional local editorial adjustments.
2. If desired, do one final editorial pass so README / Model Card / ROI simulation use exactly the same publication wording and caveat language.
3. If the repository is prepared for a public push after that, execute the release packaging/publication step with the synchronized backup as support.
4. As the next analytical upgrade beyond this portfolio-ready state, replace the scenario-based ROI layer with experimentally grounded uplift / threshold optimization.

## Risks / open questions
- The core v2 risk is now confirmed empirically: even after filtering to repeat customers with 90+ days of tenure, the current adaptive label still produces a very high positive rate and may continue to limit separability.
- The refreshed ROI simulation is still intentionally illustrative and scenario-based; it is stronger for publication/storytelling, but it is not yet a causal or experimentally validated business case.
- The latest run-metadata hardening pass is now synchronized and verified in Drive, but public-release wording should still be reviewed once more before any new GitHub publication step.
- The new n8n support API now runs on port `62881` by user-approved design instead of `62880`, because `62880` is occupied in this runtime by the existing OpenClaw Node server.
- A watchdog script plus persistent OpenClaw cron job now re-check the API every minute so the service comes back automatically after container restarts, provided the OpenClaw gateway itself starts normally.
- There is a methodological risk of over-iterating on too many variants; the benchmark should therefore stay intentionally short (around 3-4 candidate formulations).
- NB06 explainability is still expected to rely on a robust sample rather than full-population SHAP unless runtime permits broader execution.
- n8n remains acceptable for the current orchestration baseline, but a later v3 may replace it with a more hardened automation architecture.
- Phase 2 and the minimum viable Phase 3 layer should preserve explicit comparability against v1 so the portfolio narrative remains traceable.
