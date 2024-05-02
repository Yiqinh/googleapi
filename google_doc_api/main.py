from read_doc import read_doc
from read_gmail import read_gmail

def main():
    test_doc_id = ["1XhiXkajb8_9kgX3fTSucOfcqRADVoHFo0OLjlmr7ZCE","1XhiXkajb8_9kgX3fTSucOfcqRADVoHFo0OLjlmr7ZCE" ]

    #read_doc(test_doc_id, 'doc_output.txt', 'credentials.json')
    read_gmail('client_id.json', 'gmail_output.txt')

if __name__ == '__main__':
    main()
