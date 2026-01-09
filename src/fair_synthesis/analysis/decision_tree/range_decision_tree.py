"""
Custom Decision Tree Classifier with Range-Based Splits
========================================================

This module provides a RangeDecisionTreeClassifier that extends traditional
decision trees to support range-based split conditions.

Supported split types:
1. Standard splits: feature <= threshold
2. Range splits: feature in [lower, upper]

The "outside range" case is automatically the false branch of the range split.
"""

import numpy as np
from collections import Counter
from sklearn.base import BaseEstimator, ClassifierMixin


class Node:
    """
    Represents a node in the decision tree.

    Attributes:
        feature: Index of the feature to split on (None for leaf nodes)
        threshold: Threshold value for standard splits
        range_bounds: Tuple (lower, upper) for range splits
        split_type: 'standard' or 'range'
        left: Left child node (True branch)
        right: Right child node (False branch)
        value: Class prediction for leaf nodes
        samples: Number of samples at this node
        impurity: Gini impurity at this node
    """

    def __init__(self, feature=None, threshold=None, range_bounds=None,
                 split_type='standard', left=None, right=None, value=None,
                 samples=None, impurity=None):
        self.feature = feature
        self.threshold = threshold
        self.range_bounds = range_bounds
        self.split_type = split_type
        self.left = left
        self.right = right
        self.value = value
        self.samples = samples
        self.impurity = impurity


class RangeDecisionTreeClassifier(BaseEstimator, ClassifierMixin):
    """
    Decision Tree Classifier with support for range-based splits.

    This classifier extends standard decision trees (CART) to evaluate both
    traditional threshold-based splits (feature <= threshold) and range-based
    splits (feature in [lower, upper]). At each node, the algorithm evaluates
    both split types and selects the one with the highest information gain.

    Parameters
    ----------
    max_depth : int, default=None
        The maximum depth of the tree. If None, then nodes are expanded until
        all leaves are pure or until they contain less than min_samples_split samples.

    min_samples_split : int, default=2
        The minimum number of samples required to split an internal node.

    min_samples_leaf : int, default=1
        The minimum number of samples required to be at a leaf node.

    split_strategy : str, default='both'
        Strategy for evaluating splits:
        - 'standard': Only evaluate standard <= threshold splits
        - 'range': Only evaluate range [a,b] splits
        - 'both': Evaluate both types at each node and select the best

    max_range_splits : int, default=10
        Maximum number of range combinations to evaluate per feature.
        This controls computational cost. Higher values are more thorough
        but slower. For datasets with ~50 samples, 10 is a good default.

    random_state : int, default=None
        Controls the randomness in range split evaluation.

    Attributes
    ----------
    tree_ : Node
        The underlying tree structure.

    classes_ : ndarray of shape (n_classes,)
        The class labels.

    n_classes_ : int
        The number of classes.

    n_features_ : int
        The number of input features.

    feature_importances_ : ndarray of shape (n_features_,)
        Impurity-based feature importances.

    Examples
    --------
    >>> from sklearn.datasets import make_classification
    >>> from sklearn.model_selection import train_test_split
    >>> X, y = make_classification(n_samples=100, n_features=4, n_classes=2, random_state=42)
    >>> X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    >>> clf = RangeDecisionTreeClassifier(max_depth=3, split_strategy='both')
    >>> clf.fit(X_train, y_train)
    >>> clf.score(X_test, y_test)
    """

    def __init__(
            self,
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            split_strategy='both',
            max_range_splits=10,
            random_state=None):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.split_strategy = split_strategy
        self.max_range_splits = max_range_splits
        self.random_state = random_state

        self.tree_ = None
        self.classes_ = None
        self.n_classes_ = None
        self.n_features_ = None
        self.feature_importances_ = None

    def _gini_impurity(self, y):
        """
        Calculate Gini impurity for a set of class labels.

        Gini impurity measures the probability of incorrectly classifying a
        randomly chosen element if it were randomly labeled according to the
        class distribution at this node.

        Gini = 1 - sum(p_i^2) where p_i is the proportion of class i

        Parameters
        ----------
        y : array-like of shape (n_samples,)
            Class labels.

        Returns
        -------
        float
            Gini impurity value between 0 (pure) and 0.5 (maximally impure).
        """
        if len(y) == 0:
            return 0

        counter = Counter(y)
        impurity = 1.0

        for count in counter.values():
            prob = count / len(y)
            impurity -= prob ** 2

        return impurity

    def _information_gain(self, y, y_left, y_right):
        """
        Calculate information gain from a split.

        Information Gain = Impurity(parent) - weighted_average(Impurity(children))

        Parameters
        ----------
        y : array-like of shape (n_samples,)
            Class labels of parent node.

        y_left : array-like of shape (n_left,)
            Class labels of left child.

        y_right : array-like of shape (n_right,)
            Class labels of right child.

        Returns
        -------
        float
            Information gain from the split.
        """
        n = len(y)
        n_left = len(y_left)
        n_right = len(y_right)

        if n_left == 0 or n_right == 0:
            return 0

        impurity_parent = self._gini_impurity(y)
        impurity_left = self._gini_impurity(y_left)
        impurity_right = self._gini_impurity(y_right)

        weighted_impurity = (n_left / n) * impurity_left + \
            (n_right / n) * impurity_right

        return impurity_parent - weighted_impurity

    def _evaluate_standard_splits(self, X, y, feature_idx):
        """
        Evaluate all standard threshold splits for a feature.

        Tests splits at midpoints between consecutive unique values of the feature.
        This is the standard CART approach.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Feature matrix.

        y : array-like of shape (n_samples,)
            Class labels.

        feature_idx : int
            Index of the feature to evaluate.

        Returns
        -------
        dict or None
            Dictionary containing:
            - 'gain': information gain of the best split
            - 'feature': feature index
            - 'threshold': threshold value
            - 'split_type': 'standard'
            - 'left_mask': boolean array for left branch
            Or None if no valid split found.
        """
        unique_values = np.unique(X[:, feature_idx])

        if len(unique_values) <= 1:
            return None

        # Test midpoints between consecutive unique values
        thresholds = (unique_values[:-1] + unique_values[1:]) / 2

        best_gain = -np.inf
        best_threshold = None
        best_left_mask = None

        for threshold in thresholds:
            left_mask = X[:, feature_idx] <= threshold
            right_mask = ~left_mask

            # Check minimum samples constraint
            if np.sum(left_mask) < self.min_samples_leaf or \
                    np.sum(right_mask) < self.min_samples_leaf:
                continue

            gain = self._information_gain(y, y[left_mask], y[right_mask])

            if gain > best_gain:
                best_gain = gain
                best_threshold = threshold
                best_left_mask = left_mask

        if best_threshold is None:
            return None

        return {
            'gain': best_gain,
            'feature': feature_idx,
            'threshold': best_threshold,
            'split_type': 'standard',
            'left_mask': best_left_mask
        }

    def _evaluate_range_splits(self, X, y, feature_idx):
        """
        Evaluate range-based splits for a feature.

        Tests multiple [lower, upper] range combinations and evaluates:
        1. Left branch: values INSIDE the range
        2. Right branch: values OUTSIDE the range

        To avoid O(n^2) complexity, the number of tested ranges is limited
        by max_range_splits.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Feature matrix.

        y : array-like of shape (n_samples,)
            Class labels.

        feature_idx : int
            Index of the feature to evaluate.

        Returns
        -------
        dict or None
            Dictionary containing:
            - 'gain': information gain of the best split
            - 'feature': feature index
            - 'range_bounds': tuple (lower, upper)
            - 'split_type': 'range'
            - 'left_mask': boolean array for left branch (inside range)
            Or None if no valid split found.
        """
        unique_values = np.sort(np.unique(X[:, feature_idx]))

        if len(unique_values) <= 2:
            return None

        best_gain = -np.inf
        best_range = None
        best_left_mask = None

        # Limit number of ranges to evaluate
        n_values = len(unique_values)
        if n_values > self.max_range_splits:
            rng = np.random.RandomState(self.random_state)
            lower_indices = rng.choice(n_values - 1,
                                       size=self.max_range_splits,
                                       replace=False)
        else:
            lower_indices = range(n_values - 1)

        # Try different range combinations
        for i in lower_indices:
            for j in range(i + 1, min(i + n_values // 2, n_values)):
                lower = unique_values[i]
                upper = unique_values[j]

                # Split: inside range (left) vs outside range (right)
                inside_mask = (X[:, feature_idx] >= lower) & (
                    X[:, feature_idx] <= upper)
                outside_mask = ~inside_mask

                if np.sum(inside_mask) < self.min_samples_leaf or \
                        np.sum(outside_mask) < self.min_samples_leaf:
                    continue

                gain = self._information_gain(
                    y, y[inside_mask], y[outside_mask])

                if gain > best_gain:
                    best_gain = gain
                    best_range = (lower, upper)
                    best_left_mask = inside_mask

        if best_range is None:
            return None

        return {
            'gain': best_gain,
            'feature': feature_idx,
            'range_bounds': best_range,
            'split_type': 'range',
            'left_mask': best_left_mask
        }

    def _find_best_split(self, X, y):
        """
        Find the best split across all features and split types.

        Evaluates all features with the specified split_strategy and returns
        the split with the highest information gain.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Feature matrix.

        y : array-like of shape (n_samples,)
            Class labels.

        Returns
        -------
        dict or None
            Dictionary with split information or None if no valid split found.
        """
        n_samples, n_features = X.shape

        if n_samples < self.min_samples_split:
            return None

        best_split = None
        best_gain = -np.inf

        for feature_idx in range(n_features):
            # Evaluate standard splits
            if self.split_strategy in ['standard', 'both']:
                split_info = self._evaluate_standard_splits(X, y, feature_idx)
                if split_info and split_info['gain'] > best_gain:
                    best_gain = split_info['gain']
                    best_split = split_info

            # Evaluate range splits
            if self.split_strategy in ['range', 'both']:
                split_info = self._evaluate_range_splits(X, y, feature_idx)
                if split_info and split_info['gain'] > best_gain:
                    best_gain = split_info['gain']
                    best_split = split_info

        return best_split

    def _build_tree(self, X, y, depth=0):
        """
        Recursively build the decision tree.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Feature matrix.

        y : array-like of shape (n_samples,)
            Class labels.

        depth : int, default=0
            Current depth in the tree (for max_depth check).

        Returns
        -------
        Node
            Root node of the constructed subtree.
        """
        n_samples, n_features = X.shape
        n_classes = len(np.unique(y))

        # Stopping criteria
        if (self.max_depth is not None and depth >= self.max_depth) or \
                n_classes == 1 or \
                n_samples < self.min_samples_split:
            # Create leaf node
            leaf_value = Counter(y).most_common(1)[0][0]
            return Node(value=leaf_value,
                        samples=n_samples,
                        impurity=self._gini_impurity(y))

        # Find best split
        split_info = self._find_best_split(X, y)

        if split_info is None:
            # No valid split found, create leaf node
            leaf_value = Counter(y).most_common(1)[0][0]
            return Node(value=leaf_value,
                        samples=n_samples,
                        impurity=self._gini_impurity(y))

        # Create child nodes recursively
        left_mask = split_info['left_mask']
        right_mask = ~left_mask

        left_child = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        right_child = self._build_tree(X[right_mask], y[right_mask], depth + 1)

        # Create internal node
        node = Node(
            feature=split_info['feature'],
            threshold=split_info.get('threshold'),
            range_bounds=split_info.get('range_bounds'),
            split_type=split_info['split_type'],
            left=left_child,
            right=right_child,
            samples=n_samples,
            impurity=self._gini_impurity(y)
        )

        return node

    def _predict_sample(self, x, node):
        """
        Predict class for a single sample by traversing the tree.

        Parameters
        ----------
        x : array-like of shape (n_features,)
            Single feature vector.

        node : Node
            Current node in the tree.

        Returns
        -------
        class_label
            Predicted class label.
        """
        if node.value is not None:
            return node.value

        if node.split_type == 'standard':
            # Standard split: feature <= threshold
            if x[node.feature] <= node.threshold:
                return self._predict_sample(x, node.left)
            else:
                return self._predict_sample(x, node.right)

        elif node.split_type == 'range':
            # Range split: feature in [lower, upper]
            lower, upper = node.range_bounds
            if lower <= x[node.feature] <= upper:
                return self._predict_sample(x, node.left)  # Inside range
            else:
                return self._predict_sample(x, node.right)  # Outside range

    def fit(self, X, y):
        """
        Build decision tree classifier from training data.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training feature matrix.

        y : array-like of shape (n_samples,)
            Target values.

        Returns
        -------
        self : RangeDecisionTreeClassifier
            Fitted classifier.
        """
        # Convert to numpy arrays
        X = np.array(X)
        y = np.array(y)

        # Store training information
        self.classes_ = np.unique(y)
        self.n_classes_ = len(self.classes_)
        self.n_features_ = X.shape[1]

        # Build tree
        self.tree_ = self._build_tree(X, y)

        # Calculate feature importances
        self._compute_feature_importances(X, y)

        return self

    def _compute_feature_importances(self, X, y):
        """
        Compute feature importances based on impurity decrease.

        The importance of a feature is the (normalized) total decrease in
        impurity in all splits caused by that feature.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Feature matrix.

        y : array-like of shape (n_samples,)
            Class labels.
        """
        importances = np.zeros(self.n_features_)

        def traverse(node, n_samples):
            """Recursively compute feature importances."""
            if node.value is not None:  # Leaf node
                return

            # Calculate weighted impurity decrease
            if node.left and node.right:
                n_left = node.left.samples
                n_right = node.right.samples

                decrease = node.impurity - (
                    (n_left / n_samples) * node.left.impurity +
                    (n_right / n_samples) * node.right.impurity
                )

                importances[node.feature] += decrease * n_samples

                # Recursively process children
                traverse(node.left, n_samples)
                traverse(node.right, n_samples)

        traverse(self.tree_, len(y))

        # Normalize to sum to 1
        if np.sum(importances) > 0:
            importances = importances / np.sum(importances)

        self.feature_importances_ = importances

    def predict(self, X):
        """
        Predict class labels for samples in X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Feature matrix.

        Returns
        -------
        y : ndarray of shape (n_samples,)
            Predicted class labels.
        """
        X = np.array(X)
        return np.array([self._predict_sample(x, self.tree_) for x in X])

    def score(self, X, y):
        """
        Return the mean accuracy on the given test data and labels.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Test feature matrix.

        y : array-like of shape (n_samples,)
            True labels.

        Returns
        -------
        float
            Mean accuracy score.
        """
        y_pred = self.predict(X)
        return np.mean(y_pred == y)

    def print_tree(self, node=None, depth=0, feature_names=None):
        """
        Print a text representation of the tree structure.

        This method recursively prints the tree in a human-readable format.
        Split conditions are clearly labeled with their type (standard or range).

        Parameters
        ----------
        node : Node, optional
            Node to print (defaults to root).

        depth : int, default=0
            Current depth (used for indentation).

        feature_names : list, optional
            Feature names for more readable output. If None, uses X[i] notation.

        Examples
        --------
        >>> clf.print_tree(feature_names=['conc', 'equiv', 'temp'])
        """
        if node is None:
            node = self.tree_

        indent = "  " * depth

        # Leaf node
        if node.value is not None:
            print(f"{indent}Leaf: class={node.value} (samples={node.samples}, "
                  f"impurity={node.impurity:.3f})")
            return

        # Internal node - print split condition
        if feature_names is not None:
            feat_name = feature_names[node.feature]
        else:
            feat_name = f"X[{node.feature}]"

        if node.split_type == 'standard':
            print(f"{indent}If {feat_name} <= {node.threshold:.3f}:")
        elif node.split_type == 'range':
            lower, upper = node.range_bounds
            print(f"{indent}If {feat_name} in [{lower:.3f}, {upper:.3f}]:")

        # Print left branch (True condition)
        print(f"{indent}  [TRUE] Left branch:")
        self.print_tree(node.left, depth + 2, feature_names)

        # Print right branch (False condition)
        print(f"{indent}  [FALSE] Right branch:")
        self.print_tree(node.right, depth + 2, feature_names)


# Utility function for extracting decision rules
def extract_rules(tree_classifier, feature_names=None):
    """
    Extract all decision rules from a trained RangeDecisionTreeClassifier.

    Parameters
    ----------
    tree_classifier : RangeDecisionTreeClassifier
        A fitted classifier.

    feature_names : list, optional
        Names for features. If None, uses X[i] notation.

    Returns
    -------
    list of tuples
        Each tuple contains (rule_str, predicted_class) where rule_str is
        a human-readable condition string.

    Examples
    --------
    >>> clf = RangeDecisionTreeClassifier()
    >>> clf.fit(X, y)
    >>> rules = extract_rules(clf, feature_names=['conc', 'equiv', 'temp'])
    >>> for rule, pred_class in rules:
    ...     print(f"IF {rule} THEN {pred_class}")
    """
    rules = []

    def traverse(node, path=[]):
        """Recursively extract rules."""
        if node.value is not None:
            # Reached a leaf - save the rule
            if path:
                rule_str = " AND ".join(path)
            else:
                rule_str = "True"
            rules.append((rule_str, node.value))
            return

        # Format feature name
        if feature_names is not None:
            feat_name = feature_names[node.feature]
        else:
            feat_name = f"X[{node.feature}]"

        # Create condition strings based on split type
        if node.split_type == 'standard':
            condition_true = f"{feat_name} <= {node.threshold:.3f}"
            condition_false = f"{feat_name} > {node.threshold:.3f}"
        elif node.split_type == 'range':
            lower, upper = node.range_bounds
            condition_true = f"{feat_name} in [{lower:.3f}, {upper:.3f}]"
            condition_false = f"{feat_name} NOT in [{lower:.3f}, {upper:.3f}]"

        # Traverse left (condition true)
        traverse(node.left, path + [condition_true])

        # Traverse right (condition false)
        traverse(node.right, path + [condition_false])

    traverse(tree_classifier.tree_)
    return rules
