# Phase 6 — Prioritized Retention Intervention Recommendations
### VivaMarket Brasil · Daily Customer Churn Predictor · Phase 5B closure

**Date:** 2026-07-18 · **Status:** Phase 6 gate met · **Depends on:** Phase 1 intervention catalog (INT-01–INT-08), Phase 2-5 validated A/B testing framework, Phase 1 guardrail-coverage decision (confirmed 2026-07-18)

---

## 1. Purpose and scope

This report closes Phase 6 of the Phase 5B block: it translates the eight literature-grounded retention interventions researched in Phase 1 into a **prioritized, ready-to-pilot recommendation set**, using the validated A/B testing engine (Phase 2–5) and the real margin/cost figures already available from Phase 4.

**What this report delivers:**
- A prioritization of the 8 candidate interventions into tiers, based on guardrail risk, evidence strength, and economic upside.
- An explicit economic framework (not fabricated outcomes) for translating a future real test result into business value.
- A recommended rollout sequence and a test-design template ready for a real pilot.

**What this report does not claim:** none of the 8 interventions has been run against real VivaMarket customers. All conversion-lift figures cited below come from third-party literature (see Phase 1 catalog) or from Phase 4's own scenario modeling — not from a completed pilot of these specific interventions. The economic figures in Section 4 are a **valuation framework** to apply once a real test produces an observed lift, not a projection of what that lift will be. This keeps the same evidence boundary the rest of the project applies to Phase 4.

---

## 2. Inputs carried into this report

| Input | Source | What it provides |
|---|---|---|
| 8-intervention catalog (`INT-01`–`INT-08`) | Phase 1 | Hypothesis, cited literature, expected effect direction, candidate copy, guardrail type per intervention |
| Guardrail-coverage decision | Phase 1 scope question, confirmed 2026-07-18 | 3/8 interventions have a guardrail measurable by the current framework; the other 5 require mandatory manual review before any real pilot (see Section 3) |
| A/B testing engine | Phase 2 (`ab_testing_framework.py`), validated Phase 4-5 | Power Guardrail, Wilson CI, Holm-Bonferroni correction, 2-arm and 3-arm verdict logic, 53/53 tests, verified against 16 real scenarios |
| Real baseline conversion (`p0`) | Phase 4 KPI monitor / Model Card, cross-confirmed | HIGH-tier holdout conversion **9.6%** over a 14-day window — the best available real anchor for sample-size planning |
| Margin/cost model | Phase 4 `roi_simulation_20260519.html` | Implicit margin by tier (`ENTRY 45 · GROWTH 70 · VIP 110`, value units) and discount cost (**≈35% of implicit margin**) |

---

## 3. Guardrail coverage: how it gates this report's recommendations

The framework only measures **opt-out rate** as a quantitative guardrail. Of the 8 interventions, only 3 (`INT-01`, `INT-02`, `INT-04`) have a guardrail the system can check automatically. The other 5 touch real risks — perceived manipulation (`INT-03`, `INT-08`), review credibility (`INT-06`), accumulated communication fatigue (`INT-07`), and operational complexity rather than a customer-facing risk (`INT-05`) — that the framework cannot quantify today.

**Confirmed decision (2026-07-18):** this partial coverage is accepted. Interventions without a measurable guardrail are not blocked from testing, but **none of them may proceed to a real customer pilot without an explicit manual review and sign-off**, in addition to whatever the automated engine reports. This mirrors the same escalate-to-human-review pattern already adopted for the Power Guardrail (Decision A of Phase 5), rather than either forcing automatic coverage or freezing the roadmap until the framework is extended. Extending the framework to quantify these risks remains an optional, non-blocking future line (see the project Roadmap).

This decision directly shapes the tiering in Section 5: guardrail measurability is the single largest factor separating Tier 1 from Tier 2.

---

## 4. Economic framework (not a projection)

Phase 4's margin/cost model gives a **net value per additional conversion**, after accounting for the discount cost of the incentive:

> **Net value per incremental conversion = implicit margin × (1 − discount cost rate) = implicit margin × 0.65**

| Tier | Implicit margin | Discount cost (≈35%) | Net value per incremental conversion |
|:-----|:---------------:|:---------------------:|:---------------------:|
| ENTRY | 45 | 15.75 | **29.25** |
| GROWTH | 70 | 24.50 | **45.50** |
| VIP | 110 | 38.50 | **71.50** |

**How this is used, not what it predicts:** this table does not say what lift any intervention will produce — no real test has run yet. What it does is weight prioritization by *where in the customer base* an intervention operates. An intervention that only applies to customers with tier history (`INT-08`) is, per customer converted, worth roughly **1.6–2.4× more** than the same relative lift applied to an ENTRY-tier customer — even though its addressable population is narrower. This is why `INT-08` is ranked above where its guardrail risk alone would place it (see Section 5).

Once a real pilot for any intervention produces an observed lift (`p1 − p0`), the same table converts it directly into a projected value: `(p1 − p0) × addressable segment size × net value per conversion`. That calculation is intentionally left for the pilot stage — plugging in a lift that hasn't been measured would misrepresent this report as containing results it does not have.

---

## 5. Prioritized recommendations

### Tier 1 — Ready for a real pilot now (measurable guardrail, no new infrastructure)

| Rank | Intervention | Why it's Tier 1 | Applicable population |
|:----:|:-------------|:-----------------|:-----------------------|
| **1** | **`INT-02` — Personalization by purchase history** | Strongest literature backing of the catalog (statistically significant retention association, T=2.87 p=0.004; +26% 12-month retention; +26% open rate with personalized subject lines); guardrail (opt-out/frequency) is directly measurable; applies to the broad eligible population, not a narrow segment | All customers with a purchase-history-derived category |
| **2** | **`INT-04` — Channel: email vs. SMS/push for non-openers** | Strong, specific evidence (~90% SMS open rate vs. 25-30% email in retail benchmarks); zero new infrastructure — the n8n V9 workflow already dispatches through OneSignal; targets a segment the current channel is demonstrably not reaching | Risk customers with no opens across the last 2-3 emails |
| **3** | **`INT-01` — Urgency vs. value-first framing** | Simplest possible test (copy-only, same channel, same segment); guardrail measurable; literature suggests value-first is marginally better but is explicitly ambiguous in absolute terms — a good first, low-risk test to validate the pipeline end-to-end with a real customer send before layering in higher-stakes interventions | Medium/high-risk customers with prior purchase experience |

**Recommended rollout order:** `INT-02` first — it has the strongest evidence and the broadest applicable population, so it is both the highest-expected-value test and the best stress-test of the full pipeline (scoring → orchestration → guardrail → verdict) end-to-end on a real send. `INT-04` and `INT-01` can follow, potentially in parallel since they act on largely non-overlapping segments (channel-switch vs. same-channel copy).

### Tier 2 — Test-ready, but require mandatory manual review before any real pilot

| Rank | Intervention | Why it's Tier 2 | Manual review focus |
|:----:|:-------------|:------------------|:----------------------|
| **4** | **`INT-08` — Tier/loyalty status-loss framing** | Narrow applicable population (customers with tier history) but the highest per-conversion economic value in the catalog (GROWTH/VIP-weighted); shares the same manipulation-perception risk as `INT-03` | Confirm the "status loss" framing doesn't read as coercive to a VIP-relationship segment where trust matters most |
| **5** | **`INT-03` — Monetary incentive vs. loss-framed incentive** | Explicitly ambiguous by design in the literature — a genuine "test to find out" candidate; manipulation-perception risk is real but the same review gate used for `INT-08` applies directly | Confirm loss-framed copy ("your 300 points expire in 7 days") reads as informative, not manipulative |
| **6** | **`INT-06` — Social proof (reviews/testimonials)** | Solid literature support (+25% CTR with reviews in email; effective in high-churn segments), but requires sourcing genuinely real, verifiable customer reviews — a data-availability dependency, not just a copy change | Confirm every review used is real and attributable before it goes anywhere near a customer send |
| **7** | **`INT-07` — Reciprocity (value-first, two-touch sequence)** | Good supporting evidence (+12% win-back in a prior lifecycle sequence), but the current framework only measures opt-out per individual send, not accumulated fatigue across a 2-touch sequence — needs a review step until fatigue tracking exists | Confirm the sequence doesn't read as manipulative "priming" and doesn't compound with other concurrent sends to the same customer |

### Tier 3 — Lower immediate priority (operational, not guardrail-driven)

| Rank | Intervention | Why it's Tier 3 |
|:----:|:-------------|:------------------|
| **8** | **`INT-05` — Optimized send timing vs. fixed 08:00 cron`** | Not a customer-facing guardrail risk at all — the barrier is operational (engineering time to replace the fixed n8n cron trigger with an engagement-optimized schedule). Literature suggests a real but split effect (Tuesday leads opens, Friday leads conversions), so the objective function isn't even settled yet. Recommended to defer until Tier 1/2 pilots have used up available send capacity and engineering bandwidth. |

---

## 6. Test design template (for the first Tier 1 pilot — `INT-02`)

This is the design that should be used to run the first real pilot, once authorized — it reuses the already-validated engine as-is, with no new statistical machinery required.

| Parameter | Recommended setting | Rationale |
|---|---|---|
| Arms | 2 (control: generic copy · treatment: personalized copy) | Matches the catalog's tested contrast; the engine's 2-arm z-test/Fisher-exact path applies directly |
| Baseline conversion (`p0`) | 9.6% (real Phase 4 HIGH-tier holdout, 14-day window) | Best available real anchor; to be replaced with the actual segment's observed baseline once the pilot population is finalized |
| Guardrail | Opt-out rate, same 2.0% threshold pattern already used in the validated scenario matrix | Reuses the same Power Guardrail logic verified against all 16 synthetic scenarios — no new guardrail code needed |
| Sample size | Calculated by the engine's existing power routine, once the real segment size and desired minimum detectable effect are set | Do not reuse a scenario-matrix `n` verbatim — those were sized for synthetic validation, not for this specific segment |
| Multiple-comparisons handling | Holm-Bonferroni, as already implemented | Only relevant once `INT-04`/`INT-01` run concurrently on overlapping customers |
| Decision precedence | Unchanged: (1) guardrail breach → (2) power check → (3) significance | Same precedence rule that is the core fix from Phase 5 |

Once `INT-02` completes, the same template applies to `INT-04` and `INT-01`, substituting the relevant guardrail (SMS/push opt-out for `INT-04`) and segment.

---

## 7. Closure statement

With this report, **Phase 6 (Section 6 closure criteria, item #7) is met**: the validated intervention catalog has been translated into prioritized, economically-framed recommendations with a ready-to-execute test design for the first pilot. Combined with the Phase 1 guardrail-coverage decision confirmed the same day, no technical or scoping work remains open in this block — what remains is Phase 8 (final case study and explicit sign-off).

**Not yet claimed, by design:** real customer-response evidence for any of these 8 interventions. That evidence can only come from actually running the Section 6 test design against real VivaMarket customers, which is outside the scope of this portfolio/demo block.
