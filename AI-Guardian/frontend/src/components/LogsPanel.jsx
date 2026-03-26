import React, { useEffect, useState } from 'react'

export default function LogsPanel() {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('http://localhost:8000/logs')
      .then((r) => r.json())
      .then((data) => {
        setLogs(data.logs || [])
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  return (
    <section className="card">
      <h2>Logs</h2>
      {loading ? (
        <div>Loading...</div>
      ) : (
        <div style={{ maxHeight: 240, overflow: 'auto' }}>
          <ul>
            {logs.slice(-20).reverse().map((l, i) => (
              <li key={i} style={{ fontFamily: 'monospace' }}>
                [{l?.timestamp}] {l?.event} - {JSON.stringify(l?.details)}
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  )
}
