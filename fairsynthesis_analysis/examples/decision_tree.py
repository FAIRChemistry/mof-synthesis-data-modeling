import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import RepeatedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeRegressor, export_text
from sklearn.tree import ExtraTreeRegressor
import fairsynthesis_data_model.fairsynthesis_data_model.mofsy_api as api
from molmass import Formula

BASE = Path(__file__).parents[2] # repository root

sum_formula = {
    "COF-366-Co": "C60H36CoN8",
    "MOCOF-1": "C52H33CoN8",
    "unknown": "C44H31CoN8",
}
formula_mass = {k: Formula(v).mass for k, v in sum_formula.items()}

# 1. Load raw data
params_path = BASE / "data" / "MOCOF-1" / "converted" / "params_from_sciformation.json"
proc_path   = BASE / "data" / "MOCOF-1" / "converted" / "procedure_from_sciformation.json"
char_path   = BASE / "data" / "MOCOF-1" / "converted" / "characterization_from_sciformation.json"
frac_path   = BASE / "fairsynthesis_analysis" / "examples" / "data" / "pxrd_molar_fraction_overview.csv"

with open(params_path) as f:
    raw_params = json.load(f)

# Load the structured objects
procedure = api.load_procedure(str(proc_path))
characterization = api.load_characterization(str(char_path))

# 2. Build flat DataFrames from the three sources
# 2.1 Parameters (already flat)
params_df = (
    pd.DataFrame.from_dict(raw_params, orient="index")
    .reset_index()
    .rename(columns={"index": "id"})
)

# 2.2 Molar fractions (PXRD)
frac_df = pd.read_csv(frac_path)


# 2.3 Characterisation – extract the weight (mg) -> g
char_rows = []
for exp_id in frac_df["id"]:
    char_entry = api.get_characterization_by_experiment_id(characterization, exp_id)
    if char_entry is None:
        continue
    w = api.find_product_mass(char_entry)          # returns Quantity or None
    if w and hasattr(w, "value"):
        mass_mg = float(w.value)
    else:
        mass_mg = np.nan
    char_rows.append({"id": exp_id, "product_mass_g": mass_mg / 1000.0})

char_df = pd.DataFrame(char_rows)

# 3. Merge everything
df = (
    params_df
    .merge(frac_df, on="id", how="inner")
    .merge(char_df, on="id", how="left")
)

# 4. Helper columns (equivalence ratios + other values)
df["ald_per_amine"] = df["aldehyde_monomer_amount_umol"] / df["aminoporphyrin_monomer_amount_umol"]
df["water_per_amine"] = df["water_amount_umol"] / df["aminoporphyrin_monomer_amount_umol"]
df["water_per_aldeyde"] = df["water_amount_umol"] / df["aldehyde_monomer_amount_umol"]

df["precursor_amount_mol"] = (
    df["aminoporphyrin_monomer_amount_umol"] * 1e-6
)
df["total_volume_uL"] = df[["solvent_1_volume_uL", "solvent_2_volume_uL", "solvent_3_volume_uL"]].sum(axis=1)
df["acid_mol_ratio"] = df["acid_amount_umol"] / df["aminoporphyrin_monomer_amount_umol"]

# 5. Yield calculation (real values)

# avoid division by zero – rows with missing precursor or product mass will be dropped later
df["yield_MOCOF-1"] = (
    df["MOCOF-1"]
    * df["product_mass_g"]
    / (
        df["COF-366-Co"] * formula_mass["COF-366-Co"]
        + df["MOCOF-1"] * formula_mass["MOCOF-1"]
    )
    / df["precursor_amount_mol"]
)

df["yield_MOCOF-1"] = df["yield_MOCOF-1"].round(2)

# 6. Remove rows where the target is NaN (missing mass or precursor)
TARGET = "yield_MOCOF-1"

n_before = len(df)
mask_missing = df[[TARGET, "precursor_amount_mol", "product_mass_g"]].isnull().any(axis=1)
missing_counts = {
    "target_nan":               int(df[TARGET].isnull().sum()),
    "precursor_amount_nan":     int(df["precursor_amount_mol"].isnull().sum()),
    "product_mass_nan":         int(df["product_mass_g"].isnull().sum()),
}
dropped_ids = df.loc[mask_missing, "id"].tolist()

df = df.dropna(subset=[TARGET, "precursor_amount_mol", "product_mass_g"]).reset_index(drop=True)
y = df[TARGET].values
# drop these as they give information about the result and should not be used for prediction
to_drop_from_X = ["COF-366-Co", "MOCOF-1", "unknown", "product_mass_g"]
X = df.drop(columns=["id", TARGET] + to_drop_from_X)

n_after = len(df)
print("\n=== Drop‑NaN‑Report ===")
print(f"Columns before filtering: {n_before}")
print(f"Columns after Filtering: {n_after}")
print(f"Removed (Total): {n_before - n_after}")
print("Reason (Amount per Column):")
for k, v in missing_counts.items():
    print(f"  {k:20s} → {v}")
print(f"Example‑IDs of removed experiments (max 10): {dropped_ids[:10]}")

# 7. Pre‑processing: numeric vs. categorical
numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_cols = X.select_dtypes(include=["object", "bool"]).columns.tolist()

numeric_pipe = Pipeline([("imputer", SimpleImputer(strategy="median"))])
categorical_pipe = Pipeline(
    [
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]
)

preprocess = ColumnTransformer(
    [("num", numeric_pipe, numeric_cols), ("cat", categorical_pipe, categorical_cols)]
)

# 8. Decision‑Tree pipeline
other_regressor = False
if other_regressor:
    model = Pipeline(
        [("preprocess", preprocess), ("regressor", ExtraTreeRegressor(
        max_depth=5,  # Explizite Limitierung
        min_samples_leaf=5,
        random_state=42
    ))]
    )
else:
    model = Pipeline(
        [("preprocess", preprocess), ("regressor", DecisionTreeRegressor(random_state=42))]
    )

# 9. Repeated 5‑fold CV (3 repeats) – report R^2 & MSE
cv = RepeatedKFold(n_splits=5, n_repeats=3, random_state=42)

r2 = cross_val_score(model, X, y, cv=cv, scoring="r2")
mse = -cross_val_score(model, X, y, cv=cv, scoring="neg_mean_squared_error")

print(f"R^2  mean ± std : {r2.mean():.3f} ± {r2.std():.3f}")
print(f"MSE mean ± std : {mse.mean():.4f} ± {mse.std():.4f}")

# 10. Fit on the full data set & extract insight
model.fit(X, y)
tree = model.named_steps["regressor"]

# feature names after one‑hot encoding
ohe = model.named_steps["preprocess"].named_transformers_["cat"].named_steps["onehot"]
cat_feature_names = list(ohe.get_feature_names_out(categorical_cols))
feature_names = numeric_cols + cat_feature_names

print("\nTop‑10 feature importances")
for idx in np.argsort(tree.feature_importances_)[-10:][::-1]:
    print(f"{feature_names[idx]:30s} : {tree.feature_importances_[idx]:.4f}")

print("\nDecision‑tree (first 3 levels)")
print(export_text(tree, feature_names=feature_names, max_depth=10))