import re
from urllib.parse import urlparse
from typing import Dict, List

SHORTENERS = {"bit.ly", "t.co", "goo.gl", "tinyurl.com", "ow.ly", "buff.ly"}

SUSPICIOUS_TOKENS = ["verify", "password", "login", "bank", "credit"]


def _extract_domain(url: str) -> str:
    try:
        return urlparse(url).netloc
    except Exception:
        return url


def analyze_link(url: str) -> Dict:
    domain = _extract_domain(url or "")
    reasons: List[str] = []
    score = 0

    if not url:
        return {
            "risk_score": 0,
            "risk_level": "Safe",
            "reasons": ["No URL provided"],
            "recommendation": "Provide a URL to analyze.",
        }

    # Shortened URL detection
    if domain in SHORTENERS:
        reasons.append("URL appears to be shortened")
        score += 25

    # Suspicious keywords in the URL
    lower_url = url.lower()
    for tok in SUSPICIOUS_TOKENS:
        if tok in lower_url:
            reasons.append(f"Suspicious token in URL: {tok}")
            score += 10
            break

    # Heuristic for random-looking path components
    path = urlparse(url).path or ""
    if re.search(r"[a-z0-9]{14,}", path):
        reasons.append("Path contains long random-looking string")
        score += 12

    # Very recent domains (simple heuristic: if domain ends with a country code that is uncommon)
    # Placeholder for potential VirusTotal integration
    if score >= 70:
        level = "Dangerous"
    elif score >= 40:
        level = "Warning"
    else:
        level = "Safe"

    # Optional VirusTotal integration placeholder
    # Try to read API key from env; if not present, skip.
    import os

    VT_KEY = os.environ.get("VIRUSTOTAL_API_KEY")
    if VT_KEY:
        try:
            import httpx

            # This is a placeholder call; real integration requires URL encoding steps.
            # We won't perform an actual VT check here to keep the example self-contained.
            _ = httpx.get(
                "https://www.virustotal.com/api/v3/urls",
                headers={"x-apikey": VT_KEY},
                timeout=5,
            )
        except Exception:
            pass

    if score < 0:
        score = 0
    if score > 100:
        score = 100

    if score >= 70:
        recommendation = "Avoid clicking. Mark as dangerous."
    elif score >= 40:
        recommendation = "Exercise caution. Scan with security tools before proceeding."
    else:
        recommendation = "URL appears benign based on heuristics."

    return {
        "risk_score": int(score),
        "risk_level": level,
        "reasons": reasons or ["No obvious red flags detected."],
        "recommendation": recommendation,
    }
