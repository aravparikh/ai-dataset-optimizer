"""Vercel serverless entry point — ensure local app/ package is importable."""

import os
import sys

# Make sure this directory (api/) is on sys.path so `app` resolves to api/app/.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from app.main import app  # noqa: E402, F401

handler = app
