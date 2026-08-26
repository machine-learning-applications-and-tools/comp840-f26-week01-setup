"""
hello_1_call.py

Your very first program in this course: one call to a language model.

How to run this file:
    Windows:   python hello_1_call.py
    Mac:       python3 hello_1_call.py
"""

# generate() is a helper (defined in llm.py, in this same folder) that sends
# a prompt to the model and handles the annoying parts -- rate limits,
# retries -- for you. You will use it in every lab this term.
from llm import generate

# The prompt is just a Python string: text wrapped in quotes. This is the
# question we are going to send to the model.
prompt = "In one paragraph, what is an AI agent?"

# This line does the actual work: it sends `prompt` to the model and waits
# for a response. The response comes back as an object with several pieces
# of information attached to it (we only need one piece today: the text).
#
# We store that response in a variable named `response` so we can use it
# on the next line. A variable is just a name we choose that points at a
# value -- here, it points at whatever generate() gives back.
response = generate(prompt)

# print() displays text in the terminal. response.text is the model's
# reply -- the ".text" part reaches into the response object and pulls out
# just the answer, as a plain string.
print("Prompt: ", prompt)
print("Answer: ", response.text)
