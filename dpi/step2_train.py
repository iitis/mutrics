#!/usr/bin/env python3

import sys
import argparse
import random
from HTClass import *

def main(P, src, dst):
	samples = []

	# read data
	for line in src:
		line = line.strip()
		if len(line) == 0 or not line[0].isdigit(): continue

		(fid, proto, port, ups, downs, gt) = line.split("\t")
		up   = ups[:P.n]
		down = downs[:P.n]

		k = "\t".join([proto, port, up, down])
		samples.append((k, gt))

	# take random samples
	if P.t > 0:
		samples = random.sample(samples, P.t + P.T)
		train = samples[:P.t]
		test = samples[P.t:]
	else:
		train = samples
		test = []

	# compute the minc
	minc = int(P.p * len(train))
	print("minc=", minc)

	# train
	knc = HTClass(minc=minc)
	knc.fit([x[0] for x in train], [x[1] for x in train])

	# test
	if len(test) > 0:
		(acc, ratio, err) = knc.score([x[0] for x in test], [x[1] for x in test])
		print("%.4f\t%.4f\t%d errors" % (acc * 100.0, ratio * 100.0, err))

	# store model
	if dst:
		knc.store(dst)

if __name__ == "__main__":
	p = argparse.ArgumentParser(description='First payload bytes traffic classifier')
	p.add_argument('model', nargs='?', help='output file')
	p.add_argument("-n", type=int, default=2, help="number of bytes [2]")
	p.add_argument("-p", type=float, default=0.00002, help="minc factor [0.0001]")

	p.add_argument("-t", type=int, default=0, help="number of training patterns [0=all]")
	p.add_argument("-T", type=int, default=0, help="number of testing patterns [0=none]")
	p.add_argument("--exe", help="exec given Python file first (e.g. for params)")
	args = p.parse_args()

	if args.model: marg = open(args.model, "wb")
	else: marg = None

	if args.exe: exec(open(args.exe).read())

	main(args, sys.stdin, marg)

