import re
import email

def emailstr2tuples(emailstring):
        namematches = re.findall('"[^"]*"', emailstring)
        for nm in namematches:
                emailstring = emailstring.replace(nm, ' '.join(map(lambda x: x.strip(), nm.split(','))))
        tuples = map(lambda x: email.utils.parseaddr(x.strip()), emailstring.split(','))
        return map(lambda x: (x[0], x[1].lower()), tuples)

