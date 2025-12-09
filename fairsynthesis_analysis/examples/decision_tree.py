import json
from pathlib import Path

import numpy as np
import pandas as pd
pd.set_option("display.max_rows", None)
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import RepeatedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeRegressor, export_text, plot_tree
from sklearn.tree import ExtraTreeRegressor
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.tree import export_graphviz
import graphviz
import fairsynthesis_data_model.mofsy_api as api
from molmass import Formula

BASE = Path(__file__).parents[2] # repository root

TASK_IS_CLASSIFICATION = True # Classification vs. Regression
EXTRA_TREE = False # Use ExtraTree instead of DecisionTree

sum_formula = {
    "COF-366-Co": "C60H36CoN8",
    "MOCOF-1": "C52H33CoN8",
    "unknown": "C44H31CoN8", #assuming Co(H−1tapp)
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

# 4. Parameter conversion
df["dialdehyde_equiv"] = df["aldehyde_monomer_amount_umol"] / df["aminoporphyrin_monomer_amount_umol"]
df["water_per_dialdehyde"] = df["water_amount_umol"] / df["aldehyde_monomer_amount_umol"]
df["porphyrin_conc_mmol_L"] = (df["aminoporphyrin_monomer_amount_umol"] / df[["solvent_1_volume_uL", "solvent_2_volume_uL", "solvent_3_volume_uL"]].sum(axis=1)*1e3).round()
df["acid_conc_mol_L"] = df["acid_amount_umol"] / df[["solvent_1_volume_uL", "solvent_2_volume_uL", "solvent_3_volume_uL"]].sum(axis=1).round(1)
df["solvent_hydrophobic_fraction"] = df["solvent_2_volume_uL"] / df[["solvent_1_volume_uL", "solvent_2_volume_uL"]].sum(axis=1)
df["additional_m-dinitrobenzene"] = (df["solvent_3_volume_uL"] > 0)

centers = np.array([7, 10, 13, 20, 40])
bin_edges = [-np.inf, 8.5, 11.5, 16.5, 30, np.inf]
cats = pd.cut(
    df["porphyrin_conc_mmol_L"],
    bins=bin_edges,
    include_lowest=True,
)
df["porphyrin_conc_mmol_L"] = centers[cats.cat.codes]

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
if TASK_IS_CLASSIFICATION:
    if EXTRA_TREE:
        model = Pipeline([
            ("preprocess", preprocess),
            ("classifier", ExtraTreeClassifier(  # Changed to Classifier
                max_depth=5,
                min_samples_leaf=5,
                random_state=42
            ))
        ])
    else:
        model = Pipeline([
            ("preprocess", preprocess),
            ("classifier", DecisionTreeClassifier(  # Changed to Classifier
                    #criterion="gini",
                    #min_impurity_decrease=1e-3,
                    max_depth=None,
                    random_state=0
            ))
        ])
else:
    if EXTRA_TREE:
        model = Pipeline(
            [("preprocess", preprocess), ("regressor", ExtraTreeRegressor(
            max_depth=5,  # Explicit limit
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

if TASK_IS_CLASSIFICATION:
    accuracy = cross_val_score(model, X, y, cv=cv, scoring="accuracy")
    print(f"Accuracy: {accuracy.mean():.2f} ± {accuracy.std():.2f}")

else:
    r2 = cross_val_score(model, X, y, cv=cv, scoring="r2")
    mse = -cross_val_score(model, X, y, cv=cv, scoring="neg_mean_squared_error")

    print(f"R^2  mean ± std : {r2.mean():.3f} ± {r2.std():.3f}")
    print(f"MSE mean ± std : {mse.mean():.4f} ± {mse.std():.4f}")

# 10. Fit on the full data set & extract insights
model.fit(X, y)
if TASK_IS_CLASSIFICATION:
    tree = model.named_steps["classifier"]
else:
    tree = model.named_steps["regressor"]

# feature names after one‑hot encoding
ohe = model.named_steps["preprocess"].named_transformers_["cat"].named_steps["onehot"]
cat_feature_names = list(ohe.get_feature_names_out(categorical_cols))
feature_names = numeric_cols + cat_feature_names

#print("\nTop‑10 feature importances")
#for idx in np.argsort(tree.feature_importances_)[-10:][::-1]:
#    print(f"{feature_names[idx]:30s} : {tree.feature_importances_[idx]:.4f}")

#print("\nDecision‑tree (first 7 levels)")
#print(export_text(tree, feature_names=feature_names, max_depth=7))

clf = model.named_steps["classifier"]
feature_names = model.named_steps["preprocess"].get_feature_names_out()

# Plot and save as PDF
plt.figure(figsize=(16, 8))
# Full export using matplotlib, but not suitable for publication
plot_tree(
    clf,
    feature_names=feature_names,
    class_names=[str(c) for c in clf.classes_],
    filled=True,
    rounded=True,
)
plt.savefig("MOCOF-1_decision_tree.pdf", format="pdf", dpi=300, bbox_inches="tight")

# customized export using graphviz, suitable for publication. Subset of graph.
dot = export_graphviz(
    clf,
    feature_names=feature_names,
    class_names=[str(c) for c in clf.classes_],
    filled=True,
    rounded=True,
    max_depth=3,
    impurity=False,        # remove gini
    proportion=False,
    node_ids=False,
    out_file=None
)

graph = graphviz.Source(dot)
graph.format = "pdf"
graph.render("MOCOF-1_decision_tree_subset_pub", cleanup=True)


# customized export using graphviz, suitable for publication. Full graph.
dot = export_graphviz(
    clf,
    feature_names=feature_names,
    class_names=[str(c) for c in clf.classes_],
    filled=True,
    rounded=True,
    proportion=False,
    node_ids=False,
    out_file=None
)

graph = graphviz.Source(dot)
graph.format = "pdf"
graph.render("MOCOF-1_decision_tree_full_pub", cleanup=True)


print("\nFeature importances")
importances = clf.feature_importances_
for name, imp in sorted(zip(feature_names, importances), key=lambda x: -x[1]):
    print(f"{name}: {imp:.4f}")