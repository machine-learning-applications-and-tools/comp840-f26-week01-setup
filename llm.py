"""
Shared helper for talking to the Gemini API.

Every lab in this course should call generate() from this file rather than
using the SDK directly. It does three things for you:

  1. Throttles requests so you stay under the free-tier limit (5 per minute).
  2. Retries automatically when the API says "slow down" or has a hiccup.
  3. Keeps a running count of calls and tokens, so you can see what a lab cost.

Usage:
    from llm import generate

    resp = generate("Why is the sky blue?")
    print(resp.text)
"""

import random
import time
import logging
logging.getLogger("google_genai.models").setLevel(logging.ERROR)

from dotenv import load_dotenv
from google import genai
from google.genai import errors

from config import MODEL, REQUESTS_PER_MINUTE

load_dotenv()

client = genai.Client()

# Minimum seconds between calls to the same model, derived from the quota.
_MIN_INTERVAL = 60.0 / REQUESTS_PER_MINUTE

# When did we last call each model? Keyed by model name because the free-tier
# quota is enforced per model -- using two models gives you two budgets.
_last_call = {}

# Running totals for the whole script run.
stats = {"calls": 0, "retries": 0, "input_tokens": 0, "output_tokens": 0}


def _is_rate_limit(err):
    return getattr(err, "code", None) == 429 or "429" in str(err)


def _throttle(model):
    """Sleep just long enough that we don't exceed the per-minute quota."""
    last = _last_call.get(model)
    if last is not None:
        elapsed = time.monotonic() - last
        if elapsed < _MIN_INTERVAL:
            time.sleep(_MIN_INTERVAL - elapsed)
    _last_call[model] = time.monotonic()


def generate(contents, config=None, model=None, max_retries=6, verbose=True):
    """
    Call the model, waiting and retrying as needed.

    contents -- a string, or a list of types.Content for multi-turn calls
    config   -- an optional types.GenerateContentConfig (tools, temperature, ...)
    model    -- override the default model from config.py
    """
    model = model or MODEL

    for attempt in range(max_retries):
        _throttle(model)
        try:
            resp = client.models.generate_content(
                model=model, contents=contents, config=config
            )
        except errors.ClientError as e:
            if not _is_rate_limit(e) or attempt == max_retries - 1:
                raise
            wait = min(2**attempt, 60) + random.uniform(0, 1)
            stats["retries"] += 1
            if verbose:
                print(f"  [rate limited, waiting {wait:.1f}s]")
            time.sleep(wait)
        except errors.ServerError as e:
            # 5xx: the API is having a bad moment. Not our fault, still retry.
            if attempt == max_retries - 1:
                raise
            wait = min(2**attempt, 30) + random.uniform(0, 1)
            stats["retries"] += 1
            if verbose:
                print(f"  [server error {e}, retrying in {wait:.1f}s]")
            time.sleep(wait)
        else:
            stats["calls"] += 1
            usage = getattr(resp, "usage_metadata", None)
            if usage:
                stats["input_tokens"] += usage.prompt_token_count or 0
                stats["output_tokens"] += usage.total_token_count or 0
            return resp

    raise RuntimeError(f"gave up after {max_retries} attempts")


def report():
    """Print what this script run consumed. Call at the end of a lab."""
    print(
        f"\n{stats['calls']} calls"
        f" | {stats['retries']} retries"
        f" | {stats['input_tokens']} input tokens"
        f" | {stats['output_tokens']} total tokens"
    )
