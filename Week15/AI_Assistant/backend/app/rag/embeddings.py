"""
Wraps the embedding model. This is the piece that converts text into
a vector (a list of ~384 numbers) capturing its meaning, so that
'similar meaning' text ends up with 'similar' vectors.

Using a small local model (all-MiniLM-L6-v2) - about 80MB, runs fine
on CPU, no API key or network call needed after the first download.
"""
from sentence_transformers import SentenceTransformer

_model: SentenceTransformer | None = None


def get_embedding_model() -> SentenceTransformer:
    """
    Lazy-loaded singleton: the model is only loaded into memory the
    first time it's actually needed, not at server startup. Keeps
    startup fast and RAM usage low if RAG features are never used.
    """
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Turns a list of text chunks into a list of embedding vectors."""
    model = get_embedding_model()
    embeddings = model.encode(texts, convert_to_numpy=False)
    return [e.tolist() for e in embeddings]