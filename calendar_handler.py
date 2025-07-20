from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/calendar']


def format_to_rfc3339(dt_str):
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        return dt.isoformat()
    except Exception as e:
        print("❌ Time format error:", e)
        return None


def get_calendar_service():
    creds = None
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)
    return build('calendar', 'v3', credentials=creds)


def create_event(event_data):
    service = get_calendar_service()

    start = format_to_rfc3339(event_data["start_time"])
    end = format_to_rfc3339(event_data["end_time"])

    if not start or not end:
        print("❌ Skipping event: Invalid time format.")
        return

    event = {
        'summary': event_data['title'],
        'start': {'dateTime': start, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end, 'timeZone': 'Asia/Kolkata'},
        'description': event_data.get('description', ''),
        'location': event_data.get('location', '')
    }

    created_event = service.events().insert(
        calendarId='primary', body=event).execute()
    print(f"✅ Event created: {created_event.get('htmlLink')}")
