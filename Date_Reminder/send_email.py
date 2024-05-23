from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import base64
import os
def send_email(email):
    # Load Credentials
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()
    message["To"] = email
    message["From"] = "notetaker998@gmail.com"
    message["Subject"] = "Test Time"
    message.set_content("This is a reminder for your test in two days. Go ahead and study the summaries you submitted, good luck!")

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {"raw": encoded_message}
    send_message = (
        service.users()
        .messages()
        .send(userId="notetaker998@gmail.com", body=create_message)
        .execute()
    )

    print(f'Message Id: {send_message["id"]}')