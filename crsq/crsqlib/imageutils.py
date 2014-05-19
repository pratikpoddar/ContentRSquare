import cStringIO
import urllib
import Image

def imagesize(url):
	try:
		file = urllib.urlopen(url)
		im = cStringIO.StringIO(file.read())
		img = Image.open(im)
		width, height = img.size
		return (width, height)
	except:
		return (0,0)

