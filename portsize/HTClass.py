# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

import pickle

class HTClass:
	def __init__(self, minc = 2, draws = False):
		self.ht = {}
		self.minc = minc
		self.draws = draws

	def store(self, dst): pickle.dump(self.ht, dst)
	def load(self, src): self.ht = pickle.load(src)

	def fit(self, X, Y):
		db = {}
		cnts = {}

		for k,y in zip(X, Y):
			if k not in db: db[k] = {}
			if y not in db[k]: db[k][y] = 0
			if y not in cnts: cnts[y] = 0

			db[k][y] += 1
			cnts[y] += 1

		dropped = 0
		saved = 0
		for k,protos in db.items():
			# if no draws...
			if len(protos) == 1:
				(p, c) = list(protos.items())[0]
				r = 100.0 * c / cnts[p]
				if c < self.minc and r < 1.0:
					dropped += c
				else:
					self.ht[k] = p
					saved += c
				continue

			# skip draws?
			if not self.draws:
				continue

			### optional: try to resolve draws... ###

			# skip very small counts
			cand = 0
			(selc, selp) = (0, "")

			for p in protos.keys():
				c = protos[p]

				if c == 1:
					dropped += c
					continue
				else:
					cand += 1
					(selc, selp) = (c, p)

			# still a draw or 0 candidates?
			if cand != 1:
				dropped += selc
				continue

			# skip if its not an important rule anyway
			r = 100.0 * selc / cnts[selp]
			if r < 25.0:
				dropped += selc
				continue
			else:
				self.ht[k] = p
				saved += selc

		return saved, dropped

	def score(self, X, Y):
		ok = 0
		err = 0
		unk = 0

		if len(X) == 0:
			return (1.0, 1.0)

		for k,y in zip(X, Y):
			if k not in self.ht:
				unk += 1
			elif self.ht[k] == y:
				ok += 1
			else:
				#print("error: %s is %s not %s" % (k, y, self.ht[k]))
				err += 1

		#print "input %d, unk %d, ok %d, err %d" % (len(X), unk, ok, err)
		if ok+err > 0:
			acc = 1.0 * ok / (ok+err)
		else:
			acc = 0.0

		scope = 1.0 - 1.0 * unk / len(X)

		return (acc, scope, err)

	def one(self, k):
		try:
			return self.ht[k]
		except:
			return "Unknown"
