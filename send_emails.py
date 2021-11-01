import smtplib
import ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def send_email(sender,
    receivers,
    subject,
    body,
    email=EMAIL, 
    password=PASSWORD
    ):

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = email
    msg['To'] = ",".join(receivers)

    part = MIMEText(body, 'html')
    msg.attach(part)

    port = 465
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(EMAIL, PASSWORD)
        server.sendmail(sender, receivers, msg.as_string())

if __name__ == "__main__":
    sender = 'auto-trader@test.com'
    receivers = [EMAIL]
    body = """<pre style='color:#000000;background:#ffffff;'>test</pre>"""
    subject = "test"
    # body = "<b>test</b>"
    send_email(
        sender,
        receivers,
        subject,
        body
    )