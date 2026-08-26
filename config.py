"""Course-wide settings"""

# Verified working 26 August 2026. A 404 means the model was withdrawn.
# To list what is available:
#   python -c "from google import genai; c=genai.Client(); [print(m.name) for m in c.models.list()]"
# The model uses by default.
MODEL = "gemini-3.5-flash-lite"

# Alternates.
MODEL_TEMP_VARIATION = "gemini-3-flash-preview"
MODEL_SMALL = "gemini-3.5-flash-lite"
MODEL_LARGE = "gemini-3.7-flash"

# Free-tier quota is 5 requests per minute, per project, PER MODEL.
REQUESTS_PER_MINUTE = 15
