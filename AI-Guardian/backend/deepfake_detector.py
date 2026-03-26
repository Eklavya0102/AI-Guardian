import hashlib
from typing import Dict


def analyze_image(image_bytes: bytes) -> Dict:
    # Lightweight placeholder: derive a deterministic probability from image bytes.
    # This is not a real deepfake detector; replace with a model in production.
    if not image_bytes:
        return {
            "manipulation_probability": 0.0,
            "explanation": "No image data provided.",
        }

    h = hashlib.sha256(image_bytes).digest()
    # Use first two bytes to create a pseudo-random but deterministic value in [0, 0.4)
    val = (h[0] << 8 | h[1]) % 1000
    probability = (val / 1000.0) * 0.4  # scale to 0.0 - 0.4
    # Simple heuristic: higher image size slightly nudges probability upward
    if len(image_bytes) > 500 * 1024:
        probability += 0.05
    probability = max(0.0, min(1.0, probability))

    explanation = (
        "Placeholder deepfake detector: probability derived from image bytes. "
        "Replace with a real model for production use."
    )
    return {
        "manipulation_probability": round(probability, 4),
        "explanation": explanation,
    }
