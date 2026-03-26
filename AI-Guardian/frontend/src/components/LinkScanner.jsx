import React, { useState } from 'react'
import ResultCard from './ResultCard.jsx'

export default function LinkScanner() {
  const [url, setUrl] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  async function analyze() {
    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/scan-link', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
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
      <h2>Malicious Link Scanner</h2>
      <input
        type="text"
        placeholder="https://example.com"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <button onClick={analyze} disabled={loading}>{loading ? 'Scanning...' : 'Analyze Link'}</button>
      {result && <ResultCard title="Link Analysis" result={result} />}
    </section>
  )
}
