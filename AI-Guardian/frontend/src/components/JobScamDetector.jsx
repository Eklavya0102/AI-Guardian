import React, { useState } from 'react'
import ResultCard from './ResultCard.jsx'

export default function JobScamDetector() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  async function analyze() {
    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/detect-job-scam', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      })
      const data = await res.json()
      setResult(data)
    } catch {
      setResult({ risk_score: 0, risk_level: 'Safe', reasons: ['Unable to analyze'], recommendation: 'Try again.' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="card">
      <h2>Job Scam Detector</h2>
      <textarea
        placeholder="Paste a job description..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={6}
      />
      <button onClick={analyze} disabled={loading}>{loading ? 'Analyzing...' : 'Analyze Job'}</button>
      {result && <ResultCard title="Job Scam Analysis" result={result} />}
    </section>
  )
}
