#!/usr/bin/env python3

import sys
import argparse
import random
from HTClass import *

def main(param, src, dst, numtrain, numtest):
	samples = []

	# read data
	for line in src:
		line = line.strip()
		if len(line) == 0 or not line[0].isdigit(): continue

		(fid, proto, port, up, down, gt) = line.split()

		k = ",".join([proto, port, up, down])
		samples.append((k, gt))

	# take random samples
	if numtrain > 0:
		samples = random.sample(samples, numtrain + numtest)
		train = samples[:numtrain]
		test = samples[numtrain:]
	else:
		train = samples
		test = []

	# compute the minc
	minc = int(0.00001 * len(train))
	print("minc=%d" % minc)

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
	p = argparse.ArgumentParser(description='First packets size traffic classifier')
	p.add_argument('model', nargs='?', help='output file')

	p.add_argument("-t", type=int, default=0, help="number of training patterns [0=all]")
	p.add_argument("-T", type=int, default=0, help="number of testing patterns [0=none]")
	p.add_argument("--exe", help="exec given Python file first (e.g. for params)")
	args = p.parse_args()

	if args.model: marg = open(args.model, "wb")
	else: marg = None

	if args.exe: exec(open(args.exe).read())

	main(args, sys.stdin, marg, args.t, args.T)

