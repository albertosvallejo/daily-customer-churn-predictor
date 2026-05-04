import logging

import joblib
import pandas as pd

logger = logging.getLogger(__name__)

def apply_risk_tier(probability: float) -> str:
    if probability > 0.70:
        return 'HIGH'
    if probability >= 0.40:
        return 'MEDIUM'
    return 'LOW'

def score_dataframe(df: pd.DataFrame, package_path: str) -> pd.DataFrame:
    bundle = joblib.load(package_path)
    package = bundle['model_package']
    model = package['model']
    feature_columns = package['feature_columns']

    encoded = pd.get_dummies(df.copy(), columns=['customer_state'], dtype=float)
    encoded = encoded.reindex(columns=feature_columns, fill_value=0.0)
    probabilities = model.predict_proba(encoded)[:, 1]

    scored = df.copy()
    scored['churn_probability'] = probabilities
    scored['risk_tier'] = [apply_risk_tier(value) for value in probabilities]
    return scored
