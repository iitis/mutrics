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
		if not line[0].isdigit(): continue

		(fid, addr, port, gt) = line.split()
		samples.append((str([addr, port]), gt))

	# take random samples
	if numtrain > 0:
		samples = random.sample(samples, numtrain + numtest)
		train = samples[:numtrain]
		if numtest > 0:
			test  = samples[numtrain:]
		else:
			test = []
	else:
		random.shuffle(samples)
		train = samples
		test = []

	# compute the minc
	minc = int(0.0001 * len(train))
	print(minc)

	# train
	knc = HTClass(minc=minc)
	knc.fit([x[0] for x in train], [x[1] for x in train])

	# test
	if len(test) > 0:
		(acc, ratio, err) = knc.score([x[0] for x in test], [x[1] for x in test])
		print("%.4f\t%.4f" % (acc * 100.0, ratio * 100.0))

	# store model
	if dst:
		knc.store(dst)

if __name__ == "__main__":
	p = argparse.ArgumentParser(description='Destination IP traffic classifier')
	p.add_argument('model', nargs='?', help='output file')
	p.add_argument('-f','--file', default="-", help='input file [stdin]')
	p.add_argument("-n", type=int, default=1, help="number of packets [1]")

	p.add_argument("-t", type=int, default=0, help="number of training patterns [0=all]")
	p.add_argument("-T", type=int, default=0, help="number of testing patterns [0=none]")
	p.add_argument("--exe", help="exec given Python file first (e.g. for params)")
	args = p.parse_args()

	if args.model:
		marg = open(args.model, "wb")
	else:
		marg = None

	if args.file == "-":
		farg = sys.stdin
	else:
		farg = open(args.file, "r")

	if args.exe:
		exec(open(args.exe).read())

	main(args, farg, marg, args.t, args.T)

