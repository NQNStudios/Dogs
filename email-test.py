#! /usr/bin/env python3

import smtplib
from email.mime.text import MIMEText
import config

if __name__ == "__main__":
    from_address = "nleroybot@gmail.com"
    to_address = "nelson.nleroy@gmail.com"

    subject = "Test email"
    body = """
    <html>
      <head></head>
      <body>
        <p>Hi!<br>
           How are you?<br>
           Here is the <a href="https://www.python.org">link</a> you wanted.
        </p>
      </body>
    </html>
    """
    gmail_user = "nleroybot@gmail.com"
    gmail_password = config.bot_password

    message = MIMEText(body, "html")
    message['From'] = from_address
    message['To'] = to_address
    message['Subject'] = subject

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_password)
    server.sendmail(from_address, [ to_address ], message.as_string())
    server.close()
