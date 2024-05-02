from google.oauth2 import service_account
from googleapiclient.discovery import build


def read_doc(id_list, txt_file, credentials):
    # Path to your service account key file

    SERVICE_ACCOUNT_FILE = credentials
    #'credentials.json'

    open(txt_file, "w").close()
    with open(txt_file, 'a') as file:
        for DOCUMENT_ID in id_list:
            # Document ID of the Google Docs file
            #DOCUMENT_ID = '1XhiXkajb8_9kgX3fTSucOfcqRADVoHFo0OLjlmr7ZCE'

            # Scopes required by the Docs API
            SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

            # Authenticate and build the service
            credentials = service_account.Credentials.from_service_account_file(
                    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            service = build('docs', 'v1', credentials=credentials)

            # Fetch the document
            document = service.documents().get(documentId=DOCUMENT_ID).execute()

            # Print the document title and contents
            print('The title of the document is: {}'.format(document.get('title')))
            file.write("Title: " + '\n'+ document.get('title') + '\n' + "body: " + '\n')

            content = document.get('body').get('content')
            for element in content:
                if 'paragraph' in element:
                    for text_element in element['paragraph']['elements']:
                        if 'textRun' in text_element:      
                            file.write(text_element['textRun']['content'])
                            print(text_element['textRun']['content'], end='')
