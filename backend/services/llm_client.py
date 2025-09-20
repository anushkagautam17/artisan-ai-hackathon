# backend/services/llm_client.py
import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_completion(prompt: str, model: str = "gpt-3.5-turbo", max_tokens: int = 300, temperature: float = 0.7):
    """Get completion using new OpenAI API"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        # Return a fallback response instead of crashing
        return """{
            "title": "Handcrafted Artisan Product", 
            "description": "Beautiful handmade craftsmanship using traditional techniques",
            "bullets": ["Beautiful handmade craftsmanship", "Traditional techniques", "High quality materials", "Unique design"],
            "price": "₹300 - ₹600",
            "suggested_price": "₹450"
        }"""

def extract_first_json(text: str):
    """Extract first JSON object from text"""
    try:
        # Clean the text first
        cleaned_text = text.strip()
        
        # Remove code block markers if present
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text.strip("`")
            if cleaned_text.lower().startswith("json"):
                cleaned_text = cleaned_text[4:].strip()
        
        # Try to parse the entire text as JSON first
        data = json.loads(cleaned_text)
        return data, cleaned_text
    except json.JSONDecodeError:
        # Look for JSON within text using more robust pattern
        json_pattern = r'\{[\s\S]*\}'
        match = re.search(json_pattern, text, re.DOTALL)
        if match:
            try:
                json_str = match.group()
                data = json.loads(json_str)
                return data, json_str
            except json.JSONDecodeError:
                # Try to fix common JSON issues
                try:
                    # Try adding quotes to unquoted keys
                    fixed_json = re.sub(r'(\w+):', r'"\1":', json_str)
                    data = json.loads(fixed_json)
                    return data, fixed_json
                except:
                    pass
    return None, text