from unidecode import unidecode

def removeNonAscii(s): 
	try:
		s = unidecode(s)
	except:
		pass
	try:
		return "".join(i for i in s if ord(i)<128)
	except:
		return ""

def crsq_unicode(s):

        if s  == None:
                return s

        try:
                s = s.replace(u'\xc2\xa0', ' ')
        except:
                pass

        try:
                s = s.replace(u'\xc2', ' ')
        except:
                pass

        try:
                s = s.replace(u'\xa0', ' ')
        except:
                pass


        if isinstance(s, unicode):
		return s
        else:
		try:
			return unidecode(s.decode('utf-8'))
		except:
			return s.decode('utf-8')


