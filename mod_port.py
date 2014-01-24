# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

from port import HTClass

class mod_port:
	def __init__(self, model):
		self.htc = HTClass.HTClass()
		self.htc.load(open(model, "rb"))

	def classify(self, f):
		k = f["fc_proto"] + "/" + f["fc_dst_port"]
		return self.htc.one(k)
