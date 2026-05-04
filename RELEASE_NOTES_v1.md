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
