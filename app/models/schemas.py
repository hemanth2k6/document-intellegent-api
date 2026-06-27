class ChunkingResponse(BaseModel):
    document_id: str
    total_chunks: int
    avg_chunk_size: float
    min_chunk_size: int
    max_chunk_size: int
    total_words: int
    status: str
    message: str

class ChunkInfo(BaseModel):
    chunk_index: int
    word_count: int
    text_preview: str
    document_id: str