import json
from pathlib import Path

import numpy as np
import pandas as pd

pd.set_option("display.max_rows", None)
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import RepeatedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
import fairsynthesis_data_model.mofsy_api as api
from plot_decision_tree import plot_decision_tree_matplotlib, plot_decision_tree_dtreeviz, plot_decision_tree_graphviz
from molmass import Formula
from deduplicate_experiments import get_duplicate_indices
from decision_tree_model import create_model

BASE = Path(__file__).parents[2] # repository root

TASK_IS_CLASSIFICATION = True # Classification vs. Regression
RANGE_TREE = False
EXTRA_TREE = False # Use ExtraTree instead of DecisionTree
MAX_DEPTH = 3
DEDUPLICATE = True
DEDUPLICATE_RELATIVE_TOLERANCE = 3.0 # in percent

sum_formula = {
    "COF-366-Co": "C60H36CoN8",
    "MOCOF-1": "C52H33CoN8",
    "unknown": "C44H31CoN8", #assuming Co(H−1tapp)
}
formula_mass = {k: Formula(v).mass for k, v in sum_formula.items()}

params_path = BASE / "data" / "MOCOF-1" / "converted" / "params_from_sciformation.json"
proc_path   = BASE / "data" / "MOCOF-1" / "converted" / "procedure_from_sciformation.json"
char_path   = BASE / "data" / "MOCOF-1" / "converted" / "characterization_from_sciformation.json"
frac_path   = BASE / "fairsynthesis_analysis" / "examples" / "data" / "pxrd_molar_fraction_overview.csv"

# 1. Load raw data
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

# 2.3 Characterisation – extract the product mass (mg) -> g
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

# Shorten parameter names for visualization
df = df.rename(columns={"aminoporphyrin_monomer_type": "TAPP_precursor"}).replace("C128H104N8O8.Co", "TDPP").replace("C128H104N8O8.2C6H6N2O2.CHF3O3S.Co","Co(III)-TDPP").replace("C44H32N8.Co","TAPP")
df = df.rename(columns={"acid_pKa_DMSO": "Acid_pKa"})
df = df.rename(columns={"degassing": "Degas"})
df = df.rename(columns={"temperature_C": "Temp_degC"})
df = df.rename(columns={"solvent_2_name": "Solvent2"}).replace("o-dichlorobenzene", "o-DCB").replace("nitrobenzene", "PhNO2")
df = df.rename(columns={"aldehyde_monomer_structure": "TPA_substitution"}).replace("C8H6O2", "none").replace("C10H10O4", "(OMe)2").replace("C8H4F2O2","F2")
df = df.rename(columns={"vessel": "Vessel"})
df = df.rename(columns={"other_additives": "Additive"}).replace("C6H6BrN", "PBA").replace("C19H16O", "TrOH")

# 4. Parameter conversion
df["TPA_eq"] = df["aldehyde_monomer_amount_umol"] / df["aminoporphyrin_monomer_amount_umol"]
df["H2O_per_TPA"] = df["water_amount_umol"] / df["aldehyde_monomer_amount_umol"]
df["TAPP_conc_mM"] = (df["aminoporphyrin_monomer_amount_umol"] / df[["solvent_1_volume_uL", "solvent_2_volume_uL", "solvent_3_volume_uL"]].sum(axis=1)*1e3).round()
df["Acid_conc_M"] = df["acid_amount_umol"] / df[["solvent_1_volume_uL", "solvent_2_volume_uL", "solvent_3_volume_uL"]].sum(axis=1).round(1)
df["Solvent2_fraction"] = df["solvent_2_volume_uL"] / df[["solvent_1_volume_uL", "solvent_2_volume_uL"]].sum(axis=1)
df["m-DNB"] = (df["solvent_3_volume_uL"] > 0)

centers = np.array([7, 10, 13, 20, 40])
bin_edges = [-np.inf, 8.5, 11.5, 16.5, 30, np.inf]
cats = pd.cut(
    df["TAPP_conc_mM"],
    bins=bin_edges,
    include_lowest=True,
)
df["TAPP_conc_mM"] = centers[cats.cat.codes]

# 5. Yield calculation (real values) and categorical main product
df["yield_MOCOF-1"] = (
    df["MOCOF-1"]
    * df["product_mass_g"]
    / (
        df["COF-366-Co"] * formula_mass["COF-366-Co"]
        + df["MOCOF-1"] * formula_mass["MOCOF-1"]
        + df["unknown"] * formula_mass["unknown"]
    )
    / df["aminoporphyrin_monomer_amount_umol"] / 1e-6
).round(2)
df["yield_COF-366-Co"] = (
    df["COF-366-Co"]
    * df["product_mass_g"]
    / (
        df["COF-366-Co"] * formula_mass["COF-366-Co"]
        + df["MOCOF-1"] * formula_mass["MOCOF-1"]
        + df["unknown"] * formula_mass["unknown"]
    )
    / df["aminoporphyrin_monomer_amount_umol"] / 1e-6
).round(2)
# Assuming the amorphous component was Co(tapp)nXn. Minimum function to avoid overestimation.
df["yield_Co(tapp)nXn"] = (
    np.minimum(1 - df["yield_COF-366-Co"] - df["yield_MOCOF-1"],
            df["unknown"]
            * df["product_mass_g"]
            / (
                df["COF-366-Co"] * formula_mass["COF-366-Co"]
                + df["MOCOF-1"] * formula_mass["MOCOF-1"]
                + df["unknown"] * formula_mass["unknown"]
            )
            / df["aminoporphyrin_monomer_amount_umol"] / 1e-6
    )
).round(2)
df["yield_Co(tapp)"] = (1 - df["yield_Co(tapp)nXn"] - df["yield_COF-366-Co"] - df["yield_MOCOF-1"]).round(2)

yield_cols = ["yield_COF-366-Co", "yield_MOCOF-1", "yield_Co(tapp)nXn", "yield_Co(tapp)"]
df["main_product"] = df[yield_cols].idxmax(axis=1).str.replace("yield_", "")
#print(df[["id"] + yield_cols + ["main_product"]])
TARGET = "main_product"

# 6. Remove rows where the target is NaN
n_before = len(df)
mask_missing = df[[TARGET]].isnull().any(axis=1)
missing_counts = {
    "target_nan":               int(df[TARGET].isnull().sum()),
}
dropped_ids = df.loc[mask_missing, "id"].tolist()
df = df.dropna(subset=[TARGET]).reset_index(drop=True)
n_after = len(df)
print("\n=== Drop‑NaN‑Report ===")
print(f"Columns before filtering: {n_before}")
print(f"Columns after Filtering: {n_after}")
print(f"Removed (Total): {n_before - n_after}")
print("Reason (Amount per Column):")
for k, v in missing_counts.items():
    print(f"  {k:20s} → {v}")
print(f"Example‑IDs of removed experiments (max 10): {dropped_ids[:10]}")

# 7.1. Pre-processing: input parameters
# Remove already converted parameters, characterization parameters, and workup parameters that are irrelevant for phase selectivity.
X = df.drop(columns=["id", TARGET] + yield_cols + ["product_mass_g", "COF-366-Co", "MOCOF-1", "unknown", "water_amount_umol", "acid_amount_umol", "acid_name", "aminoporphyrin_monomer_amount_umol", "aldehyde_monomer_amount_umol", "solvent_1_volume_uL", "solvent_2_volume_uL", "solvent_3_name", "solvent_3_volume_uL", "activation_with_scCO2", "workup_with_NaCl", "MeOH_in_scCO2_activation", "activation_under_vacuum", "duration_h"])
y = df[TARGET].values

# Find duplicates in X
if DEDUPLICATE:
    print("\n=== Deduplicating feature matrix ===")

    duplicate_indices, duplicate_pairs, epsilon_dict, param_stats = get_duplicate_indices(
        X,
        relative_tolerance=DEDUPLICATE_RELATIVE_TOLERANCE,
        verbose=False
    )

    print(f"Found {len(duplicate_indices)} duplicate rows")
    # print the experiment id for all duplicates
    print("Duplicate experiment IDs:")
    for (i,j) in duplicate_pairs:
        print(f"  {df.loc[i, 'id']} is duplicate of {df.loc[j, 'id']}")

    # Remove duplicates from both X and y
    X = X.drop(duplicate_indices)
    mask = np.ones(len(y), dtype=bool)
    mask[duplicate_indices] = False
    y = y[mask]

    print(f"Final shapes: X={X.shape}, y={y.shape}")

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
class_names_ordered = label_encoder.classes_

# 7.2. Pre‑processing: numeric vs. categorical
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
model_endless = create_model(TASK_IS_CLASSIFICATION, RANGE_TREE, EXTRA_TREE, 10000, preprocess)
model = create_model(TASK_IS_CLASSIFICATION, RANGE_TREE, EXTRA_TREE, MAX_DEPTH, preprocess)

# 9. Repeated 5‑fold CV (3 repeats) – report R^2 & MSE
def print_decision_tree_results(model, X, y):
    cv = RepeatedKFold(n_splits=5, n_repeats=3, random_state=42)
    if TASK_IS_CLASSIFICATION:
        accuracy = cross_val_score(model, X, y, cv=cv, scoring="accuracy")
        print(f"Accuracy: {accuracy.mean():.2f} ± {accuracy.std():.2f}\n")

    else:
        r2 = cross_val_score(model, X, y, cv=cv, scoring="r2")
        mse = -cross_val_score(model, X, y, cv=cv, scoring="neg_mean_squared_error")

        print(f"R^2  mean ± std : {r2.mean():.3f} ± {r2.std():.3f}")
        print(f"MSE mean ± std : {mse.mean():.4f} ± {mse.std():.4f}")

print("\n=== Decision tree results for limitless tree ===")
print_decision_tree_results(model_endless, X, y_encoded)
#print("\n=== Decision tree results for max_depth={} ===".format(MAX_DEPTH))
#print_decision_tree_results(model, X, y_encoded)

# 10. Fit on the full data set & extract insights
model_endless.fit(X, y_encoded)
model.fit(X, y_encoded)
if TASK_IS_CLASSIFICATION:
    tree_endless = model_endless.named_steps["classifier"]
    tree = model.named_steps["classifier"]
else:
    tree_endless = model_endless.named_steps["regressor"]
    tree = model.named_steps["regressor"]

def process_dt_results(model):
    # feature names after one‑hot encoding
    ohe = model.named_steps["preprocess"].named_transformers_["cat"].named_steps["onehot"]
    cat_feature_names = list(ohe.get_feature_names_out(categorical_cols))
    feature_names = numeric_cols + cat_feature_names
    clf = model.named_steps["classifier"]
    importances = clf.feature_importances_
    return ohe, cat_feature_names, feature_names, clf, importances

(ohe_l, cat_feature_names_l, feature_names_l, clf_l, importances_l) = process_dt_results(model_endless)
print("Feature importances")
for name, imp in sorted(zip(feature_names_l, importances_l), key=lambda x: -x[1]):
    print(f"{name}: {imp:.4f}")
print("\n")
#print("\n=== Decision tree insights for max_depth={} ===".format(MAX_DEPTH))
(ohe, cat_feature_names, feature_names, clf, importances) = process_dt_results(model)

# First plot both full trees with matplotlib for debugging
#plot_decision_tree_matplotlib("matplotlib_decision_tree_l_full", clf_l, feature_names_l)
#plot_decision_tree_matplotlib("matplotlib_decision_tree_max_depth_{}".format(MAX_DEPTH), clf, feature_names)

# plot limitless tree with graphviz
plot_decision_tree_graphviz("Decision-tree_full", clf_l, feature_names_l, max_depth=10000000)
#plot_decision_tree_graphviz("graphviz_decision_tree_l_max_depth_{}".format(MAX_DEPTH), clf_l, feature_names_l, max_depth=MAX_DEPTH)

# plot max_depth tree with dtreeviz
plot_decision_tree_dtreeviz("Decision-tree_{}-levels".format(MAX_DEPTH), clf, model, X, y_encoded, class_names_ordered, max_depth=MAX_DEPTH)
#plot_decision_tree_dtreeviz("dtreeviz_decision_tree_l_full", clf_l, model_endless, X, y_encoded, class_names_ordered, max_depth=10000000)
#plot_decision_tree_dtreeviz("dtreeviz_decision_tree_l_max_depth_{}".format(MAX_DEPTH), clf_l, model_endless, X, y_encoded, class_names_ordered, max_depth=MAX_DEPTH)