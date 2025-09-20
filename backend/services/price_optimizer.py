# backend/services/price_optimizer.py
import re

def _material_baseline(text: str):
    t = (text or "").lower()
    if "silk" in t or "pashmina" in t:
        return 700
    if "metal" in t or "brass" in t or "bronze" in t:
        return 400
    if "wood" in t or "rosewood" in t:
        return 350
    if "ceramic" in t or "pottery" in t or "clay" in t:
        return 300
    if "cotton" in t or "handloom" in t:
        return 250
    return 200

def estimate_price_range(description: str, vision_caption: str, size_category: str, keywords: list):
    """
    Returns (low, high) ints representing INR estimate, then caller can format as "₹X - ₹Y"
    Heuristics-based baseline + multipliers.
    """
    base = _material_baseline(" ".join([description or "", vision_caption or ""]))
    # complexity: look for words suggesting intricacy
    complexity = 1.0
    txt = (description or "") + " " + (vision_caption or "")
    if any(w in txt.lower() for w in ["intricate", "detailed", "hand-carved", "finely"]):
        complexity = 1.5
    # size multiplier
    size_mult = {"small": 0.8, "medium": 1.0, "large": 1.3}.get(size_category, 1.0)
    # keywords add small premium
    kw_premium = 1.0 + 0.05 * min(len(keywords or []), 6)
    low = int(base * size_mult * complexity * 0.8 * kw_premium)
    high = int(base * size_mult * complexity * 1.6 * kw_premium)
    # clamp to allowed range
    low = max(50, min(low, 5000))
    high = max(low, min(high, 5000))
    return low, high

def format_price_range(low: int, high: int):
    return f"₹{low} - ₹{high}"
