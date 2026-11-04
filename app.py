"""
Hugging Face Spaces Entry Point (SDK: Gradio - 100% Free Tier, No Credit Card Required)
Mounts the FastAPI app and Google Stitch UI so it runs natively on Hugging Face Spaces.
"""
import os
import uvicorn
from main import app as fastapi_app

# Set default port for Hugging Face Spaces
PORT = int(os.environ.get("PORT", 7860))

if __name__ == "__main__":
    uvicorn.run(fastapi_app, host="0.0.0.0", port=PORT)
