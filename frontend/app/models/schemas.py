"""Pydantic models for request/response validation."""

from pydantic import BaseModel
from typing import List, Dict, Optional, Any


class UploadResponse(BaseModel):
    file_id: str
    filename: str
    shape: List[int]
    columns: List[str]
    dtypes: Dict[str, str]
    preview: List[Dict[str, Any]]


class AnalyzeRequest(BaseModel):
    file_id: str
    target_column: Optional[str] = None


class ColumnStats(BaseModel):
    name: str
    dtype: str
    missing_count: int
    missing_pct: float
    unique_count: int
    mean: Optional[float] = None
    std: Optional[float] = None
    min_val: Optional[float] = None
    max_val: Optional[float] = None
    median: Optional[float] = None
    top_values: Optional[Dict[str, int]] = None


class Issue(BaseModel):
    column: Optional[str] = None
    issue_type: str
    severity: str
    description: str


class Recommendation(BaseModel):
    issue_type: str
    column: Optional[str] = None
    action: str
    description: str


class SubScore(BaseModel):
    name: str
    score: float
    max_score: float
    description: str


class QualityScore(BaseModel):
    total: float
    max_total: float
    sub_scores: List[SubScore]


class AnalyzeResponse(BaseModel):
    file_id: str
    shape: List[int]
    columns: List[str]
    dtypes: Dict[str, str]
    duplicate_count: int
    column_stats: List[ColumnStats]
    issues: List[Issue]
    recommendations: List[Recommendation]
    quality_score: QualityScore
    class_distribution: Optional[Dict[str, int]] = None
    target_column: Optional[str] = None


class CleanRequest(BaseModel):
    file_id: str
    target_column: Optional[str] = None
    scale_numeric: bool = False


class CleanResponse(BaseModel):
    file_id: str
    cleaned_file_id: str
    original_shape: List[int]
    cleaned_shape: List[int]
    actions_taken: List[str]
    whats_wrong: str
    how_we_fixed: str
