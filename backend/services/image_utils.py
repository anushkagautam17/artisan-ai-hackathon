# backend/services/image_utils.py
from PIL import Image
import io

def get_image_info_bytes(file_bytes: bytes, filename: str = "image"):
    """
    file_bytes: raw bytes of the uploaded image
    returns a short description to append to prompt (dominant rgb, size, filename)
    """
    try:
        img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        # small resize for speed
        small = img.resize((80, 80))
        colors = small.getcolors(80*80)  # list of (count, (r,g,b))
        dominant = max(colors, key=lambda x: x[0])[1] if colors else (0,0,0)
        width, height = img.size
        return f"filename:{filename}, size:{width}x{height}, dominant_rgb:{dominant}"
    except Exception as e:
        return f"filename:{filename}, error_reading_image"
