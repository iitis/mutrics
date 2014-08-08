# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

import operator
import pickle
from collections import defaultdict, Counter
from common import *
from multiprocessing import Pool

def ask_task(task):
	i, f = task
	step = BKS.steps[i]
	proto = "Skip"

	if hasattr(step, "init"):
		step.init(f)
	if step.check(f):
		proto = step.classify(f)
	if hasattr(step, "finish"):
		step.finish(f)

	return proto

class BKS(object):
	def __init__(self):
		self.Tr = dict()
		self.T = dict()
		self.stats = defaultdict(int)
		self.p = Pool()

	def ask(self, f):
		ret = []

		self.stats["in"] += 1

		tasks = [(i, f) for i in range(len(self.steps))]
#		res = self.p.map(ask_task, tasks)
		res = map(ask_task, tasks)

		for (proto, step) in zip(res, self.steps):
			if proto != "Skip":
				step.stats["chk"] += 1

				if proto == "Unknown":
					step.stats["unk"] += 1
				else:
					step.stats["ans"] += 1

					if proto == f.gt:
						step.stats["ok"] += 1
					else:
						step.stats["err"] += 1

				ret.append(proto)
			else:
				step.stats["skp"] += 1
				ret.append("Unknown")

		return ret

	## classify Flow and update stats
	def classify(self, f, s):
		k = ','.join(s)
		proto = "Unknown"

		if k in self.T:
			proto = self.T[k]
		else:
			proto = self.majority(s)

		f.classify(proto, "BKS")

		if proto == "Unknown":
			self.stats["unk"] += 1
		else:
			self.stats["ans"] += 1

			if f.isok():
				self.stats["ok"] += 1
			else:
				self.stats["err"] += 1

	## do majority voting
	def majority(self, s):
		cl = Counter(s).most_common(2)
		if cl[0][0] == "Unknown" and len(cl) > 1:
			return cl[1][0]
		else:
			return cl[0][0]

	## count s as belonging to gt
	def train(self, s, gt):
		k = ','.join(s)

		# FIXME: dont count all-unknowns?

		if k not in self.Tr:
			self.Tr[k] = {gt: 1}
		else:
			if gt not in self.Tr[k]:
				self.Tr[k][gt] = 1
			else:
				self.Tr[k][gt] += 1

	## reduce self.Tr by choosing the most frequent answers
	def train_finish(self):
		self.T = {k:max(v.items(), key=operator.itemgetter(1))[0] for (k,v) in self.Tr.items()}

	def train_show(self):
		for (k,v) in self.T.items(): print("  %s -> %s" % (k,v))

	def train_store(self, dst):
		pickle.dump(self.T, dst)
		dst.flush()

	def train_load(self, src):
		self.T = pickle.load(src)

	def get_stats(self):
		s = ""

		if len(self.steps) == 0: return

		tot = float(self.stats["in"])
		s += "Total: %s (#tot)\n" % fc(tot)

		for step in self.steps:
			ss = step.stats

			s += "[%-10s]\n" % step.name
			s += "  -> chk: %s (%s #tot)\n" % (fc(ss["chk"]), pc(ss["chk"], tot))
			s += "  -> unk: %s (%s #tot)\n" % (fc(ss["unk"]), pc(ss["unk"], tot))
			s += "  -> ok/err: %s/%s (%s/%s #ans)\n" % \
				(fc(ss["ok"]), fc(ss["err"]), pc(ss["ok"], ss["ans"]), pc(ss["err"], ss["ans"]))

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

		cls.steps.append(step)
