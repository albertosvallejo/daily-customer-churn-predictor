
import logging

import joblib
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def apply_risk_tier(probability: float, thresholds: dict) -> str:
    if probability >= thresholds['high_min_score']:
        return 'HIGH'
    if probability >= thresholds['medium_min_score']:
        return 'MEDIUM'
    return 'LOW'


def attach_retention_rules(scored: pd.DataFrame, metadata: dict) -> pd.DataFrame:
    retention_rules = metadata['retention_rules']
    scored = scored.copy()
    scored['recommended_discount_pct'] = scored['risk_tier'].map(lambda x: retention_rules[x]['base_discount_pct'])
    scored['free_shipping_flag'] = scored['risk_tier'].map(lambda x: retention_rules[x]['free_shipping'])
    scored['priority_level'] = scored['risk_tier'].map(lambda x: retention_rules[x]['priority_level'])
    vip_cutoff = scored['total_payment_value'].quantile(0.75) if 'total_payment_value' in scored.columns else np.inf
    scored['vip_human_touch_flag'] = (scored['risk_tier'].eq('HIGH') & (scored.get('total_payment_value', pd.Series(index=scored.index, dtype=float)).fillna(0) >= vip_cutoff))
    scored.loc[scored['vip_human_touch_flag'], 'recommended_discount_pct'] = retention_rules['HIGH']['vip_discount_pct']
    return scored


def score_dataframe(df: pd.DataFrame, package_path: str) -> pd.DataFrame:
    bundle = joblib.load(package_path)
    package = bundle['model_package']
    metadata = bundle['metadata']
    model = package['model']
    feature_columns = package['feature_columns']

    encoded = pd.get_dummies(df.copy(), columns=['customer_state'], dtype=float)
    encoded = encoded.reindex(columns=feature_columns, fill_value=0.0)
    probabilities = model.predict_proba(encoded)[:, 1]

    scored = df.copy()
    scored['churn_probability'] = probabilities
    scored['risk_tier'] = [apply_risk_tier(value, metadata['risk_thresholds']) for value in probabilities]
    scored = attach_retention_rules(scored, metadata)
    return scored
