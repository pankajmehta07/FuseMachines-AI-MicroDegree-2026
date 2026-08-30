"""
Wraps ChromaDB - our vector database. Stores chunk text + its embedding
+ metadata (like which document it came from), and lets us search for
the most similar chunks to a given query vector.

Using ChromaDB's embedded/persistent mode: it runs inside this same
Python process (no separate server/container), and saves data to disk
so it survives container restarts.
"""
import chromadb

_client = None
_collection = None

CHROMA_PERSIST_DIR = "/app/chroma_data"
COLLECTION_NAME = "documents"


def get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        _collection = _client.get_or_create_collection(name=COLLECTION_NAME)
    return _collection


def add_chunks(chunks: list[str], embeddings: list[list[float]], source: str):
    collection = get_collection()
    ids = [f"{source}-{i}" for i in range(len(chunks))]
    metadatas = [{"source": source, "chunk_index": i} for i in range(len(chunks))]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )


def search(query_embedding: list[float], top_k: int = 3) -> list[dict]:
    collection = get_collection()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    hits = []
    for doc, meta, distance in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        hits.append({"text": doc, "source": meta["source"], "distance": distance})
    return hits