# AI Assistant — Week 15 Assignment

An AI assistant built with modern LLM APIs and RAG architecture (Task 1), 
productionized into a reliable, containerized web application (Task 2).

## Table of Contents
1. Overview
2. Architecture
3. Tech Stack & Design Decisions
4. Project Structure
5. Environment Configuration (.env)
6. Setup & Running Instructions
7. API Endpoints
8. Core Functionality Details
9. Reliability Features
10. Performance Engineering
11. Model Optimization (ONNX) — Justification
12. Known Limitations
13. Testing the Application

---

## 1. Overview

This project implements an AI assistant with:
- Multi-provider LLM integration (OpenAI, Google Gemini, local Qwen2.5-coder via Ollama)
- Prompt engineering with configurable temperature/top_p
- Structured JSON output extraction
- Tool/function calling
- A full RAG (Retrieval-Augmented Generation) pipeline
- A Streamlit web UI
- Production reliability features: retry logic, rate limiting, provider/model fallback, graceful error handling
- Full Docker containerization (no host dependencies beyond Docker + native Ollama for model weights)

## 2. Architecture

```
    ┌───────────────────┐       ┌───────────────────────────────────────────┐
    │                   │ HTTP  │              Backend (FastAPI)            │
    │   Streamlit UI    │──────▶│                                           │
    │   (port 8501)     │       │  ┌─────────────┐      ┌─────────────────┐ │
    │                   │       │  │  Routers    │      │   Reliability   │ │
    └───────────────────┘       │  │  /chat      │─────▶│  - retry        │ │
                                │  │  /structured│      │  - fallback     │ │
                                │  │  /rag       │      │  - rate limit   │ │
                                │  │  /health    │      └─────────────────┘ │
                                │  └──────┬──────┘                          │
                                │         │                                 │
                                │  ┌──────▼────────────────────────────┐    │
                                │  │    Provider Abstraction Layer     │    │
                                │  │   (LLMProvider base + registry)   │    │
                                │  └────┬──────────┬──────────┬────────┘    │
                                │       │          │          │             │
                                │    OpenAI      Gemini    Local (Ollama)   │
                                │                                           │
                                │  ┌────────────────────────────────────┐   │
                                │  │           RAG Pipeline             │   │
                                │  │  Chunking → Embeddings (local)     │   │
                                │  │       → ChromaDB (vector store)    │   │
                                │  └────────────────────────────────────┘   │
                                └────────────────────┬──────────────────────┘
                                                     │
                                ┌────────────────────▼──────────────────────┐
                                │     Ollama Container (port 11435)         │
                                │      Serving: qwen2.5-coder:3b            │
                                └───────────────────────────────────────────┘
```

**Data flow for a normal chat request:**
1. User sends message via Streamlit UI
2. Backend receives it at `/chat`, rate-limiter checks the client isn't over quota
3. Request routed to selected provider through the fallback wrapper
4. Fallback wrapper calls the provider with retry (exponential backoff on failure)
5. If the chosen provider fails, it automatically tries the next provider in priority order (local → gemini → openai)
6. Response returned to UI

**Data flow for a RAG query:**
1. User's question is embedded into a vector (using local sentence-transformers model)
2. ChromaDB is searched for the most similar previously-ingested chunks
3. Retrieved chunks + question are combined into a grounding prompt
4. Prompt sent to the selected LLM provider, which answers using only the provided context
5. Answer + the retrieved chunks (with similarity distance) returned to UI for transparency

## 3. Tech Stack & Design Decisions

| Component | Choice | Reasoning |
|---|---|---|
| Backend framework | FastAPI | Async-native, automatic docs, clean typing via Pydantic |
| Cloud LLM providers | OpenAI (gpt-4o-mini) + Google Gemini (gemini-3.6-flash) | OpenAI is on the assignment's approved list but has no free tier (requires prepaid credits); Gemini added as a genuinely free-tier-compatible alternative, also on the approved list |
| Local LLM serving | Ollama serving Qwen2.5-coder:3b (GGUF format) | See Section 11 (ONNX justification) for why Ollama/GGUF was chosen over vLLM/ONNX on CPU-only hardware |
| Vector database | ChromaDB (embedded/persistent mode) | Runs in-process inside the backend container — no separate server container needed, minimal RAM footprint |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`), local | ~80MB model, runs on CPU, no API key/quota needed, avoids adding a 4th external dependency |
| Frontend | Streamlit | Pure Python, no separate JS/Node build step, lighter weight than React for a constrained machine |
| Rate limiting | slowapi | Lightweight, built specifically for FastAPI/Starlette |
| Containerization | Docker Compose, 3 services (ollama, backend, frontend) | Fully isolated environments; no venv needed since each container manages its own Python environment |

## 4. Project Structure

```
    ai-assistant/
    ├── docker-compose.yml
    ├── .env
    ├── .gitignore
    ├── README.md
    ├── backend/
    │ ├── Dockerfile
    │ ├── requirements.txt
    │ └── app/
    │ ├── init.py
    │ ├── main.py               # FastAPI app factory, router registration
    │ ├── config.py             # centralized env/config loading
    │ ├── schemas.py            # all Pydantic request/response models
    │ ├── providers/
    │ │ ├── init.py             # PROVIDER_REGISTRY
    │ │ ├── base.py             # LLMProvider abstract interface
    │ │ ├── openai_provider.py
    │ │ ├── local_provider.py
    │ │ └── gemini_provider.py
    │ ├── tools/
    │ │ ├── init.py
    │ │ ├── implementations.py  # calculator, get_current_datetime
    │ │ └── registry.py         # tool definitions + dispatch map
    │ ├── rag/
    │ │ ├── init.py
    │ │ ├── chunking.py         # text splitting
    │ │ ├── embeddings.py       # sentence-transformers wrapper
    │ │ ├── vector_store.py     # ChromaDB wrapper
    │ │ └── pipeline.py         # ingestion + retrieval orchestration
    │ ├── reliability/
    │ │ ├── init.py
    │ │ ├── retry.py            # retry decorator with backoff
    │ │ ├── fallback.py         # provider fallback logic
    │ │ └── rate_limiter.py     # shared slowapi Limiter instance
    │ └── routers/
    │ ├── init.py
    │ ├── health.py
    │ ├── chat.py
    │ ├── structured.py
    │ └── rag.py
    └── frontend/
    │ ├── Dockerfile
    │ ├── requirements.txt
    │ └── app.py
```

## 5. Environment Configuration (.env)

Fill in your real API keys:

### OpenAI (note: requires prepaid billing credits, no free tier available)

```bash
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
```

### Google Gemini (free tier available at https://aistudio.google.com/apikey)

```bash
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-3.6-flash
GEMINI_FALLBACK_MODEL=gemini-3.5-flash-lite
```

### Ports (host-side; change if these conflict with something else on your machine)

```bash
BACKEND_PORT=8000
FRONTEND_PORT=8501
OLLAMA_PORT=11435
```

### Local model configuration

```bash
LOCAL_LLM_MODEL=qwen2.5-coder:3b
```


**Notes:**
- `.env` is gitignored — never commit real API keys.
- `OLLAMA_PORT` defaults to `11435` (not the standard `11434`) to avoid conflicting with a native Ollama installation that may already be running on the host machine for other purposes.
- `GEMINI_FALLBACK_MODEL` is used automatically if the primary `GEMINI_MODEL` hits a rate limit (HTTP 429) — see Section 9.

## 6. Setup & Running Instructions

### Prerequisites
- Docker and Docker Compose installed
- A Google Gemini API key (free): https://aistudio.google.com/apikey
- (Optional) An OpenAI API key with billing enabled, if you want to test that provider live

### Steps

```bash
# 1. Clone/download the project, then navigate into it
cd ai-assistant

# 2. Set up environment variables
# Edit .env and paste in your real API keys

# 3. Build and start all containers (first run downloads ~1-2GB of dependencies:
#    PyTorch for embeddings, the Ollama image, etc. Be patient on first build.)
docker compose up --build

# 4. In a separate terminal, pull the local model into the Ollama container
#    (this is a fresh Ollama instance inside Docker - separate from any
#    native Ollama install on your host machine)
docker exec -it local-llm ollama pull qwen2.5-coder:3b

# 5. Open the app
#    Web UI:      http://localhost:8501
#    API docs:    http://localhost:8000/docs (auto-generated by FastAPI)
```

### Stopping / restarting

```bash
docker compose down          # stop containers, keep data (volumes persist)
docker compose down -v       # stop containers AND wipe all data (fresh start)
docker compose up -d         # restart in background
```

### Rebuilding after changing requirements.txt

```bash
docker compose up --build
```

(Code changes inside `backend/app/` and `frontend/app.py` hot-reload automatically without rebuilding, since they're mounted as volumes.)

## 7. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Backend liveness check |
| GET | `/health/local-llm` | Checks Ollama connectivity + lists available local models |
| GET | `/health/openai` | Confirms OpenAI key is loaded |
| GET | `/health/gemini` | Confirms Gemini key is loaded |
| POST | `/chat` | Main chat endpoint (provider selection, tool calling, temperature/top_p/max_tokens control) |
| POST | `/structured/extract-task` | Structured JSON output demo — extracts a task object from free text |
| POST | `/rag/ingest/text` | Ingest raw pasted text into the knowledge base |
| POST | `/rag/ingest/file` | Ingest a `.pdf` or `.txt` file |
| GET | `/rag/documents` | List everything currently stored in the vector DB |
| POST | `/rag/query` | Ask a question answered using only retrieved document context |

Full interactive API documentation (Swagger UI) is auto-generated by FastAPI at `http://localhost:8000/docs`.

## 8. Core Functionality Details

### LLM Integration
Three providers implemented behind a common `LLMProvider` interface:
- **OpenAI** (`gpt-4o-mini`) — via official `openai` Python SDK
- **Gemini** (`gemini-3.6-flash`, fallback `gemini-3.5-flash-lite`) — via official `google-genai` SDK
- **Local** (`qwen2.5-coder:3b`) — via Ollama's REST API, served in a separate container

### Prompt Engineering
- Centralized system prompt in `config.py`
- `temperature`, `top_p`, and `max_tokens` are all exposed as request parameters and adjustable live from the UI sidebar

### Structured Output
`/structured/extract-task` forces the model to return valid JSON matching a defined Pydantic schema (`ExtractedTask`: title, assignee, due date, priority, tags). Uses:
- OpenAI: `response_format={"type": "json_object"}`
- Gemini: `response_mime_type: "application/json"`
- Local: Ollama's `format: "json"` parameter

### Tool Calling
Two tools implemented: a safe arithmetic `calculator` (character-whitelisted, not raw `eval` on arbitrary input) and `get_current_datetime`. Tool definitions are stored once in OpenAI-style JSON schema format and translated per-provider (Gemini requires uppercase type names like `STRING`/`OBJECT` instead of lowercase — handled via a schema conversion function).

### RAG Pipeline
- **Chunking:** fixed-size character windows (500 chars) with 50-character overlap, to avoid losing context at chunk boundaries. (A production system might use sentence-aware or semantic chunking instead — noted as a design tradeoff.)
- **Embeddings:** local `all-MiniLM-L6-v2` model via sentence-transformers, lazy-loaded on first use to keep idle RAM usage low
- **Vector DB:** ChromaDB in persistent embedded mode, data survives container restarts via a named Docker volume
- **Retrieval + Generation:** top-k similarity search, retrieved chunks injected into a grounding prompt that instructs the model to answer only from the provided context (reduces hallucination)

## 9. Reliability Features

### Retry Mechanism
`reliability/retry.py` — a decorator (`@with_retry`) applying exponential backoff (1s, 2s, 4s...) to any async function. Applied to provider calls in the fallback layer.

### Provider Fallback
`reliability/fallback.py` — if the requested provider fails after retries, automatically tries the next provider in a priority order: `local → gemini → openai`. The response's `"provider"` and `"model"` fields always indicate which one actually answered, so fallback is transparent and traceable in the API response and logs.

### Model-Level Fallback (Gemini)
Beyond whole-provider fallback, `gemini_provider.py` independently tries a lighter fallback model (`GEMINI_FALLBACK_MODEL`) specifically when the primary model returns an HTTP 429 (rate limit/quota) error — without escalating to a full provider switch for a problem that's specific to one model.

### Rate Limiting
`slowapi`-based limiter enforcing 10 requests/minute per client IP on the `/chat` endpoint, protecting the backend from being overwhelmed.

### Error Handling & Graceful Degradation
If every provider in the fallback chain fails, the API returns a clean structured `503` JSON response (`{"error": ..., "hint": ...}`) instead of a raw Python traceback / generic 500 error.

## 10. Performance Engineering

### Concurrency
FastAPI + Uvicorn's async architecture allows the server to handle multiple in-flight requests concurrently — while one request awaits a network response (from Ollama, OpenAI, or Gemini), the event loop is free to begin processing another incoming request. The local provider's `httpx.AsyncClient` calls are fully non-blocking within this model.

**Known limitation:** the OpenAI and Gemini SDK calls (`self._client.chat.completions.create(...)` / `self._client.models.generate_content(...)`) are synchronous under the hood, even though wrapped inside `async def` methods. This means these specific calls do not yield control back to the event loop while waiting on the network the way the local provider's `httpx` calls do. Under heavy concurrent load, this could reduce achievable throughput for cloud-provider requests specifically. A fix (running these calls via `asyncio.to_thread`) was identified but deliberately not implemented in this version, to keep the provider layer simple; documented here as a known optimization opportunity for future work.

### Measured Latency

Simple end-to-end request latency (`time curl ...`), single request, no concurrent load:

| Provider | Total request time |
|---|---|
| Local (Qwen2.5-coder:3b via Ollama, CPU) | ~0.61s |
| Gemini (gemini-3.6-flash) | ~1.60s |

**Interpretation:** the local model responded faster in this test despite running on CPU with no GPU acceleration, because it has zero network round-trip — the request never leaves the machine. Gemini's higher latency here reflects network round-trip time plus cloud-side queuing/processing, not raw inference slowness; for longer or more complex responses, the cloud provider's dedicated inference hardware would likely become faster overall despite the fixed network overhead. These are single-sample measurements, not statistically rigorous benchmarks — included to demonstrate the measurement approach and directional difference, not as precise performance claims.

### Throughput
Rate limiting was used as a practical throughput demonstration: firing 12 rapid sequential requests at `/chat` resulted in the first 10 succeeding (`200 OK`) and the last 2 being rejected (`429 Too Many Requests`), confirming the configured limit of 10 requests/minute per client is correctly enforced.

## 11. Model Optimization (ONNX) — Justification for Non-Applicability

ONNX conversion was evaluated and determined **not applicable** to this project, for the following reasons:

1. **Cloud providers (OpenAI, Gemini):** These are accessed exclusively via hosted APIs. The model weights are never available to the client — there is nothing to convert. This applies to any project built on hosted LLM APIs, not a limitation specific to this implementation.

2. **Local provider (Qwen2.5-coder:3b via Ollama):** Ollama serves models in **GGUF** format, a quantization and serving format purpose-built for efficient CPU inference (via `llama.cpp` under the hood). GGUF already accomplishes the same underlying goals ONNX conversion would target — reduced precision/quantization and hardware-optimized execution. Additionally, Ollama does not natively support ONNX models; adopting ONNX would require abandoning Ollama entirely in favor of a separate ONNX Runtime serving pipeline, solely to satisfy this one requirement, at the cost of the working Ollama-based setup already in place.

This project also originally considered **vLLM** (explicitly named in the assignment) for local model serving, but vLLM's CPU backend requires a from-source build (`Dockerfile.cpu`) and benefits significantly from AVX512 CPU support — a fragile, high-setup-cost path on this project's CPU-only development machine. Ollama was substituted as a more CPU-appropriate, equally valid open-source local serving solution, and this same CPU-first reasoning extends directly to why ONNX was not pursued as an additional optimization layer on top of it.

## 12. Known Limitations

- **OpenAI provider:** implemented correctly and passes all code-level checks (valid API key, valid model, correctly formed requests, confirmed via `/v1/models`), but is blocked from producing live responses due to a $0 prepaid credit balance on the developer account — OpenAI's API requires prepaid billing with no ongoing free tier, unlike Gemini. The provider automatically falls back to Gemini/local in this scenario (see Section 9).
- **Local model tool calling:** Qwen2.5-coder:3b (3B parameters) inconsistently uses Ollama's structured `tool_calls` response field. It correctly identifies which tool to call and with what arguments, but sometimes outputs this as plain JSON-shaped text in the message content instead of the structured field our code checks for — meaning tool execution doesn't trigger for the local provider in these cases. This is a known behavior of smaller local models compared to hosted frontier models (GPT-4o, Gemini), which reliably support function calling. Verified working correctly via the Gemini provider instead.
- **RAG conversation memory:** each RAG query (`/rag/query`) is treated as an independent question; there is no conversational memory/history carried between RAG queries (this is a deliberate scope decision, not a bug).
- **Chunking strategy:** uses simple fixed-size character windows rather than sentence- or semantic-aware chunking; adequate for this project's scale but a production system would likely use a more linguistically-aware approach.
- **Calculator tool:** uses Python's `eval()` restricted to a character whitelist (digits, operators, parentheses) — safe for this scoped use case, but a production system would use a dedicated expression-parsing library instead of `eval` under any restriction.
- **Async SDK calls:** see Section 10 — OpenAI/Gemini SDK calls are synchronous under the hood despite being called from async functions; documented as a known optimization opportunity, not implemented in this version.

## 13. Testing the Application

### Health checks
```bash
curl http://localhost:8000/health
curl http://localhost:8000/health/local-llm
curl http://localhost:8000/health/openai
curl http://localhost:8000/health/gemini
```

### Basic chat (try each provider)
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is 2+2?", "provider": "local"}'
```

### Structured output
```bash
curl -X POST http://localhost:8000/structured/extract-task \
  -H "Content-Type: application/json" \
  -d '{"text": "Please ask Priya to finish the slide deck by next Friday, its urgent.", "provider": "local"}'
```

### Tool calling
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is 45 * 12, and what is todays date?", "provider": "gemini", "use_tools": true}'
```

### RAG pipeline
```bash
# Ingest
curl -X POST http://localhost:8000/rag/ingest/text \
  -H "Content-Type: application/json" \
  -d '{"text": "The Eiffel Tower was completed in 1889 and designed by Gustave Eiffel.", "source": "eiffel-facts"}'

# Query
curl -X POST http://localhost:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Who designed the Eiffel Tower?", "provider": "local"}'

# Inspect the knowledge base
curl http://localhost:8000/rag/documents
```

### Rate limiting
```bash
for i in {1..12}; do curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "hi", "provider": "local"}'; done
# Expect: ten 200s, then two 429s
```

### Fallback behavior
```bash
# Request openai (blocked by quota) - should silently succeed via fallback
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is 2+2?", "provider": "openai"}'
# Check the "provider" field in the response - it will show which provider actually answered
```
