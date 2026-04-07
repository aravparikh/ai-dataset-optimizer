import React, { useState, useCallback } from "react";
import Upload from "./components/Upload";
import DataPreview from "./components/DataPreview";
import CleanSection from "./components/CleanSection";
import QualityScore from "./components/QualityScore";
import ColumnStatsTable from "./components/ColumnStatsTable";
import Issues from "./components/Issues";
import Recommendations from "./components/Recommendations";
import Visualizations from "./components/Visualizations";
import { uploadFile, analyzeFile, cleanFile } from "./api/client";
import "./App.css";

export default function App() {
  const [uploadData, setUploadData] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [cleanResult, setCleanResult] = useState(null);
  const [targetColumn, setTargetColumn] = useState("");
  const [scaleNumeric, setScaleNumeric] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [cleaning, setCleaning] = useState(false);
  const [error, setError] = useState(null);

  const handleUpload = useCallback(async (file) => {
    setUploading(true);
    setError(null);
    setAnalysis(null);
    setCleanResult(null);
    setTargetColumn("");
    try {
      const data = await uploadFile(file);
      setUploadData(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Upload failed");
    } finally {
      setUploading(false);
    }
  }, []);

  const handleAnalyze = useCallback(async () => {
    if (!uploadData) return;
    setAnalyzing(true);
    setError(null);
    setCleanResult(null);
    try {
      const data = await analyzeFile(uploadData.file_id, targetColumn);
      setAnalysis(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Analysis failed");
    } finally {
      setAnalyzing(false);
    }
  }, [uploadData, targetColumn]);

  const handleClean = useCallback(async () => {
    if (!uploadData) return;
    setCleaning(true);
    setError(null);
    try {
      const data = await cleanFile(uploadData.file_id, targetColumn, scaleNumeric);
      setCleanResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Cleaning failed");
    } finally {
      setCleaning(false);
    }
  }, [uploadData, targetColumn, scaleNumeric]);

  const handleReset = () => {
    setUploadData(null);
    setAnalysis(null);
    setCleanResult(null);
    setTargetColumn("");
    setScaleNumeric(false);
    setError(null);
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <div className="logo">
            <svg width="28" height="28" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 0v3.75c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125v-3.75" />
            </svg>
            <h1>AI Dataset Optimizer</h1>
          </div>
          {uploadData && (
            <button className="btn btn-ghost" onClick={handleReset}>
              New Upload
            </button>
          )}
        </div>
      </header>

      <main className="main">
        {error && (
          <div className="error-banner">
            <p>{error}</p>
            <button onClick={() => setError(null)}>&times;</button>
          </div>
        )}

        {!uploadData && <Upload onUploadComplete={handleUpload} loading={uploading} />}

        {uploadData && (
          <>
            <DataPreview uploadData={uploadData} />

            <CleanSection
              columns={uploadData.columns}
              targetColumn={targetColumn}
              setTargetColumn={setTargetColumn}
              scaleNumeric={scaleNumeric}
              setScaleNumeric={setScaleNumeric}
              onAnalyze={handleAnalyze}
              onClean={handleClean}
              cleanResult={cleanResult}
              analyzing={analyzing}
              cleaning={cleaning}
            />

            {analysis && (
              <>
                <QualityScore qualityScore={analysis.quality_score} />

                <div className="two-col">
                  <Issues issues={analysis.issues} />
                  <Recommendations recommendations={analysis.recommendations} />
                </div>

                <Visualizations
                  columnStats={analysis.column_stats}
                  classDistribution={analysis.class_distribution}
                />

                <ColumnStatsTable columnStats={analysis.column_stats} />
              </>
            )}
          </>
        )}
      </main>

      <footer className="footer">
        <p>AI Dataset Optimizer &mdash; Clean your data, train better models.</p>
      </footer>
    </div>
  );
}
