from dpi import DT

class mod_dpi:
	def __init__(self, model, i=8):
		self.i = i
		self.cls = DT.DT()
		self.cls.load(open(model, "rb"))
		self.cls.algo.set_params(n_jobs=1)

		self.keys = []
		self.keys.extend(["pl_%d_up"%(x+1) for x in range(self.i)])
		self.keys.extend(["pl_%d_down"%(x+1) for x in range(self.i)])

	def check(self, f):
		return "pl_1_up" in f.data

	def classify(self, f):
		proto  = 1 if f["fc_proto"] == "TCP" else 2
		port   = int(f["fc_dst_port"])
		pl     = [int(f[k]) for k in self.keys]

		v = [proto, port] + pl
		return self.cls.one(v)
