import email
import imaplib
import os

from bs4 import BeautifulSoup as bs

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

def parse_body(body):
    soup = bs(body, features="html.parser")
    signals = {}
    for paragraph in soup.find_all('p'):
        ultag = paragraph.next_sibling
        signals[paragraph.text] = []
        for litag in ultag.find_all('li'):
            crypto_label = litag.find('a')
            signals[paragraph.text].append(crypto_label.text)
    return signals

if __name__ == "__main__":
    query = '(SUBJECT "Trading signals of Top 12 Cryptocurrency (daily) for Sunday 17 October 2021")'
    # query = '(SUBJECT "Trading signals of Top 12 Cryptocurrency (daily) for Monday 18 October 2021")'
    mail = connect_inbox(EMAIL, PASSWORD, SERVER)
    mail_from, mail_subject, message = get_mail(mail, query)

    
    # print(message)
    signals = parse_body(message)
    print(signals)