import json
from openai import OpenAI
from fastapi import HTTPException

from app.config import OPENAI_API_KEY, OPENAI_MODEL, SYSTEM_PROMPT
from app.schemas import ChatRequest, ChatResponse
from app.providers.base import LLMProvider
from app.tools.registry import TOOL_DEFINITIONS, TOOL_DISPATCH


class OpenAIProvider(LLMProvider):
    def __init__(self):
        self._client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

    async def chat(self, req: ChatRequest) -> ChatResponse:
        if not self._client:
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": req.message},
        ]

        kwargs = dict(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=req.temperature,
            top_p=req.top_p,
            max_tokens=req.max_tokens,
        )
        if req.use_tools:
            kwargs["tools"] = TOOL_DEFINITIONS
            kwargs["tool_choice"] = "auto"

        completion = self._client.chat.completions.create(**kwargs)
        message = completion.choices[0].message

        tool_calls_log = None

        # If the model wants to call a tool, execute it and ask again with the result
        if message.tool_calls:
            tool_calls_log = []
            messages.append(message.model_dump(exclude_none=True))

            for call in message.tool_calls:
                fn_name = call.function.name
                fn_args = json.loads(call.function.arguments or "{}")
                result = TOOL_DISPATCH.get(fn_name, lambda **_: {"error": "unknown tool"})(**fn_args)

                tool_calls_log.append({"name": fn_name, "arguments": fn_args, "result": result})

                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result),
                })

            # Second call: model incorporates tool result into final answer
            followup = self._client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                temperature=req.temperature,
                top_p=req.top_p,
                max_tokens=req.max_tokens,
            )
            reply = followup.choices[0].message.content
        else:
            reply = message.content

        return ChatResponse(provider="openai", model=OPENAI_MODEL, reply=reply, tool_calls=tool_calls_log)