"""
Experiment Deduplication for Pandas DataFrames with Adaptive Epsilon

This script deduplicates rows in a pandas DataFrame based on parameter-specific
similarity thresholds calculated from the data distribution.

For each numerical column, epsilon is calculated as:
    epsilon = mean * relative_tolerance / 100

This approach is standard in analytical chemistry (RSD < 5% for precision).

Usage (as imported module):
    from deduplicate_experiments_adaptive_df import get_duplicate_indices

    duplicate_indices = get_duplicate_indices(
        X,  # Feature matrix (DataFrame)
        relative_tolerance=5.0
    )

    X_clean = X.drop(duplicate_indices)
    y_clean = y[~X.index.isin(duplicate_indices)]

Key differences from JSON version:
- Works directly on feature matrix X (not df)
- Returns only duplicate indices for removal
- Caller handles removal of X and y
- No need to exclude columns (pass only X)
"""

import pandas as pd
import numpy as np
from typing import Dict, List
import statistics


def calculate_dataframe_statistics(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Calculate statistics (min, max, mean, std) for each numerical column.

    Args:
        df: pandas DataFrame (typically the feature matrix X)

    Returns:
        Dictionary mapping column names to their statistics
    """
    param_stats = {}

    for col in df.columns:
        # Skip non-numeric columns
        if not pd.api.types.is_numeric_dtype(df[col]):
            continue

        # Extract numeric values, ignoring NaN
        values = df[col].dropna().values.tolist()

        if len(values) > 0:
            param_stats[col] = {
                'min': float(np.min(values)),
                'max': float(np.max(values)),
                'mean': float(np.mean(values)),
                'count': len(values)
            }

            # Calculate standard deviation if we have enough data points
            if len(values) >= 2:
                param_stats[col]['std'] = float(np.std(values, ddof=1))
            else:
                param_stats[col]['std'] = 0.0

    return param_stats


def calculate_adaptive_epsilon(param_stats: Dict[str, Dict[str, float]], 
                               relative_tolerance: float = 5.0) -> Dict[str, float]:
    """
    Calculate epsilon for each parameter based on its statistical distribution.

    Standard approach in analytical chemistry:
    - Use relative tolerance (% of mean) as the similarity threshold
    - Typical values: 5% (precise), 10% (acceptable), 20% (loose)

    Args:
        param_stats: Statistics for each parameter
        relative_tolerance: Percentage of mean to use as epsilon (default: 5%)

    Returns:
        Dictionary mapping parameter names to their epsilon values
    """
    epsilon_dict = {}

    for param_name, stats in param_stats.items():
        mean = stats['mean']

        # Calculate epsilon as percentage of mean
        epsilon = abs(mean) * (relative_tolerance / 100.0)

        # Handle edge case where mean is very close to zero
        if abs(mean) < 1e-10:
            value_range = stats['max'] - stats['min']
            epsilon = value_range * (relative_tolerance / 100.0) if value_range > 0 else 1e-6

        epsilon_dict[param_name] = epsilon

    return epsilon_dict


def compare_dataframe_rows(row1: pd.Series, 
                           row2: pd.Series, 
                           epsilon_dict: Dict[str, float]) -> bool:
    """
    Compare two DataFrame rows for similarity using parameter-specific epsilon values.

    Returns True if rows are similar (should be removed), False otherwise.

    Logic:
    1. Compare numerical values using parameter-specific epsilon
    2. Compare boolean values - if ANY differ, not similar
    3. Compare string values - if ANY differ, not similar
    4. If all checks pass, rows are similar
    """
    for col in row1.index:
        val1 = row1[col]
        val2 = row2[col]

        # Skip NaN values
        if pd.isna(val1) and pd.isna(val2):
            continue

        # If one is NaN and other is not, they're different
        if pd.isna(val1) or pd.isna(val2):
            return False

        # Check if both are numerical
        if pd.api.types.is_numeric_dtype(type(val1)) and pd.api.types.is_numeric_dtype(type(val2)):
            # Get parameter-specific epsilon, default to 0.01 if not found
            epsilon = epsilon_dict.get(col, 0.01)

            # Compare numerical values with parameter-specific epsilon tolerance
            if abs(float(val1) - float(val2)) > epsilon:
                return False  # Found significant numerical difference

        # Check if both are boolean
        elif isinstance(val1, (bool, np.bool_)) and isinstance(val2, (bool, np.bool_)):
            if val1 != val2:
                return False  # Found boolean difference

        # For string values, they must match exactly
        elif isinstance(val1, str) and isinstance(val2, str):
            if val1 != val2:
                return False  # String values differ

        # If types don't match, not similar
        elif type(val1) != type(val2):
            return False

    # No significant differences found - rows are similar
    return True

def get_duplicate_indices(
    X: pd.DataFrame,
    relative_tolerance: float = 5.0,
    verbose: bool = True
) -> tuple:

    if verbose:
        print("\nCalculating feature statistics...")
    param_stats = calculate_dataframe_statistics(X)

    if verbose:
        print("Calculating adaptive epsilon values...")
    epsilon_dict = calculate_adaptive_epsilon(param_stats, relative_tolerance)

    duplicate_indices = []
    duplicate_pairs = []

    if verbose:
        print(f"\nProcessing {len(X)} rows...")

    n = len(X)

    # Outer loop backwards: newest → oldest
    for i in range(n - 1, -1, -1):
        if verbose and ((n - i) % 10 == 0):
            print(f"Processed {n - i}/{n} rows...")

        current_row = X.iloc[i]

        # Compare against even newer rows only
        for j in range(n - 1, i, -1):

            if j in duplicate_indices:
                continue

            newer_row = X.iloc[j]

            if compare_dataframe_rows(current_row, newer_row, epsilon_dict):
                duplicate_indices.append(i)
                duplicate_pairs.append((i, j))
                if verbose:
                    print(f"  → Row {i} is similar to row {j} (marked as duplicate).")
                break

    return duplicate_indices, duplicate_pairs, epsilon_dict, param_stats