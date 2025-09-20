from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import os
import sys
from dotenv import load_dotenv

# Add the parent directory to Python path to fix import issues
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Now try to import - use a try/except to handle different scenarios
try:
    from backend.services.ai import generate_listing
    print("DEBUG: Successfully imported from backend.services.ai")
except ImportError as e:
    print(f"DEBUG: Import error: {e}")
    try:
        # Try importing directly from services if backend is the current directory
        from services.ai import generate_listing
        print("DEBUG: Successfully imported from services.ai")
    except ImportError as e2:
        print(f"DEBUG: Second import error: {e2}")
        # Create a mock function for testing
        def generate_listing(image_bytes, description, target_lang="en", api_key=None):
            return {
                "title": f"Beautiful {description.split()[0]} Product",
                "bullets": [
                    "Handcrafted by skilled artisans",
                    "Made with traditional techniques",
                    "Eco-friendly and sustainable materials",
                    "Unique design that tells a story"
                ],
                "price": "₹1,200 - ₹1,800",
                "suggested_price": "₹1,499",
                "origin_hint": "India",
                "vision": {
                    "caption": f"A beautiful {description.split()[0]} with intricate details",
                    "keywords": ["handmade", "artisan", "traditional", "craft", description.split()[0]],
                    "dominant_color": "Blue"
                },
                "recommendations": [
                    "Use natural lighting for better product photos",
                    "Show the product from multiple angles",
                    "Include a story about the artisan who made it"
                ],
                "image_fix_suggestions": [
                    "Crop the image to focus on the product",
                    "Adjust the brightness for better visibility"
                ]
            }

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("WARNING: OPENAI_API_KEY not found in .env file, using simulation mode")
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

        # Call the AI pipeline - adapt to your ai.py function signature
        result = generate_listing(
            image_bytes=resized_image,
            description=description,
            target_lang=target_lang
        )
        
        # Add additional fields that your frontend expects
        enhanced_result = {
            "title": result.get("title", ""),
            "bullets": result.get("bullets", []),
            "price": result.get("price", ""),
            "suggested_price": result.get("price", "").replace("₹", "").split("-")[0].strip() + " (exact)",
            "origin_hint": "India",  # Default value
            "vision": {
                "caption": result.get("title", "") + " - Handcrafted with care",
                "keywords": ["artisan", "handmade", "traditional"],
                "dominant_color": "Natural"
            },
            "recommendations": [
                "Use natural lighting for photography",
                "Include product dimensions in description",
                "Share the story behind this artisan piece"
            ],
            "image_fix_suggestions": [
                "Crop to focus on product",
                "Adjust brightness for better clarity"
            ]
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
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)