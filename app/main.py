from app.models.schemas import ChunkingResponse, ErrorResponse
from app.services.document_processor import DocumentProcessor


@app.post("/chunk/{document_id}")
async def chunk_document(document_id: str):
    logger.info(f"Chunking request for document: {document_id}")
    import glob
    import os
    file_pattern = os.path.join(settings.upload_dir, f"{document_id}_*.pdf")
    files = glob.glob(file_pattern)
    if not files:
        raise HTTPException(
            status_code=404,
            detail=f"Document {document_id} not found"
        )
    file_path = files[0]
    try:
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        text_parts = [page.extract_text() for page in reader.pages]
        full_text = "\n".join(text_parts)
        cleaned_text = doc_processor._clean_text(full_text)
        chunks = doc_processor.chunker.chunk_document(
            text=cleaned_text,
            document_id=document_id
        )
        stats = doc_processor.chunker.get_chunk_statistics(chunks)
        response = ChunkingResponse(
            document_id=document_id,
            total_chunks=stats['total_chunks'],
            avg_chunk_size=round(stats['avg_chunk_size'], 2),
            min_chunk_size=stats['min_chunk_size'],
            max_chunk_size=stats['max_chunk_size'],
            total_words=stats['total_words'],
            status="success",
            message=f"Document chunked into {stats['total_chunks']} chunks"
        )
        logger.info(f"Chunking successful for {document_id}")
        return response
    except Exception as e:
        logger.error(f"Chunking failed for {document_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Chunking failed: {str(e)}"
        )

@app.get("/chunks/{document_id}")
async def get_chunks(document_id: str, limit: int = 5):
    logger.info(f"Fetching chunks for {document_id}")
    return {"message": "Will implement when we have vector storage"}