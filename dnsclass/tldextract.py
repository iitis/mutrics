'''Very simple replacement for the original tldextract'''

class Result(object):
	def __init__(self, text):
		self.tld = ""
		self.domain = ""
		self.subdomain = ""

		l = text.split('.')

		try:
			self.tld = l.pop()
			self.domain = l.pop()
		except: pass

		if len(l):
			self.subdomain = ".".join(l)

	def __str__(self):
		return self.subdomain + " " + self.domain + " " + self.tld

def extract(text):
	return Result(text)
