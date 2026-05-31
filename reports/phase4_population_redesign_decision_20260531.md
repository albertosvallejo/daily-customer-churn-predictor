![VivaMarket logo](../assets/images/logo.gif)

# Phase 4 Population Redesign Decision — 2026-05-31

**Measurement scope:** Portfolio decision benchmark

## Decision
`support_population_redesign_candidate`

## Benchmark summary
| Segment | Customers | Avg closed evals | Avg conversion rate | Avg treated CR | Avg holdout CR | Avg holdout lift | Avg score |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| retainable | 1163 | 41.4 | 0.1707 | 0.1736 | 0.1456 | 0.0281 | 0.6605 |
| structural_single_purchase | 2183 | 35.1 | 0.0595 | 0.0637 | 0.0543 | 0.0094 | 0.4506 |

## Rationale
- The benchmark uses the current portfolio evidence layer.
- This is a portfolio/demo redesign benchmark, not a production-observed retraining decision.
- Retainable customers show stronger average holdout lift than the structurally single-purchase segment, supporting the redesign hypothesis.

## Interpretation
- This benchmark uses the current portfolio evidence layer rather than live production telemetry.
- It is therefore valid for portfolio/demo decision-making, but not for claiming live causal superiority in production.
- The V2C baseline remains the permanent reference point.

## Next recommended action
- If the redesign candidate is only marginally better, keep V2C as the canonical public baseline and document the population problem as real but not yet decisively solved.
- If the redesign candidate is materially stronger, use this note as the basis for a later `v4.0.0` redesign workstream with explicit retraining scope.
