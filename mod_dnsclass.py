#
# DNS-Class
#
# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3
#

from dnsclass.libshorttext import classifier
from dnsclass.libshorttext.classifier import learner
from dnsclass import tokenizer

class mod_dnsclass:
	def __init__(self, model, F=3, T=0.3):
		self.m = classifier.TextModel(model)

		self.tc = self.m.text_converter
		self.tc.text_prep.tokenizer = tokenizer.tokenizer

		self.F = F
		self.T = T

	def check(self, f):
		if "dns_flow" not in f.data: return False
		if f["dns_flow"] == "1": return True
		if f["dns_name"][0] != '?': return True
		return False

	def classify(self, f):
		if f["dns_flow"] == "1": return "DNS"

		### convert to feature vector
		text = "{dns_name}:{fc_dst_port}/{fc_proto}".format_map(f)
		svm = self.m.text_converter.toSVM(text)
		if len(svm) < self.F: return "Unknown"

		### predict
		y, dec = learner.predict_one(svm, self.m.svm_model)
		y = int(y)

		if dec[y-1] < self.T:
			return "Unknown"
		else:
			return self.tc.getClassName(y)
