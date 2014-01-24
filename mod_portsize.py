# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

from portsize import HTClass

class mod_portsize:
	def __init__(self, model):
		self.htc = HTClass.HTClass()
		self.htc.load(open(model, "rb"))

	def classify(self, f):
		l = [f["fc_proto"], f["fc_dst_port"], f["pks_1_up"], f["pks_1_down"]]

		return self.htc.one(",".join(l))
