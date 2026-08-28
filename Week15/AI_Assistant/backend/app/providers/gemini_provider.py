from google import genai
from google.genai import types
from fastapi import HTTPException

from app.config import GEMINI_API_KEY, GEMINI_MODEL, SYSTEM_PROMPT
from app.schemas import ChatRequest, ChatResponse
from app.providers.base import LLMProvider
from app.tools.registry import TOOL_DEFINITIONS, TOOL_DISPATCH


def _convert_schema_types(schema: dict) -> dict:
    converted = dict(schema)

    if "type" in converted and isinstance(converted["type"], str):
        converted["type"] = converted["type"].upper()

    if "properties" in converted:
        converted["properties"] = {
            k: _convert_schema_types(v)
            for k, v in converted["properties"].items()
        }

    if "items" in converted:
        converted["items"] = _convert_schema_types(converted["items"])

    return converted

def _to_gemini_tools() -> list[types.Tool]:
    declarations = []

    for tool in TOOL_DEFINITIONS:
        fn = tool["function"]

        declarations.append(
            types.FunctionDeclaration(
                name=fn["name"],
                description=fn["description"],
                parameters=_convert_schema_types(fn["parameters"]),
            )
        )

    return [types.Tool(function_declarations=declarations)]


class GeminiProvider(LLMProvider):

    def __init__(self):
        self._client = (
            genai.Client(api_key=GEMINI_API_KEY)
            if GEMINI_API_KEY
            else None
        )

    async def chat(self, req: ChatRequest) -> ChatResponse:

        if not self._client:
            raise HTTPException(
                status_code=500,
                detail="GEMINI_API_KEY not configured"
            )

        config_kwargs = {
            "system_instruction": SYSTEM_PROMPT,
            "temperature": req.temperature,
            "top_p": req.top_p,
            "max_output_tokens": req.max_tokens,
        }

        if req.use_tools:
            config_kwargs["tools"] = _to_gemini_tools()

        config = types.GenerateContentConfig(**config_kwargs)

        # Stateful chat session
        chat = self._client.chats.create(
            model=GEMINI_MODEL,
            config=config,
        )

        tool_calls_log = []

        response = chat.send_message(req.message)

        # Keep executing tools until Gemini returns text.
        while True:

            parts = response.candidates[0].content.parts

            function_calls = [
                p.function_call
                for p in parts
                if getattr(p, "function_call", None)
            ]

            if not function_calls:
                break

            tool_results = []

            for fc in function_calls:

                name = fc.name
                args = dict(fc.args or {})

                handler = TOOL_DISPATCH.get(name)

                if handler is None:
                    result = {
                        "error": f"Unknown tool '{name}'"
                    }
                else:
                    try:
                        result = handler(**args)
                    except Exception as e:
                        result = {
                            "error": str(e)
                        }

                tool_calls_log.append(
                    {
                        "name": name,
                        "arguments": args,
                        "result": result,
                    }
                )

                tool_results.append(
                    types.Part.from_function_response(
                        name=name,
                        response=result,
                    )
                )

            # Send tool outputs back.
            response = chat.send_message(tool_results)

        return ChatResponse(
            provider="gemini",
            model=GEMINI_MODEL,
            reply=response.text,
            tool_calls=tool_calls_log if tool_calls_log else None,
        )