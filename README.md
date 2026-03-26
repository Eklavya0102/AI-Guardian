# AI Guardian – Personal Digital Safety Assistant

Overview
- AI Guardian is an AI-powered cybersecurity assistant that analyzes emails, links, job descriptions, and deepfake images to detect scams and malicious content.

Project Structure (target layout)
- frontend/
- backend/
- README.md

Frontend
- public/index.html
- src/
  - components/EmailScanner.jsx
  - components/LinkScanner.jsx
  - components/JobScamDetector.jsx
  - components/DeepfakeDetector.jsx
  - components/ResultCard.jsx
  - components/Navbar.jsx
  - App.js
  - index.js
  - styles.css
- package.json

Backend
- main.py
- phishing_detector.py
- link_checker.py
- job_scam_detector.py
- deepfake_detector.py
- requirements.txt

How to run (local)
- Start backend: cd backend && uvicorn main:app --reload
- Start frontend: cd frontend && npm install && npm start

Notes
- This is a scaffold with heuristic detectors and optional HF integrations via environment variables.
- Replace placeholders with real models as needed.
