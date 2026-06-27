
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.chunking import TextChunker
from app.config import settings

def test_chunking():
    
    sample_text = """
    Artificial intelligence (AI) is the simulation of human intelligence in machines 
    that are programmed to think and learn. The modern field of AI came into existence 
    in 1956, but it took decades of work to make significant progress. 
    
    Machine learning is a subset of AI that enables systems to learn and improve from 
    experience. Deep learning, a further subset of machine learning, uses neural networks 
    with many layers. These neural networks attempt to simulate the behavior of the 
    human brain—albeit far from matching its ability—in order to "learn" from large 
    amounts of data. 
    
    Natural language processing (NLP) is another important area of AI. It deals with 
    the interaction between computers and human language. Applications of NLP include 
    speech recognition, sentiment analysis, and machine translation.
    
    Large language models (LLMs) like GPT-4 and Gemini are the latest advancement in AI. 
    They are trained on massive datasets and can generate human-like text, answer 
    questions, and even write code.
    
    The ethical implications of AI are significant. Issues include bias in algorithms, 
    privacy concerns, job displacement, and the potential for misuse. As AI continues 
    to advance, it's crucial to develop responsible AI practices.
    """
    
    print("=" * 60)
    print("TESTING TEXT CHUNKING")
    print("=" * 60)
    chunker = TextChunker(chunk_size=50, chunk_overlap=20)
    print(f"Chunk size: {chunker.chunk_size} words")
    print(f"Chunk overlap: {chunker.chunk_overlap} words")
    print()
    

    chunks = chunker.chunk_document(sample_text, "test_doc_123")
 
    print(f"Created {len(chunks)} chunks")
    print()
    
    for i, chunk in enumerate(chunks):
        word_count = chunk['metadata']['word_count']
        text_preview = chunk['text'][:100] + "..." if len(chunk['text']) > 100 else chunk['text']
        print(f"Chunk {i+1}: {word_count} words")
        print(f"Preview: {text_preview}")
        print("-" * 40)
    stats = chunker.get_chunk_statistics(chunks)
    print("STATISTICS:")
    print(f"  Total chunks: {stats['total_chunks']}")
    print(f"  Average chunk size: {stats['avg_chunk_size']:.1f} words")
    print(f"  Min chunk size: {stats['min_chunk_size']} words")
    print(f"  Max chunk size: {stats['max_chunk_size']} words")
    print(f"  Total words: {stats['total_words']}")
    print("\nVERIFYING OVERLAP:")
    if len(chunks) > 1:
        chunk1_words = chunks[0]['text'].split()
        chunk2_words = chunks[1]['text'].split()
        overlap_found = False
        for i in range(min(50, len(chunk1_words))):
            if chunk1_words[-i:] == chunk2_words[:i] and i > 0:
                print(f"  ✓ Overlap found: {i} words")
                overlap_found = True
                break
        
        if not overlap_found:
            print("  ⚠ No overlap detected (check implementation)")
    else:
        print("  Only one chunk, no overlap to verify")
    
    print("=" * 60)
    print("TEST COMPLETE")

if __name__ == "__main__":
    test_chunking()