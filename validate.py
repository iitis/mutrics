#!/usr/bin/env python3
# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

import sys
import argparse
import itertools
import random
import time

import optimize

from Flow import *
from Cascade import *
from BKS import *
from arff_tools import ArffReader

#########################################################################

def readflows():
	src = ArffReader.ArffReader(sys.stdin)

	if hasattr(P, "skip"):
		check = lambda gt: gt not in P.skip
	elif hasattr(P, "select"):
		check = lambda gt: gt in P.select
	else:
		check = lambda: True

	flows = []
	for d in src:
		gt = d[P.gtcol]
		if not check(gt): continue
		f = Flow(src, d, gt)
		flows.append(f)

	return flows

def makeprofile(flows):
	cs = BKS(True)
	for f in flows: cs.ask(f)
	return cs.Pr

def generator(profile):
	E = list(profile.keys() - "F")
	ret = []

	for m in range(1, len(E)+1):
		for Y in itertools.combinations(E, m):
			for X in itertools.permutations(Y):
				ret.append(X)

	return ret

def compare(flows, profile, X):

	### real cascade
	cs = Cascade()
	cs.steps = []
	for x in X: cs.steps.append(P.mods[x])

	real_err = 0
	real_unk = 0
	start = time.time()
	for f in flows:
		f.proto = "Unknown"
		cs.classify(f)
		if f.isunk(): real_unk += 1
		elif f.iserr(): real_err += 1
	real_time = time.time() - start

	### simulated cascade
	sim_time, sim_err, sim_unk, sim_stats = optimize.evaluate(profile, X)

	return (real_time, real_err, real_unk), (sim_time, sim_err, sim_unk)

#########################################################################

def main():
	# parse arguments
	p = argparse.ArgumentParser(description='Validate real vs simulated classification costs')

	p.add_argument("-n", "--num", type=int, default=100, help="number of cascades to generate")
	p.add_argument("--exe", default='./params.py', help="exec given Python file first (e.g. for params)")
	p.add_argument("--gt", help="column with ground-truth")
	args = p.parse_args()

	# params
	if args.exe: exec(open(args.exe).read())
	if args.gt: P.gtcol = args.gt

	###
	print("Reading flows...")
	flows = readflows()
	print("  read %d flows" % len(flows))

	print("Profiling...")
	profile = makeprofile(flows)
	print("  done")

	print("Generating %d cascades..." % args.num)
	cascades = random.sample(generator(profile), args.num)

	print("Validating...")
	for X in cascades:
		real, sim = compare(flows, profile, X)
		print(("%g\t%d\t%d\t%g\t%d\t%d\t" % (real[0], real[1], real[2], sim[0], sim[1], sim[2])), X)

if __name__ == "__main__": main()
