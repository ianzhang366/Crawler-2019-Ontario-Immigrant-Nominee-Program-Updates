import smtplib
from email.mime.text import MIMEText
from log_control import log_main

logger = log_main('log_pnp')
import _config

import sys
sys.path.append(_config.SEN_CONFIG.data_location)
import config


EMAIL_TITLE='Alter! New updates @ PNP website'
SMTP_SERVER='smtp.gmail.com'
SMTP_PORT=587

def send_email_template(gmail_user, gmail_pwd, recipients, subject, content):
	logger.info('ENTRY')
# Create message container - the correct MIME type is multipart/alternative.
	try:
		try:
			msg = MIMEText(content,'html')
			msg['Subject'] = subject
			msg['From'] = gmail_user

			msg['To'] = ', '.join(recipients)
			logger.debug(msg)
		except Exception as err:
			logger.exception(err)
		# Send the message via local SMTP server.
		server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_pwd)
		server.sendmail(gmail_user, recipients, msg.as_string())
		server.close()
		logger.info('EXIT')
		return True
	except Exception as err:
		logger.exception(err)
		return False

def _send_email(content, title= EMAIL_TITLE):
	logger.info('ENTRY')
	gmail_user = config.SENT_EMAIL.gmail_user
	gmail_pwd = config.SENT_EMAIL.gmail_pwd
	recipient = config.SENT_EMAIL.recipient
	# send email with content html
	subject = title
	try:
		send_email_template(gmail_user, gmail_pwd, recipient, subject, content)
		logger.info('EXIT')
		return True
	except Exception as err:
		logger.exception(err)
		return False

if __name__ == '__main__':
	content = 'mulit reciever testing'
	# _send_email(content, title= 'Alter! New updates @ PNP website')
	print config.SENT_EMAIL.gmail_user
	# print config.LOG_CONFIG.location