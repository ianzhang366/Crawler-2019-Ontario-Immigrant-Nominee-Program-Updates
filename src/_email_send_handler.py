import smtplib
from email.mime.text import MIMEText
from log_control import log_main
logger = log_main('log_pnp')


def send_email_template(gmail_user, gmail_pwd, recipients, subject, content):
	logger.info('ENTRY: send_email_template(gmail_user, gmail_pwd, recipient, subject, content)')
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
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_pwd)
		server.sendmail(gmail_user, recipients, msg.as_string())
		server.close()
		return True
	except Exception as err:
		logger.exception(err)
		return False

def _send_email(content, title= 'Alter! New updates @ PNP website'):
	logger.info('ENTRY: main_send_email(content)')
	gmail_user = 'ian.zhang366@gmail.com'
	gmail_pwd = 'p@ss4Goog'
	recipient = ['ian.zhang366@gmail.com', 'lisa411854746@gmail.com']
	# send email with content html
	subject = title
	# print 'in a'
	try:
		send_email_template(gmail_user, gmail_pwd, recipient, subject, content)
		return True
	except Exception as err:
		logger.exception(err)
		return False

if __name__ == '__main__':
	content = 'mulit reciever testing'
	_send_email(content, title= 'Alter! New updates @ PNP website')
	