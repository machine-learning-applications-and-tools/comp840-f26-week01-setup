"""
Confirms that function calling works end to end.

This is one full turn of the agent loop:
    ask -> model requests a tool -> we run it -> model answers using the result
"""

from google.genai import types

from llm import generate, report

# --- 1. Describe a tool to the model ------------------------------------
get_weather = {
    "name": "get_weather",
    "description": "Get the current temperature for a city.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name, e.g. Boston"}
        },
        "required": ["city"],
    },
}

config = types.GenerateContentConfig(
    tools=[types.Tool(function_declarations=[get_weather])],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)

question = "What's the weather in Boston right now?"

# --- 2. Ask. The model should ask us to run the tool ---------------------
resp = generate(question, config=config)

call = None
for part in resp.candidates[0].content.parts:
    if getattr(part, "function_call", None):
        call = part.function_call
        break

if call is None:
    print("NO TOOL CALL -- the model answered with text instead:")
    print(resp.text)
    raise SystemExit(1)

print(f"Model asked for: {call.name}({dict(call.args)})")

# --- 3. "Run" the tool. A real tool would call a weather API here --------
result = {"temperature_c": 18, "conditions": "cloudy"}
print(f"We answered:     {result}")

# --- 4. Hand the result back and let the model finish -------------------
contents = [
    types.Content(role="user", parts=[types.Part(text=question)]),
    resp.candidates[0].content,
    types.Content(
        role="user",
        parts=[types.Part.from_function_response(name=call.name, response=result)],
    ),
]

final = generate(contents, config=config)
print(f"\nFinal answer:    {final.text}")

report()
