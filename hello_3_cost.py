"""
hello_3_cost.py

One API call, then some arithmetic: what would 10,000 calls like this one
actually cost?

Every response from the model comes back with a token count attached --
tokens are the chunks of text the model reads and writes internally,
roughly 4 characters each for English. Providers bill per token, and
input tokens (your prompt) are priced differently from output tokens
(the model's reply).

How to run this file:
    Windows:   python hello_3_cost.py
    Mac:       python3 hello_3_cost.py
"""

from llm import generate

# ---------------------------------------------------------------------
# PRICING USD per 1 million tokens.
#
# These numbers WILL go stale. Prices change, and course labs run for
# years. Verify the current numbers at: https://ai.google.dev/pricing
# ---------------------------------------------------------------------
PRICING = {
    "flash": {"input_per_million": 0.075, "output_per_million": 0.30},
    "pro":   {"input_per_million": 1.25,  "output_per_million": 5.00},
}

N_CALLS = 10_000

# --- 1. Make one call and read the token counts off the response -------
prompt = "In one sentence, what is an AI agent?"
response = generate(prompt)

usage = response.usage_metadata
input_tokens = usage.prompt_token_count
output_tokens = usage.candidates_token_count
total_tokens = usage.total_token_count

print("Prompt: ", prompt)
print("Answer: ", response.text.strip())
print()
print("Tokens for this one call:")
print(f"  input:  {input_tokens}")
print(f"  output: {output_tokens}")
print(f"  total:  {total_tokens}")

#print(response.usage_metadata)

# --- 2. Extrapolate: what would N_CALLS calls like this one cost? ------
print(f"\nIf every one of {N_CALLS:,} calls used the same number of tokens "
      f"as this one:")

for tier, rates in PRICING.items():
    input_cost = (input_tokens * N_CALLS / 1_000_000) * rates["input_per_million"]
    output_cost = (output_tokens * N_CALLS / 1_000_000) * rates["output_per_million"]
    total_cost = input_cost + output_cost
    print(
        f"  {tier:5s}: {N_CALLS:,} calls -> "
        f"${input_cost:,.2f} input + ${output_cost:,.2f} output "
        f"= ${total_cost:,.2f} total"
    )

print("\n(Rates above are illustrative -- verify at ai.google.dev/pricing "
      "before using them to make a real decision.)")
