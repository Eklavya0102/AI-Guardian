import React from 'react'

export default function Navbar() {
  return (
    <header className="navbar">
      <div className="brand">AI Guardian</div>
      <nav className="nav-links" aria-label="Main Navigation">
        <span>Dashboard</span>
        <span>Settings</span>
      </nav>
    </header>
  )
}
