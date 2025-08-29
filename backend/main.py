from fastapi import FastAPI

app = FastAPI(
    title="Artisans Hackathon Backend",
    description="Backend API for Artisan AI Hackathon project",
    version="1.0.0"
)

@app.get("/health")
def health():
    return {"ok": True, "app": "Artisans Hackathon Backend"}

