import React from "react";

const SEVERITY_COLORS = {
  high: { bg: "#fef2f2", border: "#fca5a5", text: "#991b1b" },
  medium: { bg: "#fffbeb", border: "#fcd34d", text: "#92400e" },
  low: { bg: "#f0fdf4", border: "#86efac", text: "#166534" },
};

export default function Issues({ issues }) {
  if (!issues || issues.length === 0) return null;

  return (
    <div className="card">
      <h2>
        What's Wrong With Your Dataset
        <span className="issue-count">{issues.length} issues</span>
      </h2>
      <div className="issues-list">
        {issues.map((issue, i) => {
          const colors = SEVERITY_COLORS[issue.severity] || SEVERITY_COLORS.low;
          return (
            <div
              key={i}
              className="issue-item"
              style={{ background: colors.bg, borderLeft: `4px solid ${colors.border}` }}
            >
              <span
                className="severity-badge"
                style={{ background: colors.border, color: colors.text }}
              >
                {issue.severity}
              </span>
              <p>{issue.description}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
