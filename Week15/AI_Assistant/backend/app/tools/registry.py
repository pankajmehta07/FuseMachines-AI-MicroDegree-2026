"""
Central place that:
1. Describes each tool in OpenAI/Gemini function-calling JSON schema format
2. Maps tool names to their actual Python implementation
This is what the LLM "sees" as its available tools.
"""
from app.tools.implementations import calculator, get_current_datetime

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate a basic arithmetic expression (numbers, + - * / and parentheses only).",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The arithmetic expression to evaluate, e.g. '12 * (3 + 4)'",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Get the current UTC date and time.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

TOOL_DISPATCH = {
    "calculator": calculator,
    "get_current_datetime": get_current_datetime,
}