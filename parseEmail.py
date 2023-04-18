from __future__ import print_function
import os.path
import base64
from datetime import date
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/gmail.send']

# parses the HTML elements in the email and gets the article title and summary, output to output.txt
def getArticles(soup):
    charCount = 0
    textBlocks = soup.find_all('div', {'class': 'text-block'})

    with open("output.txt", mode="w", encoding="utf-8") as outputFile:
        for block in textBlocks:
            innerSpan1 = block.find("span")
            if innerSpan1:
                innerSpan2 = innerSpan1.find_all("span")
                if innerSpan2 and len(innerSpan2) == 2:
                    title = innerSpan2[0].text.strip()
                    summary = innerSpan2[1].text.strip()                    
                    if title[-5:] == "read)":
                        articleTextLen = len(title) + len(summary) + 7
                        if (charCount + articleTextLen) < 4900:
                            charCount += articleTextLen
                            outputFile.write(f"Title: {title}")
                            outputFile.write(f"{summary}\n")


def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)

        # the email that we want to view emails from
        tldrEmail = "NEWSLETTER_EMAIL" # Change

        # date and time of emails we want to see
        todayDate = date.today()

        # Call the Gmail API
        results = service.users().messages().list(userId='me', q=f'from:{tldrEmail} after:{todayDate}').execute()
        messages = results.get('messages', [])

        # check if there are any messages from the email
        if not messages:
            print("There are no messages from", tldrEmail)
        else:

            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                payload = msg['payload']

                if 'parts' in payload:
                    parts = payload['parts']
                    for part in parts:
                        if part['filename']:
                            continue # if there are attachments to this email, skip it
                        data = part['body']['data']
                        if data:
                            # Decode the base64-encoded data and print the email content
                            data = data.replace("-", "+").replace("_", "/")
                            decoded_data = base64.b64decode(data)
                            soup = BeautifulSoup(decoded_data, 'html.parser')

                            # get article name and summary
                            getArticles(soup)

        print("successfully parsed newsletter and outputted content.")

    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()