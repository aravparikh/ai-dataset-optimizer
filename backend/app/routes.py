"""API routes for dataset upload, analysis, cleaning, and download."""

import os
import uuid

import pandas as pd
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

from app.models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    CleanRequest,
    CleanResponse,
    UploadResponse,
)
from app.services.analyzer import (
    get_column_stats,
    get_class_distribution,
    get_duplicate_count,
    get_preview,
)
from app.services.detector import detect_issues, generate_recommendations
from app.services.scorer import compute_quality_score
from app.services.cleaner import clean_dataset

router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _load_csv(file_id: str) -> pd.DataFrame:
    """Load a CSV by file_id, raising 404 if missing."""
    path = os.path.join(UPLOAD_DIR, f"{file_id}.csv")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return pd.read_csv(path)


# ── Upload ──────────────────────────────────────────────────────────────────

@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Accept a CSV upload, persist it, and return a preview."""
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.csv")

    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    try:
        df = pd.read_csv(file_path)
    except Exception as exc:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail=f"Could not parse CSV: {exc}")

    return UploadResponse(
        file_id=file_id,
        filename=file.filename,
        shape=[int(df.shape[0]), int(df.shape[1])],
        columns=df.columns.tolist(),
        dtypes={col: str(dtype) for col, dtype in df.dtypes.items()},
        preview=get_preview(df),
    )


# ── Analyze ─────────────────────────────────────────────────────────────────

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_file(request: AnalyzeRequest):
    """Run full quality analysis on a previously uploaded file."""
    df = _load_csv(request.file_id)
    target = request.target_column

    col_stats = get_column_stats(df)
    dup_count = get_duplicate_count(df)
    issues = detect_issues(df, col_stats, dup_count, target)
    recs = generate_recommendations(issues)
    score = compute_quality_score(df, col_stats, dup_count, issues, target)

    class_dist = None
    if target:
        class_dist = get_class_distribution(df, target)

    return AnalyzeResponse(
        file_id=request.file_id,
        shape=[int(df.shape[0]), int(df.shape[1])],
        columns=df.columns.tolist(),
        dtypes={col: str(dtype) for col, dtype in df.dtypes.items()},
        duplicate_count=dup_count,
        column_stats=col_stats,
        issues=issues,
        recommendations=recs,
        quality_score=score,
        class_distribution=class_dist,
        target_column=target,
    )


# ── Clean ───────────────────────────────────────────────────────────────────

@router.post("/clean", response_model=CleanResponse)
async def clean_file(request: CleanRequest):
    """Auto-clean a dataset and persist the result for download."""
    df = _load_csv(request.file_id)

    # Re-detect issues so cleaning is based on current state
    col_stats = get_column_stats(df)
    dup_count = get_duplicate_count(df)
    issues = detect_issues(df, col_stats, dup_count, request.target_column)

    cleaned_df, actions, whats_wrong, how_we_fixed = clean_dataset(
        df,
        issues,
        target_column=request.target_column,
        scale_numeric=request.scale_numeric,
    )

    cleaned_id = str(uuid.uuid4())
    cleaned_path = os.path.join(UPLOAD_DIR, f"{cleaned_id}.csv")
    cleaned_df.to_csv(cleaned_path, index=False)

    return CleanResponse(
        file_id=request.file_id,
        cleaned_file_id=cleaned_id,
        original_shape=[int(df.shape[0]), int(df.shape[1])],
        cleaned_shape=[int(cleaned_df.shape[0]), int(cleaned_df.shape[1])],
        actions_taken=actions,
        whats_wrong=whats_wrong,
        how_we_fixed=how_we_fixed,
    )


# ── Download ────────────────────────────────────────────────────────────────

@router.get("/download/{file_id}")
async def download_file(file_id: str):
    """Download a cleaned CSV by its file_id."""
    path = os.path.join(UPLOAD_DIR, f"{file_id}.csv")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(
        path,
        media_type="text/csv",
        filename=f"cleaned_{file_id[:8]}.csv",
    )
