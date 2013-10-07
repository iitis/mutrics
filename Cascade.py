class Cascade:
	_modules = []
	def register(name, check, classify):
		assert(name and check and classify)
		Cascade._modules.append({"name": name, "check": check, "classify": classify})

	######################################################

	def __init__(self):
		Cascade.register("END", lambda f: True, lambda f: "Unknown")

	def classify(self, f):
		history = []
		name = "?"
		proto = "?"

		for mod in Cascade._modules:
			name = mod["name"]

			if mod["check"](f):
				# enable module and attempt classification
				proto = mod["classify"](f)

				if proto == "Unknown":
					# no decision, move to next module
					history.append(name + ":Unk")
				else:
					# success, quit the tree
					history.append(name + ":End")
					break
			else:
				# skip the classifier
				history.append(name + ":Skp")

		return (name, proto, history)
