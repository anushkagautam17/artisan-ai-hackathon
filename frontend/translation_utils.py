# frontend/translation_utils.py
import requests

def translate_text(text, target_lang, source_lang="en"):
    """
    Translate text using the backend API
    """
    if target_lang == source_lang:
        return text
    
    try:
        response = requests.post(
            "http://localhost:8000/translate",
            data={"text": text, "target_lang": target_lang},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("translated_text", text)
    except:
        # Fallback to simple translation dictionary
        pass
    
    # Simple fallback translations for common phrases
    translations = {
        "hi": {
            "Product Listing": "उत्पाद सूची",
            "Social Media": "सोशल मीडिया",
            "Multilingual": "बहुभाषी",
            "Create beautiful product descriptions": "सुंदर उत्पाद विवरण बनाएं",
            "Generate Instagram and WhatsApp content": "Instagram और WhatsApp सामग्री उत्पन्न करें",
            "Reach customers in their language": "ग्राहकों तक उनकी भाषा में पहुंचें"
        },
        "bn": {
            "Product Listing": "পণ্য তালিকা",
            "Social Media": "সোশ্যাল মিডিয়া",
            "Multilingual": "বহুভাষিক",
            "Create beautiful product descriptions": "সুন্দর পণ্য বিবরণ তৈরি করুন",
            "Generate Instagram and WhatsApp content": "Instagram এবং WhatsApp কনটেন্ট তৈরি করুন",
            "Reach customers in their language": "গ্রাহকদের তাদের ভাষায় reaching করুন"
        }
    }
    
    return translations.get(target_lang, {}).get(text, text)