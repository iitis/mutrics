# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

from collections import defaultdict
from common import *

class Cascade(object):
	def classify(self, f, dump=None, dumpl=None):
		ret = (dump == None)
		sel = False

		# call init functions
		for step in self.steps:
			if hasattr(step, "init"): step.init(f)

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

		# call finish functions
		for step in self.steps:
			if hasattr(step, "finish"): step.finish(f)

		return ret

	def get_stats(self):
		s = ""

		if len(self.steps) == 0: return

		tot = float(self.steps[0].stats["in"])
		s += "Total: %s (#tot)\n" % fc(tot)

		for step in self.steps:
			ss = step.stats

			s += "  |\n  | %s (%s #tot)\n  |\n" % (fc(ss["in"]), pc(ss["in"], tot))
			s += "[%-10s]" % step.name
			s += " -> chk: %s (%s #tot)\n" % (fc(ss["chk"]), pc(ss["chk"], tot))
			s += "%15s >>> ok/err: %s/%s (%s/%s #ans)\n" % ("", fc(ss["ok"]), fc(ss["err"]),
				pc(ss["ok"], ss["ans"]), pc(ss["err"], ss["ans"]))
			s += "%12s <- unk: %s (%s #chk)\n" % ("", fc(ss["unk"]), pc(ss["unk"], ss["chk"]))

		unk = self.steps[-1].stats["out"]
		s += "  |\n  |\nUnknown: %s (%s #tot)" % (fc(unk), pc(unk, tot))

		return s

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

		Cascade.steps.append(step)
