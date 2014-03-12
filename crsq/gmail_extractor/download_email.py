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
		emaildict = parse_email(username, raw_email)
		emails.append(emaildict)
		e = EmailInfo(**emaildict)
		e.save()

	return emails

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

#python oauth2.py --generate_oauth2_token --client_id=292712397025-bh6dhs8n9eluc4me3hujtugg7fndd539.apps.googleusercontent.com --client_secret=4YOc_uf_4Lxyg37QPvZ18HST
#Enter verification code: 4/9QJabTZfaOxomMFyOyeP1AqSTDPh.sm4IIt5tu3cYXE-sT2ZLcbStqXtpiQI
#Refresh Token: 1/LN46RBqkOIq-TDrcSTwVwnhYy0z-32cBuVpL0EIDKjg
#Access Token: ya29.1.AADtN_UxN-Wv5WO5CI_FGdOM84ZirA7rKYYNP-EtXMEeSaJjgHq1Y_SpMzNKz3Tf7IqF8w
#Access Token Expiration Seconds: 3600

e = get_last_emails_gmail('pratik.phodu@gmail.com', 'indiarocks', 150)
file=open('pratikgmaildump.txt', 'w')
pickle.dump(e,file)
file.close()

