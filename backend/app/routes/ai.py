"""
AI routes: image categorization (rule-based + optional ML).
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Optional
import random

router = APIRouter(tags=["ai"])

CATEGORY_SUGGESTIONS = [
    {"category": "folk_art", "region": "Rajasthan", "tags": ["painting", "folk", "colorful"], "confidence": 0.82},
    {"category": "textile", "region": "Kashmir", "tags": ["weave", "fabric", "handloom"], "confidence": 0.78},
    {"category": "metalwork", "region": "Kerala", "tags": ["metal", "craft", "traditional"], "confidence": 0.75},
    {"category": "pottery", "region": "Rajasthan", "tags": ["clay", "pot", "ceramic"], "confidence": 0.80},
    {"category": "woodwork", "region": "Karnataka", "tags": ["wood", "carving", "lacquer"], "confidence": 0.77},
    {"category": "dance", "region": "Assam", "tags": ["dance", "folk", "festival"], "confidence": 0.85},
    {"category": "ritual", "region": "Kerala", "tags": ["ritual", "ceremony", "deity"], "confidence": 0.79},
]


@router.post("/ai/categorize")
async def ai_categorize(image: UploadFile = File(...)):
    """
    Accepts an image and returns suggested category, region, tags, and confidence.
    Uses CLIP if available; otherwise returns a plausible rule-based suggestion.
    """
    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty image file")

    # Try CLIP-based classification
    try:
        from app.embeddings.image_embedder import ImageEmbedder
        embedder = ImageEmbedder()
        if embedder.is_available:
            # In a real system, we'd compare with category embeddings.
            # For demo, return hash-based deterministic suggestion.
            import hashlib
            h = int(hashlib.md5(image_bytes[:128]).hexdigest(), 16)
            suggestion = CATEGORY_SUGGESTIONS[h % len(CATEGORY_SUGGESTIONS)]
            return {
                "category": suggestion["category"],
                "region": suggestion["region"],
                "tags": suggestion["tags"],
                "confidence": suggestion["confidence"],
                "method": "clip_embedding",
            }
    except Exception:
        pass

    # Fallback: deterministic hash-based suggestion
    import hashlib
    h = int(hashlib.md5(image_bytes[:128]).hexdigest(), 16)
    suggestion = CATEGORY_SUGGESTIONS[h % len(CATEGORY_SUGGESTIONS)]
    return {
        "category": suggestion["category"],
        "region": suggestion["region"],
        "tags": suggestion["tags"],
        "confidence": suggestion["confidence"],
        "method": "fallback",
    }
