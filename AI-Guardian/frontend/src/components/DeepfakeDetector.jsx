import React, { useState } from 'react'
import ResultCard from './ResultCard.jsx'

export default function DeepfakeDetector() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  async function analyze(e) {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    const form = new FormData()
    form.append('file', file)
    try {
      const res = await fetch('http://localhost:8000/detect-deepfake', {
        method: 'POST',
        body: form,
      })
      const data = await res.json()
      setResult(data)
    } catch {
      setResult({ manipulation_probability: 0.0, explanation: 'Unable to analyze' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="card">
      <h2>Deepfake Detector</h2>
      <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      <button onClick={analyze} disabled={loading}>{loading ? 'Analyzing...' : 'Analyze Image'}</button>
      {result && <ResultCard title="Deepfake Analysis" result={result} />}
    </section>
  )
}
