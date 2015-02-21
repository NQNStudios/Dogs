import smtplib
from email.mime.text import MIMEText

def send_rankings(rankings, rank_method, stake_type):
    from_address = "nleroybot@gmail.com"
    to_address = "daniel.campbell@slcschools.org"

    subject = rank_method.name + " (" + stake_type + ")"
    body_html = """
        <html>
            <head></head>
            <body>
                <p>
        """

    num = 1
    for dog in rankings:
        body_html += str(num) + ". <a href=\"http://www.fieldtrialdatabase.com/" + dog.url \
                + "\">" + rank_method.format(dog, stake_type) + "</a><br>"

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
