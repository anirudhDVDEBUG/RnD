#!/usr/bin/env python3
"""Generate a realistic biomedical research dataset for demo purposes."""

import numpy as np
import pandas as pd

np.random.seed(42)
N = 200

treatments = np.random.choice(["Drug_A", "Drug_B", "Placebo"], size=N, p=[0.35, 0.35, 0.3])
ages = np.random.normal(55, 12, N).clip(25, 85).astype(int)
biomarker_baseline = np.random.lognormal(mean=3.0, sigma=0.5, size=N)

# Treatment effect
effect = np.where(treatments == "Drug_A", -0.35,
         np.where(treatments == "Drug_B", -0.20, 0.0))
noise = np.random.normal(0, 0.15, N)
biomarker_week12 = biomarker_baseline * (1 + effect + noise)
biomarker_week12 = biomarker_week12.clip(0.5, None)

survival_months = (
    24 + 8 * (treatments == "Drug_A").astype(float)
       + 4 * (treatments == "Drug_B").astype(float)
       - 0.15 * ages
       + np.random.normal(0, 5, N)
).clip(1, 60).round(1)

response = np.where(
    (biomarker_week12 / biomarker_baseline) < 0.75, "Responder", "Non-responder"
)

gender = np.random.choice(["Male", "Female"], N, p=[0.52, 0.48])

df = pd.DataFrame({
    "patient_id": [f"PT-{i+1:04d}" for i in range(N)],
    "treatment": treatments,
    "gender": gender,
    "age": ages,
    "biomarker_baseline": biomarker_baseline.round(2),
    "biomarker_week12": biomarker_week12.round(2),
    "survival_months": survival_months,
    "response": response,
})

# Inject 3% missing values in biomarker_week12
mask = np.random.rand(N) < 0.03
df.loc[mask, "biomarker_week12"] = np.nan

df.to_csv("sample_clinical_trial.csv", index=False)
print(f"Generated sample_clinical_trial.csv  ({N} rows, {len(df.columns)} columns)")
