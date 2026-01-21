import re
import dtreeviz
import graphviz
from pathlib import Path
from sklearn.tree import export_graphviz
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
import pandas as pd
pd.set_option("display.max_rows", None)


def plot_decision_tree_matplotlib(label, clf, feature_names):  # unused now
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


def plot_decision_tree_graphviz(label, clf, feature_names, max_depth, plots_dir: Path):
    # customized export using graphviz, suitable for full tree
    dot = export_graphviz(
        clf,
        feature_names=feature_names,
        filled=True,
        rounded=False,
        max_depth=max_depth,
        impurity=False,
        proportion=False,
        node_ids=False,
        out_file=None,
    )
    # display conditions at the bottom
    node_re = re.compile(r'(\d+) \[label="([^"]*)"', re.MULTILINE)

    def reorder_label(match):
        node_id = match.group(1)
        label = match.group(2)
        lines = label.split("\\n")
        # identify condition and value lines
        cond_lines = [l for l in lines if "<=" in l or ">" in l]
        value_lines = [l for l in lines if l.startswith("value =")]
        other_lines = [l for l in lines if l not in cond_lines + value_lines]
        new_lines = value_lines + cond_lines + other_lines
        new_label = "\\n".join(new_lines)
        return f'{node_id} [label="{new_label}"'
    dot = node_re.sub(reorder_label, dot)
    # remove sample numbers
    dot = re.sub(r'\\nsamples = [^\\n"]*', '', dot)
    # convert "value = [31.0, 36.0, 55.0, 20.0]" -> "value = [31, 36, 55, 20]"

    def round_value_line(m):
        nums = m.group(1).split(',')
        ints = [str(int(float(x))) for x in nums]
        return "value = [" + ", ".join(ints) + "]"
    dot = re.sub(r'value = \[([0-9eE\.\+,\-\s]+)\]', round_value_line, dot)
    # add legend
    class_names = ["COF-366-Co", "Co(tapp)", "Co(tapp)nXm",
                   "MOCOF-1"][:len([str(c) for c in clf.classes_])]
    class_colors = ["#e08343", "#59e346", "#499de2", "#d344e2"]
    rows = []
    for name, color in zip(class_names, class_colors):
        rows.append(
            f'<TR>'
            f'<TD BGCOLOR="{color}" WIDTH="20" HEIGHT="20"></TD>'
            f'<TD ALIGN="LEFT">{name}</TD>'
            f'</TR>'
        )
    legend_html = (
        '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">'
        '<TR><TD COLSPAN="2"><B>Main product</B></TD></TR>'
        + "".join(rows) +
        '</TABLE>>'
    )
    legend_node = (
        '\nlegend [shape=plaintext, style=filled, fillcolor="white", '
        'fontcolor="black", label=' + legend_html + '];\n'
    )
    dot = dot.replace("\n}", legend_node + "}")
    # plot
    graph = graphviz.Source(dot)
    graph.format = "pdf"
    graph.render(label, directory=str(plots_dir), cleanup=True)


def plot_decision_tree_dtreeviz(
        label,
        clf,
        model,
        X,
        y_encoded,
        class_names_ordered,
        max_depth,
        target_label,
        plots_dir: Path):
    # Plot with statistics. Suitable for small trees

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
        X_transformed.toarray() if hasattr(
            X_transformed,
            "toarray") else X_transformed,
        columns=feature_names_clean,
    )

    # Create the model wrapper for dtreeviz using cleaned names
    viz_model = dtreeviz.model(
        clf,
        X_train=X_transformed_df,
        y_train=y_encoded,
        feature_names=feature_names_clean,
        target_name=target_label,
        class_names=list(class_names_ordered),
    )

    v_subset = viz_model.view(
        fancy=True,
        histtype="barstacked",
        show_node_labels=False,
        show_just_path=False,
        label_fontsize=14,
        ticks_fontsize=14,
        depth_range_to_display=(0, max_depth),
        scale=1,
        #orientation="LR"
    )
    outfile = plots_dir / f"{label}.svg"
    v_subset.save(str(outfile))
    outfile.with_suffix("").unlink()