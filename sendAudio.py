from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
import base64
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/gmail.send']

# Set up the Gmail API client
creds = Credentials.from_authorized_user_file('token.json', SCOPES)
service = build('gmail', 'v1', credentials=creds)

# Set up the email message
message = MIMEMultipart()
message['to'] = 'YOUR EMAIL'
message['from'] = 'YOUR EMAIL'
today = datetime.date.today()
date_string = today.strftime('%Y-%m-%d')
message['subject'] = ('TLDR Newsletter Audio | ' + date_string)


# Attach the audio file
path = "output.mp3"
filename = os.path.basename(path)
with open(path, 'rb') as f:
    audio_data = f.read()
audio_part = MIMEAudio(audio_data, _subtype='mpeg', name=filename)
message.attach(audio_part)

# Send the email message
create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
try:
    send_message = (service.users().messages().send(userId="me", body=create_message).execute())
    print(F'The email was sent to {message["to"]} Message Id: {send_message["id"]}')
except HttpError as error:
    print(F'An error occurred: {error}')
    send_message = None
