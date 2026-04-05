"""Vercel serverless entry point — exposes the FastAPI app."""

import sys
import os

# Add backend to the Python path so imports resolve
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.main import app  # noqa: E402, F401 — Vercel picks this up
