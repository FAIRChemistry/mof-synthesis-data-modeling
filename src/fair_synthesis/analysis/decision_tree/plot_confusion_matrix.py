import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


def plot_confusion_matrix(y_encoded, y_pred_cv, class_names_ordered):
    cm_cv_norm = confusion_matrix(
        y_encoded,
        y_pred_cv,
        labels=np.arange(len(class_names_ordered)),
        normalize="true"
    )

    disp_norm = ConfusionMatrixDisplay(
        confusion_matrix=cm_cv_norm,
        display_labels=class_names_ordered
    )

    fig, ax = plt.subplots(figsize=(8, 8))
    disp_norm.plot(
        ax=ax,
        cmap="Blues",
        values_format=".2f",
        xticks_rotation=45
    )
    ax.set_title("Normalized Cross-Validated Confusion Matrix")
    plt.tight_layout()
    plt.show()