import React from "react";

function ScoreRing({ score, maxScore }) {
  const pct = (score / maxScore) * 100;
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (pct / 100) * circumference;

  let color = "#10b981";
  if (pct < 50) color = "#ef4444";
  else if (pct < 75) color = "#f59e0b";

  return (
    <div className="score-ring">
      <svg width="140" height="140" viewBox="0 0 120 120">
        <circle cx="60" cy="60" r={radius} fill="none" stroke="#e5e7eb" strokeWidth="10" />
        <circle
          cx="60" cy="60" r={radius} fill="none"
          stroke={color} strokeWidth="10" strokeLinecap="round"
          strokeDasharray={circumference} strokeDashoffset={offset}
          transform="rotate(-90 60 60)"
        />
      </svg>
      <div className="score-value">
        <span className="score-number">{score}</span>
        <span className="score-max">/ {maxScore}</span>
      </div>
    </div>
  );
}

export default function QualityScore({ qualityScore }) {
  if (!qualityScore) return null;

  return (
    <div className="card score-card">
      <h2>Dataset Quality Score</h2>
      <div className="score-layout">
        <ScoreRing score={qualityScore.total} maxScore={qualityScore.max_total} />
        <div className="sub-scores">
          {qualityScore.sub_scores.map((sub) => {
            const pct = (sub.score / sub.max_score) * 100;
            return (
              <div key={sub.name} className="sub-score-row">
                <div className="sub-score-header">
                  <span className="sub-score-name">{sub.name}</span>
                  <span className="sub-score-val">
                    {sub.score} / {sub.max_score}
                  </span>
                </div>
                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{
                      width: `${pct}%`,
                      background:
                        pct < 50 ? "#ef4444" : pct < 75 ? "#f59e0b" : "#10b981",
                    }}
                  />
                </div>
                <p className="sub-score-desc">{sub.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
