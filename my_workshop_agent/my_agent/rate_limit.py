import asyncio
import logging
import os
import time

from google.adk.models.llm_request import LlmRequest
from google.adk.agents.callback_context import CallbackContext

logger = logging.getLogger(__name__)

INTERVAL_SECONDS = float(os.getenv("API_CALL_INTERVAL_SECONDS", "60"))
_last_call_monotonic = 0.0


async def throttle_before_model(
    callback_context: CallbackContext,
    llm_request: LlmRequest,
):
    """Wait between LLM calls to stay under free-tier RPM limits."""
    global _last_call_monotonic

    now = time.monotonic()
    if _last_call_monotonic > 0:
        elapsed = now - _last_call_monotonic
        remaining = INTERVAL_SECONDS - elapsed
        if remaining > 0:
            logger.info(
                "Rate limit: waiting %.0fs before next API call...",
                remaining,
            )
            await asyncio.sleep(remaining)

    _last_call_monotonic = time.monotonic()
    return None
