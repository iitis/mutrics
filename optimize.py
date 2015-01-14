#!/usr/bin/env python3
# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2014-2015 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

import sys
import argparse
import pickle
import math

from Cascade import *
from collections import defaultdict

def optimizer_start(profile, sol):
	E = list(profile.keys() - "F")
	print(profile.keys())

	for m in E:
		print("--> %s <--" % m)
		optimizer_branch(profile, sol, len(profile["F"]), profile["F"].copy(), [], E.copy(), 0.0, 0.0, m, "  ")

def optimizer_branch(profile, sol, L, G, X, E, tX, eX, m, i=""):
	X.append(m)
	E.remove(m)

	P = profile[m]
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

def evaluate(profile, X):
	G = profile["F"].copy()
	tX = 0.0
	eX = 0.0
	uX = 0.0
	cs = Cascade()
	cs.steps = []

	for x in X:
		P = profile[x]

		num_in  = len(G)
		num_chk = len(G.difference(P["FS"]))
		num_ok  = len(G.intersection(P["FO"]))
		num_err = len(G.intersection(P["FE"]))

		# update cost factors
		tX += num_in * P["ts"] + num_chk * P["tc"]
		eX += num_err
		G.difference_update(P["FO"])
		G.difference_update(P["FE"])

		# make stats
		step = lambda:0
		step.name = x
		step.stats = defaultdict(int)
		cs.steps.append(step)

		ss = step.stats
		ss["in"]  = num_in
		ss["chk"] = num_chk
		ss["skp"] = num_in - num_chk
		ss["unk"] = num_chk - num_ok - num_err
		ss["ans"] = num_ok + num_err
		ss["ok"]  = num_ok
		ss["err"] = num_err
		ss["out"] = len(G)

	uX = len(G)

	return tX, eX, uX, cs.get_stats()

def cost(L, tX, eX, uX):
	# normalize
	tX = tX/L * 1000000.0
	eX = eX/L * 1000000.0
	uX = uX/L * 1000000.0

	# compute
	C = math.pow(tX, 0.95) + math.pow(eX, 1.75) + math.pow(uX, 1.2);

	return C

#########################################################################

def main():
	# parse arguments
	p = argparse.ArgumentParser(description='Waterfall optimizer')
	p.add_argument("--exe", help="exec given Python file first (e.g. for params)")
	p.add_argument('-P','--profile', required=True, type=argparse.FileType('rb'), help="file with module profiles")
	p.add_argument('-E','--evaluate', nargs='+', type=str, help="cascade to evaluate")
	args = p.parse_args()

#	for e in args.evaluate: print(e)
#	return

	if args.exe: exec(open(args.exe).read())

	###
	profile = pickle.load(args.profile)
	sol = {"bestC": float("inf"), "bestX": []}
	optimizer_start(profile, sol)

	print("Solution %s: %g" % (sol["bestX"], sol["bestC"]))

	tX, eX, uX, stats = evaluate(profile, sol["bestX"])
	print(stats)

if __name__ == "__main__": main()
