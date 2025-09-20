# backend/services/vision.py
import base64
import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_image_bytes(image_bytes: bytes) -> dict:
    """
    Analyze image using OpenAI's GPT-4 Vision with new API
    """
    try:
        # Encode image to base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        prompt = """Analyze this product image in detail and return ONLY JSON with this exact structure:
        {
            "caption": "detailed description of the product",
            "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
            "dominant_color": "RGB(r,g,b)",
            "size_category": "small/medium/large",
            "width": 300,
            "height": 400
        }
        
        Be very detailed in the caption. Describe colors, materials, patterns, and any distinctive features."""
        
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "high"
                            }
                        },
                    ],
                }
            ],
            max_tokens=500,
        )
        
        # Parse the response
        result_text = response.choices[0].message.content
        return _parse_vision_response(result_text)
        
    except Exception as e:
        print(f"Vision analysis error: {e}")
        # Return meaningful fallback data
        return {
            "caption": "Handcrafted artisan product - detailed analysis unavailable due to image quality or API issue",
            "keywords": ["handmade", "artisan", "craft", "traditional", "unique"],
            "dominant_color": "RGB(150, 120, 90)",
            "size_category": "medium",
            "width": 300,
            "height": 400
        }

def _parse_vision_response(text: str) -> dict:
    """Parse the vision analysis response"""
    try:
        # Clean the text
        cleaned_text = text.strip()
        
        # Remove code block markers
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text.strip("`")
            if cleaned_text.lower().startswith("json"):
                cleaned_text = cleaned_text[4:].strip()
        
        # Try to parse as JSON
        data = json.loads(cleaned_text)
        return data
        
    except json.JSONDecodeError:
        # If JSON parsing fails, try to extract structured data
        try:
            # Look for JSON pattern
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Fallback: create structured response from text
        return {
            "caption": "Artisan handmade product with traditional craftsmanship",
            "keywords": _extract_keywords_from_text(text),
            "dominant_color": "RGB(150, 120, 90)",
            "size_category": "medium",
            "width": 300,
            "height": 400
        }

def _extract_keywords_from_text(text: str) -> list:
    """Extract potential keywords from text"""
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    # Common product keywords to prioritize
    product_keywords = ['handmade', 'artisan', 'craft', 'traditional', 'unique', 
                       'handcrafted', 'quality', 'natural', 'organic', 'vintage']
    
    keywords = []
    for kw in product_keywords:
        if kw in text.lower():
            keywords.append(kw)
    
    # Add other unique words
    for word in words:
        if word not in keywords and len(keywords) < 8:
            keywords.append(word)
    
    return keywords[:6]  # Return max 6 keywords