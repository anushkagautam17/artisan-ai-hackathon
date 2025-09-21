# backend/main.py
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import os
import sys
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Add the current directory to Python path to fix import issues
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Now try to import - use a try/except to handle different scenarios
try:
    # Try importing from services.listing (this is the correct one)
    from services.listing import generate_listing
    print("DEBUG: Successfully imported from services.listing")
except ImportError as e:
    print(f"DEBUG: Import error from services.listing: {e}")
    try:
        # Fallback to services.ai if listing doesn't work
        from services.ai import generate_listing
        print("DEBUG: Successfully imported from services.ai")
    except ImportError as e2:
        print(f"DEBUG: Import error from services.ai: {e2}")
        # Create a mock function for testing
        def generate_listing(description, image_bytes=None):
            print("DEBUG: Using mock generate_listing function")
            product_type = description.split()[0] if description else "Artisan"
            return {
                "title": f"Handcrafted {product_type} - Traditional Artisan Work",
                "description": f"Beautiful handmade {product_type} crafted by skilled artisans",
                "bullets": [
                    "Handmade by skilled artisans using traditional techniques",
                    "Made with natural, eco-friendly materials",
                    "Unique design that reflects cultural heritage",
                    "Perfect for home decoration or as a special gift"
                ],
                "price": "₹1,200 - ₹1,800",
                "suggested_price": "₹1,499",
                "origin_hint": "Rajasthan, India" if "pottery" in description.lower() else "India",
                "vision": {
                    "caption": f"A beautiful {product_type} with intricate traditional patterns",
                    "keywords": ["handmade", "artisan", "traditional", "craft", product_type.lower()],
                    "dominant_color": "Blue" if "blue" in description.lower() else "Earth tones",
                    "size_category": "medium"
                },
                "recommendations": [
                    "Include information about the artisan who created this piece",
                    "Show the product being used in different settings",
                    "Highlight the cultural significance of the designs"
                ],
                "image_fix_suggestions": [
                    "Use natural light to better show the colors and textures",
                    "Take photos from multiple angles to showcase details",
                    "Include a scale reference to show product size"
                ]
            }

# Check if we have OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("WARNING: OPENAI_API_KEY not found in .env file, using simulation mode")
else:
    print("DEBUG: OpenAI API key found")

print("DEBUG: Server starting...")

app = FastAPI(title="Artisan Marketplace API", version="1.0.0")

# Enable CORS for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to resize image
def resize_image(image_data: bytes, max_size: tuple = (512, 512)) -> bytes:
    """Resize image to reduce file size before processing."""
    try:
        image = Image.open(io.BytesIO(image_data))

        # Convert RGBA (transparent PNG) to RGB (white background) for JPEG
        if image.mode == "RGBA":
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background

        image.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Convert to JPEG for consistency
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="JPEG", quality=85)
        return img_byte_arr.getvalue()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Artisan Marketplace API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}


@app.post("/generate")
async def generate_listing_endpoint(
    image: UploadFile = File(...),
    description: str = Form(...),
    target_lang: str = Form("en"),
):
    try:
        print(f"DEBUG: Received request - description: '{description}', target_lang: '{target_lang}'")
        
        # Read and resize the image
        image_data = await image.read()
        if not image_data:
            raise HTTPException(status_code=400, detail="No image data received")

        resized_image = resize_image(image_data)
        print(f"DEBUG: Resized image size: {len(resized_image)} bytes")

        # Call the AI pipeline
        result = generate_listing(
            description=description,
            image_bytes=resized_image
        )
        
        print(f"DEBUG: Result keys: {list(result.keys())}")
        
        # Enhanced result with all fields expected by frontend
        enhanced_result = {
            "title": result.get("title", "Product Title"),
            "description": result.get("description", description),
            "bullets": result.get("bullets", []),
            "price": result.get("price", "₹0"),
            "suggested_price": result.get("suggested_price", result.get("price", "₹0").split(" - ")[0] if " - " in result.get("price", "₹0") else result.get("price", "₹0")),
            "origin_hint": result.get("origin_hint", "India"),
            "vision": result.get("vision", {
                "caption": result.get("title", "") + " - Handcrafted with care",
                "keywords": ["artisan", "handmade", "traditional"],
                "dominant_color": "Natural",
                "size_category": "medium"
            }),
            "recommendations": result.get("recommendations", [
                "Use natural lighting for photography",
                "Include product dimensions in description",
                "Share the story behind this artisan piece"
            ]),
            "image_fix_suggestions": result.get("image_fix_suggestions", [
                "Crop to focus on product",
                "Adjust brightness for better clarity"
            ]),
            "_raw_model_output": result.get("_raw_model_output", ""),
            "_raw_recommendations_output": result.get("_raw_recommendations_output", "")
        }

        print("DEBUG: Success! Returning result")
        return enhanced_result

    except Exception as e:
        print(f"DEBUG: Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)