from collections import defaultdict

class Cascade(object):
	def classify(self, f, dump, dumpl):
		ret = (dump == None)
		sel = False

		for step in self.steps:
			if   sel: break
			elif dump: sel = (step.name == dump)

			if sel and "in" in dumpl: ret = True
			step.stats["in"] += 1

			# check
			if step.check(f):
				if sel and "chk" in dumpl: ret = True
				step.stats["chk"] += 1
			else:
				if sel and "skp" in dumpl: ret = True
				step.stats["skp"] += 1

				if sel and "out" in dumpl: ret = True
				step.stats["out"] += 1

				f.history.append(step.name + ":Skp")
				continue

			# classify
			proto = step.classify(f)
			if proto == "Unknown":
				if sel and "unk" in dumpl: ret = True
				step.stats["unk"] += 1

				if sel and "out" in dumpl: ret = True
				step.stats["out"] += 1

				f.history.append(step.name + ":Unk")
			else:
				f.classify(proto, step.name)

				if sel and "ans" in dumpl: ret = True
				step.stats["ans"] += 1

				if f.isok():
					if sel and "ok"  in dumpl: ret = True
					step.stats["ok"] += 1
				else:
					if sel and "err" in dumpl: ret = True
					step.stats["err"] += 1

				f.history.append(step.name + ":Ans")
				break

		else: # end of steps
			if not sel:
				f.history.append("N/A")

		return ret

	def get_stats(self):
		ret = []

		for step in self.steps:
			ret.append({"name": step.name, "stats": step.stats})

		return ret

	######################################################

	steps = []
	@classmethod
	def register(cls, step):
		# add some properties
		if not hasattr(step, "name"):
			step.name = step.__module__[4:]
		if not hasattr(step, "check"):
			step.check = lambda f: True
		if not hasattr(step, "stats"):
			step.stats = defaultdict(int)

		cls.steps.append(step)
