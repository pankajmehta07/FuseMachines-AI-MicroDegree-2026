import json
import httpx

from app.config import LOCAL_LLM_URL, LOCAL_LLM_MODEL, SYSTEM_PROMPT
from app.schemas import ChatRequest, ChatResponse
from app.providers.base import LLMProvider
from app.tools.registry import TOOL_DEFINITIONS, TOOL_DISPATCH


class LocalProvider(LLMProvider):
    async def chat(self, req: ChatRequest) -> ChatResponse:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": req.message},
        ]

        payload = {
            "model": LOCAL_LLM_MODEL,
            "messages": messages,
            "stream": False,
            "options": {"temperature": req.temperature, "top_p": req.top_p},
        }
        if req.use_tools:
            payload["tools"] = TOOL_DEFINITIONS

        tool_calls_log = None

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(f"{LOCAL_LLM_URL}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
            message = data["message"]

            if message.get("tool_calls"):
                tool_calls_log = []
                messages.append(message)

                for call in message["tool_calls"]:
                    fn_name = call["function"]["name"]
                    fn_args = call["function"].get("arguments", {})
                    if isinstance(fn_args, str):
                        fn_args = json.loads(fn_args or "{}")
                    result = TOOL_DISPATCH.get(fn_name, lambda **_: {"error": "unknown tool"})(**fn_args)

                    tool_calls_log.append({"name": fn_name, "arguments": fn_args, "result": result})
                    messages.append({"role": "tool", "content": json.dumps(result)})

                followup_payload = {
                    "model": LOCAL_LLM_MODEL,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": req.temperature, "top_p": req.top_p},
                }
                followup = await client.post(f"{LOCAL_LLM_URL}/api/chat", json=followup_payload)
                followup.raise_for_status()
                reply = followup.json()["message"]["content"]
            else:
                reply = message["content"]

        return ChatResponse(provider="local", model=LOCAL_LLM_MODEL, reply=reply, tool_calls=tool_calls_log)