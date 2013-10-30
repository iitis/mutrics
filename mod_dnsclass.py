#
# DNS-Class
#
# TODO: check the new tldextract
#

from dnsclass.libshorttext import classifier
from dnsclass import tokenizer

class mod_dnsclass:
	def __init__(self, model):
		self.m = classifier.TextModel(model)
		self.m.text_converter.text_prep.tokenizer = tokenizer.tokenizer

	def check(self, f):
		if f["dns_flow"] == "1": return True
		if f["dns_name"][0] != '?': return True
		return False

	def classify(self, f):
		if f["dns_flow"] == "1": return "DNS"

		k = "{dns_name}:{fc_dst_port}/{fc_proto}".format_map(f)
		r = classifier.predict_single_text(k, self.m)

		return r.predicted_y
