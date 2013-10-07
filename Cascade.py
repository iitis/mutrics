class Cascade(object):
	def classify(self, f):
		history = []

		for step in self.steps:
			if not step.check(f):
				history.append(step.name + ":Skp")
				continue # skip the classifier

			proto = step.classify(f)
			if proto != "Unknown":
				history.append(step.name + ":Ans")
				break    # quit the cascade here

			history.append(step.name + ":Unk")
		else:
			history.append("N/A")
			return ("END", "Unknown", history)

		return (step.name, proto, history)

	######################################################

	steps = []
	@classmethod
	def register(cls, step):
		if not hasattr(step, "name"):
			step.name = step.__module__[4:]
		if not hasattr(step, "check"):
			step.check = lambda f: True
		cls.steps.append(step)

class CascadeEnd:
	name = "END"
	def classify(self, f): return "Unknown"
