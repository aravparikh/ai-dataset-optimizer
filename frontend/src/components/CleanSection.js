import React from "react";
import { downloadUrl } from "../api/client";

export default function CleanSection({
  columns,
  targetColumn,
  setTargetColumn,
  scaleNumeric,
  setScaleNumeric,
  onAnalyze,
  onClean,
  cleanResult,
  analyzing,
  cleaning,
}) {
  return (
    <div className="card clean-card">
      <h2>Configure & Clean</h2>

      <div className="control-row">
        <div className="control-group">
          <label htmlFor="target-select">Target column (optional)</label>
          <select
            id="target-select"
            value={targetColumn}
            onChange={(e) => setTargetColumn(e.target.value)}
          >
            <option value="">-- None --</option>
            {columns.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>

        <div className="control-group">
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={scaleNumeric}
              onChange={(e) => setScaleNumeric(e.target.checked)}
            />
            Scale numeric features (StandardScaler)
          </label>
        </div>
      </div>

      <div className="btn-row">
        <button className="btn btn-secondary" onClick={onAnalyze} disabled={analyzing}>
          {analyzing ? "Analyzing..." : "Analyze Dataset"}
        </button>
        <button className="btn btn-primary" onClick={onClean} disabled={cleaning}>
          {cleaning ? "Cleaning..." : "Fix My Dataset"}
        </button>
      </div>

      {cleanResult && (
        <div className="clean-result">
          <div className="clean-summary">
            <div className="shape-compare">
              <div>
                <span className="label">Original</span>
                <span className="value">
                  {cleanResult.original_shape[0]} x {cleanResult.original_shape[1]}
                </span>
              </div>
              <span className="arrow">&rarr;</span>
              <div>
                <span className="label">Cleaned</span>
                <span className="value">
                  {cleanResult.cleaned_shape[0]} x {cleanResult.cleaned_shape[1]}
                </span>
              </div>
            </div>
          </div>

          <div className="explanation-section">
            <div className="explanation-block">
              <h3>What's wrong with your dataset</h3>
              <div className="explanation-text">
                {cleanResult.whats_wrong.split("\n").map((line, i) => (
                  <p key={i}>{line}</p>
                ))}
              </div>
            </div>

            <div className="explanation-block">
              <h3>How we fixed it</h3>
              <div className="explanation-text">
                {cleanResult.how_we_fixed.split("\n").map((line, i) => (
                  <p key={i}>{line}</p>
                ))}
              </div>
            </div>
          </div>

          <a
            href={downloadUrl(cleanResult.cleaned_file_id)}
            className="btn btn-download"
            download
          >
            Download Cleaned CSV
          </a>
        </div>
      )}
    </div>
  );
}
