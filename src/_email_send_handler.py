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
	"""
	Set up email communication details
	Inputs: user's email name(string) and pwd(string); recipients (list), subject(string), content(string)
	Return: Boolean, if sent success then True
	"""
	logger.info('ENTRY')
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
		#server.ehlo()
		logger.debug(server)
		logger.debug(gmail_user)
		logger.debug(gmail_pwd)

		server.login(gmail_user, gmail_pwd)
		server.sendmail(gmail_user, recipients, msg.as_string())
		server.quit()
		logger.info('EXIT')
		return True
	except Exception as err:
		logger.exception(err)
		return False

def _send_email(content, title= EMAIL_TITLE):
	"""
	call send_email_template() to send the email
	Input: content(string), title(string)
	Return: Boolean, if sent success then True
	"""
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
	assert _send_email(content, title= 'Alter! New updates @ PNP website'), True
