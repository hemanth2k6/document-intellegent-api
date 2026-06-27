from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.models.schemas import DocumentUploadResponse, ErrorResponse
from app.services.document_processor import DocumentProcessor
from app.utils.logging import logger
from app.config import settings
from datetime import datetime

app = FastAPI(
    title="Document Intelligence API",
    description="AI-powered RAG pipeline for document Q&A",
    version="1.0.0"
)
doc_processor = DocumentProcessor()

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

@app.post("/upload", 
          response_model=DocumentUploadResponse,
          responses={400: {"model": ErrorResponse}, 413: {"model": ErrorResponse}})
async def upload_pdf(file: UploadFile = File(...)):
    logger.info(f"Received upload request: {file.filename}")
    
    try:
        result = await doc_processor.process_pdf(file)
        response = DocumentUploadResponse(
            document_id=result["document_id"],
            filename=result["filename"],
            page_count=result["page_count"],
            character_count=result["character_count"],
            word_count=result["word_count"],
            status="success",
            message=f"PDF processed successfully. Extracted {result['word_count']} words from {result['page_count']} pages.",
            uploaded_at=result["uploaded_at"]
        )
        
        logger.info(f"Upload successful: {response.document_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in upload endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )