"""
Actual Python functions the AI is allowed to call.
Each function should be small, pure, and safe - the model only ever
gets to call what's explicitly defined here.
"""
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def calculator(expression: str) -> dict:
    """
    Safely evaluates a basic arithmetic expression.
    Only allows numbers and + - * / ( ) . to avoid arbitrary code execution.
    """
    allowed_chars = set("0123456789+-*/(). ")
    if not set(expression) <= allowed_chars:
        return {"error": "Expression contains disallowed characters"}
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"error": str(e)}


# def get_current_datetime():
#     """Returns the current UTC date and time."""
#     now = datetime.now(timezone.utc)
#     return {
#         "utc_datetime": now.isoformat(),
#         "date": now.strftime("%Y-%m-%d"),
#         "time": now.strftime("%H:%M:%S"),
#         "weekday": now.strftime("%A"),
#     }


def get_current_datetime() -> dict:
    """Returns the current date and time."""
    now = datetime.now(ZoneInfo("Asia/Kathmandu"))

    return {
        "datetime": now.isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "weekday": now.strftime("%A"),
        "timezone": "Asia/Kathmandu",
    }