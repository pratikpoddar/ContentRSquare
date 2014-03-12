import email
import pickle
from bs4 import BeautifulSoup
from crsq.models import EmailInfo
from dateutil.parser import parse

def get_last_emails_gmail(username, password, n=500):

	for email_id in email_ids:
 		raw_email = data[0][1]
		emaildict = parse_email(username, raw_email)
		e = EmailInfo(**emaildict)
		e.save()

def parse_email(username, raw_email):
	
	msg = email.message_from_string(raw_email)
	body = ''
	cleanbody = ''
	if msg.is_multipart():
	    for payload in msg.get_payload():
        	body += str(payload.get_payload()) + ' '
	else:
	    body += msg.get_payload()

	body = body.strip()
	body = body.decode("quopri")

	return {'user': username, 'emailto': msg['To'], 'subject': msg['Subject'], 'emailtime': parse(msg['Date']), 'messageid': msg['Message-ID'], 'emailfrom': msg['From'] , 'body': body, 'emailccto': msg['Cc'], 'emailbccto': msg['Bcc']}

