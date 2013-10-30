from dpi import HTClass

class mod_dpi:
	def __init__(self, model, n=2):
		self.n = n
		self.htc = HTClass.HTClass()
		self.htc.load(open(model, "rb"))

	def classify(self, f):
		l = [f["fc_proto"], f["fc_dst_port"], f["pl_up"][:self.n], f["pl_down"][:self.n]]

		return self.htc.one("\t".join(l))
