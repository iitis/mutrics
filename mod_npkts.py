from npkts import kNN

class mod_npkts:
	def __init__(self, model):
		self.n = 1
		self.cls = kNN.kNN()
		self.cls.load(open(model, "rb"))

	def check(self, f):
		if f["pks_1_up"] == "0" or f["pks_1_down"] == "0":
			return False
		else:
			return True

	def classify(self, f):
		up   = [int(f["pks_%d_up"%i])   for i in range(1,self.n+1)]
		down = [int(f["pks_%d_down"%i]) for i in range(1,self.n+1)]

		return self.cls.one(up + down)
