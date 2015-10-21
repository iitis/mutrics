# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

from portname import HTClass

class mod_portname:
	def __init__(self, model):
		self.htc = HTClass.HTClass()
		self.htc.load(open(model, "rb"))

	def check(self, f):
		if "dns_flow" not in f.data: return False
		if f["dns_name"][0] != '?': return True
		return False

	def classify(self, f):
		l = [f["fc_proto"], f["fc_dst_port"], f["dns_name"]]

		return self.htc.one(",".join(l))
