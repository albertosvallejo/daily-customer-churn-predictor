# PHASE 6 SPEC — DYNAMIC EVIDENCE SYSTEM

## Objective
Build the first operational slice of the new Phase 6 evidence system for the Daily Customer Churn Predictor project. This slice must transform the inherited static intervention references into a controlled, versioned, and reviewable evidence baseline that can later feed recommendation refreshes and the business approval loop.

## Scope of this first implementation cut

### Included now
- Formal Phase 6 operating spec aligned with the approved `_private/phase6_action_plan_v3.md`.
- Curated source allowlist with source-level ceilings, open-access rule, monthly cadence, single approver, and simulated A/B launch mode.
- Seed evidence ingestion from the inherited static Phase 5 intervention references.
- First versioned evidence catalog generation as an immutable snapshot.
- Summary artifact describing the generated catalog and current governance constraints.

### Explicitly deferred
- Automated web fetching/search across external open-access sources.
- LLM-based extraction from live source texts.
- Recommendation ranking refresh based on newly discovered evidence.
- n8n production-write path, approval UI, KPI dashboard, and live/simulated A/B launcher.

## Operating constraints
- Open-access sources only.
- Monthly cadence only.
- One approver only: `architect.openclaw@gmail.com`.
- Simulated A/B launch mode only in this first Phase 6 launch.
- `confidence_score` remains bounded by the source-level ceiling.
- `actionability_score` is independent and cannot override low confidence.
- Generated catalogs are append-only snapshots and must never overwrite prior dated catalogs.

## Inputs
- `config/evidence_sources_allowlist.yaml`
- `data/interim/phase6_seed_evidence.json`

## Outputs
- `data/processed/evidence_catalog_<YYYYMMDD>.json`
- `reports/phase6_evidence_catalog_summary_<YYYYMMDD>.md`

## Data contract for each evidence entry
- `entry_id`
- `catalog_run_date`
- `intervention_id`
- `ref_id`
- `source_name`
- `source_level`
- `peer_review_status`
- `confidence_ceiling`
- `study_design`
- `sample_size`
- `publication_year`
- `effect_size`
- `effect_size_text`
- `expected_lift`
- `actionable_elements`
- `applicability_to_vivamarket`
- `citation_status`
- `quote_or_anchor`
- `confidence_score`
- `actionability_score`
- `approval_mode`
- `single_approver`
- `ab_mode`
- `open_access_only`
- `catalog_role`

## Scoring rules in this slice

### Confidence score
This first slice uses deterministic bootstrap rules because no live-source parser exists yet.
- Start from a heuristic base by `study_design`:
  - `rct` -> `high`
  - `quasi_experimental` -> `medium`
  - `observational` -> `medium`
  - `industry_benchmark` -> `low`
  - `industry_heuristic` -> `low`
  - unknown -> `low`
- If `peer_review_status == published`, allow the base score as-is.
- If `peer_review_status == preprint`, never exceed `medium` before the source ceiling is applied.
- If `peer_review_status == none`, never exceed `low` before the source ceiling is applied.
- Apply the hard ceiling from source level A/B/C/D at the end.

### Actionability score
Derived from the completeness of `actionable_elements`:
- 4 populated fields -> `high`
- 2-3 populated fields -> `medium`
- 0-1 populated fields -> `low`

## Execution contract
The implementation entrypoint is a local pipeline script that:
1. loads the allowlist and seed evidence;
2. enriches each seed entry with governance fields and deterministic bootstrap scoring;
3. writes a dated immutable catalog snapshot;
4. writes a dated summary report;
5. returns the generated artifact paths.

## Acceptance criteria for this cut
- The script runs locally without manual edits.
- At least the approved seed baseline for `INT-01`, `INT-02`, and `INT-04` is included in the generated catalog.
- The catalog is versioned by date and is not written as an in-place mutable file.
- The summary report explicitly states that this is still a seed baseline, not a live-discovery system.
- A regression test validates the bootstrap catalog generation contract.

## Next step after this cut
Sub-phase 6.2 can build on this contract to add live open-access discovery and richer synthesis logic without changing the governance baseline defined here.
