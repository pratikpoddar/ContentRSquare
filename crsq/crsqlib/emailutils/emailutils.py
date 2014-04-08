import re
import email
from collections import Counter
from crsq.models import EmailInfo

def emailstr2tuples(emailstring):
        namematches = re.findall('"[^"]*"', emailstring)
        for nm in namematches:
                emailstring = emailstring.replace(nm, ' '.join(map(lambda x: x.strip(), nm.split(','))))
        tuples = map(lambda x: email.utils.parseaddr(x.strip()), emailstring.split(','))
        return map(lambda x: (x[0], x[1].lower()), tuples)

def relatedemailaddr(username, emailaddr):

        emailpartners = filter(lambda y: emailaddr in y, map(lambda x: ', '.join(filter(lambda t: t, [x['emailfrom'], x['emailto'], x['emailccto'], x['emailbccto']])), EmailInfo.objects.filter(username=username).values()))
	
	emailpartners = map(lambda x: list(set(map(lambda y: y[1], emailstr2tuples(x)))), emailpartners)

	counter =  Counter(sum(emailpartners, []))

	return filter(lambda y: y[0] not in username + ' ' + emailaddr, sorted(counter.items(), key=lambda x: -x[1]))[:4]

	

