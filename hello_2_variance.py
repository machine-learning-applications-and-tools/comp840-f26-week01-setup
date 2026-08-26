"""
hello_2_variance.py

Same short prompt, asked five times at temperature=1.0 and then five times
at temperature=0.0. Watch what changes.

"Temperature" controls how much randomness the model uses when picking its
next word. High temperature (close to 1.0 here) lets it take more chances,
so the wording -- sometimes the content -- shifts from run to run. Low
temperature (0.0) pushes it toward the single most likely answer each time,
so repeats tend to look the same, or nearly so.

This is not a bug to work around. Language models are non-deterministic by
default: the same prompt can produce different output every time you run
it. Some labs later in the course will care about that a lot.

How to run this file:
    Windows:   python hello_2_variance.py
    Mac:       python3 hello_2_variance.py

Note: this script makes 10 calls. At 5 requests/minute (the free-tier
limit), that takes a little over a minute -- generate() handles the
waiting for you, so just let it run.
"""

from google.genai import types

from llm import generate, report

prompt = "Give a short description of happiness. Use exactly two sentences."


def ask_five_times(temperature):
    # GenerateContentConfig is how we pass options -- like temperature --
    # to the model. Without it, generate() just uses the model's defaults.
    config = types.GenerateContentConfig(temperature=temperature)

    for i in range(1, 4):  # range(1, 6) counts 1, 2, 3
        response = generate(prompt, config=config)
        print(f"  {i}. {response.text.strip()}")


print(f"Prompt: {prompt!r}\n")

print("Temperature = 1.5 (more random)")
ask_five_times(temperature=1.5)

print("\nTemperature = 0.0 (least random)")
ask_five_times(temperature=0.0)

report()
