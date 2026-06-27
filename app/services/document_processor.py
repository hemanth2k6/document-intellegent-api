
from app.services.chunking import TextChunker

class DocumentProcessor:
    def __init__(self):
        self.upload_dir = settings.upload_dir
        self.chunker = TextChunker()  #
    
    async def process_pdf_with_chunks(self, file: UploadFile) -> Dict[str, Any]:
        result = await self.process_pdf(file)
        chunks = self.chunker.chunk_document(
            text=result["cleaned_text"],
            document_id=result["document_id"]
        )
        result["chunks"] = chunks
        result["chunk_statistics"] = self.chunker.get_chunk_statistics(chunks)
        
        return result