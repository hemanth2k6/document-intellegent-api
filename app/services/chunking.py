import re
from typing import List, Dict, Any
from app.utils.logging import logger
from app.config import settings

class TextChunker:
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
        
    def chunk_document(self, text: str, document_id: str) -> List[Dict[str, Any]]:
        if not text or len(text.strip()) == 0:
            logger.warning(f"Empty text for document {document_id}")
            return []
        sentences = self._split_into_sentences(text)
        logger.info(f"Split into {len(sentences)} sentences")
        if not sentences:
            return []
        chunks = self._create_chunks_with_overlap(sentences, document_id)
        total_words = sum(len(chunk['text'].split()) for chunk in chunks)
        avg_chunk_size = total_words / len(chunks) if chunks else 0
        logger.info(
            f"Created {len(chunks)} chunks for document {document_id}. "
            f"Average chunk size: {avg_chunk_size:.1f} words"
        )
        return chunks
    
    def _split_into_sentences(self, text: str) -> List[str]:
        text = text.replace('\n', ' ')  
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    def _create_chunks_with_overlap(self, sentences: List[str], document_id: str) -> List[Dict[str, Any]]:
        chunks = []
        current_chunk = []
        current_word_count = 0
        chunk_index = 0
        for i, sentence in enumerate(sentences):
            sentence_words = len(sentence.split())
            if current_word_count + sentence_words > self.chunk_size and current_chunk:
                chunk_text = ' '.join(current_chunk)
                chunks.append({
                    'text': chunk_text,
                    'metadata': {
                        'document_id': document_id,
                        'chunk_index': chunk_index,
                        'start_sentence': i - len(current_chunk),
                        'end_sentence': i - 1,
                        'word_count': len(chunk_text.split())
                    }
                })
                overlap_sentences = self._get_overlap_sentences(current_chunk)
                current_chunk = overlap_sentences.copy()
                current_word_count = sum(len(s.split()) for s in current_chunk)
                chunk_index += 1
            current_chunk.append(sentence)
            current_word_count += sentence_words
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                'text': chunk_text,
                'metadata': {
                    'document_id': document_id,
                    'chunk_index': chunk_index,
                    'start_sentence': len(sentences) - len(current_chunk),
                    'end_sentence': len(sentences) - 1,
                    'word_count': len(chunk_text.split())
                }
            })
        return chunks
    
    def _get_overlap_sentences(self, sentences: List[str]) -> List[str]:
        overlap_sentences = []
        overlap_word_count = 0
        for sentence in reversed(sentences):
            sentence_words = len(sentence.split())
            if overlap_word_count + sentence_words <= self.chunk_overlap:
                overlap_sentences.insert(0, sentence)
                overlap_word_count += sentence_words
            else:
                if overlap_sentences:
                    break
                else:
                    words = sentence.split()
                    overlap_words = words[:self.chunk_overlap]
                    overlap_sentences = [' '.join(overlap_words)]
                    overlap_word_count = len(overlap_words)
                    break
        return overlap_sentences
    
    def get_chunk_statistics(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not chunks:
            return {
                'total_chunks': 0,
                'avg_chunk_size': 0,
                'min_chunk_size': 0,
                'max_chunk_size': 0,
                'total_words': 0
            }
        chunk_sizes = [chunk['metadata']['word_count'] for chunk in chunks]
        return {
            'total_chunks': len(chunks),
            'avg_chunk_size': sum(chunk_sizes) / len(chunk_sizes),
            'min_chunk_size': min(chunk_sizes),
            'max_chunk_size': max(chunk_sizes),
            'total_words': sum(chunk_sizes)
        }
    
    def chunk_document_simple(self, text: str, document_id: str, 
                              chunk_size: int = 500, overlap: int = 50) -> List[Dict[str, Any]]:
        words = text.split()
        if not words:
            return []
        chunks = []
        step = chunk_size - overlap
        for i in range(0, len(words), step):
            chunk_words = words[i:i + chunk_size]
            chunk_text = ' '.join(chunk_words)
            actual_chunk_size = len(chunk_words)
            if actual_chunk_size > 20:  
                chunk_index = len(chunks)
                chunks.append({
                    'text': chunk_text,
                    'metadata': {
                        'document_id': document_id,
                        'chunk_index': chunk_index,
                        'start_word': i,
                        'end_word': i + actual_chunk_size - 1,
                        'word_count': actual_chunk_size,
                        'chunk_size_target': chunk_size,
                        'overlap': overlap
                    }
                })
        logger.info(
            f"Simple chunking: Created {len(chunks)} chunks "
            f"from {len(words)} words"
        )
        return chunks