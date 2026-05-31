![VivaMarket logo](../assets/images/logo.gif)

# MODEL CARD — DAILY CUSTOMER CHURN PREDICTOR (PHASE 4 V3 DEMO)

**Card version:** 20260531  
**Measurement scope:** Simulated campaign baseline

## 1. Model identity
- **Project:** Daily Customer Churn Predictor — VivaMarket Brasil
- **Analytical line:** canonical `V2C` baseline with Phase 4 synthetic feedback-loop governance layer
- **Primary model:** XGBoost
- **Evaluation frame:** held-out temporal test split + synthetic closed-conversion measurement baseline for portfolio governance review

## 2. Intended use
- Demonstrate a production-minded retention scoring workflow with explicit governance and measurement layers.
- Support stakeholder review of tiering, drift, holdout integrity, and portfolio-grade experimentation logic.
- Keep all campaign-performance evidence clearly labeled as demo/simulated until real customer outcome telemetry exists.

## 3. Performance snapshot
- **ROC AUC:** 0.8016
- **Average precision:** 0.9937
- **Precision@Top 10%:** 0.9970
- **Closed conversion evaluations:** 131,432
- **Current dispatch-ready rows:** 2,844

## 4. Comparison vs prior baselines
| Version | Model | ROC AUC | Avg precision | Precision@Top 10% |
| --- | --- | ---: | ---: | ---: |
| v1 | xgboost | 0.8016 | 0.9937 | 0.9970 |
| v2 | xgboost | 0.8016 | 0.9937 | 0.9970 |

## 5. Observed governance / measurement layer
### Holdout lift by tier (simulated benchmark)
| Tier | Window (days) | Treated CR | Holdout CR | Lift |
| --- | ---: | ---: | ---: | ---: |
| HIGH | 14 | 0.1767 | 0.0964 | 0.0803 |
| LOW | 30 | 0.0572 | 0.0413 | 0.0159 |
| MEDIUM | 21 | 0.1092 | 0.0589 | 0.0504 |

### Drift trigger summary
- No retraining trigger breached on the current portfolio governance pass.

## 6. Active drift monitor snapshot
| Feature | Baseline mean | Current mean | KS stat | Trigger |
| --- | ---: | ---: | ---: | --- |
| recency_days | 186.7735 | 186.6698 | 0.0046 | NO |
| total_orders | 2.1237 | 2.1336 | 0.0054 | NO |
| total_payment_value | 310.0993 | 316.2762 | 0.0068 | NO |
| orders_30d | 0.0637 | 0.0633 | 0.0004 | NO |
| orders_90d | 0.2215 | 0.2191 | 0.0032 | NO |

## 7. Tier stability snapshot
| Tier | Baseline share | Current share | Delta |
| --- | ---: | ---: | ---: |
| HIGH | 0.2002 | 0.1980 | -0.0023 |
| LOW | 0.5000 | 0.5039 | 0.0039 |
| MEDIUM | 0.2998 | 0.2982 | -0.0016 |

## 8. Top active driver families
| Tier | Driver family | Offer type | Rows |
| --- | --- | --- | ---: |
| LOW | monetary | value_bundle_offer | 843 |
| HIGH | frequency | repeat_purchase_nurturing | 530 |
| MEDIUM | frequency | repeat_purchase_nurturing | 505 |
| LOW | frequency | repeat_purchase_nurturing | 380 |

## 9. Main limitations and honesty note
- Campaign outcomes in this card are synthetic/demo-generated and must not be presented as observed production lift.
- The target remains positive-heavy, so ranking strength is more trustworthy than naive probability interpretation.
- Governance triggers are useful here as a design demonstration, but the portfolio scope still lacks true production-time telemetry.

## 10. Recommended next step
- Use this governance baseline to support Block F population-redesign benchmarking, keeping the `V2C` baseline as the permanent reference and documenting whether the redesign yields materially better holdout lift or only a marginal/null improvement.
