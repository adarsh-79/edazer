import pandas as pd
from typing import List
from itertools import product
from ..core import Edazer

def get_primary_key(
    df: pd.DataFrame,
    threshold: float = 0.9,
    n_combos: int = 1,
    valid_column_dtypes: List[str] = None,
) -> List[str]:
    """
    Identify column(s) or column combinations that can serve as unique keys.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame to analyze.
    threshold : float, optional
        Proportion of uniqueness required for a column or combination 
        to be considered a candidate key. Default is 0.9 (i.e., at least 90% unique).
    n_combos : int, optional
        The number of columns to combine when checking for composite keys.
        Default is 1 (i.e., single-column keys).
    valid_column_dtypes : List[str], optional
        List of data types to consider for candidate keys.
        Default is ["int", "datetime64", "object"].

    Returns
    -------
    List[str] or List[List[str]]
        A list of candidate key columns or combinations of columns that are 
        likely to uniquely identify rows in the DataFrame.

    Notes
    -----
    - Columns must have one of the valid data types to be tested.
    - When n_combos > 1, all unique combinations of eligible columns are tested.
    - A column/combination is considered a candidate key if it has a uniqueness 
      ratio >= `threshold`, or if it is fully unique (n_unique == n_rows).
    """

    # Initialize Edazer with pandas backend
    df_zer = Edazer(df, backend="pandas")
    n_rows = len(df)
    candidate_keys = []

    # Default to these dtypes if not provided
    if valid_column_dtypes is None:
        valid_column_dtypes = ["int", "datetime64", "object"]

    # Get columns of valid dtypes
    valid_columns = df_zer.cols_with_dtype(valid_column_dtypes)

    # Sanity check
    if n_combos < 1:
        raise ValueError("`n_combos` must be >= 1")

    # Helper function to check if a Series qualifies as a key
    def is_candidate_key(ds: pd.Series) -> bool:
        n_uniques = ds.nunique()
        return (n_uniques == n_rows) or (n_uniques >= threshold * n_rows)

    # ---- Case 1: Single-column keys ----
    if n_combos == 1:
        for col in valid_columns:
            if is_candidate_key(df[col]):
                candidate_keys.append(col)
        return candidate_keys

    # ---- Case 2: Multi-column (composite) keys ----
    all_combinations = [
        list(combo)
        for combo in product(valid_columns, repeat=n_combos)
        if len(set(combo)) == n_combos  # avoid duplicate column pairs
    ]

    for col_combo in all_combinations:
        concatenated = df[list(col_combo)].astype(str).agg(" ".join, axis=1)
        if is_candidate_key(concatenated):
            candidate_keys.append(col_combo)

    return candidate_keys
