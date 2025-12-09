
import re
import pandas as pd
pd.set_option("display.max_rows", None)
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from sklearn.tree import export_graphviz
import graphviz
import dtreeviz


def plot_decision_tree(clf, model, feature_names, X, y_encoded, class_names_ordered, max_depth):

    # even better plot for publication using dtreeviz
    # Transform X for dtreeviz (needs the preprocessed data)
    X_transformed = model.named_steps["preprocess"].transform(X)

    # Convert to DataFrame with proper feature names for dtreeviz
    X_transformed_df = pd.DataFrame(
        X_transformed.toarray() if hasattr(X_transformed, 'toarray') else X_transformed,
        columns=feature_names
    )

    # Create the model wrapper
    viz_model = dtreeviz.model(
        clf,
        X_train=X_transformed_df,
        y_train=y_encoded,
        feature_names=feature_names,
        target_name='Product',
        class_names=list(class_names_ordered)  # Original string names in correct order
    )

    # Generate full tree visualization with customizations
    v = viz_model.view(
        fancy=True,                    # Use fancy rendering
        histtype='barstacked',                # Use bar charts for class distributions
        show_node_labels=False,        # Remove "samples = " and "class = " labels
        scale=1.5,                     # Increase size for better readability
    )

    v.save("MOCOF-1_decision_tree_dtreeviz.svg")
    print("\nDtreeviz plot saved as: MOCOF-1_decision_tree_dtreeviz.svg")

    # Alternative: Specify depth limit for cleaner visualization
    v_subset = viz_model.view(
        fancy=True,
        histtype='barstacked',
        show_node_labels=False,
        show_just_path=False,           # ensure full sub-tree, not only a single path
        depth_range_to_display=(0, max_depth),  # Only show first X levels
        scale=2.0,
    )

    v_subset.save("MOCOF-1_decision_tree_dtreeviz_subset.svg")
