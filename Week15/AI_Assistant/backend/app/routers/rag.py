"""
Endpoints:
- POST /rag/ingest/text - paste raw text directly
- POST /rag/ingest/file - upload a .txt or .pdf file
- POST /rag/query - ask a question; retrieves relevant chunks and
                     asks the LLM to answer using them as context
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from io import BytesIO

from app.rag.pipeline import ingest_document, retrieve_context
from app.schemas import (
    IngestTextRequest, IngestResponse,
    RagQueryRequest, RagQueryResponse, RetrievedChunk,
)
from app.providers import PROVIDER_REGISTRY
from app.schemas import ChatRequest

router = APIRouter(prefix="/rag", tags=["rag"])


@router.post("/ingest/text", response_model=IngestResponse)
def ingest_text(req: IngestTextRequest):
    count = ingest_document(req.text, source=req.source)
    return IngestResponse(source=req.source, chunks_created=count)


@router.post("/ingest/file", response_model=IngestResponse)
async def ingest_file(file: UploadFile = File(...)):
    content = await file.read()

    if file.filename.lower().endswith(".pdf"):
        from pypdf import PdfReader
        reader = PdfReader(BytesIO(content))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    elif file.filename.lower().endswith(".txt"):
        text = content.decode("utf-8", errors="ignore")
    else:
        raise HTTPException(status_code=400, detail="Only .pdf and .txt files are supported")

    count = ingest_document(text, source=file.filename)
    return IngestResponse(source=file.filename, chunks_created=count)


@router.post("/query", response_model=RagQueryResponse)
async def rag_query(req: RagQueryRequest):
    hits = retrieve_context(req.question, top_k=req.top_k)

    if not hits:
        raise HTTPException(status_code=404, detail="No documents ingested yet - nothing to search")

    # Build a prompt that grounds the LLM's answer in the retrieved chunks
    context_block = "\n\n".join(f"[{h['source']}]: {h['text']}" for h in hits)
    grounded_message = (
        f"Answer the question using ONLY the context below. "
        f"If the answer isn't in the context, say you don't know.\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question: {req.question}"
    )

    provider = PROVIDER_REGISTRY.get(req.provider)
    if provider is None:
        raise HTTPException(status_code=400, detail=f"Unknown provider '{req.provider}'")

    chat_req = ChatRequest(message=grounded_message, provider=req.provider)
    chat_response = await provider.chat(chat_req)

    return RagQueryResponse(
        provider=chat_response.provider,
        model=chat_response.model,
        answer=chat_response.reply,
        retrieved_chunks=[RetrievedChunk(**h) for h in hits],
    )
