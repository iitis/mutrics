class ArffReader:
	def __init__(self, src):
		self.src = src
		self.fields = []

		# read field definitions
		for line in src:
			line = line.strip()
			if line[0:11] == '@attribute ':
				self.fields.append(line.split()[1])
			elif line[0:5] == '@data':
				break

	def __iter__(self):
		for line in self.src:
			line = line.strip()
			yield dict(zip(self.fields, line.split(',')))
