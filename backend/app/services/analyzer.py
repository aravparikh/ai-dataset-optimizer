"""Dataset analysis service — computes per-column and dataset-level statistics."""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional


def get_column_stats(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Compute descriptive statistics for every column."""
    stats = []
    for col in df.columns:
        series = df[col]
        missing_count = int(series.isna().sum())
        total = len(df)
        missing_pct = round(missing_count / total * 100, 1) if total > 0 else 0.0
        unique_count = int(series.nunique())

        col_stat: Dict[str, Any] = {
            "name": col,
            "dtype": str(series.dtype),
            "missing_count": missing_count,
            "missing_pct": missing_pct,
            "unique_count": unique_count,
        }

        if pd.api.types.is_numeric_dtype(series):
            clean = series.dropna()
            if len(clean) > 0:
                col_stat["mean"] = round(float(clean.mean()), 4)
                col_stat["std"] = round(float(clean.std()), 4)
                col_stat["min_val"] = round(float(clean.min()), 4)
                col_stat["max_val"] = round(float(clean.max()), 4)
                col_stat["median"] = round(float(clean.median()), 4)
        else:
            value_counts = series.dropna().value_counts().head(5)
            col_stat["top_values"] = {str(k): int(v) for k, v in value_counts.items()}

        stats.append(col_stat)
    return stats


def get_duplicate_count(df: pd.DataFrame) -> int:
    """Count the number of fully duplicated rows."""
    return int(df.duplicated().sum())


def get_class_distribution(
    df: pd.DataFrame, target_column: str
) -> Optional[Dict[str, int]]:
    """Return value counts for a categorical target column."""
    if target_column not in df.columns:
        return None
    series = df[target_column].dropna()
    # Treat high-cardinality numeric columns as regression targets
    if pd.api.types.is_numeric_dtype(series) and series.nunique() > 20:
        return None
    counts = series.value_counts()
    return {str(k): int(v) for k, v in counts.items()}


def get_preview(df: pd.DataFrame, n: int = 10) -> List[Dict[str, Any]]:
    """Return the first *n* rows as JSON-safe dicts."""
    preview = df.head(n).copy()
    preview = preview.where(pd.notnull(preview), None)

    records: List[Dict[str, Any]] = []
    for _, row in preview.iterrows():
        record: Dict[str, Any] = {}
        for col in preview.columns:
            val = row[col]
            if isinstance(val, (np.integer,)):
                record[col] = int(val)
            elif isinstance(val, (np.floating,)):
                record[col] = None if np.isnan(val) else float(val)
            elif isinstance(val, np.bool_):
                record[col] = bool(val)
            else:
                record[col] = val
        records.append(record)
    return records
