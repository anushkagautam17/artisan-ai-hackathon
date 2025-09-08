import base64
import json
import os
from typing import Dict, Any, List, Optional

from pydantic import BaseModel, ValidationError, Field

# ---------- Simulation Mode (for testing without Google credentials) ----------
SIMULATION_MODE = True  # Set to False when you have real Google credentials

# ---------- Pydantic schema for safe parsing ----------
import json
import os
from typing import Dict, Any, List, Optional

from pydantic import BaseModel, ValidationError, Field

# Load env early
from dotenv import load_dotenv
load_dotenv()

SIMULATION_MODE = True  # Set to False when you have real Google credentials

# ---------- Pydantic schema for safe parsing ----------
class Listing(BaseModel):
    title: str
    bullets: List[str] = Field(min_items=1)
    price: str

def validate_and_clamp_price(price_str: str) -> str:
    """
    Validates the price string from the AI.
    If the price is outside the expected range (â‚¹50 - â‚¹5000),
    it clamps it to the nearest boundary and adds a note.
    """
    # Default range bounds
    min_price = 50
    max_price = 5000
    
    try:
        # Extract numbers from strings like "â‚¹350 - â‚¹600" or "â‚¹1000"
        import re
        numbers = re.findall(r'â‚¹(\d+)', price_str)
        if numbers:
            # Take the first number (lower bound) for checking
            first_price = int(numbers[0])
            
            # Check if the price is outside our desired range
            if first_price < min_price:
                return f"â‚¹{min_price} - â‚¹{max_price} (Price adjusted to minimum)"
            elif first_price > max_price:
                return f"â‚¹{min_price} - â‚¹{max_price} (Price adjusted to maximum)"
            
        # If it's within range or we can't parse it, return the original
        return price_str
        
    except (ValueError, IndexError):
        # If anything goes wrong in parsing, return a default safe price
        return f"â‚¹{min_price} - â‚¹{max_price} (Default price)"
    
# ---------- Prompt loading ----------
PROMPT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "prompts")
LISTING_PROMPT_PATH = os.path.join(PROMPT_DIR, "listing.txt")

def read_prompt_template(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

# ---------- Vertex (Gemini) ----------
USE_VERTEX = True  # flip to False to avoid Vertex and use OpenAI fallback

def _vertex_generate(image_bytes: bytes, description: str) -> str:
    """
    Calls Gemini (Vertex AI) with image + text and asks for JSON-only output.
    Returns raw text (expected to be JSON string).
    """
    # Lazy-import so app starts even if libs missing
    from vertexai import init as vertex_init
    from vertexai.generative_models import GenerativeModel, Part, GenerationConfig

    project = os.getenv("VERTEX_PROJECT_ID")
    location = os.getenv("VERTEX_LOCATION", "us-central1")
    if not project:
        raise RuntimeError("VERTEX_PROJECT_ID missing in .env")

    vertex_init(project=project, location=location)

    system_prompt = read_prompt_template(LISTING_PROMPT_PATH)

    image_part = Part.from_data(mime_type="image/jpeg", data=image_bytes)

    user_prompt = f"""
DESCRIPTION (user wrote):
{description}

Follow the RULES strictly and return ONLY JSON.
"""

    model = GenerativeModel("gemini-1.5-flash")  # fast + multimodal
    cfg = GenerationConfig(
        temperature=0.2,
        # Ask model to return JSON only (works on current Vertex SDKs)
        response_mime_type="application/json",
    )

    resp = model.generate_content(
        [system_prompt, image_part, user_prompt],
        generation_config=cfg,
    )
    return resp.text  # should be JSON string

# ---------- OpenAI fallback ----------
def _openai_generate(image_bytes: bytes, description: str) -> str:
    """
    Uses OpenAI (gpt-4o-mini) for image+text â†’ JSON-only output.
    """
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY missing in .env")

    b64 = base64.b64encode(image_bytes).decode("utf-8")
    system_prompt = read_prompt_template(LISTING_PROMPT_PATH)

    # Using chat.completions for wide compatibility
    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"DESCRIPTION (user wrote):\n{description}\n\nReturn ONLY JSON."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}  # works for png too
                ],
            },
        ],
        temperature=0.2,
    )
    return completion.choices[0].message["content"]

# ---------- Public function ----------
def generate_listing(image_bytes: bytes, description: str, target_lang: Optional[str] = None) -> Dict[str, Any]:
    if SIMULATION_MODE:
        # Return simulated data for testing
        print("DEBUG: Using simulation mode (no Google API calls)")
        return {
            "title": "Handwoven Bamboo Basket with Leather Handles",
            "bullets": [
                "Handcrafted from natural bamboo",
                "Durable leather handles for easy carrying",
                "Traditional artisan craftsmanship",
                "Perfect for storage or decorative use"
            ],
            "price": "₹450 - ₹800"
        }
    
    # ... rest of your original code for real API calls ...
    """
    1) Calls AI (Vertex or OpenAI) to get JSON
    2) Validates JSON to required shape
    3) Optionally translates title + bullets to target_lang (e.g., "hi")
    """
    raw = _vertex_generate(image_bytes, description) if USE_VERTEX else _openai_generate(image_bytes, description)

    # Sometimes models wrap JSON in code fences â€” strip gracefully
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        # remove leading language hint like json\n
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        # Last-resort: try to locate {...} inside text
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1:
            data = json.loads(cleaned[start:end+1])
        else:
            raise RuntimeError(f"AI did not return valid JSON. Raw:\n{raw}") from e

    # Validate with Pydantic
    try:
        listing = Listing(**data)
    except ValidationError as e:
        raise RuntimeError(f"AI JSON missing required fields or wrong types:\n{e}\nRaw:\n{data}")

    result = listing.dict()
    result["price"] = validate_and_clamp_price(result["price"])
    
    # Optional translation
    if target_lang and target_lang.lower() != "en":
        try:
            from .translate import translate_texts
            result["title"] = translate_texts([result["title"]], target_lang)[0]
            result["bullets"] = translate_texts(result["bullets"], target_lang)
            # price stays in INR, no translation
        except Exception as e:
            # Don't fail the whole request if translation breaks
            result["translation_error"] = str(e)

    return result

