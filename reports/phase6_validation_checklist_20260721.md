# PHASE 6 VALIDATION CHECKLIST

- Review sample entries in `data/processed/evidence_catalog_20260721.json` against their inherited source anchors.
- Verify that a second run with the same `run_date` does not overwrite the previous dated catalog snapshot and fails explicitly instead.
- Confirm that only `medium` / `high` confidence entries are marked as `approval_gate_eligible` in the dynamic recommendations report.
- Compare ordering between `reports/phase5_step6_intervention_recommendations_20260718.md` and `reports/phase6_dynamic_evidence_recommendations_20260721.md` to detect unstable ranking changes.
- Verify that every recommendation preserves the seed-baseline interpretation and does not overstate the evidence boundary.
- Record manual findings before promoting this prototype toward any 6.4 integration work.
