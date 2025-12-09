
import re
import pandas as pd
pd.set_option("display.max_rows", None)
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from sklearn.tree import export_graphviz
import graphviz
import dtreeviz


def plot_decision_tree(clf, model, feature_names, X, y_encoded, class_names_ordered, max_depth):
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
        max_depth=max_depth,
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

    # Another graphviz attempt with edge labels for conditions
    def customize_dot_for_edge_labels(dot_string):
        """
        Modify graphviz DOT to move split conditions from nodes to edges.
        Also removes 'samples = ' and simplifies display.
        """
        lines = dot_string.split('\n')
        node_conditions = {}  # Store conditions for each node
        modified_lines = []

        # First pass: extract conditions from node labels
        for line in lines:
            # Match node definitions: 0 [label="feature <= threshold\n..."]
            node_match = re.match(r'^(\d+) \[label="([^"]+)"', line)
            if node_match:
                node_id = node_match.group(1)
                label_content = node_match.group(2)

                # Extract the condition (first line before \n)
                parts = label_content.split('\\n')
                if len(parts) > 0 and '<=' in parts[0]:
                    condition = parts[0]
                    node_conditions[node_id] = condition

                    # Remove condition from node, keep only class distribution
                    new_parts = [p for p in parts[1:] if not p.startswith('samples =')]
                    new_label = '\\n'.join(new_parts)
                    modified_line = f'{node_id} [label="{new_label}"'
                    # Copy the rest of the line (styling attributes)
                    rest_of_line = line[line.index('[label="') + len(f'[label="{label_content}"'):]
                    modified_lines.append(modified_line + rest_of_line)
                else:
                    # Leaf node - just remove 'samples ='
                    new_parts = [p for p in parts if not p.startswith('samples =')]
                    new_label = '\\n'.join(new_parts)
                    modified_line = line.replace(label_content, new_label)
                    modified_lines.append(modified_line)
            else:
                modified_lines.append(line)

        # Second pass: add conditions to edges
        final_lines = []
        for line in modified_lines:
            # Match edges: 0 -> 1 ;
            edge_match = re.match(r'^(\d+) -> (\d+) ;', line)
            if edge_match:
                parent_id = edge_match.group(1)
                child_id = edge_match.group(2)

                # Determine if this is True (left) or False (right) branch
                if parent_id in node_conditions:
                    # Find position of this edge to determine branch
                    parent_edges = [l for l in modified_lines if l.startswith(f'{parent_id} ->')]
                    is_true_branch = (parent_edges.index(line) == 0)

                    condition = node_conditions[parent_id]
                    if is_true_branch:
                        edge_label = f'True\\n{condition}'
                    else:
                        edge_label = f'False'

                    final_lines.append(f'{parent_id} -> {child_id} [label="{edge_label}"] ;')
                else:
                    final_lines.append(line)
            else:
                final_lines.append(line)

        return '\n'.join(final_lines)

    # Export with graphviz and customize
    dot_original = export_graphviz(
        clf,
        feature_names=feature_names,
        class_names=[str(c) for c in class_names_ordered],
        filled=True,
        rounded=True,
        max_depth=max_depth,
        impurity=False,
        proportion=True,  # Show proportions instead of sample counts
        out_file=None
    )

    # Apply customization
    dot_custom = customize_dot_for_edge_labels(dot_original)

    graph = graphviz.Source(dot_custom)
    graph.format = "pdf"
    graph.render("MOCOF-1_decision_tree_edges_custom", cleanup=True)