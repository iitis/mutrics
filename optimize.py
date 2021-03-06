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

def optimizer_start(args, profile, sol):
	E = list(profile.keys() - "F")
	E.sort()
	print(E)

	for m in E:
		print("--> %s <--" % m)
		optimizer_branch(args, profile, sol, len(profile["F"]), profile["F"].copy(), [], E.copy(), 0.0, 0.0, m, "  ")

counter = 0
def optimizer_branch(args, profile, sol, L, G, X, E, tX, eX, m, i=""):
	global counter
	counter += 1

	X.append(m)
	E.remove(m)

	P = profile[m]
	tX += len(G)*P["ts"] + len(G.difference(P["FS"]))*P["tc"]
	eX += len(G.intersection(P["FE"]))
	G.difference_update(P["FO"])
	G.difference_update(P["FE"])
	uX = len(G)

	C,tXn,eXn,uXn = cost(args, L, tX, eX, uX)
	if C < sol["bestC"]:
		print("%s%s: %g %g %g -> %g" % (i, X, tXn, eXn, uXn, C))
		sol["bestC"] = C
		sol["bestX"] = X

	# recurse
	for m in E:
		optimizer_branch(args, profile, sol, L, G.copy(), X.copy(), E.copy(), tX, eX, m, i+"  ")

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

def cost(args, L, tX, eX, uX):
	# normalize
	tX = tX/L * 1000000.0
	eX = eX/L * 1000000.0
	uX = uX/L * 1000000.0

	# compute
	C = math.pow(tX, args.t) + math.pow(eX, args.e) + math.pow(uX, args.u);

	return C,tX,eX,uX

#########################################################################

def main():
	# parse arguments
	p = argparse.ArgumentParser(description='Waterfall optimizer')
	p.add_argument("--exe", help="exec given Python file first (e.g. for params)")
	p.add_argument('-P','--profile', required=True, type=argparse.FileType('rb'), help="file with module profiles")
	p.add_argument('-E','--evaluate', type=str, help="cascade to evaluate (mod1,mod2,...)")
	p.add_argument('-t', type=float, default=0.95, help='f(): tX exponent')
	p.add_argument('-e', type=float, default=1.75, help='e(): eX exponent')
	p.add_argument('-u', type=float, default=1.20, help='u(): UX exponent')
	p.add_argument('--show', action='store_true', help='show profile and quit')
	args = p.parse_args()

	if args.exe: exec(open(args.exe).read())

	###
	profile = pickle.load(args.profile)

	# display the profile
	#L = float(len(profile["F"]))
	for mod in profile:
		if mod == "F": continue
		P = profile[mod]
		print("%-10s: T=%6.1f" % (mod, (P["ts"]+P["tc"]*1e6)))
#		fser = (L - len(P["FS"])) / L*100.0
#		frr = len(P["FR"]) / L*100.0
#		fer = len(P["FE"]) / L*100.0
#		print("%-10s: T=%6.1f, FE=%.1f%%" %
#			(mod, (P["ts"]+P["tc"]*1e6), fer))
	print("")
	if args.show: return

	# just evaluate given X?
	if args.evaluate:
		X = args.evaluate.split(',')

	# find the best!
	else:
		sol = {"bestC": float("inf"), "bestX": []}
		optimizer_start(args, profile, sol)
		print("Best solution %s: %g" % (sol["bestX"], sol["bestC"]))
		X = sol["bestX"]

	tX, eX, uX, stats = evaluate(profile, X)
	C,tXn,eXn,uXn = cost(args, len(profile["F"]), tX, eX, uX)
	print(stats)
	print("\n%s\t%.1f\t%.1f\t%.1f\t%.1f" % (",".join(X), tXn, eXn, uXn, C))

	global counter
	print("\nnumber of iterations: %d" % (counter))

if __name__ == "__main__": main()
