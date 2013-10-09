class Flow(object):
	def __init__(self, txt):
		self._origtxt = txt
		self.data = dict(zip(self.arff_fields, txt.split(',')))
		self.gt = self["lpi_proto"]

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

	def write(self, out, fmt):
		if fmt == "none":
			return

		elif fmt == "txt":
			src = "{fc_src_addr:}:{fc_src_port}".format_map(self.data)
			dst = "{fc_dst_addr:}:{fc_dst_port}".format_map(self.data)
			s1 = "{0[fc_id]:7} {0[fc_proto]} {1:>21}<->{2:<21}".format(self.data, src, dst)
			s2 = self.data["lpi_proto"] # ground-truth
			s3 = "{0.proto}".format(self)
			s4 = " ".join(self.history)

			s = "{0} {1:>10} is {2:<10} # {3}".format(s1, s2, s3, s4)

		elif fmt == "arff":
			self.write_arff_header(out)

			s = ""
			for f in self.arff_fields:
				s += self.data[f] + ","
			s += self.mod + "," + self.proto

		out.write(s + "\n")

	####### ARFF READER #######################################
	arff_header = []
	arff_fields = []
	@classmethod
	def read_arff_header(cls, farg):
		for line in farg:
			line = line.strip()
			cls.arff_header.append(line)

			if line[0:11] == '@attribute ':
				cls.arff_fields.append(line.split()[1])
			elif line[0:5] == '@data':
				return

	arff_written = False
	@classmethod
	def write_arff_header(cls, out):
		if cls.arff_written: return

		for line in cls.arff_header:
			if line[0:5] == '@data':
				out.write("%% MuTriCs Multilevel Traffic Classifier\n")
				out.write("% mutrics_module: classifier that contributed the answer\n")
				out.write("% mutrics_proto: the identified protocol\n")
				out.write("@attribute mutrics_module string\n")
				out.write("@attribute mutrics_proto string\n")
				out.write("\n")

			out.write(line + "\n")

		cls.arff_written = True
