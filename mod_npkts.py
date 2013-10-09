#
# TODO: try k-NN with unknown detection
#

from npkts import HTClass

class mod_npkts:
	def __init__(self, model, n):
		self.n = n
		self.htc = HTClass.HTClass()
		self.htc.load(open(model, "rb"))

	def check(self, f):
		return (f["pks_1_down"] != "0" and f["pks_1_up"] != "0")

	def classify(self, f):
		pp = "%s/%s" % (f["fc_proto"], f["fc_dst_port"])
		up   = [f["pks_%d_up"%i]   for i in range(1,self.n+1)]
		down = [f["pks_%d_down"%i] for i in range(1,self.n+1)]

		return self.htc.one([pp] + up + down)
