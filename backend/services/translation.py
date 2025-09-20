# backend/services/translate.py
import os
from typing import List

def translate_texts(texts: List[str], target_language: str) -> List[str]:
    """
    Uses Google Cloud Translate v3 to translate a batch of strings.
    Falls back to mock translation if Google Cloud is not available.
    """
    # Check if we have the required Google Cloud credentials
    project_id = os.getenv("VERTEX_PROJECT_ID")
    
    if not project_id:
        print("WARNING: VERTEX_PROJECT_ID not set, using mock translation")
        return _mock_translate_texts(texts, target_language)
    
    try:
        from google.cloud import translate_v3 as translate

        client = translate.TranslationServiceClient()

        location = os.getenv("VERTEX_LOCATION", "us-central1")
        parent = f"projects/{project_id}/locations/{location}"

        response = client.translate_text(
            contents=texts,
            target_language_code=target_language,
            parent=parent,
            mime_type="text/plain",
        )
        return [t.translated_text for t in response.translations]
    
    except ImportError:
        print("WARNING: google-cloud-translate not installed, using mock translation")
        return _mock_translate_texts(texts, target_language)
    
    except Exception as e:
        print(f"WARNING: Google Translate failed: {e}, using mock translation")
        return _mock_translate_texts(texts, target_language)


def _mock_translate_texts(texts: List[str], target_language: str) -> List[str]:
    """
    Mock translation function for testing when Google Translate is not available.
    Returns the same texts but adds a language tag prefix.
    """
    print(f"DEBUG: Using mock translation to {target_language}")
    
    # Simple mock translations for common phrases
    common_translations = {
        "hi": {
            "Handcrafted": "हस्तनिर्मित",
            "artisan": "कारीगर",
            "traditional": "पारंपरिक",
            "natural materials": "प्राकृतिक सामग्री",
            "eco-friendly": "पर्यावरण के अनुकूल",
            "unique design": "अनोखा डिजाइन",
            "beautiful": "सुंदर",
            "handmade": "हाथ से बना",
            "skilled": "कुशल",
            "craftsmanship": "शिल्प कौशल"
        },
        "bn": {
            "Handcrafted": "হস্তনির্মিত",
            "artisan": "কারিগর",
            "traditional": "প্রথাগত",
            "natural materials": "প্রাকৃতিক উপকরণ",
            "eco-friendly": "পরিবেশ বান্ধব",
            "unique design": "অনন্য নকশা",
            "beautiful": "সুন্দর",
            "handmade": "হাতে তৈরি",
            "skilled": "দক্ষ",
            "craftsmanship": "কারুকার্য"
        },
        "ta": {
            "Handcrafted": "கைவினை",
            "artisan": "கைவினைஞர்",
            "traditional": "பாரம்பரிய",
            "natural materials": "இயற்கை பொருட்கள்",
            "eco-friendly": "சூழலுக்கு உகந்த",
            "unique design": "தனித்த வடிவமைப்பு",
            "beautiful": "அழகான",
            "handmade": "கைவினை",
            "skilled": "திறமையான",
            "craftsmanship": "கைவினைத் திறன்"
        }
    }
    
    translated_texts = []
    for text in texts:
        if target_language in common_translations:
            # Try to translate common words
            translated = text
            for eng, trans in common_translations[target_language].items():
                translated = translated.replace(eng, trans)
            translated_texts.append(translated)
        else:
            # Just add a language tag for other languages
            translated_texts.append(f"[{target_language}] {text}")
    
    return translated_texts