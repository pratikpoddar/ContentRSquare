from crsq.gmail_extractor.oauth2g import *
from crsq.models import EmailUser, EmailInfo
import email
import pickle
from bs4 import BeautifulSoup
from dateutil.parser import parse

client_id = '292712397025-bh6dhs8n9eluc4me3hujtugg7fndd539.apps.googleusercontent.com'
client_secret = '4YOc_uf_4Lxyg37QPvZ18HST'
scope = 'https://mail.google.com/'

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def getUser():

	name = raw_input('Write your name: ')
	email = raw_input('Write your email: ')
	print 'To authorize token, visit this url and follow the directions:'
	print '  %s' % GeneratePermissionUrl(client_id, scope)
	authorization_code = raw_input('Enter verification code: ')
	response = AuthorizeTokens(client_id, client_secret,
                             authorization_code)
	print 'Refresh Token: %s' % response['refresh_token']
	print 'Access Token: %s' % response['access_token']
	print 'Access Token Expiration Seconds: %s' % response['expires_in']

	eu = EmailUser(name = name, email = email, refreshtoken = response['refresh_token'], accesstoken = response['access_token'], lastid = 0)
	eu.save()

	return response

def getNewAccessToken(user, refreshtoken):

	response = RefreshToken(client_id, client_secret,
                            refreshtoken)
	print 'Access Token: %s' % response['access_token']
	print 'Access Token Expiration Seconds: %s' % response['expires_in']
	
	eu = EmailUser.objects.get(email=user)
	eu.accesstoken = response['access_token']
	eu.save()

	return response

def getConnection(user):

	resp = getNewAccessToken(user, EmailUser.objects.get(email=user).refreshtoken)
	accesstoken = resp['access_token']
	
	imap_conn = imaplib.IMAP4_SSL('imap.gmail.com')
	imap_conn.debug = 4
	imap_conn.authenticate('XOAUTH2', lambda x: GenerateOAuth2String(user, accesstoken,
                             base64_encode=False))
	imap_conn.select('INBOX', readonly=True)
	
	return imap_conn

def getNewEmails(user):

	lastid = EmailUser.objects.get(email=user).lastid

	imap_conn = getConnection(user)
	result, data = imap_conn.search(None, 'FROM', '"gmail"')

	ids = data[0] # data is a list.
	id_list = ids.split() # ids is a space separated string
	id_list.reverse()
	email_ids = filter(lambda x: int(x) > int(lastid), id_list)[:100]

	if len(email_ids)==0:
		return

	newlastid = max(map(lambda x: int(x), email_ids))

	counter = 0
	for email_id in email_ids:
        	result, data = imap_conn.fetch(email_id, "(X-GM-THRID X-GM-MSGID RFC822)") # fetch the email body (RFC822) for the given ID
	        raw_email = data[0][1]
	        gmail_extra_info = data[0][0]
		emaildict = parse_email(user, raw_email)
		emaildict['extrainfo'] = gmail_extra_info
                if EmailInfo.objects.filter(messageid=emaildict['messageid']).count()==0:
                        e = EmailInfo(**emaildict)
                        try:
                                e.save()
                        except Exception as exc:
                                print exc

	        print counter
	        counter+=1

	eu = EmailUser.objects.get(email=user)
	eu.lastid = str(newlastid)
	eu.save()

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
        body = removeNonAscii(body.decode("quopri").replace('\r',' ').replace('\n', ' ').strip())

        return {'user': username, 'emailto': msg['To'], 'subject': msg['Subject'], 'emailtime': parse(msg['Date']), 'messageid': msg['Message-ID'], 'emailfrom': msg['From'] , 'body': body, 'emailccto': msg['Cc'], 'emailbccto': msg['Bcc']}




