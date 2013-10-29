class Flow(object):
	def __init__(self, src, data, gt):
		self.src = src
		self.data = data
		self.gt = gt
		self.proto = "Unknown"
		self.mod = "N/A"
		self.history = []

	def __getitem__(self, key):
		return self.data[key]

	def classify(self, proto, mod):
		self.mod = mod
		self.proto = proto

	def isok(self):  return self.proto == self.gt
	def iserr(self): return self.proto != self.gt
	def isunk(self): return self.proto == "Unknown"

	def write(self, fmt, dst):
		if fmt == "none":
			return

		elif fmt == "txt":
			srca = "{fc_src_addr:}:{fc_src_port}".format_map(self.data)
			dsta = "{fc_dst_addr:}:{fc_dst_port}".format_map(self.data)
			s1 = "{0[fc_id]:7} {0[fc_proto]} {1:>21}<->{2:<21}".format(self.data, srca, dsta)
			s2 = self.gt
			s3 = "{0.proto}".format(self)
			s4 = " ".join(self.history)

			dst.write("{0} {1:>10} is {2:<10} # {3}\n".format(s1, s2, s3, s4))

		elif fmt == "arff":
			add = ",'" + self.mod + "','" + self.proto + "'"
			self.src.printd(self.data, add=add, dst=dst)
