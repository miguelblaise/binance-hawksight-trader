import email
import imaplib
import os

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
SERVER = os.getenv("SERVER")

def connect_inbox(email, pw, server):
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)

    mail.select('inbox')

    return mail

def get_mail(client, query):
    status, data = client.search(None, query)
    mail_ids = []

    for block in data:

        mail_ids += block.split()

    for i in mail_ids:

        status, data = mail.fetch(i, '(RFC822)')
        raw_email = email.message_from_bytes(data[0][1])

        mail_from = raw_email['from']
        mail_subject = raw_email['subject']

        body = ''
        for part in raw_email.get_payload():
            body += part.get_payload()
        return mail_from, mail_subject, body

if __name__ == "__main__":
    query = '(SUBJECT "Trading signals of Top 12 Cryptocurrency (daily) for Thursday 21 October 2021")'
    mail = connect_inbox(EMAIL, PASSWORD, SERVER)
    mail_from, mail_subject, message = get_all_mail(mail, query)
    print(message)