class mod_dummy:
	skip = ['TCP_Empty', 'Unknown']

	def check(self, f):
		return f.data["lpi_proto"] in self.skip

	def classify(self, f):
		return "SKIP"
