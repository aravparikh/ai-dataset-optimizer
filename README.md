# AI Dataset Optimizer

A web app that helps you upload a CSV dataset, analyze data quality issues, and automatically clean it for machine learning.

Upload your CSV, see what's wrong, get recommendations, and download a cleaned version — all in one click.

## Features

- **CSV Upload** — drag-and-drop or browse, preview first 10 rows, see shape and column types
- **Data Quality Analysis** — missing values, duplicates, summary stats, class imbalance detection
- **Issue Detection** — plain-English descriptions of every problem found
- **Smart Recommendations** — actionable fix suggestions for each issue
- **Quality Score** — 0–10 rating with sub-scores for completeness, uniqueness, balance, and feature usefulness
- **Auto-Clean** — one-click dataset cleaning (dedup, impute, encode, scale)
- **Explainability** — "What's wrong" and "How we fixed it" sections in simple language
- **Visualizations** — missing value and class distribution bar charts

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 |
| Backend | Python FastAPI |
| Data Processing | pandas, NumPy, scikit-learn |

## Project Structure

```
ai-dataset-optimizer/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── routes.py            # API endpoints
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic request/response models
│   │   └── services/
│   │       ├── analyzer.py      # Column stats, previews, duplicates
│   │       ├── detector.py      # Issue detection engine
│   │       ├── scorer.py        # Quality scoring (0-10)
│   │       └── cleaner.py       # Auto-clean transformations
│   ├── uploads/                 # Uploaded/cleaned CSV files
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js               # Main app with state management
│   │   ├── App.css              # All styles
│   │   ├── api/
│   │   │   └── client.js        # Axios API client
│   │   └── components/
│   │       ├── Upload.js        # Drag-and-drop file upload
│   │       ├── DataPreview.js   # First 10 rows table
│   │       ├── CleanSection.js  # Target selector + Fix button
│   │       ├── QualityScore.js  # Score ring + sub-score bars
│   │       ├── Issues.js        # Flagged issues list
│   │       ├── Recommendations.js
│   │       ├── Visualizations.js
│   │       └── ColumnStatsTable.js
│   └── package.json
└── README.md
```

## Setup & Run

### Prerequisites

- Python 3.9+
- Node.js 16+

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API will be running at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the interactive Swagger UI.

### 2. Frontend

```bash
cd frontend
npm install
npm start
```

The app will open at `http://localhost:3000`.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/upload` | Upload a CSV file |
| POST | `/api/analyze` | Run quality analysis |
| POST | `/api/clean` | Auto-clean and get download ID |
| GET | `/api/download/{file_id}` | Download a cleaned CSV |

## How It Works

1. **Upload** a CSV — the backend saves it and returns a preview
2. **Choose a target column** (optional) to enable class imbalance detection
3. **Analyze** — the backend computes stats, detects issues, scores quality, and generates recommendations
4. **Fix My Dataset** — the backend applies cleaning rules and returns a download link
5. **Download** the cleaned CSV, ready for model training
