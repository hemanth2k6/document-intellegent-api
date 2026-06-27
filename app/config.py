import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    
    
    qdrant_host: str = os.getenv("QDRANT_HOST", "localhost")
    qdrant_port: int = int(os.getenv("QDRANT_PORT", "6333"))
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "documents")
    
    
    upload_dir: str = os.getenv("UPLOAD_DIR", "./uploads")
    max_file_size: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "500"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "50"))
    
    
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    
    embedding_model: str = "models/embedding-001"
    generation_model: str = "models/gemini-pro"

settings = Settings()


os.makedirs(settings.upload_dir, exist_ok=True)