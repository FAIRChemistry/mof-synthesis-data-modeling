import pandas as pd
pd.set_option("display.max_rows", None)
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from sklearn.tree import export_graphviz
import graphviz
import dtreeviz


def plot_decision_tree_matplotlib(label, clf, feature_names):
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
    plt.savefig(label + ".pdf", format="pdf", dpi=300, bbox_inches="tight")

def plot_decision_tree_graphviz(label, clf, feature_names, max_depth):
    # customized export using graphviz, suitable for publication
    dot = export_graphviz(
        clf,
        feature_names=feature_names,
        class_names=[str(c) for c in clf.classes_],
        filled=True,
        rounded=True,
        max_depth=max_depth,
        impurity=False,        # remove gini
        proportion=False,
        node_ids=False,
        out_file=None
    )
    graph = graphviz.Source(dot)
    graph.format = "pdf"
    graph.render(label + "_pub", cleanup=True)

def plot_decision_tree_dtreeviz(label, clf, model, X, y_encoded, class_names_ordered, max_depth):
    # Get original feature names from the ColumnTransformer
    raw_feature_names = model.named_steps["preprocess"].get_feature_names_out()

    # Strip 'num__' and 'cat__' prefixes for readability
    def strip_prefix(name: str) -> str:
        for prefix in ("num__", "cat__"):
            if name.startswith(prefix):
                return name[len(prefix):]
        return name

    feature_names_clean = [strip_prefix(n) for n in raw_feature_names]

    # Transform X
    X_transformed = model.named_steps["preprocess"].transform(X)

    # Convert to DataFrame with cleaned feature names
    X_transformed_df = pd.DataFrame(
        X_transformed.toarray() if hasattr(X_transformed, "toarray") else X_transformed,
        columns=feature_names_clean,
    )

    # Create the model wrapper for dtreeviz using cleaned names
    viz_model = dtreeviz.model(
        clf,
        X_train=X_transformed_df,
        y_train=y_encoded,
        feature_names=feature_names_clean,
        target_name="Product",
        class_names=list(class_names_ordered),
    )

    v_subset = viz_model.view(
        fancy=True,
        histtype="barstacked",
        show_node_labels=False,
        show_just_path=False,
        depth_range_to_display=(0, max_depth),
        scale=2.0,
    )
    v_subset.save(label + ".svg")
