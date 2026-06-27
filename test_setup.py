import sys
import os

print(f"Python version:{sys.version}")
try:
    import fastapi
    import uvicorn
    import pypdf
    import qdrant_client
    import google.generativeai as genai
    print("all imports successful")
except ImportError as e:
    print(f"import error:{e}")
from dotenv import load_dotenv
load_dotenv()
gemini_key=os.getenv("GEMINI_API_KEY")
if gemini_key:
    print("gemini api key found in .env")
else:
    print("gemini api key not found in .env")
from app.main import app
print("fastapi app created successfully")