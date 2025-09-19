from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

# ✅ Correct import for running from project root
from backend.services.ai import generate_listing

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

        # 🔥 Call the real AI pipeline
        result = generate_listing(
            image_bytes=resized_image,
            description=description,
            target_lang=target_lang
        )

        print("DEBUG: Success! Returning result")
        return result

    except Exception as e:
        print(f"DEBUG: Error occurred: {str(e)}")
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

