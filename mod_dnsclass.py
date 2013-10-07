#
# DNS-Class
#

import logging
logging.disable(logging.ERROR)

from dnsclass.libshorttext import classifier
from dnsclass import tokenizer

class mod_dnsclass:
	m = None

	def __init__(self, model):
		self.m = classifier.TextModel(model)
		self.m.text_converter.text_prep.tokenizer = tokenizer.tokenizer

	def check(self, f):
		if "dns_name" in f.data and f.data["dns_name"][0] != '?':
			return True
		elif f.data["lpi_proto"] == "DNS":
			return True
		else:
			return False

	def classify(self, f):
		# TODO: query the dns_flow field
		if f["fc_dst_port"] == "53" and f["fc_proto"] == "UDP":
			return "DNS"

		k = "{dns_name}:{fc_dst_port}/{fc_proto}".format(**f.data)
		r = classifier.predict_single_text(k, self.m)

		return r.predicted_y
