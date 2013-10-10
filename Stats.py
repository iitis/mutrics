from collections import defaultdict
from common import *

class Stats(object):
	def __init__(self):
		self.total = 0
		self.ans = 0
		self.ok = 0
		self.err = 0
		self.flows = defaultdict(int)
		self.cm = dict()
		self.tp = defaultdict(int)
		self.fp = defaultdict(int)

	def count(self, f):
		self.total += 1
		self.flows[f.gt] += 1

		if f.gt not in self.cm: self.cm[f.gt] = defaultdict(int)
		self.cm[f.gt][f.proto] += 1

		if f.isok():
			self.tp[f.proto] += 1
		else:
			self.fp[f.proto] += 1

		if not f.isunk():
			self.ans += 1
			if f.isok(): self.ok += 1
			else: self.err += 1

	def get_cm(self):
		# proto list
		pl = sorted(self.flows.keys(), key=lambda s:s.lower())

		tps = []
		fps = []

		h = "%-15s\t%7s" % ("Protocol", "Flows")
		s = ""
		for i,p in enumerate(pl):
			L = int2str(i)
			flows = self.flows[p]

			h += "\t%7s" % L
			s += "\n%s = %-11s\t%7s" % (L, p[0:11], fc(flows))

			for p2 in pl + ["Unknown"]:
				v = pc(self.cm[p][p2], self.flows[p])
				if v == '0%': v = ""
				s += "\t%7s" % v

			# true/false positives
			tp = pc(self.tp[p], flows)
			fp = pc(self.fp[p], self.total - flows)
			s += "\t%7s\t%7s" % (tp, fp)

			# for the global average
			tps.append(100.0 * self.tp[p]/flows)
			fps.append(100.0 * self.fp[p]/(self.total-flows))
		h += "\t%7s\t%7s\t%7s" % ("UNK", '%TP', '%FP')

		if len(tps):
			tp = 1.0 * sum(tps) / len(tps)
			fp = 1.0 * sum(fps) / len(fps)

			s += "\n\nAverage %%TP: %6.3g%%\n" % tp
			s += "Average %%FP: %6.3g%%\n" % fp
			s += "Selected: %s of flows\n" % pc(self.ans, self.total)
			s += "  ok:  %4s\n" % pc(self.ok, self.ans)
			s += "  err: %4s" % pc(self.err, self.ans)

		return h + s
