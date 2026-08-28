import json
from fastapi import APIRouter, HTTPException

from app.config import OPENAI_API_KEY, OPENAI_MODEL, SYSTEM_PROMPT
from app.schemas import TaskExtractionRequest, TaskExtractionResponse, ExtractedTask
from openai import OpenAI

router = APIRouter(prefix="/structured", tags=["structured-output"])

_openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

EXTRACTION_PROMPT = (
    "Extract a single task from the user's text. "
    "Respond ONLY with valid JSON matching this schema: "
    '{"task_title": str, "assignee": str|null, "due_date": str|null, '
    '"priority": "low"|"medium"|"high", "tags": [str]}. '
    "No markdown, no extra commentary - JSON only."
)


@router.post("/extract-task", response_model=TaskExtractionResponse)
async def extract_task(req: TaskExtractionRequest):
    if req.provider == "openai":
        if not _openai_client:
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")

        completion = _openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": EXTRACTION_PROMPT},
                {"role": "user", "content": req.text},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        raw = completion.choices[0].message.content
        model_used = OPENAI_MODEL

    elif req.provider == "local":
        import httpx
        from app.config import LOCAL_LLM_URL, LOCAL_LLM_MODEL

        payload = {
            "model": LOCAL_LLM_MODEL,
            "messages": [
                {"role": "system", "content": EXTRACTION_PROMPT},
                {"role": "user", "content": req.text},
            ],
            "format": "json",
            "stream": False,
            "options": {"temperature": 0.2},
        }
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(f"{LOCAL_LLM_URL}/api/chat", json=payload)
            resp.raise_for_status()
            raw = resp.json()["message"]["content"]
        model_used = LOCAL_LLM_MODEL

    elif req.provider == "gemini":
        from google import genai
        from app.config import GEMINI_API_KEY, GEMINI_MODEL

        if not GEMINI_API_KEY:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY not configured")

        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=f"{EXTRACTION_PROMPT}\n\nText: {req.text}",
            config={"temperature": 0.2, "response_mime_type": "application/json"},
        )
        raw = response.text
        model_used = GEMINI_MODEL

    else:
        raise HTTPException(status_code=400, detail="Unknown provider")

    try:
        parsed = json.loads(raw)
        extracted = ExtractedTask(**parsed)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Model did not return valid structured JSON: {e}")

    return TaskExtractionResponse(provider=req.provider, model=model_used, extracted=extracted)