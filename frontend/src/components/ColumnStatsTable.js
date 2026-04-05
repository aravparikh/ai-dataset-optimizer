import React, { useState } from "react";

export default function ColumnStatsTable({ columnStats }) {
  const [expanded, setExpanded] = useState(false);
  if (!columnStats || columnStats.length === 0) return null;

  const shown = expanded ? columnStats : columnStats.slice(0, 8);

  return (
    <div className="card">
      <h2>Column Statistics</h2>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Column</th>
              <th>Type</th>
              <th>Missing</th>
              <th>Unique</th>
              <th>Mean</th>
              <th>Std</th>
              <th>Min</th>
              <th>Max</th>
            </tr>
          </thead>
          <tbody>
            {shown.map((s) => (
              <tr key={s.name}>
                <td className="col-name">{s.name}</td>
                <td><span className="dtype">{s.dtype}</span></td>
                <td className={s.missing_pct > 5 ? "warn-val" : ""}>
                  {s.missing_count} ({s.missing_pct}%)
                </td>
                <td>{s.unique_count}</td>
                <td>{s.mean != null ? s.mean.toFixed(2) : "-"}</td>
                <td>{s.std != null ? s.std.toFixed(2) : "-"}</td>
                <td>{s.min_val != null ? s.min_val.toFixed(2) : "-"}</td>
                <td>{s.max_val != null ? s.max_val.toFixed(2) : "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {columnStats.length > 8 && (
        <button className="link-btn" onClick={() => setExpanded(!expanded)}>
          {expanded ? "Show less" : `Show all ${columnStats.length} columns`}
        </button>
      )}
    </div>
  );
}
