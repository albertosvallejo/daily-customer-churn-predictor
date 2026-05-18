# Daily Customer Churn Predictor

**Spec-Driven Churn Intelligence System for VivaMarket Brasil**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Modeling-EC6B23.svg)](https://xgboost.readthedocs.io/)
[![Scikit--learn](https://img.shields.io/badge/scikit--learn-Validation-F7931E.svg)](https://scikit-learn.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook%20Pipeline-F37626.svg)](https://jupyter.org/)
[![License](https://img.shields.io/badge/License-Personal%20Portfolio-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-v1.0.0%20Baseline%20%7C%20v2%20+%20Phase%202%20Complete-orange.svg)]()
[![Workflow](https://img.shields.io/badge/Workflow-Spec--Driven%20%2B%20Human%20Supervision-005090.svg)]()

---

## Executive Summary

> ⚠️ **BEFORE YOU START — ANALYTICAL BASELINE NOTE**: This repository contains both the historical **v1.0.0 published baseline** and the current locally hardened **canonical v2 candidate**. The original v1 baseline should not be interpreted as a final analytical definition of churn for VivaMarket Brasil: the 90-day forward target was structurally too positive-heavy, which kept average precision near **0.994** while limiting business separability (ROC AUC ~**0.589** on the v1 test split). The current local v2 candidate materially improves ranking quality (**ROC AUC ~0.8016**) through a redesigned `V2C` formulation, but the target remains positive-heavy and should still be interpreted cautiously. This is not a model failure — it is a consequence of marketplace dynamics, one-time-buyer dominance, and the difficulty of defining a truly retainable customer population. The limitation is explicit and should be handled as a genuine business-first analytical design problem.

This is a **personal deep-dive project** built after completing a Master's in Data Science to gain hands-on experience with production-oriented churn modeling in a realistic marketplace setting. It implements a **complete end-to-end churn workflow** for VivaMarket Brasil, covering the full path from raw SQLite extraction to scored retention queues, explainability outputs, automation-ready payloads, and business-facing HTML reporting.

The goal was to go beyond a typical academic churn notebook and build a pipeline that addresses the real challenges of marketplace churn: irregular purchase behavior, analytically complex target definition, temporal consistency requirements, and the need to translate model scores into operational business decisions.

**Development approach:** This project was built using **The Architect (v1)**, a personal Spec-Driven DS framework developed alongside this project. Every notebook was analytically specified before being built, executed with OpenClaw agent support, and reviewed under explicit human supervision before the next step was started. The workflow prioritizes traceability, notebook-by-notebook QA, and clean versioned evolution over execution speed.

**Current local v2 candidate — key metrics:**

| Metric | Value | Context |
|:-------|:-----:|:--------|
| ROC AUC (test split) | ~0.8016 | Canonical `V2C` candidate |
| Average Precision | ~0.9937 | Still influenced by positive-heavy target |
| Precision@Top 5% | 1.0000 | Held-out scored set |
| Precision@Top 10% | ~0.9970 | Held-out scored set |
| SHAP explainability | ✅ robust scored sample | NB06 |
| Deployment prep | ✅ scoring package + smoke test | NB07 |
| Orchestration | ✅ n8n workflow V9 — two-workflow architecture (main + error handler), executed end-to-end in production (Phase 2 internal orchestration, validated 2026-05-18) | NB08 |
| Reporting | ✅ branded HTML dashboard | NB09 |

**Top churn driver families (current local candidate):**

| Driver family | Interpretation |
|:--------------|:---------------|
| `frequency` | Purchase regularity and cadence degradation |
| `monetary` | Spend and value-related weakening |
| `recency` | Time since last purchase and recent inactivity |
| `experience / other` | Review, delivery, and residual quality signals |

**Key analytical finding:** The project demonstrates a technically complete and operationally coherent churn system, but the central modeling lesson remains the same: the most important next improvement is not blind tuning. It is a **business-first redesign of who counts as a retainable customer** and therefore who should enter the eligible modeling population.

---

## Quick Start

> **Current status:** NB01–NB09 complete with canonical executed notebooks. Phase 2 is complete: the n8n workflow (V9, two-workflow architecture) has been executed end-to-end in a real production environment. The historical v1 baseline is documented; the current local repository reflects the synchronized **canonical V2C candidate** with Docker support, tests, updated reporting, and verified Drive backup.

### Running the notebook pipeline

```bash
# 1. Clone the repository
git clone https://github.com/albertosvallejo/daily-customer-churn-predictor.git
cd daily-customer-churn-predictor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place the source SQLite database in data/raw/
# Required: marketplace SQLite database compatible with the project extraction logic

# 4. Run notebooks in order (mandatory sequence)
# 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09
```

### Running with Docker

```bash
docker build -t churn-vivamarket .
docker run --rm -p 8888:8888 churn-vivamarket
```

### Recommended execution context

- Python 3.11+
- Jupyter / Google Colab / local JupyterLab
- 8GB+ RAM for feature engineering and explainability sampling
- Source SQLite database placed in `data/raw/`

**Prerequisites:**
- All notebooks must be executed in sequence — each notebook's outputs feed directly into the next
- NB06 explainability is run on a robust scored sample to keep execution stable in the current environment
- NB07 generates a scoring package that NB08 consumes for the n8n blueprint

---

## Development Methodology

This repository was built as a **Spec-Driven Data Science project with OpenClaw agent support and explicit human supervision**.

**Spec-Driven** means every notebook was defined analytically before being built — inputs, outputs, transformations, and validation criteria were specified explicitly before any code was written. This reduces scope drift, makes QA tractable notebook by notebook, and produces artifacts whose lineage is traceable across the full pipeline.

**OpenClaw** is the agent framework used to execute and iterate on notebooks inside a structured workspace. It acts as the execution layer — running code, surfacing errors, and generating outputs — while analytical decisions, validations, and direction changes remain under human control.

**Human supervision** means no output was accepted without review. Every notebook's results were inspected against the spec before the next step was started. The agent accelerates execution; the human owns the analytical decisions.

### The Architect (v1)

The Spec-Driven workflow in this project was developed using **The Architect**, a personal DS project framework (v1) created specifically to structure data science work from analytical specification through to operational delivery.

A few honest notes about The Architect v1:

- It is a **personal framework**, not a published tool. v1 was built and battle-tested for the first time on this project.
- Because it is a personal platform, it runs against a **ChatGPT Pro monthly subscription** rather than an API-first billing model — a deliberate choice to keep project costs controlled.
- It will **evolve with each new project**. As agent-assisted DS best practices mature and future projects surface new edge cases, The Architect will be updated to reflect those learnings.

The result is a workflow that emphasizes structured execution, notebook-by-notebook QA, operational traceability, reproducibility, and business-facing deliverables that can evolve cleanly across versions.

---

## Table of Contents

- [Project Context](#project-context)
- [Business Problem](#business-problem)
- [Development Methodology](#development-methodology)
- [Methodology](#methodology)
- [Modeling Approach](#modeling-approach)
- [Project Evolution](#project-evolution)
- [Results & Performance](#results--performance)
- [System Architecture](#system-architecture)
- [Notebook Pipeline Reference](#notebook-pipeline-reference)
- [Main Deliverables](#main-deliverables)
- [File Structure](#file-structure)
- [Technical Stack](#technical-stack)
- [Methodological Notes](#methodological-notes)
- [Known Limitations](#known-limitations)
- [Professional Improvement Roadmap](#professional-improvement-roadmap)
- [Future Work](#future-work)
- [Version Note](#version-note)
- [License & Contact](#license--contact)

---

## Project Context

### Why build a churn predictor for a marketplace in 2026?

Churn prediction in subscription businesses is comparatively clean: the event is defined (cancellation), the population is clear (active subscribers), and the label is explicit. Marketplace churn is much harder. There is no cancellation event. The population boundary is blurry. Most customers in many cohorts bought once and never returned, which may be normal behavior rather than churn. And "inactive for 90 days" means something very different for a customer with seven orders over two years than for a customer with a single purchase.

This project was built precisely in that harder context. The dataset reflects realistic marketplace dynamics, and the challenges it presents — one-time-buyer dominance, irregular interpurchase intervals, label leakage risk in temporal splits, and the difficulty of defining a truly retainable population — are the same challenges faced by real marketplace analytics teams.

The v1 baseline established a working end-to-end system, documented the known limitations honestly, and laid the foundation for a v2 redesign where the population and label definitions are revisited from first principles.

### Project background

This is a **personal deep-dive project** built after completing a Master's in Data Science to gain hands-on experience with production-oriented churn modeling, SHAP-based explainability, and automation-ready ML systems in a realistic ecommerce setting.

The goal was to go beyond typical course implementations and build a complete, operationally structured churn pipeline that addresses the challenges you actually face on marketplace data:

- analytically complex target definition with no natural churn event;
- population dominated by one-time buyers with no clear retention intent;
- temporal consistency requirements for feature engineering and model training;
- explainability that maps model outputs to business-actionable driver groups;
- automation-ready artifacts for downstream orchestration without over-engineering the serving layer;
- honest reporting when strong execution still reveals a real analytical constraint.

The result is a robust, well-documented workflow suitable for a senior data science / CRM analytics portfolio discussion.

### Business Context

VivaMarket Brasil is a marketplace-style ecommerce platform with a transactional customer base that purchases irregularly across multiple product categories.

**Core business challenge:** identify customers at risk of disengagement and translate model outputs into operational retention actions — discount offers, re-engagement communications, and loyalty reinforcement — in a way that can later be orchestrated automatically.

**Target user profile:** CRM manager or retention analyst responsible for daily operational decisions on which customers receive which incentives and through which channel.

---

## Business Problem

### Challenge Statement

The project addresses four interconnected analytical challenges typical of marketplace ecommerce:

**Ambiguous churn definition.** Unlike subscriptions, marketplaces have no cancellation event. Churn must be inferred from future inactivity over a chosen horizon, and that horizon interacts directly with who should count as an eligible customer.

**One-time-buyer dominance.** A large share of historical customers placed exactly one order and never returned. Including them blindly in the modeling base conflates normal single-purchase behavior with real disengagement.

**Temporal consistency.** Features must be computed strictly from history before the snapshot date, while the churn label must be computed strictly from future activity after that observation date. Any leakage breaks the analytical validity of the workflow.

**Operational translation.** A score is not a retention action. The pipeline must produce not only probabilities and tiers but also a payload that maps customers into actions, channels, and incentives that can be used operationally.

### Core Questions

1. Can we build a reproducible churn baseline from raw marketplace transactional data?
2. Can we map model scores into business-facing retention actions with a defensible tier logic?
3. Can we explain churn drivers clearly enough for operational stakeholders?
4. Can we prepare the outputs for daily automation without over-engineering the serving layer too early?

### Success Criteria

**Pipeline quality:**
- complete notebook execution `NB01 → NB09` with no broken artifact handoffs;
- temporal integrity across feature engineering and evaluation;
- explainability outputs generated successfully;
- retention payload covers the scored population;
- orchestration blueprint generated, importable, and executed end-to-end. ✅

**Business quality:**
- risk tiers map to differentiated retention actions;
- driver groupings are interpretable in business language;
- reporting artifacts are presentable to a non-technical stakeholder.

**Editorial quality:**
- notebooks and project-facing deliverables remain in English;
- VivaMarket Brasil visual identity is applied consistently;
- canonical executed notebooks are the single source of truth.

---

## Methodology

### End-to-End Flow

```text
Raw SQLite data
→ data cleaning + churn-oriented EDA
→ repeated customer snapshot engineering
→ temporal model training (XGBoost)
→ diagnostics + threshold analysis
→ explainability + driver grouping
→ deployment preparation (scoring package)
→ retention orchestration design + execution (n8n)
→ branded HTML reporting dashboard
```

### Data Foundation

The project works from a local SQLite ecommerce dataset and builds a modeling-ready customer-snapshot layer. Each snapshot represents a customer observed at a specific temporal checkpoint, with:

- behavioral features computed from history before the snapshot date;
- a future churn label computed from activity after the snapshot date;
- multiple snapshots per customer across different temporal windows.

This design allows the same customer to be observed at multiple lifecycle moments and better approximates an operational scoring setup.

### Feature Families

| Family | Features | Analytical role |
|:-------|:---------|:----------------|
| **Recency & frequency** | recency, order counts, cadence, activity windows | Primary churn signal |
| **Monetary** | revenue windows, AOV, freight, installments | Value segmentation |
| **Product breadth** | distinct categories, distinct products | Engagement depth |
| **Quality & experience** | review scores, delivery-related aggregates | Satisfaction signal |
| **Payment mix** | payment concentration, amount windows | Behavioral pattern |
| **Customer profile** | tenure and selected enrichments | Segment enrichment |

### Modeling Logic

The current synchronized local candidate uses the canonical **`V2C`** formulation:

- eligible base: `total_orders >= 2`
- tenure rule: `tenure_days >= 90`
- adaptive horizon: `min(150, max(75, round(1.25 * median_gap_days)))`
- fallback horizon: `75`

This formulation was chosen after a short controlled benchmark because it improved ranking quality while preserving the broadest operationally useful base among the tested candidates.

### Orchestration Positioning

The automation layer is implemented through **n8n**, which serves as the internal orchestration platform for Phase 2. The final architecture uses **two separate workflows**: the main pipeline (V9) and a dedicated error handler (`VivaMarket Error Handler`), connected through n8n's native Error Workflow mechanism in Settings. This two-workflow pattern avoids the known n8n issue where inline error nodes can be incorrectly auto-wired as main connections. Both workflows have been executed end-to-end in a real VPS environment, validating the full retention action pipeline from daily scoring through coupon generation, email and push notification dispatch, and database logging. A more hardened customer-facing delivery stack is scoped for Phase 3 once the underlying churn definition is analytically stable.

---

## Modeling Approach

### Modeling objective

Estimate the probability that a customer snapshot will satisfy the project's operational churn definition under the canonical `V2C` formulation, then convert that ranking into diagnostics, explainability, deployment outputs, and retention actions.

### Input population logic

The workflow is built on repeated customer snapshots rather than a single static table. This allows the project to:

- observe behavior through time,
- compute rolling behavioral aggregates,
- score the same customer across multiple temporal states,
- simulate a real churn-monitoring setup.

### Core feature families

The current feature space combines multiple behavioral blocks:

- **Recency and frequency**
- **Monetary behavior**
- **Product breadth**
- **Quality and experience signals**
- **Payment-mix features**
- **Customer profile enrichments**

### Model family and training logic

The training workflow uses a supervised gradient-boosting approach centered on **XGBoost**, supported by the broader scikit-learn evaluation stack. It was selected because it provides:

- strong nonlinear tabular performance,
- compatibility with heterogeneous engineered features,
- probability outputs and ranking suitability,
- straightforward SHAP integration.

### Validation and diagnostics logic

The project emphasizes downstream usefulness rather than a single headline metric. Diagnostics include:

- ROC AUC and average precision;
- Brier score;
- precision at top targeting bands;
- threshold trade-off tables;
- risk-tier mix summaries;
- dashboard-ready monitoring outputs.

### Explainability logic

`NB06` produces explainability on a robust scored sample. The goal is not only feature-importance ranking but business interpretation of churn drivers by risk tier. That explainability is then translated into driver-sensitive retention recommendations and VIP escalation logic.

### Operational decisioning logic

The current local candidate uses percentile-based operational tiers derived from the scored population:

- **HIGH**: top 20%
- **MEDIUM**: next 30%
- **LOW**: bottom 50%

This is more coherent with the canonical `V2C` distribution than the old fixed probability bands.

---

## Project Evolution

This repository is deliberately presented as an evolving professional project rather than a one-shot notebook dump. The analytical story matters because the biggest lesson was not a hyperparameter tweak — it was learning how the business definition of the problem changes the model much more than small technical optimizations do.

### Phase 1 — Published v1 baseline

The original v1.0.0 baseline established the full end-to-end churn workflow:

- raw SQLite extraction,
- temporal feature engineering,
- supervised training and scoring,
- diagnostics,
- explainability,
- deployment-preparation assets,
- orchestration payloads,
- branded HTML reporting.

That baseline was useful because it proved the delivery chain worked from start to finish. But it also surfaced the central analytical weakness very clearly: the initial forward 90-day churn definition was too permissive for a marketplace context dominated by one-time buyers and irregular repurchase behavior.

### Phase 2 — Canonical V2C redesign + n8n operational validation ✅

The current local candidate is a genuine redesign rather than a cosmetic continuation of v1. The main changes were:

- restricting the eligible population to customers with demonstrated recurrence potential,
- moving to the canonical `V2C` formulation,
- tightening the adaptive churn horizon to the `75-150` day bounded rule,
- preserving explicit comparability against the published v1 baseline,
- re-running diagnostics, explainability, deployment preparation, orchestration, and reporting on the redesigned analytical base.

This redesign materially improved ranking quality while keeping the key methodological caution visible: even the stronger V2 candidate still works on a highly positive-heavy label.

**Phase 2 also delivers a fully operational n8n orchestration layer (V9).** The final architecture uses two separate workflows connected through n8n's native Error Workflow mechanism: the main pipeline (`Daily Churn Retention Actions - V9`) handles the full business logic, while a dedicated `VivaMarket Error Handler` workflow manages failure alerting independently. This two-workflow pattern was adopted after resolving a known n8n issue where inline error nodes can be incorrectly auto-wired as main connections on the canvas. Both workflows were executed end-to-end in a real production environment (VPS + Docker + Postgres), validating the complete retention action pipeline: daily cron trigger, churn prediction retrieval from Postgres, SHAP explainability from the scoring API, risk routing, coupon generation, pre-send validation, email and push notification dispatch via OneSignal (credentials managed through n8n Variables), action logging with parameterized query bindings, and error alerting via the dedicated error handler. This closes Phase 2 as operationally complete, with n8n serving as the internal orchestration platform until the customer-facing delivery layer is implemented in Phase 3.

### Phase 3 — Publication hardening

Once the V2C analytical line was stabilized, the project entered a professionalization layer focused on publication readiness:

- README restructuring around Spec-Driven development and human-supervised OpenClaw execution,
- dependency cleanup and Docker support,
- lightweight scoring tests,
- asset normalization and branded report consistency,
- a stronger dashboard layer, model card, and ROI simulation artifacts for stakeholder review.

This means the repository now tells two stories at once: the historical v1 baseline that was already published, and the stronger local V2 candidate that shows how the project matured analytically and operationally.

---

## Results & Performance

### v1 historical baseline

| Metric | Value | Context |
|:-------|:-----:|:--------|
| ROC AUC | ~0.589 | Positive-heavy 90-day baseline |
| Average Precision | ~0.994 | Inflated by class imbalance |
| Interpretation | ⚠ | Operationally complete, analytically constrained |

### Current local V2 candidate outcomes

| Metric | Value |
|:-------|:-----:|
| Rows | `9,571` |
| Unique customers | `1,795` |
| Snapshots | `14` |
| Target prevalence | `~0.9748` |
| Selected model | `XGBoost` |
| ROC AUC | `~0.8016` |
| Average Precision | `~0.9937` |
| Precision@Top 5% | `1.0000` |
| Precision@Top 10% | `~0.9970` |

### Operational completion

The current synchronized local chain is complete through:

- `NB05` diagnostics
- `NB06` explainability
- `NB07` deployment packaging
- `NB08` retention orchestration
- `NB09` reporting dashboard
- n8n workflow V5 — executed end-to-end in production ✅

### Interpretation

The candidate is technically complete and operationally much stronger than the original baseline in ranking quality. However, the core analytical caveat remains: the target is still highly positive-heavy, so calibration and threshold interpretation must remain cautious.

---

## System Architecture

```text
RAW SQLITE DATA
→ NB01 Data Cleaning
→ NB02 EDA
→ NB03 Feature Engineering / Snapshot Construction
→ NB04 Model Training / Benchmarking
→ NB05 Evaluation & Diagnostics
→ NB06 Explainability
→ NB07 Deployment Preparation
→ NB08 Retention Orchestration
→ NB09 Reporting Dashboard
→ n8n Workflow V9 — two-workflow architecture (main pipeline + error handler), daily cron execution (Phase 2 internal orchestration) ✅
```

**Operational outputs currently available:**
- scored predictions,
- diagnostics tables and HTML reports,
- explainability artifacts,
- scoring package,
- orchestration payload,
- reporting dashboard,
- synchronized Drive backup,
- importable n8n workflows (V9 main pipeline + VivaMarket Error Handler, executed and validated).

### Orchestration workflow — Phase 2 (n8n — two-workflow architecture, operationally validated)

![n8n workflow diagram](assets/images/n8n_workflow_phase2.png)

> **Main pipeline (V9, executed 2026-05-18):** Cron-triggered daily pipeline: reads the top 10 highest-risk customers from the `churn_predictions` Postgres table, fetches SHAP explainability data from the internal scoring API, merges both inputs on `customer_unique_id`, routes customers by churn probability via a Rules switch (high risk ≥ 0.75 / medium risk 0.45–0.75), generates a personalized coupon via the coupon API, validates that all required fields are present before dispatch, sends a re-engagement email (SMTP) and a push notification via OneSignal (credentials managed through n8n Variables `ONE_SIGNAL_API_KEY` / `ONE_SIGNAL_APP_ID`), and logs all actions to the `retention_actions` table using parameterized query bindings. Skipped records (missing required fields) are logged to `retention_actions_skipped`.
>
> **Error handler (VivaMarket Error Handler):** A separate two-node workflow — Error Trigger → Send Error Email — connected to the main V9 pipeline through n8n's native Error Workflow setting. This two-workflow pattern was adopted to avoid the known n8n canvas issue where inline error nodes can be incorrectly auto-wired as main connections. The error handler fires automatically on any uncontrolled failure in the main pipeline during scheduled production runs and emails the DS team with workflow name, failing node, timestamp, and error detail.
>
> All nodes executed successfully end-to-end in the production environment (VPS + Docker + Postgres). Importable workflow definitions:
> - `n8n/n8n_workflow_daily_churn_retention_workflow.json` — main pipeline V9
> - `n8n/n8n_workflow_error_handler_workflow.json` — VivaMarket Error Handler

#### n8n deployment notes (Phase 2 infrastructure)

The n8n workflow runs against a real infrastructure stack. The key deployment dependencies are:

- **Scoring API:** the churn service (`src/api/churn_service.py`) runs inside the OpenClaw container on port `62881`, exposing `GET /explainability/latest` and `POST /coupons/generate`. The API must be running before the workflow executes.
- **Docker network:** n8n must be connected to the OpenClaw container network to reach the scoring API by hostname. This is achieved with `docker network connect openclaw-opvz_default n8n`. This connection persists while both containers are running; it must be re-applied if the n8n container is recreated.
- **Postgres:** the `churn_predictions` table must be populated before the workflow runs. In Phase 2 it is loaded from the `retention_actions_20260506.parquet` artifact. In Phase 3 it will be populated by the daily scoring pipeline automatically.
- **OneSignal credentials:** managed through n8n Variables (`ONE_SIGNAL_API_KEY`, `ONE_SIGNAL_APP_ID`). The `$credentials.x` syntax is not supported in HTTP Request nodes and was replaced in V9.
- **Error handler:** the `VivaMarket Error Handler` workflow must be in Published (active) state before linking it in the main V9 Settings. n8n only lists Published workflows in the Error Workflow dropdown. Importing a workflow JSON updates canvas nodes and connections but does not update the Error Workflow field in Settings — this must be set manually from the n8n UI.
- **rclone mount:** if the OpenClaw container is restarted, the Google Drive mount must be restored before relaunching the container: `fusermount -uz /mnt/gdrive && rclone mount architect-drive: /mnt/gdrive --daemon --vfs-cache-mode writes --allow-other`.
- **Production query:** the current workflow uses `WHERE send_action_flag = TRUE ORDER BY churn_probability DESC LIMIT 10`. Once the daily scoring pipeline is active and loading fresh data, the query should add `scored_date = CURRENT_DATE` to restrict to the current day's predictions.

---

## Notebook Pipeline Reference

Each notebook has a defined role and the execution sequence is mandatory.

**Execution order:** `01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09`

### Canonical notebooks

- `notebooks/01_data_cleaning.ipynb`
- `notebooks/02_eda_exploratory.ipynb`
- `notebooks/03_feature_engineering.ipynb`
- `notebooks/04_model_training.ipynb`
- `notebooks/05_model_evaluation_diagnostics.ipynb`
- `notebooks/06_churn_attribution_explainability.ipynb`
- `notebooks/07_model_deployment_preparation.ipynb`
- `notebooks/08_n8n_orchestration.ipynb`
- `notebooks/09_reporting_dashboard.ipynb`

Project rule: each step is represented by **one canonical `.ipynb` file only**. The kept notebook is the executed and debugged version.

---

## Main Deliverables

### Processed data artifacts

Examples from the current local candidate run:

- `data/processed/churn_features_20260506.parquet`
- `data/processed/churn_predictions_20260506.parquet`
- `data/processed/churn_model_metrics_20260506.csv`
- `data/processed/churn_diagnostics_20260506.csv`
- `data/processed/churn_explainability_20260506.parquet`
- `data/processed/churn_driver_summary_20260506.csv`
- `data/processed/churn_inference_smoke_test_20260506.parquet`
- `data/processed/churn_model_comparison_20260506.csv`
- `data/processed/churn_variant_benchmark_20260506.csv`
- `data/processed/retention_actions_20260506.parquet`

### Models and scoring assets

- `models/churn_model_20260506.joblib`
- `models/churn_scoring_package_20260506.joblib`
- `src/models/churn_scoring.py`

### Reporting and orchestration outputs

- `reports/model_diagnostics_20260506.html`
- `reports/churn_explainability_20260506.html`
- `reports/n8n_orchestration_20260506.html`
- `reports/churn_monitoring_dashboard_20260506.html`
- `n8n/n8n_workflow_daily_churn_retention_workflow.json` — main pipeline V9 (Phase 2, executed and validated 2026-05-18)
- `n8n/n8n_workflow_error_handler_workflow.json` — VivaMarket Error Handler (Phase 2, separate error workflow)
- `assets/images/n8n_workflow_phase2.png` — visual diagram of the orchestration workflow

---

## File Structure

```text
daily-customer-churn-predictor/
├── README.md
├── .gitignore
├── requirements.txt
├── STATUS.md
├── RELEASE_NOTES_v1.md
├── Dockerfile
├── .dockerignore
├── notebooks/
├── data/
├── models/
├── src/
├── n8n/
│   ├── n8n_workflow_daily_churn_retention_workflow.json
│   └── n8n_workflow_error_handler_workflow.json
├── reports/
├── assets/
│   └── images/
│       ├── logo.gif
│       ├── visual_identity_guide_v1.pdf
│       └── n8n_workflow_phase2.png
└── _private/
```

Project rule: public notebook continuity is represented by canonical executed notebook files only. Temporary variants and draft artifacts are not part of the kept publication state.

---

## Technical Stack

| Category | Technology | Purpose |
|:---------|:----------:|:--------|
| Language | Python 3.11 | Core development |
| Modeling | XGBoost | Binary churn classification |
| ML utilities | scikit-learn | Evaluation and model workflow |
| Explainability | SHAP | Feature attribution |
| Data manipulation | pandas / NumPy | Pipeline data handling |
| Visualization | matplotlib / seaborn / Plotly | Reporting and charts |
| Database I/O | SQLite / PostgreSQL | Source data layer + operational scoring store |
| Columnar I/O | pyarrow / parquet | Artifact persistence |
| Serialization | joblib | Model/package export |
| Orchestration | n8n (two-workflow architecture) | Internal automation platform (Phase 2, operationally validated) |
| Notebook environment | Jupyter / Colab / JupyterLab | Execution layer |
| Agent support | OpenClaw | Spec-Driven execution support |
| Containerization | Docker | Reproducible execution environment |

---

## Methodological Notes

### 1. Snapshot-based temporal modeling

Rather than building a single static customer table, the workflow constructs customer snapshots at multiple temporal checkpoints. This better reflects a daily churn-scoring system, where the same customer must be evaluated across different lifecycle states.

### 2. Explainability sample vs. full population

The explainability layer is computed on a robust scored sample rather than on the full population to keep execution stable in the current environment. This is acceptable for the current project stage, but full-population explainability or a scalable approximation would be desirable in a later version.

### 3. Population definition is a business decision first

The most important analytical lesson from the project is that the eligible population for a marketplace churn model cannot be defined by data convenience alone. Deciding who is actually retainable is a business-first decision.

### 4. n8n as the internal orchestration platform (Phase 2 — operationally validated)

Using n8n as the internal orchestration platform for Phase 2 is a deliberate sequencing choice: it provides a fully operational automation layer that validates end-to-end pipeline readiness without over-investing in customer-facing infrastructure before the analytical base is fully stabilized.

The n8n workflows included in this repository are the **V9 implementation, executed end-to-end in a real production environment on 2026-05-18**. The final architecture uses two separate workflows: the main pipeline (`n8n/n8n_workflow_daily_churn_retention_workflow.json`) and a dedicated error handler (`n8n/n8n_workflow_error_handler_workflow.json`), connected through n8n's native Error Workflow mechanism in Settings. This two-workflow pattern was adopted to resolve a known n8n issue where inline error nodes can be incorrectly auto-wired as main connections on the canvas. The main pipeline covers the complete internal retention flow: daily cron trigger, prediction retrieval from Postgres, SHAP explainability from the scoring API, risk-tier routing, coupon generation, pre-send validation, email and push notification dispatch (OneSignal credentials managed through n8n Variables), parameterized action logging, and skipped record logging.

The architecture separates two complementary layers that are not mutually exclusive:

- **Layer 2 — Internal orchestration (n8n, Phase 2):** manages the DS pipeline, reads scored predictions, generates coupons, dispatches notifications, and logs all actions. This layer is operational and remains valid in later project stages.
- **Layer 3 — Customer-facing delivery (Phase 3):** extends Layer 2 with a more hardened customer-facing stack — production scheduling, channel integration governance, event tracking, and feedback loop — consuming the same retention payload as the contract between layers.

The production-grade customer-facing automation — oriented to scalable channel delivery, operational governance, and closed-loop measurement — is scoped for **Phase 3**, once the underlying churn definition is analytically stable and the business population design decisions have been resolved.

---

## Known Limitations

1. Even after the `V2C` redesign, the churn target remains highly positive-heavy.
2. Calibration should be interpreted cautiously despite strong ranking metrics.
3. Explainability is sampled rather than full-population SHAP.
4. Operational thresholds are still strategy-oriented rather than fully ROI-optimized.
5. The n8n workflow is the Phase 2 internal orchestration platform; production-oriented customer-facing automation (scheduling + channel delivery + feedback loop) is planned as a separate complementary layer in Phase 3, once the analytical base is stabilized.
6. API persistence across container restarts requires a manual rclone remount step; automated startup handling is scoped for Phase 3.

---

## Professional Improvement Roadmap

### Priority analytical upgrades

1. **Business-first population redesign**
2. **Further churn label refinement**
3. **Parallel CLV / value layer**
4. **Probability calibration**
5. **ROI-based threshold optimization**
6. **Structured cohort analysis**
7. **Uplift / incremental-response modeling**

### Governance and MLOps upgrades

8. **Model / decision card**
9. **Drift monitoring with explicit cadence**
10. **Feature-importance stability checks across time**
11. **More hardened orchestration failure handling**
12. **Automated API startup on container restart**

### Strategic sequencing recommendation

1. Preserve explicit comparability between the historical **v1.0.0** baseline and the current **V2C** candidate.
2. Use **v2** for analytical redesign and re-run the downstream chain only after business decisions on the eligible population are clarified.
3. Use **v3** for heavier production hardening and customer-facing delivery layer once the analytical design is stable.

---

## Future Work

### v2 — Analytical redesign

1. Revisit churn-eligibility population design (business-first)
2. Refine the churn target if required
3. Add predictive CLV as a parallel decision layer
4. Recalibrate thresholds with ROI logic
5. Implement structured cohort analysis
6. Add uplift modeling
7. Re-run all downstream notebooks if the analytical base changes materially

### v3 — Production hardening

1. Build the React business-facing UI
2. Add drift monitoring and monitoring cadence
3. Implement the customer-facing delivery layer (Layer 3): a hardened stack combining production scheduling, channel execution governance (e.g. Braze or equivalent), event tracking, and feedback loop — consuming the retention payload produced by the existing n8n Layer 2 pipeline
4. Automate daily scoring pipeline so `churn_predictions` is populated without manual parquet loading
5. Implement automated API startup on container restart (remove manual rclone dependency)
6. Extend model governance and artifact registry
7. Containerize broader serving / interface stack if needed

---

## Version Note

This README documents the **current synchronized local v2 candidate with Phase 2 complete** state. The earlier GitHub publication corresponded to the **v1.0.0 baseline**. Any next public release should preserve explicit comparability between the published v1 baseline and this canonical `V2C` redesign, and document the Phase 2 n8n V9 operational validation (two-workflow architecture) as a completed milestone.

---

## License & Contact

**Personal Portfolio Project — All Rights Reserved**

This project was built as a personal deep-dive into production-grade churn modeling after completing a Master's in Data Science with AI. The VivaMarket Brasil business context is a project framing construct used for portfolio-quality analytical storytelling.

If you reuse ideas or workflow patterns from this repository, attribution is appreciated.

**Project Author:**
- **Name:** Alberto Sánchez
- **LinkedIn:** https://www.linkedin.com/in/albertosvallejo/
- **GitHub:** https://github.com/albertosvallejo/

---

**Last Updated:** May 18, 2026  
**Pipeline version:** v20260518 · n8n V9  
**Status:** NB01–NB09 Complete · Phase 2 Complete · n8n V9 Executed (two-workflow architecture) · v1.0.0 Baseline Published · Canonical V2C Candidate Synchronized

---

*This README serves both as technical documentation and as a publication-oriented narrative of the project's analytical evolution from the published v1 baseline through the current synchronized V2C candidate with Phase 2 operational validation.*
