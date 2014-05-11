from unidecode import unidecode

def removeNonAscii(s): 
	try:
		s = unidecode(s)
	except:
		pass
	return "".join(i for i in s if ord(i)<128)

def crsq_unicode(s):

        if s  == None:
                return s

        if isinstance(s, unicode):
		try:
			return unidecode(s)
		except:
			return s
        else:
		try:
			return unidecode(s.decode('utf-8'))
		except:
			return s.decode('utf-8')


