import imaplib
import email
import pickle
from bs4 import BeautifulSoup
from crsq.models import EmailInfo
from dateutil.parser import parse

def get_last_emails_gmail(username, password, n=500):

	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login(username, password)
	mail.select("inbox",readonly=True) # connect to inbox.

	result, data = mail.search(None, 'FROM', '"gmail"')
 
	ids = data[0] # data is a list.
	id_list = ids.split() # ids is a space separated string
	id_list.reverse()
	email_ids = id_list[:n]
 
	emails = []
	for email_id in email_ids:
		result, data = mail.fetch(email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
 		raw_email = data[0][1]
		emails.append(parse_email(raw_email))

	return emails

def parse_email(raw_email):
	
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

	return {'emailto': msg['To'], 'subject': msg['Subject'], 'emailtime': parse(msg['Date']), 'messageid': msg['Message-ID'], 'from': msg['From'] , 'body': body, 'emailccto': msg['Cc'], 'emailbccto': msg['Bcc']}

e = get_last_emails_gmail('pratik.phodu@gmail.com', 'indiarocks', 150)
file=open('pratikgmaildump.txt', 'w')
pickle.dump(e,file)
file.close()



