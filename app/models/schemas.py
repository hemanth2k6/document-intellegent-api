from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class DocumentUploadResponse(BaseModel):
    
    document_id: str
    filename: str
    page_count: int
    character_count: int
    word_count: int
    status: str
    message: str
    uploaded_at: datetime

class DocumentMetadata(BaseModel):
    
    document_id: str
    filename: str
    page_count: int
    total_chunks: Optional[int] = None
    uploaded_at: datetime
    
class ErrorResponse(BaseModel):
    
    error: str
    detail: Optional[str] = None
    status_code: int