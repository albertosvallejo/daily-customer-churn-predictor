# PHASE 6 DYNAMIC EVIDENCE RECOMMENDATIONS

- Run date: 20260724
- Source mode: seed-baseline bootstrap (not live-discovery yet)
- Recommendation rule: confidence determines gate eligibility; actionability and applicability determine order inside the eligible set.

## Recommended order
### 1. INT-02 — ResearchGate
- Tier: tier_2
- Readiness: approval_gate_eligible
- Confidence: medium
- Actionability: high
- Applicability to VivaMarket: medium
- Priority score: 121
- Suggested copy hypothesis: reminder_sequence
- Suggested channel hypothesis: email
- Suggested timing hypothesis: follow_up_sequence
- Suggested incentive hypothesis: repeat_offer
- Evidence anchor: Inherited study anchor with reported T=2.87, p=0.004 in the Phase 5 catalog.
- Traceability note: Inherited static reference for reminder frequency / retention sequence evidence.

### 2. INT-01 — CXL
- Tier: tier_3
- Readiness: evidence_enrichment_only
- Confidence: low
- Actionability: high
- Applicability to VivaMarket: high
- Priority score: 22
- Suggested copy hypothesis: value_first
- Suggested channel hypothesis: email_or_push
- Suggested timing hypothesis: pre-discount_message
- Suggested incentive hypothesis: percentage_coupon
- Evidence anchor: Heuristic framing guidance; no quantified lift extracted yet.
- Traceability note: Inherited static reference for value-first framing hypothesis.

### 3. INT-04 — Altcraft
- Tier: tier_3
- Readiness: evidence_enrichment_only
- Confidence: low
- Actionability: high
- Applicability to VivaMarket: high
- Priority score: 22
- Suggested copy hypothesis: short_value_message
- Suggested channel hypothesis: sms_or_push
- Suggested timing hypothesis: non_email_openers
- Suggested incentive hypothesis: same_coupon_as_control
- Evidence anchor: Inherited benchmark claim: SMS approximately 90% open rate.
- Traceability note: Inherited static reference for channel-shift intervention.

## Interpretation
- Approval-gate-eligible candidates: 1
- Evidence-enrichment-only candidates: 2
- This report is parallel to the historical `phase5_step6_intervention_recommendations_20260718.md` artifact and does not replace it yet.
- Any low-confidence item remains blocked from autonomous approval flow even if it is highly actionable.

## Validation prompts for Sub-phase 6.3
- Check that every evidence anchor maps to the expected intervention ID.
- Confirm that no low-confidence entry appears as approval-gate-eligible.
- Review whether the ordering remains stable when new seed or live evidence is added.
