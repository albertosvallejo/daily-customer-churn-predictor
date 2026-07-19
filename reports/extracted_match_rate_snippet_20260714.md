# Snippet extraído — cálculo de `match_rate` (notebook 5A archivado)

**Origen:** `notebooks/10_phase5_autonomous_agent_ab_analysis.ipynb`, celdas 4 y 10 (antes de archivar el notebook completo — ver tabla 0.3, fila 7).
**Estado:** candidato a insumo para la Fase 2 (`src/pipeline/ab_testing_framework.py`), **sin decidir todavía si se reaprovecha**. No se ha validado que el enfoque (basado en `shadow_log['match']`, dato ya invalidado — ver 0.4) sea el correcto para Fase 2; solo se conserva la lógica de cálculo por si el patrón (no el dato) resulta útil.

## Celda 4 — resumen baseline

```python
phase4_totals = phase4_kpi_payload.get('totals', {}) if phase4_kpi_payload else {}
reconciled_mask = shadow_log['has_human_decision'] if not shadow_log.empty else pd.Series(dtype=bool)
match_rate = shadow_log.loc[reconciled_mask, 'match'].fillna(0).mean() if not shadow_log.empty and reconciled_mask.any() else np.nan
baseline_summary = {
    'phase4_measurement_label': (phase4_monitor or {}).get('measurement_label', 'Unavailable'),
    'phase4_closed_evaluations': int(phase4_totals.get('closed_evaluations', 0)),
    'phase4_treated_actions': int(phase4_totals.get('actions', 0)),
    'phase5_shadow_cycles': int(len(shadow_log)),
    'phase5_reconciled_cycles': int(reconciled_mask.sum()) if not shadow_log.empty else 0,
    'phase5_match_rate': float(match_rate) if not pd.isna(match_rate) else np.nan,
    'phase5_pending_cycles': int((~reconciled_mask).sum()) if not shadow_log.empty else 0,
    'gate_target_days': 14,
    'gate_completion_pct': float(min(len(shadow_log) / 14, 1.0)) if len(shadow_log) else 0.0,
    'human_hours_rows_logged': int(len(human_hours_log)),
}
```

## Celda 10 — calidad de decisión y tendencia

```python
decision_quality = pd.DataFrame([
    {
        'shadow_cycles': int(len(shadow_log)),
        'reconciled_cycles': int(shadow_log['has_human_decision'].sum()),
        'matched_cycles': int(shadow_log.loc[shadow_log['has_human_decision'], 'match'].fillna(0).sum()),
        'divergence_cycles': int(((shadow_log['has_human_decision']) & (shadow_log['match'].fillna(0) == 0)).sum()),
        'routine_match_rate': float(shadow_log.loc[shadow_log['has_human_decision'], 'match'].fillna(0).mean()) if shadow_log['has_human_decision'].any() else np.nan,
        'gate_target_days': 14,
        'days_remaining_to_gate': max(0, 14 - int(len(shadow_log))),
    }
])
decision_trend = shadow_log.assign(
    match_label=np.where(shadow_log['has_human_decision'], np.where(shadow_log['match'].fillna(0) == 1, 'match', 'divergence'), 'pending')
).groupby(['cycle_date', 'match_label'], dropna=False).size().reset_index(name='rows')
```
