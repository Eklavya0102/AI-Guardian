import re
from typing import List, Dict

KEYWORDS = {
    "pay registration fee",
    "earn $",
    "work from home",
    "guaranteed income",
    "send money",
}


def analyze_job_scam(text: str) -> Dict:
    if not isinstance(text, str):
        text = str(text)
    lower = text.lower()
    reasons: List[str] = []
    score = 0

    for kw in KEYWORDS:
        if kw in lower:
            reasons.append(f"Job signal: '{kw}'")
            score += 20

    # Simple checks for non-corporate emails and upfront payments
    if (
        re.search(r"@gmail|@yahoo|@hotmail", lower)
        or "gmail.com" in lower
        or "yahoo.com" in lower
    ):
        reasons.append("Use of free email domains detected")
        score += 15

    if re.search(r"pay|fee|payment|deposit|bank", lower):
        reasons.append("Payment/requesting upfront payments detected")
        score += 12

    # Remove false positives
    if score < 0:
        score = 0
    if score > 100:
        score = 100

    level = "Safe"
    if score >= 70:
        level = "Dangerous"
    elif score >= 40:
        level = "Warning"

    if score >= 60:
        recommendation = "Do not proceed with this offer. Conduct further verification with the company contact channel."
    elif score >= 30:
        recommendation = "Exercise caution. Research the company and verify legitimacy before responding."
    else:
        recommendation = (
            "No strong scam signals detected. Maintain normal due diligence."
        )

    return {
        "risk_score": int(score),
        "risk_level": level,
        "reasons": reasons or ["No obvious scam indicators detected."],
        "recommendation": recommendation,
    }
