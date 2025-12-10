import pandas as pd
pd.set_option("display.max_rows", None)
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import ExtraTreeRegressor
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from range_decision_tree import RangeDecisionTreeClassifier


def create_model(task_is_classification: bool, range_tree: bool, extra_tree: bool, max_depth: int, preprocess):
    if task_is_classification:
        if range_tree:
            model = Pipeline([
                ("preprocess", preprocess),
                ("classifier", RangeDecisionTreeClassifier(
                    max_depth=4,
                    min_samples_leaf=5,
                    split_strategy='both',  # Evaluates both standard and range splits
                    max_range_splits=10,
                    random_state=0
                ))
            ])
        elif extra_tree:
            model = Pipeline([
                ("preprocess", preprocess),
                ("classifier", ExtraTreeClassifier(  # Changed to Classifier
                    max_depth=max_depth,
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
                        max_depth=max_depth,
                        random_state=0
                ))
            ])
    else:
        if extra_tree:
            model = Pipeline(
                [("preprocess", preprocess), ("regressor", ExtraTreeRegressor(
                max_depth=max_depth,  # Explicit limit
                min_samples_leaf=5,
                random_state=42
            ))]
            )
        else:
            model = Pipeline(
                [("preprocess", preprocess), ("regressor", DecisionTreeRegressor(random_state=42, max_depth=max_depth))]
            )
    return model