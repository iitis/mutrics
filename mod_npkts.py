from npkts import HTClass

class mod_npkts:
	n = 1
	htc = None

	def __init__(self, model, n):
		self.htc = HTClass.HTClass()
		self.n = n
		self.htc.load(open(model, "rb"))

	def check(self, f):
		f = f.data
		if f["pks_1_up"] == "0" or f["pks_1_down"] == "0":
			return False
		else:
			return True

	def classify(self, f):
		f = f.data
		pp = "%s/%s" % (f["fc_proto"], f["fc_dst_port"])

		up   = [str(f["pks_%d_up"%i])   for i in range(1,self.n+1)]
		down = [str(f["pks_%d_down"%i]) for i in range(1,self.n+1)]

		return self.htc.one([pp] + up + down)
