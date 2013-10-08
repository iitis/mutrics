class Cascade(object):
	def classify(self, f, dump, dumpl):
		ret = (dump == None)
		sel = False

		for step in self.steps:
			if   sel: break
			elif dump: sel = (step.name == dump)

			if sel and "in" in dumpl: ret = True

			# check
			if step.check(f):
				if sel and "chk" in dumpl: ret = True
			else:
				if sel and "skp" in dumpl: ret = True
				if sel and "out" in dumpl: ret = True
				f.history.append(step.name + ":Skp")
				continue

			# classify
			proto = step.classify(f)
			if proto == "Unknown":
				if sel and "unk" in dumpl: ret = True
				if sel and "out" in dumpl: ret = True
				f.history.append(step.name + ":Unk")
			else:
				f.classify(proto, step.name)
				if sel and "ans" in dumpl: ret = True
				if sel and "ok"  in dumpl: ret = f.isok()
				if sel and "err" in dumpl: ret = f.iserr()
				f.history.append(step.name + ":Ans")
				break

		else: # end of steps
			if not sel:
				f.history.append("N/A")

		return ret

	######################################################

	steps = []
	@classmethod
	def register(cls, step):
		if not hasattr(step, "name"):
			step.name = step.__module__[4:]
		if not hasattr(step, "check"):
			step.check = lambda f: True
		cls.steps.append(step)
