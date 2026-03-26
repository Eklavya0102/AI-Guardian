import re
import os
from typing import List, Dict

# Optional: try to load a HF text classifier if possible
PHISHING_MODEL = os.environ.get("PHISHING_MODEL")
try:
    from transformers import pipeline

    if PHISHING_MODEL:
        _PHISHING_PIPELINE = pipeline(
            "text-classification", model=PHISHING_MODEL, device=-1
        )
    else:
        _PHISHING_PIPELINE = None  # type: ignore
except Exception:
    _PHISHING_PIPELINE = None  # type: ignore

URGENCY_KEYWORDS = [
    "urgent payment",
    "verify account",
    "verify your account",
    "click immediately",
    "bank password",
    "payment required now",
]

PHISHING_DOMAINS = {
    "phish.example",
    "secure-login.example",
}

DEF_MSG = "This message could be a phishing attempt. Review the content carefully."


def _extract_urls(text: str) -> List[str]:
    url_re = re.compile(r"https?://[^\s]+", re.IGNORECASE)
    return url_re.findall(text or "")


def analyze_email(text: str) -> Dict:
    if not isinstance(text, str):
        text = str(text)
    lower = text.lower()
    reasons: List[str] = []
    score = 0

    # Keyword-based signals
    for kw in URGENCY_KEYWORDS:
        if kw in lower:
            reasons.append(f"Keyword pattern: '{kw}'")
            score += 18

    # Domain checks in detected URLs
    urls = _extract_urls(text)
    domains = []
    for u in urls:
        try:
            from urllib.parse import urlparse

            domain = urlparse(u).netloc
            domains.append(domain)
            if any(phish in domain for phish in PHISHING_DOMAINS):
                reasons.append("Suspicious domain pattern detected")
                score += 14
        except Exception:
            pass

    # Simple grammar/style cues
    if re.search(r"\b(urgent|immediately|asap)\b", lower) and not urls:
        reasons.append("Urgency language detected without links")
        score += 6

    # Optional ML classifier (best-effort)
    if _PHISHING_PIPELINE:
        try:
            res = _PHISHING_PIPELINE(text[:512])[0]
            label = res.get("label") or res.get("label_id") or "LABEL_0"
            conf = float(res.get("score", 0.0))
            if isinstance(label, str) and label.upper().startswith("LABEL_1"):
                score += int(conf * 30)
                reasons.append("AI classifier flagged potential phishing")
        except Exception:
            pass

    # Normalize score
    if score < 0:
        score = 0
    if score > 100:
        score = 100

    level = "Safe"
    if score >= 70:
        level = "Dangerous"
    elif score >= 40:
        level = "Warning"

    recommendation = (
        (
            "Review suspicious signals and avoid sharing sensitive information. "
            "If in doubt, mark as spam and block the sender."
        )
        if score > 0
        else "No obvious phishing signals detected; stay vigilant."
    )

    return {
        "risk_score": int(score),
        "risk_level": level,
        "reasons": reasons if reasons else [DEF_MSG],
        "recommendation": recommendation,
    }
