
import smtplib
from email.mime.text import MIMEText
from config import CONFIG_INFO


def send_mail(text, subject, CONFIG = CONFIG_INFO):
	try:
		FROM = CONFIG['sender']
		TO = CONFIG['receiver']
		msg = MIMEText(text)
		msg['Subject'] = subject
		msg['From'] = FROM
		msg['To'] = TO
		server = smtplib.SMTP('mailhost.cms.hu-berlin.de', 25)
		server.sendmail(FROM, TO, msg.as_string())
		server.quit()
	except Exception as e:
		print(e)
