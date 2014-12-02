#!/usr/bin/env python3
# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

import sys
import argparse
import pickle
import itertools
import math

#########################################################################

def generator(profile):
	E = list(profile.keys() - "F")

	for m in range(1, len(E)+1):
		for Y in itertools.combinations(E, m):
			for X in itertools.permutations(Y):
				yield X

#########################################################################

def evaluate(profile, X):
	G = profile["F"]
	l = float(len(G))
	tX = 0.0
	eX = 0.0
	uX = 0.0

	for x in X:
		P = profile[x]
		tX += len(G)*P["ts"] + len(G.difference(P["FS"]))*P["tc"]
		eX += len(G.intersection(P["FE"]))
		G = G.intersection(P["FS"].union(P["FR"]))

	uX = len(G)

	return (tX/l*1000000.0, eX/l*1000000.0, uX/l*1000000.0)

#########################################################################

def cost(tX, eX, uX):
	return math.pow(tX, 0.5) + math.pow(eX, 1.5) + math.pow(uX, 1.1);

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

	for X in generator(profile):
		tX, eX, uX = evaluate(profile, X)
		C = cost(tX, eX, uX)

		if (C < mincost):
			mincost = C
			minX = X
			print(X, "->", tX, eX, uX, "->", C)

	print("Solution:", minX, "- cost", mincost)

if __name__ == "__main__": main()
