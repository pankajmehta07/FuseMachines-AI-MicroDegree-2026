"""
Splits long text into overlapping chunks small enough for the embedding
model and the LLM's context window to handle well.

Why overlap? If a sentence's meaning spans a chunk boundary, overlap
means it still appears whole in at least one chunk - reduces the chance
of losing context right at a cut point.
"""

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    chunk_size: max characters per chunk
    overlap: how many characters from the end of one chunk are repeated
             at the start of the next
    """
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap  # move forward, but re-include the overlap

    return chunks