import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import html2text
from cog.config import EMAIL_SENDER, EMAIL_SENDER_NAME, SMTP_USERNAME, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT

def send_email(recipient, subject, body):
    """
    Send email. Returns true if success and false on error.
    recipient - recipient email address.
    subject - subject of email.
    body - HTML body of email.
    """
    # The HTML body of the email.
    BODY_HTML = body

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = html2text.html2text(body)

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email.utils.formataddr((EMAIL_SENDER_NAME, EMAIL_SENDER))
    msg['To'] = recipient

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(BODY_TEXT, 'plain')
    part2 = MIMEText(BODY_HTML, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Try to send the message.
    try:  
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.ehlo()
        server.starttls()
        #stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(EMAIL_SENDER, recipient, msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        print ("Email error: ", e)
        return False
    else:
        return True