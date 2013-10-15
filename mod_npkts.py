from npkts import HTClass

class mod_npkts:
	def __init__(self, model):
		self.n = 1
		self.htc = HTClass.HTClass()
		self.htc.load(open(model, "rb"))

	def classify(self, f):
		pp = "%s/%s" % (f["fc_proto"], f["fc_dst_port"])
		up   = [f["pks_%d_up"%i]   for i in range(1,self.n+1)]
		down = [f["pks_%d_down"%i] for i in range(1,self.n+1)]

		return self.htc.one(str([pp] + up + down))
