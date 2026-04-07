"""Dataset cleaning service — applies automatic fix transformations."""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Any, Optional, Tuple


def clean_dataset(
    df: pd.DataFrame,
    issues: List[Dict[str, Any]],
    target_column: Optional[str] = None,
    scale_numeric: bool = False,
) -> Tuple[pd.DataFrame, List[str], str, str]:
    """
    Auto-clean a dataset based on detected issues.

    Returns
    -------
    cleaned : pd.DataFrame
    actions : list of short action descriptions
    whats_wrong : human-readable explanation of problems
    how_we_fixed : human-readable explanation of fixes
    """
    cleaned = df.copy()
    actions: List[str] = []
    problems: List[str] = []
    fixes: List[str] = []

    # ── 1. Remove duplicate rows ────────────────────────────────────────────
    dup_count = int(cleaned.duplicated().sum())
    if dup_count > 0:
        cleaned = cleaned.drop_duplicates()
        actions.append(f"Removed {dup_count} duplicate rows")
        problems.append(
            f"Your dataset had {dup_count} duplicate rows that could bias "
            "model training."
        )
        fixes.append(f"We removed all {dup_count} duplicate rows.")

    # ── 2. Drop constant columns ────────────────────────────────────────────
    constant_cols = [c for c in cleaned.columns if cleaned[c].nunique() <= 1]
    if constant_cols:
        cleaned = cleaned.drop(columns=constant_cols)
        names = ", ".join(constant_cols)
        actions.append(f"Dropped constant columns: {names}")
        problems.append(
            f"Columns {names} had only one unique value — they provide "
            "zero information."
        )
        fixes.append(f"We dropped these constant columns: {names}.")

    # ── 3. Drop ID-like columns ─────────────────────────────────────────────
    id_cols = [
        i["column"]
        for i in issues
        if i["issue_type"] == "id_column" and i["column"] in cleaned.columns
    ]
    if target_column:
        id_cols = [c for c in id_cols if c != target_column]
    if id_cols:
        cleaned = cleaned.drop(columns=id_cols)
        names = ", ".join(id_cols)
        actions.append(f"Dropped ID-like columns: {names}")
        problems.append(
            f"Columns {names} appeared to be unique identifiers that "
            "won't help a model generalize."
        )
        fixes.append(f"We dropped these ID columns: {names}.")

    # ── 4. Drop high-missing columns (>50%) ─────────────────────────────────
    high_missing = [
        c
        for c in cleaned.columns
        if cleaned[c].isna().sum() / max(len(cleaned), 1) > 0.5
        and c != target_column
    ]
    if high_missing:
        cleaned = cleaned.drop(columns=high_missing)
        names = ", ".join(high_missing)
        actions.append(f"Dropped high-missing columns (>50%): {names}")
        problems.append(
            f"Columns {names} had more than 50% missing values — too "
            "many gaps to impute reliably."
        )
        fixes.append(f"We dropped these columns: {names}.")

    # ── 5. Impute missing numeric values (median) ──────────────────────────
    num_cols = cleaned.select_dtypes(include=[np.number]).columns.tolist()
    imputed_num: List[str] = []
    for col in num_cols:
        if cleaned[col].isna().any():
            cleaned[col] = cleaned[col].fillna(cleaned[col].median())
            imputed_num.append(col)
    if imputed_num:
        names = ", ".join(imputed_num)
        actions.append(f"Imputed missing numeric values with median: {names}")
        problems.append(f"Numeric columns {names} had missing values.")
        fixes.append(
            f"We filled missing numeric values with the column median "
            f"for: {names}."
        )

    # ── 6. Impute missing categorical values (mode) ────────────────────────
    cat_cols = cleaned.select_dtypes(include=["object", "category"]).columns.tolist()
    imputed_cat: List[str] = []
    for col in cat_cols:
        if cleaned[col].isna().any():
            mode = cleaned[col].mode()
            if len(mode) > 0:
                cleaned[col] = cleaned[col].fillna(mode.iloc[0])
                imputed_cat.append(col)
    if imputed_cat:
        names = ", ".join(imputed_cat)
        actions.append(f"Imputed missing categorical values with mode: {names}")
        problems.append(f"Categorical columns {names} had missing values.")
        fixes.append(
            f"We filled missing categorical values with the most frequent "
            f"value for: {names}."
        )

    # ── 7. One-hot encode categoricals (except target) ─────────────────────
    cat_cols = cleaned.select_dtypes(include=["object", "category"]).columns.tolist()
    if target_column and target_column in cat_cols:
        cat_cols.remove(target_column)
    if cat_cols:
        cleaned = pd.get_dummies(cleaned, columns=cat_cols, drop_first=True)
        names = ", ".join(cat_cols)
        actions.append(f"One-hot encoded categorical columns: {names}")
        problems.append(
            f"Categorical columns {names} needed encoding for ML algorithms."
        )
        fixes.append(f"We applied one-hot encoding to: {names}.")

    # ── 8. Optionally scale numeric features ───────────────────────────────
    if scale_numeric:
        num_cols = cleaned.select_dtypes(include=[np.number]).columns.tolist()
        if target_column and target_column in num_cols:
            num_cols.remove(target_column)
        if num_cols:
            scaler = StandardScaler()
            cleaned[num_cols] = scaler.fit_transform(cleaned[num_cols])
            names = ", ".join(num_cols)
            actions.append(f"Scaled numeric columns with StandardScaler: {names}")
            fixes.append(
                f"We standardized numeric features (zero mean, unit "
                f"variance) for: {names}."
            )

    # ── Build explanation strings ───────────────────────────────────────────
    if problems:
        whats_wrong = "Here's what we found:\n\n" + "\n\n".join(
            f"\u2022 {p}" for p in problems
        )
    else:
        whats_wrong = "Your dataset looks clean! No major issues were detected."

    if fixes:
        how_we_fixed = "Here's what we did:\n\n" + "\n\n".join(
            f"\u2022 {f}" for f in fixes
        )
    else:
        how_we_fixed = "No cleaning actions were needed."

    return cleaned, actions, whats_wrong, how_we_fixed
