#!/usr/bin/env python3
# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2014-2015 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

import sys
import argparse
import pickle
import itertools
import math
import random

#########################################################################

def generator(profile):
	E = list(profile.keys() - "F")

	for m in range(1, len(E)+1):
		for Y in itertools.combinations(E, m):
			for X in itertools.permutations(Y):
				yield X

def optimizer(profile, X, E, bestX, bestC, i=""):
	# evaluate this solution
	if len(X) > 0:
		cost = evaluate(profile, X)

		if cost >= bestC:
			# no need to try deeper
			return (bestX, bestC)
		else:
			# found new minima
			bestX, bestC = X, cost
			print("%s%s %s" % (i, cost, X))

	# recurse deeper
	for m in E:
		x, e = X.copy(), E.copy()
		x.append(m)
		e.remove(m)
		print("%strying %s, bestC=%s" % (i, x, bestC))
		bestX, bestC = optimizer(profile, x, e, bestX, bestC, i+"  ")

	return (bestX, bestC)

def optimizer2(profile, sol):
	E = list(profile.keys() - "F")

	for m in E:
		print("--> %s <--" % m)
		optimizer_branch(profile, sol, len(profile["F"]), profile["F"].copy(), [], E.copy(), 0.0, 0.0, m, "  ")

def optimizer_branch(profile, sol, L, G, X, E, tX, eX, m, i=""):
#	print("%s%s: adding %s" % (i, X, m))

	X.append(m)
	E.remove(m)

	P = profile[m]
#	print("|G|=%d, ts=%g, |G-FS|=%d, tc=%g" % (len(G), P["ts"], len(G.difference(P["FS"])), P["tc"]))
	tX += len(G)*P["ts"] + len(G.difference(P["FS"]))*P["tc"]
	eX += len(G.intersection(P["FE"]))
	G.difference_update(P["FO"])
	G.difference_update(P["FE"])
	uX = len(G)

	C = cost(L, tX, eX, uX)
	if C < sol["bestC"]:
		print("%s%s: %g %g %g -> %g" % (i, X, tX, eX, uX, C))
		sol["bestC"] = C
		sol["bestX"] = X

	# recurse
	for m in E:
		optimizer_branch(profile, sol, L, G.copy(), X.copy(), E.copy(), tX, eX, m, i+"  ")


#########################################################################

def evaluate(profile, X):
	G = profile["F"].copy()
	tX = 0.0
	eX = 0.0
	uX = 0.0

	for x in X:
		P = profile[x]
#		print("|G|=%d, ts=%g, |G-FS|=%d, tc=%g" % (len(G), P["ts"], len(G.difference(P["FS"])), P["tc"]))
		tX += len(G)*P["ts"] + len(G.difference(P["FS"]))*P["tc"]
		eX += len(G.intersection(P["FE"]))
#		G = G.intersection(P["FS"].union(P["FR"]))
		G.difference_update(P["FO"])
		G.difference_update(P["FE"])

	uX = len(G)

	return tX, eX, uX

def cost(L, tX, eX, uX):
	# normalize
	tX = tX/L * 1000000.0
	eX = eX/L * 1000000.0
	uX = uX/L * 1000000.0

	# compute
	C = math.pow(tX, 0.5) + math.pow(eX, 1.5) + math.pow(uX, 1.1);

	return C

#########################################################################

def main():
	# parse arguments
	p = argparse.ArgumentParser(description='Waterfall optimizer')

	p.add_argument("--exe", help="exec given Python file first (e.g. for params)")
	p.add_argument('-P','--profile', required=True, type=argparse.FileType('rb'), help="file with module profiles")

	args = p.parse_args()

	if args.exe: exec(open(args.exe).read())

	###
	profile = pickle.load(args.profile)
	mincost = float("inf")
	minX = []

	sol = {"bestC": float("inf"), "bestX": []}
	optimizer2(profile, sol)

#	return
#	minX, mincost = optimizer(profile, [], list(profile.keys() - "F"), [], float('inf'))
#	print("Solution 1:", minX, "- cost", mincost)

	for X in generator(profile):
		tX, eX, uX = evaluate(profile, X)
		C = cost(len(profile["F"]), tX, eX, uX)
		if (C < mincost):
			mincost, minX = C, X
			print("%s: %g %g %g -> %g" % (X, tX, eX, uX, C))

	print("Solution 2: %s, cost %g" % (minX, mincost))

if __name__ == "__main__": main()
