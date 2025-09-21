# backend/main.py
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import io
import os
import sys
import json
import random
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Try to import AI services
try:
    from services.listing import generate_listing
    from services.vision import analyze_image_bytes
    AI_ENABLED = True
    print("✅ AI services loaded successfully")
except ImportError as e:
    print(f"⚠️  AI services not available: {e}")
    AI_ENABLED = False

app = FastAPI(title="MadebyNaari API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501", "https://*.streamlit.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request validation
class TranslationRequest(BaseModel):
    text: str
    target_lang: str

class GenerateRequest(BaseModel):
    description: str
    target_lang: str = "en"

# Helper function to resize image
def resize_image(image_data: bytes, max_size: tuple = (512, 512)) -> bytes:
    """Resize image to reduce file size before processing"""
    try:
        image = Image.open(io.BytesIO(image_data))
        if image.mode == "RGBA":
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="JPEG", quality=85)
        return img_byte_arr.getvalue()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

# Enhanced demo data function that matches frontend expectations
def generate_demo_listing(description: str, image_data: bytes = None) -> Dict:
    """Generate realistic demo data that matches frontend expectations"""
    
    # Determine product type from description
    product_type = "Product"
    origin = "India"
    price = "₹1,200 - ₹1,800"
    suggested_price = "₹1,499"
    
    if any(word in description.lower() for word in ["pottery", "vase", "clay", "ceramic"]):
        product_type = "Pottery"
        origin = "Rajasthan, India"
        price = "₹1,200 - ₹1,500"
        suggested_price = "₹1,350"
    elif any(word in description.lower() for word in ["saree", "textile", "cloth", "fabric", "weav"]):
        product_type = "Textile"
        origin = "Varanasi, India"
        price = "₹2,500 - ₹4,000"
        suggested_price = "₹3,200"
    elif any(word in description.lower() for word in ["jewel", "necklace", "ring", "bracelet", "earring"]):
        product_type = "Jewelry"
        origin = "Delhi, India"
        price = "₹800 - ₹1,500"
        suggested_price = "₹1,150"
    
    # Generate appropriate description based on product type
    descriptions = {
        "Pottery": f"Beautiful handmade {product_type.lower()} piece featuring traditional craftsmanship. "
                  f"Each item is carefully shaped by skilled artisans using time-honored techniques, "
                  f"resulting in a unique work of art that reflects our rich cultural heritage. "
                  f"Perfect for home decoration or as a special gift.",
        
        "Textile": f"Exquisite handwoven {product_type.lower()} created by master artisans. "
                  f"Using traditional looms and techniques, each piece tells a story of cultural heritage "
                  f"and represents hours of meticulous craftsmanship. The intricate patterns and vibrant "
                  f"colors make this a truly special creation.",
        
        "Jewelry": f"Elegant handmade {product_type.lower()} piece crafted with precision and care. "
                  f"Each item is unique, featuring traditional designs that have been passed down through "
                  f"generations of skilled artisans. The attention to detail and quality materials ensure "
                  f"this piece will be cherished for years to come.",
        
        "Product": f"Beautiful handmade {product_type.lower()} crafted by skilled artisans using traditional techniques. "
                  f"Each piece is unique and reflects our cultural heritage. Made with natural materials and "
                  f"eco-friendly processes, this item represents the best of traditional craftsmanship."
    }
    
    description_text = descriptions.get(product_type, descriptions["Product"])
    
    # Generate appropriate features
    features = {
        "Pottery": [
            "Handcrafted by skilled artisans using traditional techniques",
            "Made from high-quality clay with eco-friendly glaze",
            "Unique patterns inspired by traditional Indian art",
            "Perfect for home decoration or as a thoughtful gift"
        ],
        "Textile": [
            "Handwoven by master artisans using traditional looms",
            "Made from natural fibers and eco-friendly dyes",
            "Intricate patterns that tell cultural stories",
            "Each piece is unique with slight variations"
        ],
        "Jewelry": [
            "Handcrafted by skilled jewelers using traditional methods",
            "Made with high-quality materials and attention to detail",
            "Traditional designs with modern elegance",
            "Perfect for special occasions or daily wear"
        ],
        "Product": [
            "Handmade by skilled artisans using traditional techniques",
            "Made with natural, eco-friendly materials",
            "Unique design that reflects cultural heritage",
            "Perfect for home decoration or as a special gift"
        ]
    }
    
    bullets = features.get(product_type, features["Product"])
    
    # Generate vision analysis if image is provided
    vision_data = {}
    if image_data:
        try:
            # Simple image analysis (would be replaced with real AI)
            image = Image.open(io.BytesIO(image_data))
            width, height = image.size
            size_category = "small" if max(width, height) < 400 else "medium" if max(width, height) < 800 else "large"
            
            vision_data = {
                "caption": f"A {product_type.lower()} product with traditional design elements",
                "keywords": ["handmade", "artisan", product_type.lower(), "traditional", "craft"],
                "dominant_color": "Various" if product_type == "Textile" else "Earth tones",
                "size_category": size_category,
                "width": width,
                "height": height
            }
        except:
            vision_data = {
                "caption": f"Handmade {product_type.lower()} product",
                "keywords": ["handmade", "artisan", product_type.lower()],
                "dominant_color": "Natural",
                "size_category": "medium",
                "width": 600,
                "height": 600
            }
    else:
        vision_data = {
            "caption": f"Handmade {product_type.lower()} product",
            "keywords": ["handmade", "artisan", product_type.lower()],
            "dominant_color": "Natural",
            "size_category": "medium",
            "width": 600,
            "height": 600
        }
    
    return {
        "title": f"Handcrafted {product_type} - Traditional Artisan Work",
        "description": description_text,
        "bullets": bullets,
        "price": price,
        "suggested_price": suggested_price,
        "origin_hint": origin,
        "vision": vision_data,
        "recommendations": [
            "Use natural lighting for better product photos",
            "Include multiple angles to showcase details",
            "Add a common object for scale reference",
            "Show the product being used in context"
        ],
        "image_fix_suggestions": [
            "Use natural light to reduce shadows",
            "Capture the intricate details up close",
            "Use a clean, neutral background",
            "Ensure the product is in focus"
        ]
    }

# Health endpoint
@app.get("/")
async def root():
    return {"message": "MadebyNaari API is running", "ai_enabled": AI_ENABLED}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "ai_enabled": AI_ENABLED, "service": "MadebyNaari"}

# Main generation endpoint - matches frontend expectations exactly
@app.post("/api/generate")
async def generate_listing_endpoint(
    description: str = Form(...),
    target_lang: str = Form("en"),
    image: Optional[UploadFile] = File(None)
):
    """Main endpoint for generating product listings - matches frontend API calls"""
    try:
        print(f"Received request - description: '{description}', target_lang: '{target_lang}'")
        
        image_data = None
        if image:
            image_data = await image.read()
            if image_data:
                image_data = resize_image(image_data)
                print(f"Resized image size: {len(image_data)} bytes")

        # Use AI if available, otherwise use demo data
        if AI_ENABLED:
            print("Using AI for generation")
            result = generate_listing(description=description, image_bytes=image_data)
        else:
            print("Using demo data - AI not available")
            result = generate_demo_listing(description, image_data)

        # Return the exact format expected by frontend
        return {
            "title": result.get("title", "Product Title"),
            "description": result.get("description", description),
            "bullets": result.get("bullets", []),
            "price": result.get("price", "₹0"),
            "suggested_price": result.get("suggested_price", 
                                         result.get("price", "₹0").split(" - ")[0] 
                                         if " - " in result.get("price", "₹0") 
                                         else result.get("price", "₹0")),
            "origin_hint": result.get("origin_hint", "India"),
            "vision": result.get("vision", {
                "caption": result.get("title", "") + " - Handcrafted with care",
                "keywords": ["artisan", "handmade", "traditional"],
                "dominant_color": "Natural"
            }),
            "recommendations": result.get("recommendations", [
                "Use natural lighting for photography",
                "Include product dimensions in description",
                "Share the story behind this artisan piece"
            ]),
            "image_fix_suggestions": result.get("image_fix_suggestions", [
                "Crop to focus on product",
                "Adjust brightness for better clarity"
            ])
        }

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        # Fallback to demo data on error
        result = generate_demo_listing(description, None)
        return result

# Translation endpoint - matches frontend API calls
@app.post("/api/translate")
async def translate_text_endpoint(request: TranslationRequest):
    """Translation endpoint with improved vocabulary - matches frontend API calls"""
    try:
        text = request.text
        target_lang = request.target_lang
        
        if target_lang == "en":
            return {
                "translated_text": text, 
                "original_text": text,
                "target_lang": target_lang
            }
        
        # Enhanced translation dictionaries
        translations = {
            "hi": {
                "Handcrafted": "हस्तनिर्मित",
                "Traditional": "पारंपरिक",
                "Beautiful": "सुंदर",
                "Pottery": "मिट्टी के बर्तन",
                "Textile": "वस्त्र",
                "Jewelry": "गहने",
                "India": "भारत",
                "Rajasthan": "राजस्थान",
                "Varanasi": "वाराणसी",
                "Delhi": "दिल्ली",
                "Perfect for home decoration": "घर की सजावट के लिए आदर्श",
                "as a special gift": "एक विशेष उपहार के रूप में",
                "Made by skilled artisans": "कुशल कारीगरों द्वारा निर्मित",
                "using traditional methods": "पारंपरिक तरीकों का उपयोग करके",
                "Natural and eco-friendly materials": "प्राकृतिक और पर्यावरण के अनुकूल सामग्री",
                "each piece is different": "हर टुकड़ा अलग है",
                "Supports local artisan communities": "स्थानीय कारीगर समुदायों का समर्थन करता है",
                "crafted by": "द्वारा निर्मित",
                "skilled artisans": "कुशल कारीगर",
                "unique": "अनोखा",
                "cultural heritage": "सांस्कृतिक विरासत",
                "₹": "₹"
            },
            "bn": {
                "Handcrafted": "হস্তনির্মিত",
                "Traditional": "প্রথাগত",
                "Beautiful": "সুন্দর",
                "Pottery": "মৃৎশিল্প",
                "Textile": "টেক্সটাইল",
                "Jewelry": "গহনা",
                "India": "ভারত",
                "Rajasthan": "রাজস্থান",
                "Varanasi": "বারাণসী",
                "Delhi": "দিল্লি",
                "Perfect for home decoration": "বাড়ির সাজসজ্জার জন্য উপযুক্ত",
                "as a special gift": "একটি বিশেষ উপহার হিসাবে",
                "Made by skilled artisans": "দক্ষ কারিগর দ্বারা তৈরি",
                "using traditional methods": "প্রথাগত পদ্ধতি ব্যবহার করে",
                "Natural and eco-friendly materials": "প্রাকৃতিক এবং পরিবেশ বান্ধব উপকরণ",
                "each piece is different": "প্রতিটি টুকরা আলাদা",
                "Supports local artisan communities": "স্থানীয় কারিগর সম্প্রদায়কে সমর্থন করে",
                "crafted by": "দ্বারা তৈরি",
                "skilled artisans": "দক্ষ কারিগর",
                "unique": "অনন্য",
                "cultural heritage": "সাংস্কৃতিক heritage",
                "₹": "₹"
            },
            "ta": {
                "Handcrafted": "கைவண்ண",
                "Traditional": "பாரம்பரிய",
                "Beautiful": "அழகான",
                "Pottery": "மட்பாண்ட",
                "Textile": "துணி",
                "Jewelry": "நகை",
                "India": "இந்தியா",
                "Rajasthan": "ராஜஸ்தான்",
                "Varanasi": "வாரணாசி",
                "Delhi": "டெல்லி",
                "Perfect for home decoration": "வீட்டு அலங்காரத்திற்கு சிறந்தது",
                "as a special gift": "ஒரு சிறப்பு பரிசாக",
                "Made by skilled artisans": "திறமையான கைவினைஞர்களால் தயாரிக்கப்பட்டது",
                "using traditional methods": "பாரம்பரிய முறைகளைப் பயன்படுத்தி",
                "Natural and eco-friendly materials": "இயற்கை மற்றும் சூழல் அன்புள்ள பொருட்கள்",
                "each piece is different": "ஒவ்வொரு துண்டும் வித்தியாசமானது",
                "Supports local artisan communities": "உள்ளூர் கைவினைஞர் சமூகங்களை ஆதரிக்கிறது",
                "crafted by": "மூலம் crafted",
                "skilled artisans": "திறமையான கைவினைஞர்கள்",
                "unique": "தனித்துவமான",
                "cultural heritage": "கலாச்சார மரபு",
                "₹": "₹"
            },
            "te": {
                "Handcrafted": "హస్తనిర్మిత",
                "Traditional": "సాంప్రదాయ",
                "Beautiful": "అందమైన",
                "Pottery": "మృత్పాత్ర",
                "Textile": "టెక్స్టైల్",
                "Jewelry": "నగలు",
                "India": "భారతదేశం",
                "Rajasthan": "రాజస్థాన్",
                "Varanasi": "వారణాసి",
                "Delhi": "델్హి",
                "Perfect for home decoration": "ఇంటి అలంకరణకు సరైనది",
                "as a special gift": "ఒక ప్రత్యేక బహుమతిగా",
                "Made by skilled artisans": "నైపుణ్యం గల శిల్పులచే తయారు చేయబడింది",
                "using traditional methods": "సాంప్రదాయ పద్ధతులను ఉపయోగించి",
                "Natural and eco-friendly materials": "సహజ మరియు పర్యావరణ అనుకూల పదార్థాలు",
                "each piece is different": "ప్రతి ముక్క భిన్నంగా ఉంటుంది",
                "Supports local artisan communities": "స్థానిక శిల్పి సంఘాలకు మద్దతు ఇస్తుంది",
                "crafted by": "ద్వారా crafted",
                "skilled artisans": "నైపుణ్యం గల శిల్పులు",
                "unique": "అనన్యమైన",
                "cultural heritage": "సాంస్కృతిక మార్పు",
                "₹": "₹"
            }
        }
        
        translated_text = text
        lang_dict = translations.get(target_lang, {})
        
        # Replace words that have translations
        for eng, trans in lang_dict.items():
            translated_text = translated_text.replace(eng, trans)
            
        return {
            "translated_text": translated_text,
            "original_text": text,
            "target_lang": target_lang
        }
        
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return {
            "translated_text": text,
            "original_text": text,
            "target_lang": target_lang,
            "error": str(e)
        }

# Simple text generation endpoint (no image)
@app.post("/api/generate-text")
async def generate_text_endpoint(request: GenerateRequest):
    """Generate product text without image upload"""
    try:
        description = request.description
        target_lang = request.target_lang
        
        print(f"Text generation request - description: '{description}'")
        
        # Use AI if available, otherwise use demo data
        if AI_ENABLED:
            result = generate_listing(description=description, image_bytes=None)
        else:
            result = generate_demo_listing(description, None)
        
        return {
            "title": result.get("title", "Product Title"),
            "description": result.get("description", description),
            "bullets": result.get("bullets", []),
            "price": result.get("price", "₹0"),
            "suggested_price": result.get("suggested_price", "₹0"),
            "origin_hint": result.get("origin_hint", "India")
        }
        
    except Exception as e:
        print(f"Text generation error: {str(e)}")
        result = generate_demo_listing(request.description, None)
        return result

# Language update endpoint for homepage
@app.post("/api/update-language")
async def update_language_endpoint(request: Request):
    """Update the user's language preference"""
    try:
        data = await request.json()
        language = data.get("language", "en")
        
        # Here you would typically save to database or session
        # For now, we'll just return success
        return {"status": "success", "language": language, "message": f"Language updated to {language}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Additional health check endpoint
@app.get("/api/status")
async def api_status():
    """Detailed API status information"""
    return {
        "status": "healthy",
        "ai_enabled": AI_ENABLED,
        "service": "MadebyNaari API",
        "version": "1.0.0",
        "endpoints": {
            "generate": "/api/generate",
            "translate": "/api/translate",
            "generate-text": "/api/generate-text",
            "health": "/health"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)