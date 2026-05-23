# MODEL CARD — DAILY CUSTOMER CHURN PREDICTOR (LOCAL V2 CANDIDATE)

**Card version:** 20260519

## 1. Model identity
- **Project:** Daily Customer Churn Predictor — VivaMarket Brasil
- **Analytical line:** canonical `V2C` local candidate
- **Primary model:** XGBoost
- **Evaluation frame:** held-out temporal test split on the eligible repeat-customer base
- **Operational downstream artifacts validated:** diagnostics, explainability, scoring package, retention payload, dashboard

## 2. Intended use
- Prioritize repeat customers for retention review inside a daily scoring workflow.
- Support CRM tiering, explainability review, and orchestration preparation.
- Support an internal pilot / controlled operational validation layer before any stronger customer-facing activation stack is treated as production-ready.
- Provide a portfolio-grade example of a Spec-Driven churn system with explicit operational caveats.

## 3. Not intended use
- Do not interpret scores as causal uplift or incremental treatment effect.
- Do not treat current HIGH / MEDIUM / LOW tiers as financially optimized thresholds.
- Do not present the current candidate as a final production policy without calibration and ROI validation.
- Do not present the current operational layer as a fully hardened real-send system; it is more accurately framed as an internal operational validation baseline.

## 4. Eligible population and label
- `total_orders >= 2`
- `tenure_days >= 90`
- Adaptive churn horizon: `min(150, max(75, round(1.25 * median_gap_days)))`
- Fallback horizon: `75` days
- Label interpretation: churn is inferred from lack of purchase inside the adaptive future horizon.

## 5. Performance snapshot
- **ROC AUC:** 0.8016
- **Average precision:** 0.9937
- **Precision@Top 5%:** 1.0000
- **Precision@Top 10%:** 0.9970
- **Mean predicted score (test):** 0.8703
- **Brier score:** 0.0572
- **Label prevalence (test):** 0.9770
- **Scored rows (test):** 3346

## 6. Comparison vs published v1 baseline
| version_name | model_name | split | roc_auc | average_precision | precision_at_top_5pct | precision_at_top_10pct |
| --- | --- | --- | --- | --- | --- | --- |
| v1 | xgboost | test | 0.5888 | 0.9937 | 0.9921 | 0.9934 |
| v2 | xgboost | test | 0.8016 | 0.9937 | 1.0000 | 0.9970 |

## 7. Operational output profile (latest local run)
| risk_tier | customers | rows | avg_probability | avg_discount_pct | avg_payment_value | send_rows | control_rows | vip_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HIGH | 375 | 670 | 0.9927 | 25.6343 | 251.8046 | 570 | 100 | 85 |
| LOW | 992 | 1673 | 0.7584 | 0.0000 | 358.2535 | 1673 | 0 | 0 |
| MEDIUM | 617 | 1003 | 0.9751 | 12.0000 | 268.7188 | 1003 | 0 | 0 |

## 8. Dominant driver groups
| top_driver_group | customers |
| --- | --- |
| frequency | 791 |
| monetary | 724 |
| recency | 392 |
| other | 79 |

## 9. Main strengths
- Material ranking lift versus the published v1 baseline.
- Clear handoff from probability score to driver group, incentive policy, and contact path.
- Real local execution recently revalidated through NB05–NB09 without blocking errors.
- Strong project narrative continuity from analytical redesign to internal operational activation.

## 10. Main limitations and risks
- The target remains extremely positive-heavy; average precision is therefore structurally inflated by prevalence.
- Calibration should be interpreted cautiously even though ranking quality is strong.
- Explainability remains based on a robust sample rather than a full-population SHAP pass.
- Current operational tiers are percentile-based heuristics, not ROI-optimized policy thresholds.

## 11. Calibration note
| calibration_bin | customers | avg_predicted_probability | observed_churn_rate | absolute_calibration_gap |
| --- | --- | --- | --- | --- |
| (0.0528, 0.591] | 220.0000 | 0.4027 | 0.8925 | 0.4898 |
| (0.591, 0.792] | 246.0000 | 0.7003 | 0.9731 | 0.2728 |
| (0.792, 0.878] | 243.0000 | 0.8403 | 0.9641 | 0.1238 |
| (0.878, 0.928] | 266.0000 | 0.9053 | 0.9821 | 0.0768 |
| (0.928, 0.956] | 254.0000 | 0.9440 | 0.9790 | 0.0351 |
| (0.956, 0.971] | 245.0000 | 0.9649 | 0.9940 | 0.0292 |
| (0.971, 0.981] | 235.0000 | 0.9761 | 0.9910 | 0.0149 |
| (0.981, 0.988] | 226.0000 | 0.9844 | 0.9970 | 0.0126 |
| (0.988, 0.993] | 212.0000 | 0.9903 | 1.0000 | 0.0097 |
| (0.993, 0.998] | 185.0000 | 0.9952 | 0.9970 | 0.0018 |

## 12. Threshold review note
- Threshold review table not available in the latest diagnostics export.

## 13. Governance recommendations before stronger production hardening
1. Replace provisional percentile tiers with calibrated and ROI-aware decision thresholds.
2. Validate response uplift experimentally before turning the ROI layer into a decision policy.
3. Use the current orchestration layer as an internal-pilot-first / controlled-validation baseline before presenting a true real-send production layer.
4. Add drift monitoring and a lightweight model / artifact registry for repeated scoring cycles.
5. Keep explicit comparability against the published v1 baseline in public-facing materials.
