import requests
import json
import re

OLLAMA_MODEL = "mistral"
OLLAMA_URL = "http://localhost:11434/api/generate"


def extract_event_details(email_text):
    prompt = f"""
You are an AI assistant that extracts calendar event details from emails.
Extract the following from the email below:
- Title (what the event is)
- Start time and end time (in YYYY-MM-DD HH:MM format if possible)
- Location (URL or venue if available)

Respond only in JSON format like this:
{{
  "title": "Event name",
  "start_time": "YYYY-MM-DD HH:MM",
  "end_time": "YYYY-MM-DD HH:MM",
  "location": "Event link or address"
}}

EMAIL:
{email_text}
"""

    response = requests.post(OLLAMA_URL, json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    })

    if response.status_code != 200:
        print("❌ Ollama error:", response.text)
        return None

    result = response.json().get("response", "")
    print("🤖 Ollama response:", result)

    try:
        # Try to extract JSON using regex
        match = re.search(r"\{[\s\S]*?\}", result)
        if not match:
            print("❌ No JSON found.")
            return None

        return json.loads(match.group())
    except Exception as e:
        print("❌ Failed to parse Ollama output:", e)
        return None
