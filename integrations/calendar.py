# integrations/calendar.py

import os
import datetime
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_httplib2 import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "./credentials/credentials.json")
TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE", "./credentials/token.json")


class CalendarService:
    def __init__(self):
        self.service = self.authenticate()

    def authenticate(self):
        creds = None
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        return build('calendar', 'v3', credentials=creds)

    def create_event(self, summary, start_time, duration_minutes=60, description=""):
        calendar_id = os.getenv("GOOGLE_CALENDAR_ID", "primary")

        start_dt = datetime.datetime.fromisoformat(start_time)
        end_dt = start_dt + datetime.timedelta(minutes=duration_minutes)

        event = {
            'summary': summary,
            'description': description,
            'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'UTC'},
            'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'UTC'},
        }

        created_event = self.service.events().insert(calendarId=calendar_id, body=event).execute()
        return created_event.get('htmlLink')


# Example usage

calendar = CalendarService()
calendar.create_event(
    summary="Workout - Push Day",
    start_time="2025-03-26T10:00:00",
    duration_minutes=60,
    description="Upper body workout"
)
