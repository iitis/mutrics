class Flow:
	_fields = []
	def add_field(field): Flow._fields.append(field)
	def get_fields():     return Flow._fields

	######################################################

	def __init__(self, txt):
		self._origtxt = txt
		self.data = dict(zip(Flow._fields, txt.split(',')))

		self.mod = "?"
		self.proto = "?"
		self.history = []

	def register(self, mod, proto, history):
		self.mod = mod
		self.proto = proto
		self.history = history

	def txt(self):
		src = "{fc_src_addr:}:{fc_src_port}".format_map(self.data)
		dst = "{fc_dst_addr:}:{fc_dst_port}".format_map(self.data)
		s1 = "{0[fc_id]:7} {0[fc_proto]} {1:>21}<->{2:<21}".format(self.data, src, dst)
		s2 = self.data["lpi_proto"] # ground-truth
		s3 = "{0.proto}".format(self)
		s4 = " ".join(self.history)

		return "{0} {1:>10} is {2:<10} # {3}".format(s1, s2, s3, s4)
