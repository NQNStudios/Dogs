import smtplib
from email.mime.text import MIMEText

def send_most_placements_email(most_placing_dogs):
    from_address = "nleroybot@gmail.com"
    to_address = "nelson.nleroy@gmail.com"

    subject = "Most Placing Dogs"
    body_html = """
        <html>
            <head></head>
            <body>
                <p>
        """

    num = 1
    for dog in most_placing_dogs:
        body_html += str(num) + ". <a href=\"http://www.fieldtrialdatabase.com/" + dog[0] \
                + "\">name placeholder</a><br>"

        num += 1

    body_html += """
                </p>
            </body>
        </html>
        """

    message = MIMEText(body_html, "html")
    message['From'] = from_address
    message['To'] = to_address
    message['Subject'] = subject

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(from_address, "B0taccount")
    server.sendmail(from_address, to_address, message.as_string())
    server.close()
