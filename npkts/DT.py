import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from sklearn.utils import array2d
from sklearn.tree._tree import DTYPE
#from multiprocessing import pool

class DT(object):
	def __init__(self, verb=False):
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

#	def _predict_proba(self, arg):
#		i, X = arg
#		return self.algo.estimators_[i].predict_proba(X)

	def predict_proba(self, X):
		n_samples = len(X)
		n_classes = len(self.algo.classes_)
		n_estimators = len(self.algo.estimators_)
		all_proba = np.zeros((n_samples, n_classes))

		# convert
		X = array2d(X, dtype=DTYPE)

#		# ask the trees
#		args = [(i, X) for i in range(len(self.algo.estimators_))]
#		probas = pool.Pool().map(self._predict_proba, args)
#
#		# reduce
#		for tree, proba_tree in zip(self.algo.estimators_, probas):

		for tree in self.algo.estimators_:
			proba_tree = tree.predict_proba(X)

			if n_classes == tree.n_classes_:
				all_proba += proba_tree
			else:
				for j, c in enumerate(tree.classes_):
					all_proba[:, c] += proba_tree[:, j]

		return (all_proba / n_estimators)

	def one(self, k):
		proba = self.predict_proba([k])[0]
		i = np.argmax(proba)
		if proba[i] < 1:
			return "Unknown"
		else:
			return self.algo.classes_[i]
