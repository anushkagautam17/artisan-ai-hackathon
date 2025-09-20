import os
import re
import json
from .vision import analyze_image_bytes
from .origin import guess_origin
from .price_optimizer import estimate_price_range, format_price_range
from .llm_client import get_completion, extract_first_json

# ✅ Fix paths relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_PATH = os.path.join(BASE_DIR, "../../frontend/prompts/listing.txt")
RECO_PROMPT_PATH = os.path.join(BASE_DIR, "../../frontend/prompts/recommendations.txt")

def _sanitize_title(title: str, bullets):
    words = title.strip().split()
    if 6 <= len(words) <= 8:
        return title.strip()
    if len(words) > 8:
        return " ".join(words[:8])
    extra = []
    if bullets:
        for b in bullets:
            extra += b.split()
            if len(words) + len(extra) >= 6:
                break
    new_words = (words + extra)[:8]
    while len(new_words) < 6:
        new_words.append("Handmade")
    return " ".join(new_words)

def _ensure_bullets(bullets):
    if isinstance(bullets, list):
        if len(bullets) >= 4:
            return bullets[:4]
        else:
            padded = bullets + ["Handmade quality", "Traditional craft", "Locally sourced", "Carefully finished"]
            return padded[:4]
    if isinstance(bullets, str):
        parts = re.split(r'\.\s+|,\s+|\n', bullets)
        items = [p.strip() for p in parts if p.strip()]
        return _ensure_bullets(items)
    return ["Handmade quality", "Traditional craft", "Locally sourced", "Carefully finished"]

def _sanitize_price_string(price_str):
    m = re.search(r'₹\s*([0-9]+)\s*-\s*₹?\s*([0-9]+)', price_str or "")
    if m:
        low, high = int(m.group(1)), int(m.group(2))
    else:
        nums = re.findall(r'([0-9]+)', price_str or "")
        if len(nums) >= 2:
            low, high = int(nums[0]), int(nums[1])
        elif len(nums) == 1:
            v = int(nums[0])
            low, high = max(50, v - 50), min(5000, v + 50)
        else:
            low, high = 100, 300
    low = max(50, min(low, 5000))
    high = max(low, min(high, 5000))
    return f"₹{low} - ₹{high}"

def generate_listing(description: str, image_bytes: bytes, model: str = "gpt-3.5-turbo"):
    """
    Main pipeline:
    1) vision analysis
    2) guess origin
    3) call listing LLM prompt (prompts/listing.txt)
    4) sanitize and enrich JSON
    5) generate artisan recommendations (prompts/recommendations.txt)
    6) return enriched dict for frontend
    """
    # 1) vision analysis
    vision = analyze_image_bytes(image_bytes) if image_bytes else {
        "caption": "",
        "keywords": [],
        "dominant_color": "RGB(0,0,0)",
        "size_category": "medium",
        "width": 0,
        "height": 0
    }

    # 2) guess origin
    origin_hint, matched_keyword = guess_origin(
        vision.get("caption",""), description or "", vision.get("keywords",[])
    )

    # 3) prepare listing prompt
    if os.path.exists(PROMPT_PATH):
        template = open(PROMPT_PATH, "r", encoding="utf-8").read()
    else:
        raise FileNotFoundError(f"{PROMPT_PATH} not found. Make sure the file exists.")

    vision_keywords_join = ", ".join(vision.get("keywords", []))
    prompt = template.format(
        description=description.replace("\n"," "),
        vision_caption=vision.get("caption",""),
        dominant_color=vision.get("dominant_color",""),
        size_category=vision.get("size_category",""),
        vision_keywords=vision_keywords_join
    )

    # call model
    raw = get_completion(prompt, model=model, max_tokens=400)
    parsed, raw_json_text = extract_first_json(raw)
    if parsed is None:
        prompt2 = prompt + "\n\nIMPORTANT: Return ONLY a single valid JSON object matching the requested OUTPUT FORMAT. No commentary."
        raw = get_completion(prompt2, model=model, max_tokens=400)
        parsed, raw_json_text = ex
