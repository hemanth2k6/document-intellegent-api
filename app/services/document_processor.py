import os
import uuid
import re
from typing import Dict, Any, Optional
from datetime import datetime
from pypdf import PdfReader
from fastapi import UploadFile, HTTPException
from app.utils.logging import logger
from app.config import settings

class DocumentProcessor:
    def __init__(self):
        self.upload_dir = settings.upload_dir
    async def process_pdf(self, file: UploadFile) -> Dict[str, Any]:
        self._validate_file(file)
        document_id = str(uuid.uuid4())
        file_path = await self._save_file(file, document_id)

        try:
            raw_text, page_count = self._extract_text(file_path)
            cleaned_text = self._clean_text(raw_text)
            character_count = len(cleaned_text)
            word_count = len(cleaned_text.split())
            return {
                "document_id": document_id,
                "filename": file.filename,
                "page_count": page_count,
                "character_count": character_count,
                "word_count": word_count,
                "cleaned_text": cleaned_text,  # We'll use this in Step 2
                "file_path": file_path,
                "uploaded_at": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Error processing PDF {document_id}: {str(e)}")
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=500, detail=f"PDF processing failed: {str(e)}")

    def _validate_file(self, file: UploadFile):
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )
        logger.info(f"Processing file: {file.filename}")
    
    async def _save_file(self, file: UploadFile, document_id: str) -> str:
        safe_filename = f"{document_id}_{file.filename.replace(' ', '_')}"
        file_path = os.path.join(self.upload_dir, safe_filename)
        try:
            content = await file.read()
            if len(content) > settings.max_file_size:
                raise HTTPException(
                    status_code=413,
                    detail=f"File too large. Max size: {settings.max_file_size // (1024*1024)}MB"
                )
            with open(file_path, "wb") as f:
                f.write(content)
            logger.info(f"File saved: {file_path} ({len(content)} bytes)")
            return file_path
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            raise HTTPException(status_code=500, detail=f"File save failed: {str(e)}")
    
    def _extract_text(self, file_path: str) -> tuple[str, int]:
        
        try:
            reader = PdfReader(file_path)
            page_count = len(reader.pages)
            text_parts = []
            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
                else:
                    logger.warning(f"No text extracted from page {page_num}")
            
            full_text = "\n".join(text_parts)
            logger.info(f"Extracted {len(full_text)} characters from {page_count} pages")
            return full_text, page_count
            
        except Exception as e:
            logger.error(f"Text extraction failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Could not extract text from PDF: {str(e)}"
            )
    
    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        text = text.strip()
        text = re.sub(r'[^\x20-\x7E\n\t]', '', text)
        text = text.replace('\x00', '')
        logger.info(f"Cleaned text: {len(text)} characters")
        return text
    
    def cleanup_temp_file(self, file_path: str):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to clean up {file_path}: {str(e)}")