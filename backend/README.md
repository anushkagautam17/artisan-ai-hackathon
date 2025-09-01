# Artisan Marketplace Backend

## Setup
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the server: `python main.py`

## API Endpoints
- `GET /` - Health check
- `POST /generate` - Generate product listing from image and description

## Example Request
```bash
curl -X POST "http://localhost:8000/generate" \
  -F "image=@your_image.jpg" \
  -F "description=Your product description"