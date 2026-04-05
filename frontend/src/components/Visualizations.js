import React from "react";

function BarChart({ data, title, color }) {
  if (!data || data.length === 0) return null;
  const maxVal = Math.max(...data.map((d) => d.value));

  return (
    <div className="viz-chart">
      <h3>{title}</h3>
      <div className="bar-chart">
        {data.map((d, i) => (
          <div key={i} className="bar-row">
            <span className="bar-label" title={d.label}>
              {d.label.length > 16 ? d.label.slice(0, 16) + "..." : d.label}
            </span>
            <div className="bar-track">
              <div
                className="bar-fill"
                style={{
                  width: `${maxVal > 0 ? (d.value / maxVal) * 100 : 0}%`,
                  background: color,
                }}
              />
            </div>
            <span className="bar-value">{d.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function Visualizations({ columnStats, classDistribution }) {
  // Missing values chart
  const missingData = (columnStats || [])
    .filter((s) => s.missing_count > 0)
    .sort((a, b) => b.missing_pct - a.missing_pct)
    .slice(0, 15)
    .map((s) => ({ label: s.name, value: s.missing_pct }));

  // Class distribution chart
  const classData = classDistribution
    ? Object.entries(classDistribution).map(([k, v]) => ({ label: k, value: v }))
    : [];

  if (missingData.length === 0 && classData.length === 0) return null;

  return (
    <div className="card">
      <h2>Visualizations</h2>
      <div className="viz-grid">
        {missingData.length > 0 && (
          <BarChart
            data={missingData}
            title="Missing Values (%)"
            color="#f59e0b"
          />
        )}
        {classData.length > 0 && (
          <BarChart
            data={classData}
            title="Class Distribution"
            color="#6366f1"
          />
        )}
      </div>
    </div>
  );
}
