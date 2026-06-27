from fastapi import FastAPI
from app.utils.logging import logger
from app.config import settings

app = FastAPI(
    title="Document Intelligence API",
    description="AI-powered RAG pipeline for document Q&A",
    version="1.0.0"
)

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {
        "message": "Document Intelligence API is running!",
        "status": "healthy",
        "config": {
            "chunk_size": settings.chunk_size,
            "chunk_overlap": settings.chunk_overlap,
            "qdrant_host": settings.qdrant_host
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )