# Daily Customer Churn Predictor

**Spec-Driven Churn Intelligence System for VivaMarket Brasil**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Modeling-EC6B23.svg)](https://xgboost.readthedocs.io/)
[![Scikit--learn](https://img.shields.io/badge/scikit--learn-Validation-F7931E.svg)](https://scikit-learn.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook%20Pipeline-F37626.svg)](https://jupyter.org/)
[![License](https://img.shields.io/badge/License-Personal%20Portfolio-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-v1.0.0%20Baseline%20%7C%20NB01--NB09%20Complete-yellowgreen.svg)]()
[![Workflow](https://img.shields.io/badge/Workflow-Spec--Driven%20%2B%20Human%20Supervision-005090.svg)]()

---

## Executive Summary

> ⚠️ **BEFORE YOU START — ANALYTICAL BASELINE NOTE**: This repository delivers a complete end-to-end churn prediction pipeline, but the v1 baseline should not be interpreted as a final analytical definition of churn for VivaMarket Brasil. The current forward 90-day target is structurally too positive-heavy, which keeps average precision near **0.994** while limiting business separability (ROC AUC ~0.589 on the test split). This is not a model failure — it is a known consequence of a population that is dominated by one-time buyers and a permissive churn label. The limitation is documented explicitly and must be addressed as a true **v2 analytical redesign**, not as a silent patch. See STATUS.md and the Known Limitations section for full context.

This is a **personal deep-dive project** built after completing a Master's in Data Science to gain hands-on experience with production-oriented churn modeling in a realistic marketplace setting. It implements a **complete end-to-end churn prediction workflow** for VivaMarket Brasil, a marketplace-style ecommerce business, covering the full path from raw SQLite extraction to scored customer retention queues, explainability outputs, automation-ready payloads, and business-facing HTML reporting.

The goal was to go beyond a typical academic churn notebook and build a pipeline that addresses the real challenges of marketplace churn: irregular purchase behavior, an analytically complex target definition, temporal consistency requirements, and the need to translate model scores into operational business decisions.

**Development approach:** This project was built using **The Architect (v1)**, a personal Spec-Driven DS framework developed alongside this project. Every notebook was analytically specified before being built, executed with OpenClaw agent support, and reviewed under explicit human supervision before the next step was started. The workflow prioritizes traceability, notebook-by-notebook QA, and clean versioned evolution over execution speed.

**v1 baseline — key metrics:**

| Metric | Value | Context |
|:-------|:-----:|:--------|
| ROC AUC (test split) | 0.589 | Limited by positive-heavy target |
| Average Precision | 0.994 | Inflated by class imbalance |
| Risk mix — HIGH (> 0.70) | ~30.8% | Held-out scored set |
| Risk mix — MEDIUM (0.40–0.70) | ~63.4% | Held-out scored set |
| Risk mix — LOW (< 0.40) | ~5.8% | Held-out scored set |
| SHAP explainability | ✅ 5,000-row sample | NB06 |
| Deployment prep | ✅ Scoring package + smoke test | NB07 |
| Orchestration prep | ✅ n8n blueprint + retention payload | NB08 |
| Reporting | ✅ Branded HTML dashboard | NB09 |

**Top churn drivers (SHAP global importance):**

| Feature | Interpretation |
|:--------|:---------------|
| `recency_days` | Primary driver — days since last order |
| `total_freight_value` | Delivery cost experience signal |
| `max_installments` | Payment behavior complexity |
| `total_item_price` | Cumulative spend level |
| `avg_review_score` | Quality/experience signal |
| `avg_order_value` | Ticket size behavior |
| `revenue_90d` | Recent revenue window |
| `total_orders` | Frequency signal |

**Key analytical finding:** The v1 model's separability is constrained by a one-time-buyer-heavy population and a 90-day churn label that is too permissive. A v2 redesign starting from a clear business definition of "who is a retainable customer" — before touching any code — is the correct analytical next step. That decision belongs to the business, not to the data.

---

## Quick Start

> **Current status:** NB01–NB09 complete with executed canonical notebooks. The v1 baseline is publication-ready with documented limitations. React UI and hardened automation are planned for v2/v3.

### Running the notebook pipeline

```bash
# 1. Clone the repository
git clone https://github.com/albertosvallejo/daily-customer-churn-predictor.git
cd daily-customer-churn-predictor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place the source SQLite database in data/raw/
# Required: olist_ecommerce.db (or equivalent Brazilian marketplace SQLite)

# 4. Run notebooks in order (mandatory sequence)
# 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09
```

### Recommended execution context

- Python 3.11+
- Jupyter or Google Colab
- 8GB+ RAM for feature engineering and SHAP explainability sampling
- Source SQLite database placed in `data/raw/`

**Prerequisites:**
- All notebooks must be executed in sequence — each notebook's outputs feed directly into the next
- NB06 runs SHAP on a 5,000-row sample; full-population SHAP requires 16GB+ RAM
- NB07 generates a scoring package that NB08 consumes for the n8n blueprint

---

## Development Methodology

This repository was built as a **Spec-Driven Data Science project with OpenClaw agent support and explicit human supervision**.

**Spec-Driven** means every notebook was defined analytically before being built — inputs, outputs, transformations, and validation criteria were specified explicitly before any code was written. This prevents scope drift, makes QA tractable notebook by notebook, and produces artifacts whose lineage is fully traceable across the pipeline.

**OpenClaw** is an AI agent framework used to execute and iterate on notebooks within a structured workspace. It acts as the execution layer — running code, surfacing errors, and generating outputs — while all analytical decisions, validations, and direction changes are made by the human supervisor.

**Human supervision** means no output was accepted without review. Every notebook's results were inspected against the spec before the next step was started. The agent accelerates execution; the human owns the analytical decisions.

### The Architect (v1)

The Spec-Driven workflow in this project was developed using **The Architect**, a personal DS project framework (v1) created specifically to structure the development of data science projects from analytical specification through to operational delivery.

A few honest notes about The Architect v1:

- It is a **personal framework**, not a published tool. v1 was built and battle-tested for the first time on this project.
- Because it is a personal platform, it runs against a **ChatGPT Pro monthly subscription** rather than against an API — a deliberate decision to keep project costs controlled without a per-token billing model.
- It will **evolve with each new project**. As best practices for agent-assisted DS development mature and new projects surface new edge cases, The Architect will be updated to reflect those learnings. This repository represents The Architect v1 in its initial form.

The result is a workflow that emphasizes structured execution, notebook-by-notebook QA, operational traceability, reproducibility, and business-facing deliverables that can evolve cleanly across versions.

---

## Table of Contents

- [Project Context](#project-context)
- [Business Problem](#business-problem)
- [Development Methodology](#development-methodology)
- [Methodology](#methodology)
- [Modeling Approach](#modeling-approach)
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
- [License & Contact](#license--contact)

---

## Project Context

### Why build a churn predictor for a marketplace in 2026?

Churn prediction in subscription businesses is a solved problem: the event is defined (cancellation), the population is clean (active subscribers), and the label is unambiguous. Marketplace churn is fundamentally different and much harder. There is no cancellation event. The population boundary is blurry — most customers in any marketplace cohort bought once and never returned, which is normal purchasing behavior, not churn. And "inactive for 90 days" means something very different for a customer who placed seven orders over two years versus one who placed a single order last quarter.

This project was built precisely in that harder context. The VivaMarket Brasil dataset is a real-world Brazilian marketplace transaction log, and the challenges it presents — one-time-buyer dominance, irregular interpurchase intervals, label leakage risk in temporal splits, and the difficulty of defining a "retainable" population — are the same challenges that data science teams at Mercado Libre, Shopee, or any marketplace-format ecommerce face when they try to build operationally useful churn systems.

The v1 baseline tackles these challenges as a first-pass full pipeline. It establishes a working end-to-end system, documents the known limitations honestly, and lays the analytical foundation for a v2 redesign where the population and target definitions are refined from first principles.

### Project background

This is a **personal deep-dive project** built after completing a Master's in Data Science to gain hands-on experience with production-oriented churn modeling, SHAP-based explainability, and automation-ready ML systems in a realistic ecommerce setting.

The goal was to go beyond typical course implementations and build a complete, operationally structured churn pipeline that addresses the challenges you actually face on marketplace data:

- Analytically complex target definition with no natural churn event
- Population dominated by one-time buyers with no clear retention intent
- Temporal consistency requirements for feature engineering and model training
- SHAP explainability that maps model outputs to business-actionable driver groups
- Automation-ready artifacts for downstream orchestration without over-engineering the serving layer
- Honest reporting when the v1 metric picture reveals an analytical constraint that requires a redesign

The result is a robust, well-documented pipeline I would be comfortable presenting in a senior data science or CRM analytics context.

**Completed — Master's in Data Science with AI, BIG School (2026)**  
URL: https://thebigschool.com/master-data-science-con-ia/

### Business Context

VivaMarket Brasil is a marketplace-style ecommerce platform with a transactional customer base that purchases irregularly across multiple product categories.

**Core business challenge:** VivaMarket needs to identify customers at risk of permanent disengagement in the next 90 days and translate model outputs into operational retention actions — discount offers, re-engagement communications, and loyalty reinforcement — in a way that can be orchestrated automatically on a daily basis.

**Target user profile:** CRM manager or retention analyst at VivaMarket Brasil, responsible for daily operational decisions on which customers receive which retention incentives.

---

## Business Problem

### Challenge Statement

The project addresses four interconnected analytical challenges typical of marketplace-format ecommerce:

**Ambiguous churn definition.** Unlike subscriptions, marketplaces have no cancellation event. Churn must be defined as inactivity over a forward window (90 days in v1), which is simultaneously too permissive for active multi-purchase customers and too strict for naturally low-frequency buyers. The eligible population and the label are co-dependent analytical decisions.

**One-time-buyer dominance.** A large share of the historical customer base placed exactly one order and never returned. Including these customers in the modeling population conflates normal single-purchase behavior with true disengagement, biasing the churn label toward near-universal positivity in later snapshots.

**Temporal consistency.** Building a churn model from transactional data requires careful snapshot engineering: features must be computed from history strictly before the observation date, and the churn label must be computed from future activity strictly after it. Any leakage in this temporal boundary inflates model metrics artificially.

**Operational translation.** A model score is not a retention action. The pipeline must produce not only probabilities and risk tiers but also a payload that maps each customer to a specific action, channel, and incentive level — and that payload must be automation-ready for daily orchestration.

### Core Questions

1. Can we build a reproducible churn baseline from raw marketplace transactional data?
2. Can we map model scores into business-facing retention actions with a defensible tier logic?
3. Can we explain churn drivers clearly enough for operational stakeholders using SHAP?
4. Can we prepare the outputs for daily automation via n8n without over-engineering the serving layer?

### Success Criteria

**Pipeline quality (all must pass for v1 publication):**
- Complete notebook execution NB01 → NB09 with no broken artifact handoffs
- Temporal split integrity: no feature leakage across the observation boundary
- SHAP outputs generated successfully on the scored sample
- Retention payload covers 100% of scored customers (SHAP sample + business-rule fallback)
- n8n workflow blueprint generated and validated

**Business quality (go/no-go for stakeholder delivery):**
- Risk tiers map to differentiated retention actions (not uniform treatment)
- SHAP driver groups interpretable in business language (recency, experience, frequency, monetary)
- HTML reporting deliverable presentable to a non-technical stakeholder

**Editorial quality:**
- All notebooks in English — no Spanish in Markdown, prints, or chart labels
- VivaMarket Brasil visual identity applied consistently across HTML reports
- Canonical executed notebooks as the single source of truth (no duplicate `.executed.ipynb` files)

---

## Methodology

### End-to-End Flow

```
Raw SQLite data
→ data cleaning + churn-oriented EDA
→ repeated customer snapshot engineering
→ temporal model training (XGBoost)
→ diagnostics + threshold analysis
→ SHAP explainability + driver grouping
→ deployment preparation (scoring package)
→ retention orchestration design (n8n)
→ branded HTML reporting dashboard
```

### Data Foundation

The project works from a local SQLite ecommerce dataset (Brazilian marketplace transaction log) and builds a modeling-ready customer-snapshot layer. Each snapshot represents a customer observed at a specific temporal checkpoint, with:

- behavioral features computed from history before the snapshot date
- a forward 90-day churn label computed from activity after the snapshot date
- multiple snapshots per customer across different temporal windows

This snapshot approach allows the model to observe the same customer at different stages of their lifecycle and simulates an operational daily-scoring setup.

### Feature Families

The feature space combines six behavioral blocks:

| Family | Features | Analytical role |
|:-------|:---------|:----------------|
| **Recency & frequency** | `recency_days`, order counts, activity windows, interpurchase behavior | Primary churn signal |
| **Monetary** | `total_item_price`, `revenue_90d`, `avg_order_value`, freight, installments | Value segmentation |
| **Product breadth** | Distinct categories, distinct products, category variety | Engagement depth |
| **Quality & experience** | `avg_review_score`, delivery-related aggregates | Satisfaction signal |
| **Payment mix** | Credit-card concentration, payment-amount windows | Behavioral pattern |
| **Customer profile** | Tenure, location indicators | Segment enrichment |

### Modeling Logic

The v1 baseline uses a supervised binary classification approach:

- **Target:** forward 90-day churn indicator (1 = no purchase in next 90 days)
- **Model:** XGBoost classifier with temporal train/test split
- **Training:** single temporal split respecting the snapshot chronology
- **Evaluation:** ROC AUC, average precision, precision-recall curve, threshold trade-off table
- **Risk tiers:** HIGH (> 0.70), MEDIUM (0.40–0.70), LOW (< 0.40) — provisional thresholds for v1

### Orchestration Positioning

The current automation layer is expressed through **n8n artifacts** — a workflow blueprint and retention payload designed for daily scheduled execution. For this v1 baseline, n8n is a valid professional choice: it acts as the orchestration layer rather than the analytical core, and it keeps operational complexity low while the analytical definition is still being refined. A v3 may replace this with Prefect or an equivalent production-grade orchestrator once the population and label design are stable.

---

## Modeling Approach

### Input Population Logic

The v1 baseline includes all customers with at least one recorded order in the snapshot history. This means the eligible population is not filtered to exclude one-time buyers — a known limitation documented explicitly. The practical consequence is that a large share of the HIGH-risk tier may represent customers who were always going to be one-time buyers, not customers who were retainable and disengaged.

Correcting this requires a **business-first decision** about what constitutes a retainable customer. That decision must precede any code change in NB03.

### Model Specification

```python
# XGBoost binary classifier — v1 defaults
XGBClassifier(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    use_label_encoder=False,
    eval_metric='auc',
    random_state=42
)
```

### Diagnostic Logic

NB05 produces a structured diagnostic stack covering:

- ROC curve and AUC on the held-out test split
- Precision-recall curve and average precision
- Calibration curve (reliability diagram)
- Threshold trade-off table (precision, recall, F1 across probability cutoffs)
- Risk-tier mix summary for the scored population
- Revenue-oriented diagnostic views by risk tier

### Explainability Logic

NB06 produces SHAP-based explainability on a 5,000-row scored sample. The objective is not only global feature importance ranking but business interpretation of churn drivers by risk tier. SHAP values are grouped into four interpretable driver families:

| Driver group | Key features | Business interpretation |
|:------------|:------------|:------------------------|
| **Recency** | `recency_days`, activity windows | Customer is drifting away |
| **Monetary** | Revenue windows, AOV, freight | Spend level and delivery cost signals |
| **Frequency** | Order counts, interpurchase behavior | Engagement regularity |
| **Experience** | Review score, delivery aggregates | Satisfaction and product quality |

### Operational Decisioning Logic

The v1 baseline converts probabilities into provisional risk tiers with differentiated retention actions:

| Risk tier | Probability | Retention action | Control group |
|:----------|:-----------:|:----------------|:-------------:|
| **HIGH** | > 0.70 | Urgent incentive (discount + direct outreach) | 15% holdout |
| **MEDIUM** | 0.40–0.70 | Nurturing (educational content + soft offer) | — |
| **LOW** | < 0.40 | Loyalty (upsell / LTV growth) | — |

These thresholds should not be considered final production business policy until the eligible population, target definition, and probability calibration are refined in v2.

---

## Results & Performance

### v1 Baseline Metrics

| Metric | Value | Gate |
|:-------|:-----:|:----:|
| ROC AUC (test split) | ~0.589 | ⚠ Limited separability — see Known Limitations |
| Average Precision | ~0.994 | ⚠ Inflated by class imbalance |
| SHAP explainability | ✅ 5,000-row sample | ✅ |
| Retention payload coverage | 100% of scored set | ✅ (SHAP + fallback) |
| n8n blueprint | ✅ Generated | ✅ |

### Risk Mix (Held-Out Scored Set)

| Risk tier | Share | Avg probability | Interpretation |
|:----------|:-----:|:---------------:|:---------------|
| HIGH | ~30.8% | > 0.70 | Urgent retention candidates |
| MEDIUM | ~63.4% | 0.40–0.70 | Nurturing / monitoring |
| LOW | ~5.8% | < 0.40 | Loyalty and LTV growth |

### Interpretation

The v1 model is technically complete and operationally useful as a baseline. However, the near-universal positive rate in the churn label means the model is primarily learning to score degrees of "how positive" rather than to genuinely separate churners from retained customers. The high average precision reflects class imbalance, not model quality. The correct next step is an analytical redesign of the eligible population and churn label — not calibration or threshold tuning on top of the current definition.

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        RAW DATA LAYER                             │
│  SQLite ecommerce database — Brazilian marketplace transaction log │
└──────────────────────────┬───────────────────────────────────────┘
                            │
                   NB01 — Data Cleaning
                   • Raw SQL extraction from SQLite
                   • Missing value treatment
                   • Data type normalization
                   • Customer-level join and deduplication
                            │
                   NB02 — EDA
                   • Churn-oriented exploration
                   • Purchase frequency and recency distributions
                   • Category and payment behavior analysis
                   • Feature selection justification
                            │
                   NB03 — Feature Engineering
                   • Customer snapshot construction (temporal windows)
                   • Rolling behavioral aggregates (recency, frequency, monetary)
                   • Product breadth and experience features
                   • Forward 90-day churn label computation
                   • Temporal train/test split
                            │
                   NB04 — Model Training
                   • XGBoost binary classifier
                   • Temporal train/test split (no leakage)
                   • Hyperparameter configuration
                   • Model artifact export (.joblib)
                            │
                   NB05 — Evaluation & Diagnostics
                   • ROC AUC, average precision, calibration
                   • Threshold trade-off table
                   • Risk-tier mix summary
                   • Revenue-oriented diagnostic views
                            │
                   NB06 — Explainability
                   • SHAP values on 5,000-row scored sample
                   • Global feature importance ranking
                   • Driver group assignment (recency/monetary/frequency/experience)
                   • Per-tier top driver analysis
                   • Offer recommendation mapping
                            │
                   NB07 — Deployment Preparation
                   • Scoring package export (.joblib bundle)
                   • Smoke-test inference on held-out rows
                   • Scoring script (src/models/churn_scoring.py)
                            │
                   NB08 — Orchestration (n8n)
                   • Retention action payload construction
                   • SHAP + business-rule fallback coverage
                   • n8n daily workflow blueprint (.json)
                   • Control group flagging (15% HIGH holdout)
                            │
                   NB09 — Reporting Dashboard
                   • Risk mix summary
                   • Model summary metrics
                   • Top driver mix by risk tier
                   • Retention action mix
                   • Branded HTML dashboard (churn_monitoring_dashboard_YYYYMMDD.html)
```

---

## Notebook Pipeline Reference

Each notebook has a defined input/output contract. The execution sequence is mandatory.

**Execution order:** `01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09`

---

### NB01 — Data Cleaning (`01_data_cleaning.ipynb`)

**Purpose:** Extract raw transactional data from the SQLite source, apply data quality fixes, normalize types, and output a clean customer-level dataset ready for EDA and feature engineering.

**Input:** `data/raw/*.db` (SQLite ecommerce database)

**Output:** `data/processed/churn_clean_YYYYMMDD.parquet`

**Key transformations:**
- Raw SQL queries joining orders, customers, payments, reviews, and geolocation tables
- Missing value treatment per column with documented imputation logic
- Data type enforcement (dates, numeric, categorical)
- Customer deduplication and unique ID standardization

---

### NB02 — EDA (`02_eda_exploratory.ipynb`)

**Purpose:** Characterize the transactional dataset from a churn-prediction perspective — purchase frequency distributions, recency patterns, category behavior, and review score signals — and justify the feature selection decisions applied in NB03.

**Input:** `data/processed/churn_clean_YYYYMMDD.parquet`

**Key outputs (charts and tables, not files):**
- Purchase frequency distribution — confirms one-time-buyer dominance
- Recency distribution by purchase count segment
- Revenue and AOV distributions by customer tier
- Review score distributions and their correlation with reorder behavior

---

### NB03 — Feature Engineering (`03_feature_engineering.ipynb`)

**Purpose:** Build the customer snapshot table with all behavioral features and attach the forward 90-day churn label. This notebook is the core analytical transformation step and contains the temporal boundary logic that prevents label leakage.

**Input:** `data/processed/churn_clean_YYYYMMDD.parquet`

**Output:** `data/processed/churn_features_YYYYMMDD.parquet`

**Critical implementation notes:**

- The churn label is computed as `1` if the customer has no order in the 90 days following the snapshot date. This window must be computed strictly from future data (i.e., rows with `order_purchase_timestamp > snapshot_date + 0 days`).
- All behavioral features must be computed from history strictly before the snapshot date. No future information should enter any feature computation.
- The train/test split is temporal: all snapshots before a cutoff date go to train, all after go to test. Random splits are not acceptable for time-series customer data.

---

### NB04 — Model Training (`04_model_training.ipynb`)

**Purpose:** Train the XGBoost binary classifier on the feature snapshot table, evaluate in-sample and out-of-sample performance, and export the model artifact.

**Input:** `data/processed/churn_features_YYYYMMDD.parquet`

**Output:**
- `models/churn_model_YYYYMMDD.joblib`
- `data/processed/churn_predictions_YYYYMMDD.parquet` (scored held-out set)
- `data/processed/churn_model_metrics_YYYYMMDD.csv`

---

### NB05 — Evaluation & Diagnostics (`05_model_evaluation_diagnostics.ipynb`)

**Purpose:** Comprehensive model evaluation — ROC/PR curves, calibration, threshold analysis, and risk-tier mix — providing the diagnostic foundation for the explainability and deployment steps.

**Input:** `data/processed/churn_predictions_YYYYMMDD.parquet`, `data/processed/churn_model_metrics_YYYYMMDD.csv`

**Output:** `data/processed/churn_diagnostics_YYYYMMDD.csv`, `reports/model_diagnostics_YYYYMMDD.html`

**Diagnostics performed:**
- ROC curve and AUC
- Precision-recall curve and average precision
- Reliability diagram (calibration)
- Threshold trade-off table (precision, recall, F1, lift by decile)
- Risk-tier mix summary (HIGH / MEDIUM / LOW counts and shares)
- Revenue-weighted diagnostic views per tier

---

### NB06 — Explainability (`06_churn_attribution_explainability.ipynb`)

**Purpose:** SHAP-based churn attribution on the scored sample — global and per-tier feature importance, driver group assignment, and offer recommendation mapping.

**Inputs:**
- `data/processed/churn_predictions_YYYYMMDD.parquet`
- `models/churn_model_YYYYMMDD.joblib`

**Outputs:**
- `data/processed/churn_explainability_YYYYMMDD.parquet`
- `data/processed/churn_driver_summary_YYYYMMDD.csv`
- `reports/churn_explainability_YYYYMMDD.html`

**Implementation note:** SHAP TreeExplainer runs on a 5,000-row stratified sample to keep execution time manageable in the current environment. Full-population SHAP is feasible with 16GB+ RAM by removing the sampling step. The 5,000-row sample is representative enough for global importance rankings and per-tier driver analysis.

---

### NB07 — Deployment Preparation (`07_model_deployment_preparation.ipynb`)

**Purpose:** Package the trained model into a self-contained scoring bundle, generate a scoring inference script, and validate the package with a smoke test on held-out rows.

**Input:** `models/churn_model_YYYYMMDD.joblib`, `data/processed/churn_features_YYYYMMDD.parquet`

**Output:**
- `models/churn_scoring_package_YYYYMMDD.joblib`
- `src/models/churn_scoring.py`
- `data/processed/churn_inference_smoke_test_YYYYMMDD.parquet`

---

### NB08 — Orchestration (`08_n8n_orchestration.ipynb`)

**Purpose:** Build the retention action payload, map SHAP driver groups to offer recommendations, flag control group customers, and generate the n8n daily workflow blueprint.

**Inputs:**
- `data/processed/churn_predictions_YYYYMMDD.parquet`
- `data/processed/churn_explainability_YYYYMMDD.parquet`

**Outputs:**
- `data/processed/retention_actions_YYYYMMDD.parquet`
- `n8n/daily_churn_retention_workflow_YYYYMMDD.json`
- `reports/n8n_orchestration_YYYYMMDD.html`

**Payload logic:** The retention payload covers 100% of the scored set. Customers in the SHAP sample receive driver-specific offer recommendations. Customers outside the sample receive business-rule defaults based on their risk tier. The HIGH tier includes a 15% control group holdout flagged with `control_group_flag = 1`.

**Known gap:** The current n8n blueprint does not define a dead letter queue or failure handling for cases where scoring fails, data arrives incomplete, or the model cannot be loaded. This is a documented v2 hardening item.

---

### NB09 — Reporting Dashboard (`09_reporting_dashboard.ipynb`)

**Purpose:** Consolidate prediction quality, churn drivers, and campaign readiness into a single branded HTML monitoring dashboard for stakeholder review.

**Inputs:**
- `data/processed/churn_predictions_YYYYMMDD.parquet`
- `data/processed/churn_explainability_YYYYMMDD.parquet`
- `data/processed/retention_actions_YYYYMMDD.parquet`
- `data/processed/churn_diagnostics_YYYYMMDD.csv`

**Output:** `reports/churn_monitoring_dashboard_YYYYMMDD.html`

**Dashboard sections:**
1. Risk mix (HIGH / MEDIUM / LOW counts, average probabilities, observed churn rate)
2. Model summary metrics (from diagnostics)
3. Top driver mix by risk tier
4. Retention action mix (send vs. control by tier and channel)

---

## Main Deliverables

### Processed data artifacts (v1 run — 20260502)

| File | NB | Contents |
|:-----|:--:|:---------|
| `churn_features_20260502.parquet` | NB03 | Customer snapshot table with all features + churn label |
| `churn_predictions_20260502.parquet` | NB04 | Scored held-out set with risk tiers |
| `churn_model_metrics_20260502.csv` | NB04 | ROC AUC, AP, threshold-level metrics |
| `churn_diagnostics_20260502.csv` | NB05 | Structured diagnostic output by section |
| `churn_explainability_20260502.parquet` | NB06 | SHAP values + driver group + top driver per customer |
| `churn_driver_summary_20260502.csv` | NB06 | Aggregated driver mix by risk tier |
| `churn_inference_smoke_test_20260502.parquet` | NB07 | Smoke-test inference output |
| `retention_actions_20260502.parquet` | NB08 | Full retention payload with offer + channel + control flag |

### Models and scoring assets

| File | Contents |
|:-----|:---------|
| `models/churn_model_20260502.joblib` | Trained XGBoost classifier |
| `models/churn_scoring_package_20260502.joblib` | Self-contained scoring bundle (model + feature schema) |
| `src/models/churn_scoring.py` | Inference script for operational scoring |

### Reporting and orchestration outputs

| File | Contents |
|:-----|:---------|
| `reports/model_diagnostics_20260502.html` | Branded diagnostic report |
| `reports/churn_explainability_20260502.html` | SHAP-based explainability report |
| `reports/n8n_orchestration_20260502.html` | Orchestration blueprint summary |
| `reports/churn_monitoring_dashboard_20260502.html` | Consolidated monitoring dashboard |
| `n8n/daily_churn_retention_workflow_20260502.json` | n8n workflow blueprint |

---

## File Structure

```
daily-customer-churn-predictor/
│
├── README.md
├── .gitignore
├── requirements.txt
├── STATUS.md
├── RELEASE_NOTES_v1.md
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb                    ✅ Canonical executed
│   ├── 02_eda_exploratory.ipynb                  ✅ Canonical executed
│   ├── 03_feature_engineering.ipynb              ✅ Canonical executed
│   ├── 04_model_training.ipynb                   ✅ Canonical executed
│   ├── 05_model_evaluation_diagnostics.ipynb     ✅ Canonical executed
│   ├── 06_churn_attribution_explainability.ipynb ✅ Canonical executed
│   ├── 07_model_deployment_preparation.ipynb     ✅ Canonical executed
│   ├── 08_n8n_orchestration.ipynb                ✅ Canonical executed
│   ├── 09_reporting_dashboard.ipynb              ✅ Canonical executed
│   └── Workflow.xlsx                             Pipeline planning and sequencing reference
│
├── data/
│   ├── raw/                                      # gitignored
│   │   ├── churn_sqlite_db.sqlite                # Source database
│   │   ├── churn_sqlite_db_source.txt            # Dataset origin and attribution notes
│   │   └── churn_sqlite_db_schema.png            # Database schema diagram
│   │
│   ├── interim/                                  # gitignored
│   │   └── client_database_clean_20260429.parquet  # NB01 output: cleaned customer base
│   │
│   └── processed/                               # gitignored
│       ├── churn_features_20260502.parquet       # NB03: customer snapshot + churn label
│       ├── churn_predictions_20260502.parquet    # NB04: scored held-out set + risk tiers
│       ├── churn_model_metrics_20260502.csv      # NB04: ROC AUC, AP, threshold metrics
│       ├── churn_diagnostics_20260502.csv        # NB05: structured diagnostic output
│       ├── churn_explainability_20260502.parquet # NB06: SHAP values + driver groups
│       ├── churn_driver_summary_20260502.csv     # NB06: driver mix by risk tier
│       ├── churn_inference_smoke_test_20260502.parquet  # NB07: smoke-test output
│       └── retention_actions_20260502.parquet    # NB08: full retention payload
│
├── models/                                       # gitignored
│   ├── churn_model_20260502.joblib               # Trained XGBoost classifier
│   └── churn_scoring_package_20260502.joblib     # Self-contained scoring bundle
│
├── src/
│   └── models/
│       └── churn_scoring.py                      # Operational scoring inference script
│
├── n8n/
│   └── daily_churn_retention_workflow_20260502.json   # n8n daily workflow blueprint
│
├── reports/                                      # HTML deliverables — committed to repo
│   ├── model_diagnostics_20260502.html
│   ├── churn_explainability_20260502.html
│   ├── n8n_orchestration_20260502.html
│   └── churn_monitoring_dashboard_20260502.html
│
├── assets/
│   └── images/
│       ├── logo.png                              # Project logo (static)
│       ├── logo.gif                              # Project logo (animated)
│       ├── visual_identity_guide_v1.pdf          # Brand and visual identity guide
│       └── communication_pieces_v1.pdf           # Communication design assets
│
└── _private/                                     # Internal spec docs — gitignored
```

Project rule: each notebook step is represented by **one canonical `.ipynb` file only**. The kept notebook is the executed and debugged version. No `.executed.ipynb` or `.audit_run.ipynb` variants in the public repo.

---

## Technical Stack

| Category | Technology | Version | Purpose |
|:---------|:----------:|:-------:|:--------|
| **Language** | Python | 3.11 | Core development |
| **Modeling** | XGBoost | ≥ 2.1 | Binary churn classification |
| **ML utilities** | scikit-learn | ≥ 1.5 | Feature scaling, evaluation, train/test split |
| **Explainability** | SHAP | ≥ 0.45 | TreeExplainer for feature attribution |
| **Data manipulation** | pandas | ≥ 2.2 | Pipeline data handling |
| **Numerical operations** | NumPy | ≥ 2.0 | Array ops |
| **Visualization** | matplotlib / seaborn | ≥ 3.9 / ≥ 0.13 | All charts with brand palette |
| **Interactive charts** | Plotly | ≥ 5.24 | Dashboard interactive elements |
| **Database I/O** | SQLAlchemy | ≥ 2.0 | SQLite extraction |
| **Columnar I/O** | pyarrow / parquet | — | Artifact persistence |
| **Model serialization** | joblib | — | Model and scoring package export |
| **Orchestration** | n8n | — | Daily workflow automation blueprint |
| **Notebook environment** | Jupyter / Notebook | ≥ 1.1 / ≥ 7.2 | Pipeline execution |
| **Development environment** | Local + OpenClaw agent | — | Spec-Driven execution with human supervision |

---

## Methodological Notes

### 1. Snapshot-based temporal modeling

Rather than building a single static customer table, the pipeline constructs customer snapshots at multiple temporal checkpoints. This design choice reflects the operational reality of a daily churn scoring system: the same customer is observed at different points in their lifecycle, and the model must generalize across those states rather than memorizing a single behavioral snapshot.

This approach also allows temporal train/test splitting without arbitrary customer-level holdouts, preserving the chronological integrity of the evaluation.

### 2. Business-rule fallback for full-population coverage

SHAP-based explainability runs on a 5,000-row sample for execution robustness. Rather than leaving the remainder of the scored population without an action recommendation, NB08 applies business-rule defaults based on risk tier to all customers outside the SHAP sample. This ensures the retention payload covers 100% of scored customers and is immediately operational, without requiring full-population SHAP.

The tradeoff is documented explicitly: the fallback customers receive tier-generic recommendations rather than driver-specific ones. This is acceptable for v1 but should be replaced by full-population SHAP or an equivalent approximation in v2.

### 3. Population definition as a business decision first

The most important analytical lesson from the v1 build is that the eligible population for a marketplace churn model cannot be defined by data filtering alone. Deciding to exclude one-time buyers requires first answering: "what does it mean for VivaMarket Brasil that a customer is retainable?" That question has a business answer, not a data answer. The data can inform the answer, but it cannot substitute for it.

This principle should guide the v2 redesign: the population and label decisions must be made explicitly and documented before any notebook is opened.

### 4. n8n as a valid v1 orchestration layer

The choice of n8n as the orchestration layer for v1 is deliberate. Investing in a production-grade orchestrator (Prefect, Airflow) before the analytical definition of churn is stable would mean building infrastructure around a model that is likely to change significantly in v2. n8n provides enough operational structure to validate the end-to-end flow and demonstrate orchestration readiness without coupling the infrastructure to an analytically incomplete model.

---

## Known Limitations

The following limitations apply to all v1 outputs. They are documented here for technical completeness and should be communicated to any stakeholder before any retention budget decision is made based on this model.

**Positive-heavy churn label.** The current forward 90-day churn label is extremely positive in later snapshots due to one-time-buyer dominance. This keeps average precision near 0.994 but yields an ROC AUC of ~0.589 — close to random on the separability metric that actually matters for ranking. The model is learning to distinguish degrees of positivity, not genuine churners from retained customers.

**One-time-buyer contamination.** The eligible population includes all customers with at least one order. A significant share of the HIGH-risk tier represents customers who were always going to be single-purchase — their "churn" was not a retention failure but a structural characteristic of marketplace behavior. Filtering this population requires a business-first definition of retainability, not a data-driven filter.

**Sampled SHAP explainability.** NB06 explainability is based on a 5,000-row sample rather than full-population SHAP. Global importance rankings are reliable at this sample size, but per-customer explanations outside the sample are approximated by business-rule defaults.

**Provisional risk thresholds.** The HIGH/MEDIUM/LOW probability thresholds (0.70 / 0.40) are heuristic baselines, not ROI-optimized cutoffs. They have not been calibrated against incentive cost, expected margin, or customer LTV. A proper threshold optimization requires a matrix of Expected Value crossing probability, response rate, incentive cost, and customer margin.

**No probability calibration.** The model's raw probability outputs have not been calibrated (Platt scaling or isotonic calibration). This means the absolute probability values should not be interpreted as true churn probabilities — only their relative ranking is reliable for tier assignment.

**n8n failure handling absent.** The current orchestration blueprint does not define behavior for failure cases: scoring job failure, incomplete data arrival, or model loading errors. This is the first thing that breaks in production and should be addressed before any live deployment.

---

## Professional Improvement Roadmap

### Priority analytical upgrades (v2)

1. **Business-first population redesign**
   - Define "retainable customer" with the business before touching NB03.
   - The eligible population is a business decision, not a data filter.
   - This single change is the highest-leverage improvement in the entire project.

2. **Churn label redesign**
   - Revisit the 90-day window and whether it should be uniform across segments.
   - Consider cohort-based windows (e.g., 2× median interpurchase interval per segment).
   - Re-run all downstream notebooks after the label change.

3. **Predictive CLV as a parallel layer**
   - Add a basic Customer Lifetime Value model alongside the churn score.
   - A HIGH-risk customer with low CLV does not merit the same incentive as a HIGH-risk customer with high CLV.
   - The current LTV proxy (revenue quartile in NB06) is too coarse for operational decisioning.

4. **Probability calibration**
   - Add Platt scaling or isotonic calibration after model training.
   - Required before thresholds can be used as genuine probability estimates.

5. **ROI-based threshold optimization**
   - Replace static thresholds with a matrix of Expected Value: P(churn) × P(response | action) × (margin – incentive cost).
   - The 0.40/0.70 thresholds remain arbitrary until this is done.

6. **Cohort analysis**
   - Add structured cohort retention curves: how do customers who entered in the same period behave over time?
   - This will inform whether the 90-day window is appropriate across all segments.

7. **Uplift modeling**
   - Move from "who is likely to churn" toward "who is likely to respond to a retention action."
   - Recommended approach: Two-Model method (response rate with action minus response rate without) before attempting S-learner or T-learner meta-learners.
   - Requires either randomized historical experiments or explicit assumptions about selection bias.

### Governance and MLOps upgrades (v2–v3)

8. **Model card / decision card**
   - Add a concise document covering objective, target population, label logic, limitations, bias risks, thresholds, and non-recommended use cases.

9. **Drift monitoring with defined cadence**
   - Feature drift: weekly PSI check on critical features.
   - Score drift: biweekly distribution check.
   - Retrain trigger: PSI > 0.2 on top-5 SHAP features.
   - Daily PSI is excessive and noisy — weekly is the right cadence.

10. **Feature importance stability across snapshots**
    - Verify that SHAP top drivers in January are still top drivers in July.
    - If rankings shift significantly across temporal snapshots, the model is adapting to unstable patterns that may not generalize.

11. **n8n failure handling (dead letter queue)**
    - Define behavior for: scoring job failure, incomplete data, model load error.
    - This is the highest-priority operational hardening item for any live deployment.

### Strategic sequencing recommendation

The most professional next sequence is:

1. Publish and document **v1.0.0** clearly as a baseline with documented limitations.
2. Redesign the eligible population and churn label in **v2** — business decision first.
3. Re-run all downstream notebooks on the revised analytical base.
4. Add CLV layer, calibration, ROI thresholding, cohort analysis, and uplift modeling in v2.
5. Harden monitoring, UI, and automation in **v3** once the analytical design is stable.
6. Migrate from n8n to Prefect and containerize with Docker in v3.

---

## Future Work

### v2 — Analytical redesign

1. Revisit churn-eligibility population design (business-first).
2. Redefine the churn target to improve business separability.
3. Add predictive CLV as a parallel decision layer.
4. Recalibrate action thresholds with ROI logic.
5. Implement structured cohort analysis.
6. Add uplift modeling (Two-Model approach as starting point).
7. Re-run all downstream notebooks after v2 analytical decisions.

### v3 — Production hardening

1. Build the React business-facing UI with daily operational views.
2. Add drift monitoring with defined PSI/KS cadence.
3. Implement model registry (MLflow or equivalent).
4. Harden orchestration: migrate from n8n to Prefect with proper failure handling.
5. Dockerize the full stack.
6. Integrate end-to-end with the React UI.

---

## License & Contact

**Personal Portfolio Project — All Rights Reserved**

This project was built as a personal deep-dive into production-grade churn modeling after completing a Master's in Data Science with AI. The dataset is derived from the publicly available Olist Brazilian ecommerce dataset. The VivaMarket Brasil brand and business context are fictional constructs created for this project.

The codebase, methodology, and documentation are shared publicly for portfolio and educational purposes. If you use ideas or patterns from this project, attribution is appreciated.

**Project Author:**
- **Name:** Alberto Sánchez
- **Email:** alberto.sanchez@gmail.com
- **LinkedIn:** https://www.linkedin.com/in/albertosvallejo/
- **GitHub:** https://github.com/albertosvallejo/

---

**Last Updated:** May 3, 2026  
**Pipeline version:** v20260502  
**Status:** NB01–NB09 Complete · v1.0.0 Baseline · v2 Analytical Redesign Pending

---

*This README serves as both technical documentation and a full audit trail of all modeling decisions made during v1 development. The STATUS.md file and the `_private/` directory preserve the complete development history and internal improvement notes.*
