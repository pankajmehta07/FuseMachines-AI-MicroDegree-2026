"""
A simple retry decorator with exponential backoff.
Wraps any async function; if it raises an exception, waits and retries
up to `max_attempts` times before giving up and re-raising.
"""
import asyncio
import functools
import logging

logger = logging.getLogger("reliability.retry")


def with_retry(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts:
                        delay = base_delay * (2 ** (attempt - 1))  # 1s, 2s, 4s...
                        logger.warning(
                            f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e}. "
                            f"Retrying in {delay}s..."
                        )
                        await asyncio.sleep(delay)
                    else:
                        logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
            raise last_exception
        return wrapper
    return decorator