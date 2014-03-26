from crsq.gmail_extractor.oauth2g-update import *
from crsq.models import EmailUser

client_id = '292712397025-bh6dhs8n9eluc4me3hujtugg7fndd539.apps.googleusercontent.com'
client_secret = '4YOc_uf_4Lxyg37QPvZ18HST'
scope = 'https://mail.google.com/'

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

	eu = EmailUser()
	eu.name = name
	eu.email = email
	eu.refreshtoken = response['refresh_token']
	eu.accesstoken = response['access_token']
	eu.lastid = 0
	eu.save()

	return response

def getNewAccessToken(user, refreshtoken):

	response = RefreshToken(client_id, client_secret,
                            refreshtoken)
	print 'Access Token: %s' % response['access_token']
	print 'Access Token Expiration Seconds: %s' % response['expires_in']
	
	eu = EmailUser.get(email=user)
	eu.accesstoken = response['accesstoken']
	eu.save()

	return response

def getConnection(user):

	resp = getNewAccessToken(user, EmailUser.objects.get(email=user).refreshtoken)
	accesstoken = resp['accesstoken']
	
	imap_conn = imaplib.IMAP4_SSL('imap.gmail.com')
	imap_conn.debug = 4
	imap_conn.authenticate('XOAUTH2', lambda x: GenerateOAuth2String(user, accesstoken,
                             base64_encode=False))
	imap_conn.select('INBOX', readonly=True)
	
	return imap_conn

def getEmails(imap_conn):

	result, data = imap_conn.search(None, 'FROM', '"gmail"')

	ids = data[0] # data is a list.
	id_list = ids.split() # ids is a space separated string
	id_list.reverse()
	email_ids = id_list[:500]

	emails = []
	counter = 0
	for email_id in email_ids:
        	result, data = imap_conn.fetch(email_id, "(X-GM-THRID X-GM-MSGID RFC822)") # fetch the email body (RFC822) for the given ID
	        raw_email = data[0][1]
	        extra_info = data[0][0]
	        emails.append(raw_email)
	        print counter
	        counter+=1

