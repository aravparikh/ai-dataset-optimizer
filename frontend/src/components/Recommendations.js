import React from "react";

const ACTION_ICONS = {
  impute: "\u{1F9F9}",
  drop_column: "\u{1F5D1}",
  remove_duplicates: "\u{1F4CB}",
  review: "\u{1F50D}",
  handle_imbalance: "\u2696\uFE0F",
  encode_categoricals: "\u{1F504}",
  scale_numeric: "\u{1F4CF}",
};

export default function Recommendations({ recommendations }) {
  if (!recommendations || recommendations.length === 0) return null;

  return (
    <div className="card">
      <h2>Recommendations</h2>
      <div className="rec-list">
        {recommendations.map((rec, i) => (
          <div key={i} className="rec-item">
            <span className="rec-icon">
              {ACTION_ICONS[rec.action] || "\u{1F4A1}"}
            </span>
            <div>
              <p className="rec-desc">{rec.description}</p>
              {rec.column && (
                <span className="rec-col">Column: {rec.column}</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
