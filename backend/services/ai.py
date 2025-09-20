import base64
import json
import os
import re
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

from pydantic import BaseModel, ValidationError, Field

# Load environment variables
load_dotenv()

# ---------- Simulation Mode (for testing without Google credentials) ----------
SIMULATION_MODE = os.getenv("OPENAI_API_KEY") is None  # Auto-detect based on API key

# ---------- Pydantic schema for safe parsing ----------
class Listing(BaseModel):
    title: str
    bullets: List[str] = Field(min_items=1)
    price: str

def validate_and_clamp_price(price_str: str) -> str:
    """
    Validates the price string from the AI.
    If the price is outside the expected range (₹50 - ₹5000),
    it clamps it to the nearest boundary and adds a note.
    """
    # Default range bounds
    min_price = 50
    max_price = 5000
    
    try:
        # Extract numbers from strings like "₹350 - ₹600" or "₹1000"
        numbers = re.findall(r'₹(\d+)', price_str)
        if numbers:
            # Take the first number (lower bound) for checking
            first_price = int(numbers[0])
            
            # Check if the price is outside our desired range
            if first_price < min_price:
                return f"₹{min_price} - ₹{max_price} (Price adjusted to minimum)"
            elif first_price > max_price:
                return f"₹{min_price} - ₹{max_price} (Price adjusted to maximum)"
            
        # If it's within range or we can't parse it, return the original
        return price_str
        
    except (ValueError, IndexError):
        # If anything goes wrong in parsing, return a default safe price
        return f"₹{min_price} - ₹{max_price} (Default price)"
    
# ---------- Prompt loading ----------
PROMPT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "prompts")
LISTING_PROMPT_PATH = os.path.join(PROMPT_DIR, "listing.txt")

def read_prompt_template(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        # Fallback prompt if file doesn't exist
        return """You are an expert at creating product listings for handmade artisan products. 
        Analyze the product image and description, then return a JSON object with:
        - title: engaging product title
        - bullets: array of 3-5 key features/bullet points
        - price: estimated price range in Indian Rupees (format: "₹X - ₹Y")
        
        Return ONLY valid JSON, no other text."""

# ---------- Vertex (Gemini) ----------
USE_VERTEX = False  # Default to OpenAI for now

def _vertex_generate(image_bytes: bytes, description: str) -> str:
    """
    Calls Gemini (Vertex AI) with image + text and asks for JSON-only output.
    Returns raw text (expected to be JSON string).
    """
    # Lazy-import so app starts even if libs missing
    try:
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
    except ImportError:
        print("Vertex AI not available, falling back to OpenAI")
        return _openai_generate(image_bytes, description)

# ---------- OpenAI (NEW API >=1.0.0) ----------
def _openai_generate(image_bytes: bytes, description: str) -> str:
    """
    Uses OpenAI (gpt-4o) for image+text → JSON-only output with new API.
    """
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        if not client.api_key:
            raise RuntimeError("OPENAI_API_KEY missing in .env")

        # Encode image to base64
        b64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        system_prompt = read_prompt_template(LISTING_PROMPT_PATH)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user", 
                    "content": [
                        {"type": "text", "text": f"DESCRIPTION (user wrote):\n{description}\n\nReturn ONLY JSON."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{b64_image}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            temperature=0.2,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        
        return response.choices[0].message.content
        
    except ImportError:
        raise RuntimeError("OpenAI library not installed. Run: pip install openai>=1.0.0")
    except Exception as e:
        raise RuntimeError(f"OpenAI API error: {str(e)}")

# ---------- Public function ----------
def generate_listing(image_bytes: bytes, description: str, target_lang: Optional[str] = None) -> Dict[str, Any]:
    if SIMULATION_MODE:
        # Return simulated data for testing
        print("DEBUG: Using simulation mode (no API calls)")
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
    
    try:
        # Choose which AI service to use
        if USE_VERTEX:
            raw = _vertex_generate(image_bytes, description)
        else:
            raw = _openai_generate(image_bytes, description)

        # Clean and parse the JSON response
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:].strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            # Try to extract JSON from text
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
        
        # Optional translation (if translation service exists)
        if target_lang and target_lang.lower() != "en":
            try:
                from .translate import translate_texts
                result["title"] = translate_texts([result["title"]], target_lang)[0]
                result["bullets"] = translate_texts(result["bullets"], target_lang)
            except ImportError:
                print("Translation module not available")
            except Exception as e:
                result["translation_error"] = str(e)

        return result
        
    except Exception as e:
        # Fallback to simulation mode on any error
        print(f"Error in AI generation: {str(e)}. Falling back to simulation mode.")
        return {
            "title": "Handcrafted Artisan Product",
            "bullets": [
                "Beautiful handmade craftsmanship",
                "Traditional techniques",
                "High quality materials",
                "Unique and authentic design"
            ],
            "price": "₹300 - ₹600",
            "error": str(e)
        }