import React, { useState, useCallback } from "react";

export default function Upload({ onUploadComplete, loading }) {
  const [dragOver, setDragOver] = useState(false);

  const handleFile = useCallback(
    (file) => {
      if (file && file.name.endsWith(".csv")) {
        onUploadComplete(file);
      } else {
        alert("Please upload a .csv file");
      }
    },
    [onUploadComplete]
  );

  const onDrop = useCallback(
    (e) => {
      e.preventDefault();
      setDragOver(false);
      const file = e.dataTransfer.files[0];
      handleFile(file);
    },
    [handleFile]
  );

  return (
    <div
      className={`upload-zone ${dragOver ? "drag-over" : ""}`}
      onDragOver={(e) => {
        e.preventDefault();
        setDragOver(true);
      }}
      onDragLeave={() => setDragOver(false)}
      onDrop={onDrop}
    >
      <div className="upload-icon">
        <svg width="48" height="48" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
        </svg>
      </div>
      <p className="upload-title">
        {loading ? "Uploading..." : "Drag & drop your CSV file here"}
      </p>
      <p className="upload-subtitle">or</p>
      <label className="upload-btn">
        Browse Files
        <input
          type="file"
          accept=".csv"
          hidden
          disabled={loading}
          onChange={(e) => handleFile(e.target.files[0])}
        />
      </label>
    </div>
  );
}
