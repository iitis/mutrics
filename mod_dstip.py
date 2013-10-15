from dstip import HTClass

class mod_dstip:
	def __init__(self, model):
		self.htc = HTClass.HTClass()
		self.htc.load(open(model, "rb"))

	def classify(self, f):
		key = str([f["fc_dst_addr"], f["fc_dst_port"]])
		return self.htc.one(key)
