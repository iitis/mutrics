from npkts import kNN

class mod_npkts:
	def __init__(self, model_tcp, model_udp):
		self.cls_tcp = kNN.kNN()
		self.cls_tcp.load(open(model_tcp, "rb"))

		self.cls_udp = kNN.kNN()
		self.cls_udp.load(open(model_udp, "rb"))

	def classify(self, f):
		k = [int(f["pks_1_up"]), int(f["pks_1_down"])]

		if f["fc_proto"] == "TCP":
			return self.cls_tcp.one(k)
		else:
			return self.cls_udp.one(k)
