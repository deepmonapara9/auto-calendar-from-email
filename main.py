from email_reader import fetch_unread_emails
from llm_parser import extract_event_details
from calendar_handler import create_event
from dotenv import load_dotenv
import os

load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

emails = fetch_unread_emails(EMAIL, PASSWORD)

for email_obj in emails:
    print("\n📨 Subject:", email_obj["subject"])
    parsed = extract_event_details(email_obj["body"])

    if parsed:
        print("✅ Parsed:", parsed)

        if all([parsed.get('title'), parsed.get('start_time'), parsed.get('end_time')]):
            create_event(parsed)
        else:
            print("⚠️ Incomplete event data. Skipping calendar creation.")
    else:
        print("❌ Could not extract event.")
