"""
Ties the RAG pieces together: ingestion (chunk -> embed -> store) and
retrieval (embed query -> search -> return relevant chunks).
"""
from app.rag.chunking import chunk_text
from app.rag.embeddings import embed_texts
from app.rag.vector_store import add_chunks, search


def ingest_document(text: str, source: str) -> int:
    """Returns the number of chunks created."""
    chunks = chunk_text(text)
    if not chunks:
        return 0
    embeddings = embed_texts(chunks)
    add_chunks(chunks, embeddings, source)
    return len(chunks)


def retrieve_context(query: str, top_k: int = 3) -> list[dict]:
    query_embedding = embed_texts([query])[0]
    return search(query_embedding, top_k=top_k)