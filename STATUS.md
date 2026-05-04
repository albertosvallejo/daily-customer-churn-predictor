# STATUS

## Project
Daily Customer Churn Predictor – VivaMarket Brasil

## Current state
Phase 1 notebook flow is now functionally complete through NB09. The project has been normalized to keep one canonical executed notebook per step, the early notebook set has been cleaned, the visual identity guide is now a PDF deliverable, the HTML reports were adapted to the project look & feel, and the README was rebuilt to align with FRAMEWORK-style publication standards and to give explicit weight to the Spec-Driven + OpenClaw + human-supervision methodology.

## Last completed step
- Removed obsolete notebook artifacts: `notebooks/01_data_audit_extraction_en.ipynb` and `notebooks/01_data_cleaning.audit_run.ipynb`.
- Promoted the executed/depurated notebooks as the canonical source of truth:
  - `01_data_cleaning.executed.ipynb` → `01_data_cleaning.ipynb`
  - `02_eda_exploratory.executed.ipynb` → `02_eda_exploratory.ipynb`
  - `03_feature_engineering.executed.ipynb` → `03_feature_engineering.ipynb`
- Removed legacy brand-guide/source assets from `assets/images/` and kept only `logo.png` plus the new `visual_identity_guide_v1.pdf`.
- Rebuilt `README.md` using the MMM and RAG repositories as style references and strengthened the explanation of the Spec-Driven/OpenClaw/human-supervision methodology.
- Expanded `README.md` again to include more explicit model sections: feature families, model family/training logic, diagnostic logic, explainability framing, and a professional-improvement roadmap.
- Updated `RELEASE_NOTES_v1.md` so the GitHub release context also reflects the methodology and the recommended post-v1 improvements.
- Restyled the HTML deliverables in `reports/` to follow the project brand semantics and header treatment.

## Current findings
- The model remains extremely high-recall/high-positive under the current 90-day churn definition, which keeps average precision near 0.994 but yields a more modest ROC AUC around 0.589 on the test split.
- The operational risk mix in the held-out scored set is ~30.8% HIGH, ~63.4% MEDIUM, and ~5.8% LOW under the retention thresholds from `_private/acciones_retencion.docx`.
- SHAP-based explainability is available on a 5,000-row scored sample and was converted into driver groups and offer recommendations aligned with the retention strategy.
- The retention-action payload now includes fallback business-rule defaults for rows outside the SHAP sample so the orchestration artifact remains complete.

## Next pending step
1. Publish the v1 baseline to GitHub with the README limitation note preserved.
2. Start v2 analytical redesign by revisiting the churn-eligibility population and target definition.
3. Re-run downstream notebooks after the v2 churn-definition decision.
4. Continue later with React UI and automation hardening before Dockerization.

## Risks / open questions
- The current forward 90-day churn label appears extremely positive-heavy in later snapshots, which may inflate precision-oriented metrics and reduce separability.
- NB06 explainability is sampled rather than full-population SHAP to keep execution robust in the current environment.
- n8n remains acceptable for the current orchestration baseline, but a later v3 may replace it with a more hardened automation architecture.
- v1 is suitable as a baseline publication, but the churn-definition refinement should be treated as a true analytical next version rather than a silent patch.
