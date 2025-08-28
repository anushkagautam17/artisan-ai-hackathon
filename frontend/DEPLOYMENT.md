# Deployment Guide

## Local Development
1. Install requirements: `pip install -r requirements.txt`
2. Run the app: `streamlit run app.py`

## Cloud Deployment (Google Cloud Run)
1. Create a Dockerfile
2. Build container: `gcloud builds submit --tag gcr.io/PROJECT-ID/artisanai`
3. Deploy: `gcloud run deploy --image gcr.io/PROJECT-ID/artisanai`

## Environment Variables
- `BACKEND_URL`: URL of your backend API