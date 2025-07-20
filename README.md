# Auto Calendar from Email

📧 → 🧠 → 📅

This project reads your unread Gmail emails, extracts calendar event information using an LLM (Ollama), and automatically creates Google Calendar events.

## Setup

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add:
   - `client_secret.json` (OAuth credentials)
   - Gmail app password (for IMAP)
4. Run: `python main.py`

## Features

- Uses Ollama + mistral for parsing
- Adds events to Google Calendar
- Works with Gmail via IMAP