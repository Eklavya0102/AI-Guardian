import React from 'react'
import EmailScanner from './components/EmailScanner.jsx'
import LinkScanner from './components/LinkScanner.jsx'
import JobScamDetector from './components/JobScamDetector.jsx'
import DeepfakeDetector from './components/DeepfakeDetector.jsx'
import Navbar from './components/Navbar.jsx'
import LogsPanel from './components/LogsPanel.jsx'

export default function App() {
  return (
    <div className="app-container">
      <Navbar />
      <main className="grid">
        <EmailScanner />
        <LinkScanner />
        <JobScamDetector />
        <DeepfakeDetector />
        <LogsPanel />
      </main>
    </div>
  )
}
