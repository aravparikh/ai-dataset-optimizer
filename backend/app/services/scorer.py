"""Dataset quality scoring — rates data quality from 0 to 10."""

import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional


def compute_quality_score(
    df: pd.DataFrame,
    column_stats: List[Dict[str, Any]],
    duplicate_count: int,
    issues: List[Dict[str, Any]],
    target_column: Optional[str] = None,
) -> Dict[str, Any]:
    """Return an overall score out of 10, broken into four sub-scores."""
    sub_scores: List[Dict[str, Any]] = []
    row_count = len(df)

    # ── Completeness (0–3) ──────────────────────────────────────────────────
    avg_missing = (
        float(np.mean([s["missing_pct"] for s in column_stats]))
        if column_stats
        else 0.0
    )
    completeness = round(min(3.0, max(0.0, 3.0 * (1 - avg_missing / 50))), 1)
    sub_scores.append({
        "name": "Completeness",
        "score": completeness,
        "max_score": 3.0,
        "description": f"Average missing rate: {round(avg_missing, 1)}%",
    })

    # ── Uniqueness (0–2) ───────────────────────────────────────────────────
    dup_pct = (duplicate_count / row_count * 100) if row_count else 0.0
    uniqueness = round(min(2.0, max(0.0, 2.0 * (1 - dup_pct / 30))), 1)
    sub_scores.append({
        "name": "Uniqueness",
        "score": uniqueness,
        "max_score": 2.0,
        "description": f"{duplicate_count} duplicate rows ({round(dup_pct, 1)}%)",
    })

    # ── Balance (0–2.5) ────────────────────────────────────────────────────
    balance = 2.5
    if target_column and target_column in df.columns:
        imbalance_issues = [i for i in issues if i["issue_type"] == "class_imbalance"]
        if imbalance_issues:
            series = df[target_column].dropna()
            counts = series.value_counts()
            if len(counts) >= 2:
                ratio = counts.iloc[0] / counts.iloc[-1]
                balance = round(min(2.5, max(0.0, 2.5 * (1 - (ratio - 1) / 9))), 1)
    sub_scores.append({
        "name": "Balance",
        "score": balance,
        "max_score": 2.5,
        "description": (
            "Class distribution balance"
            + (" (no target selected)" if not target_column else "")
        ),
    })

    # ── Feature Usefulness (0–2.5) ─────────────────────────────────────────
    total_cols = len(column_stats) if column_stats else 1
    useless = sum(
        1
        for i in issues
        if i["issue_type"] in ("constant_column", "id_column")
    )
    usefulness = round(
        min(2.5, max(0.0, 2.5 * (1 - useless / total_cols * 2))), 1
    )
    sub_scores.append({
        "name": "Feature Usefulness",
        "score": usefulness,
        "max_score": 2.5,
        "description": f"{useless} of {total_cols} columns flagged as uninformative",
    })

    return {
        "total": round(sum(s["score"] for s in sub_scores), 1),
        "max_total": sum(s["max_score"] for s in sub_scores),
        "sub_scores": sub_scores,
    }
