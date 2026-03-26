import React, { useState } from 'react'
import ResultCard from './ResultCard.jsx'

export default function EmailScanner() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  async function analyze() {
    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/analyze-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      })
      const data = await res.json()
      setResult(data)
    } catch (e) {
      setResult({ risk_score: 0, risk_level: 'Safe', reasons: ['Unable to analyze'], recommendation: 'Try again.' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="card">
      <h2>Email Scanner</h2>
      <textarea
        placeholder="Paste an email message here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={6}
      />
      <button onClick={analyze} disabled={loading}>{loading ? 'Analyzing...' : 'Analyze Email'}</button>
      {result && <ResultCard title="Email Analysis" result={result} />}
    </section>
  )
}
