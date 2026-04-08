"""Vercel serverless entry point — exposes the FastAPI app."""

from app.main import app  # noqa: F401

# Vercel's @vercel/python runtime auto-detects ASGI apps named `app`.
handler = app
