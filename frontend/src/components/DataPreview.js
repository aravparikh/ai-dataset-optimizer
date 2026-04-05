import React from "react";

export default function DataPreview({ uploadData }) {
  if (!uploadData) return null;
  const { filename, shape, columns, dtypes, preview } = uploadData;

  return (
    <div className="card">
      <h2>Dataset Preview</h2>
      <div className="meta-row">
        <span className="badge">{filename}</span>
        <span className="badge">{shape[0].toLocaleString()} rows</span>
        <span className="badge">{shape[1]} columns</span>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col}>
                  {col}
                  <span className="dtype">{dtypes[col]}</span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {preview.map((row, i) => (
              <tr key={i}>
                {columns.map((col) => (
                  <td key={col} className={row[col] === null ? "null-val" : ""}>
                    {row[col] === null ? "NaN" : String(row[col])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
