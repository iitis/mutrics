import pickle
import numpy as np
#from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

class DT(object):
	def __init__(self, verb=False):
#		self.algo = DecisionTreeClassifier()
		self.algo = RandomForestClassifier(n_jobs=-1)
		self.verb = verb

	def store(self, dst): pickle.dump(self.algo, dst)
	def load(self, src): self.algo = pickle.load(src)

	def fit(self, X, Y):
		protos = set(Y)
		self.algo.fit(X, Y)

	def score(self, X, Y):
		ok = 0
		err = 0
		unk = 0

		if len(X) == 0: return (1.0, 1.0, 0)

		labels = self.algo.classes_
		P = self.algo.predict_proba(X)
		for x, proba, y in zip(X, P, Y):
			i = np.argmax(proba)

			if proba[i] < 1:
				unk += 1
			else:
				l = labels[i]
				if l == y:
					ok += 1
				else:
					if self.verb: print("error: %s is %s, not %s" % (x, y, l))
					err += 1

		if ok+err > 0: acc = 1.0 * ok / (ok+err)
		else: acc = 0.0
		scope = 1.0 - 1.0 * unk/len(X)

		return (acc, scope, err)

	def one(self, k):
		try:
			proba = self.algo.predict_proba([k])[0]
			i = np.argmax(proba)
			if proba[i] < 1:
				return "Unknown"
			else:
				return self.algo.classes_[i]
		except:
			return "Unknown"
