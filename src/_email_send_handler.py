"""
 _send_email(content, title= EMAIL_TITLE)
 send_email_template(gmail_user, gmail_pwd, recipients, subject, content)

 _send_email() is mainly method for sending a email
"""
import smtplib
from email.mime.text import MIMEText
from log_control import log_main
import _config
import sys
import config

sys.path.append(_config.SEN_CONFIG.data_location)

LOGGER = log_main('log_pnp')


EMAIL_TITLE = 'Alter! New updates @ PNP website'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

def send_email_template(gmail_user, gmail_pwd, recipients, subject, content):
    """
    Set up email communication details
    Inputs: user's email name(string) and pwd(string); recipients (list), subject(string), 
            content(string)
    Return: Boolean, if sent success then True
    """
    LOGGER.info('ENTRY')
    try:
        try:
            msg = MIMEText(content, 'html')
            msg['Subject'] = subject
            msg['From'] = gmail_user

            msg['To'] = ', '.join(recipients)
            LOGGER.debug(msg)
        except Exception as err:
            LOGGER.exception(err)
        # Send the message via local SMTP server.
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()
        server.starttls()
        #server.ehlo()
        LOGGER.debug(server)
        LOGGER.debug(gmail_user)
        LOGGER.debug(gmail_pwd)

        server.login(gmail_user, gmail_pwd)
        server.sendmail(gmail_user, recipients, msg.as_string())
        server.quit()
        LOGGER.info('EXIT')
        return True
    except Exception as err:
        LOGGER.exception(err)
        return False

def _send_email(content, title=EMAIL_TITLE):
    """
    call send_email_template() to send the email
    Input: content(string), title(string)
    Return: Boolean, if sent success then True
    """
    LOGGER.info('ENTRY')
    gmail_user = config.SENT_EMAIL.gmail_user
    gmail_pwd = config.SENT_EMAIL.gmail_pwd
    recipient = config.SENT_EMAIL.recipient
    # send email with content html
    subject = title
    try:
        send_email_template(gmail_user, gmail_pwd, recipient, subject, content)
        LOGGER.info('EXIT')
        return True
    except Exception as err:
        LOGGER.exception(err)
        return False

if __name__ == '__main__':
    content = 'mulit reciever testing'
    assert _send_email(content, title='Alter! New updates @ PNP website'), True
