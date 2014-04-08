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

def relatedemailaddr(e):

	username = e['user']
	emailsinvolvedstr = ', '.join(filter(lambda t: t, [e['emailfrom'], e['emailto'], e['emailccto'], e['emailbccto']]))
	emailsinvolved = list(set(map(lambda x: x[1], emailstr2tuples(emailsinvolvedstr)))-set([username]))
	
	allemailpartners = map(lambda x: ', '.join(filter(lambda t: t, [x['emailfrom'], x['emailto'], x['emailccto'], x['emailbccto']])), EmailInfo.objects.filter(user=username).values())

	relatedemails = []
	for emailaddrinvolved in emailsinvolved:
	        emailpartners = filter(lambda y: emailaddrinvolved in y, allemailpartners)
		emailpartners = map(lambda x: list(set(map(lambda y: y[1], emailstr2tuples(x)))), emailpartners)
		counter =  Counter(sum(emailpartners, []))
		relatedemails += map(lambda z: z[0], filter(lambda y: y[0] not in username + ' '.join(emailsinvolved), sorted(counter.items(), key=lambda x: -x[1]))[:4])

	return list(set(relatedemails))

	

