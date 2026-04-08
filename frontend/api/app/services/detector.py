"""Issue detection engine — flags data quality problems in plain English."""

import pandas as pd
from typing import List, Dict, Any, Optional

# ── Thresholds ──────────────────────────────────────────────────────────────
MISSING_WARNING_PCT = 5.0
MISSING_HIGH_PCT = 50.0
LOW_VARIANCE_THRESHOLD = 0.01
IMBALANCE_RATIO_THRESHOLD = 3.0


def detect_issues(
    df: pd.DataFrame,
    column_stats: List[Dict[str, Any]],
    duplicate_count: int,
    target_column: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Run every detection rule and return a list of issue dicts."""
    issues: List[Dict[str, Any]] = []
    row_count = len(df)

    for stat in column_stats:
        pct = stat["missing_pct"]
        if pct >= MISSING_HIGH_PCT:
            issues.append({
                "column": stat["name"],
                "issue_type": "high_missing",
                "severity": "high",
                "description": (
                    f"Column '{stat['name']}' has {pct}% missing values "
                    "— consider dropping it."
                ),
            })
        elif pct >= MISSING_WARNING_PCT:
            issues.append({
                "column": stat["name"],
                "issue_type": "missing_values",
                "severity": "medium",
                "description": f"Column '{stat['name']}' has {pct}% missing values.",
            })

    # Duplicate rows
    if duplicate_count > 0:
        dup_pct = round(duplicate_count / row_count * 100, 1) if row_count else 0
        issues.append({
            "column": None,
            "issue_type": "duplicates",
            "severity": "medium" if dup_pct < 10 else "high",
            "description": (
                f"Dataset has {duplicate_count} duplicate rows ({dup_pct}% of data)."
            ),
        })

    # Constant columns (1 or 0 unique values)
    for stat in column_stats:
        if stat["unique_count"] <= 1:
            issues.append({
                "column": stat["name"],
                "issue_type": "constant_column",
                "severity": "high",
                "description": (
                    f"Column '{stat['name']}' has only {stat['unique_count']} unique "
                    "value and should likely be removed."
                ),
            })

    # ID-like columns
    for stat in column_stats:
        col = stat["name"]
        if stat["unique_count"] >= row_count * 0.95 and row_count > 10:
            name_lower = col.lower()
            id_hints = ["id", "index", "key", "uuid", "guid", "pk"]
            is_id_name = any(hint in name_lower for hint in id_hints)
            if is_id_name or stat["unique_count"] == row_count:
                issues.append({
                    "column": col,
                    "issue_type": "id_column",
                    "severity": "medium",
                    "description": (
                        f"Column '{col}' appears to be a unique identifier "
                        "and may not help prediction."
                    ),
                })

    # Low-variance numeric columns
    for stat in column_stats:
        if (
            stat.get("std") is not None
            and stat["std"] < LOW_VARIANCE_THRESHOLD
            and stat["unique_count"] > 1
        ):
            issues.append({
                "column": stat["name"],
                "issue_type": "low_variance",
                "severity": "low",
                "description": (
                    f"Column '{stat['name']}' has very low variance "
                    f"(std={stat['std']}) and may not be informative."
                ),
            })

    # Class imbalance
    if target_column and target_column in df.columns:
        series = df[target_column].dropna()
        if not pd.api.types.is_numeric_dtype(series) or series.nunique() <= 20:
            counts = series.value_counts()
            if len(counts) >= 2:
                majority = counts.iloc[0]
                minority = counts.iloc[-1]
                if minority > 0 and majority / minority > IMBALANCE_RATIO_THRESHOLD:
                    ratio = round(majority / minority, 1)
                    issues.append({
                        "column": target_column,
                        "issue_type": "class_imbalance",
                        "severity": "high",
                        "description": (
                            f"Target column '{target_column}' is highly imbalanced "
                            f"(majority/minority ratio: {ratio}x)."
                        ),
                    })

    return issues


def generate_recommendations(issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Map each detected issue to an actionable recommendation."""
    recs: List[Dict[str, Any]] = []

    action_map = {
        "missing_values": lambda i: {
            "action": "impute",
            "description": (
                f"Impute missing values in '{i['column']}' using "
                "median (numeric) or mode (categorical)."
            ),
        },
        "high_missing": lambda i: {
            "action": "drop_column",
            "description": (
                f"Drop column '{i['column']}' — too many missing values "
                "to reliably impute."
            ),
        },
        "duplicates": lambda _: {
            "action": "remove_duplicates",
            "description": "Remove duplicate rows to prevent data leakage and bias.",
        },
        "constant_column": lambda i: {
            "action": "drop_column",
            "description": (
                f"Drop column '{i['column']}' — a single unique value "
                "provides no information."
            ),
        },
        "id_column": lambda i: {
            "action": "drop_column",
            "description": (
                f"Drop column '{i['column']}' — unique identifiers "
                "don't generalize in ML models."
            ),
        },
        "low_variance": lambda i: {
            "action": "review",
            "description": (
                f"Review column '{i['column']}' — low variance may mean "
                "it's not useful, but domain context matters."
            ),
        },
        "class_imbalance": lambda i: {
            "action": "handle_imbalance",
            "description": (
                f"Consider using class weights, SMOTE, or stratified "
                f"sampling to handle imbalance in '{i['column']}'."
            ),
        },
    }

    for issue in issues:
        handler = action_map.get(issue["issue_type"])
        if handler:
            result = handler(issue)
            recs.append({
                "issue_type": issue["issue_type"],
                "column": issue.get("column"),
                **result,
            })

    # Always-present general recommendations
    recs.append({
        "issue_type": "general",
        "column": None,
        "action": "encode_categoricals",
        "description": (
            "One-hot encode remaining categorical columns for ML compatibility."
        ),
    })
    recs.append({
        "issue_type": "general",
        "column": None,
        "action": "scale_numeric",
        "description": (
            "Consider normalizing numeric features with StandardScaler "
            "for distance-based models."
        ),
    })

    return recs
