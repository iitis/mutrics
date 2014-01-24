# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

import pickle
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

class kNN(object):
	def __init__(self, k=3, verb=False):
		self.algo = KNeighborsClassifier(n_neighbors=k)
		self.verb = verb
		self.answer = None

	def store(self, dst): pickle.dump(self.algo, dst)
	def load(self, src): self.algo = pickle.load(src)

	def fit(self, X, Y):
		protos = set(Y)
		if len(protos) == 1:
			self.answer = protos.pop()
		else:
			self.algo.fit(X, Y)

	def score(self, X, Y):
		ok = 0
		err = 0
		unk = 0

		if len(X) == 0: return (1.0, 1.0, 0)

		if not self.answer:
			labels = self.algo.classes_
			P = self.algo.predict_proba(X)
			for x, proba, y in zip(X, P, Y):
				i = np.argmax(proba)
				l = labels[i]
				v = proba[i]

				if v < 1:
					unk += 1
				else:
					if l == y:
						ok += 1
					else:
						if self.verb: print("error: %s is %s, not %s" % (x, y, l))
						err += 1
		else:
			for y in Y:
				if self.answer == y:
					ok += 1
				else:
					if self.verb: print("error: %s is %s, not %s" % (x, y, l))
					err += 1

		if ok+err > 0: acc = 1.0 * ok / (ok+err)
		else: acc = 0.0
		scope = 1.0 - 1.0 * unk/len(X)

		if scope == 0.0: acc = 1.0

		return (acc, scope, err)

	def one(self, k):
		if self.answer: return self.answer

		try:
			proba = self.algo.predict_proba([k])[0]
			i = np.argmax(proba)
			if proba[i] < 1:
				return "Unknown"
			else:
				return self.algo.classes_[i]
		except:
			return "Unknown"
