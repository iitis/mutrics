#from npkts import kNN
from npkts import DT

class mod_npkts:
	def __init__(self, model, i=1):
		self.i = i
		self.cls = DT.DT()
		self.cls.load(open(model, "rb"))
		self.cls.algo.set_params(n_jobs=1)

	def classify(self, f):
		proto  = 1 if f["fc_proto"] == "TCP" else 2
		port   = int(f["fc_dst_port"])
		szup   = [int(f["pks_%d_up"  %(x+1)]) for x in range(self.i)]
		szdown = [int(f["pks_%d_down"%(x+1)]) for x in range(self.i)]

		v = [proto, port] + szup + szdown
		return self.cls.one(v)
