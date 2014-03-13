import email
import pickle
from bs4 import BeautifulSoup
from crsq.models import EmailInfo
from dateutil.parser import parse

def get_last_emails_gmail(raw_emails):

	for raw_email in raw_emails:
		emaildict = parse_email('pratik.phodu@gmail.com', raw_email)
		if EmailInfo.objects.filter(messageid=emaildict['messageid']).count()==0:
			e = EmailInfo(**emaildict)
			try:
				e.save()
			except Exception as exc:
				print exc

## TODO: Does only html messages for now
def parse_email(username, raw_email):
	
	msg = email.message_from_string(raw_email)
	body = ''
	cleanbody = ''
        if msg.is_multipart():
            for payload in msg.get_payload():
                if payload.get_content_subtype() == 'html':
                        body += str(payload.get_payload()) + ' '
                if payload.get_content_subtype() == 'alternative':
                        for payload2 in payload.get_payload():
                                if payload2.get_content_subtype() == 'html':
                                        body += str(payload2.get_payload()) + ' '
        else:
            body += msg.get_payload()

	body = body.strip()
	body = body.decode("quopri").replace('\r',' ').replace('\n', ' ').strip()

	return {'user': username, 'emailto': msg['To'], 'subject': msg['Subject'], 'emailtime': parse(msg['Date']), 'messageid': msg['Message-ID'], 'emailfrom': msg['From'] , 'body': body, 'emailccto': msg['Cc'], 'emailbccto': msg['Bcc']}

listofps = []
file = open('pratikphodugmailcom_emaildump.pickle' ,'r')
raw_emails = pickle.load(file)
file.close()

get_last_emails_gmail(raw_emails)

