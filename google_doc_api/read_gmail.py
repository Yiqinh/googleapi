from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import pickle
from base64 import urlsafe_b64decode
import email

from flask import Flask, jsonify
app = Flask(__name__)

def read_gmail(client_id, txt_file):

    open(txt_file, "w").close()

    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_id, SCOPES)
            
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API to fetch the inbox
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No messages found.')
        return
    
    emails = []

    for message in messages[:1]:  # Get the first message

        msg = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()

        msg2 = service.users().messages().get(userId='me', id=message['id']).execute()
        emails.append(msg2)

        # Decode the raw message
        msg_str = urlsafe_b64decode(msg['raw'].encode('ASCII'))
        mime_msg = email.message_from_bytes(msg_str)

        # Extract message body
        message_content = ''
        if mime_msg.is_multipart():
            for part in mime_msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if content_type == 'text/plain' and "attachment" not in content_disposition:
                    message_content = part.get_payload(decode=True).decode()
                    break
        else:
            message_content = mime_msg.get_payload(decode=True).decode()

        with open(txt_file, 'a') as file:
            file.write('BODY: ' + '\n' + message_content + '\n')

        print(message_content)
        return jsonify(emails)
    
if __name__ == '__main__':
    app.run(debug=True)