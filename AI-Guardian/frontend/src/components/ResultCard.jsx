import React from 'react'

export default function ResultCard({ title, result }) {
  const score = result?.risk_score ?? 0
  const level = result?.risk_level ?? 'Safe'
  const color = level === 'Safe' ? '#16a34a' : level === 'Warning' ? '#f59e0b' : '#ef4444'
  return (
    <div className="result-card" style={{ borderColor: color }}>
      <h3>{title}</h3>
      <div className="result-header" style={{ color }}>{`Risk Score: ${score}%`} </div>
      <div className="risk-level" style={{ color }}>{level}</div>
      {result?.reasons && (
        <ul>
          {result.reasons.map((r, idx) => (
            <li key={idx}>{r}</li>
          ))}
        </ul>
      )}
      {result?.recommendation && (
        <div className="recommendation"><strong>Recommendation:</strong> {result.recommendation}</div>
      )}
    </div>
  )
}
