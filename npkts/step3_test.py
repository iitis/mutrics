#!/usr/bin/env python3

import sys
import argparse
import random
from HTClass import *

def main(param, src, model):
	samples = []

	# read data
	for line in src:
		line = line.strip()
		if not line[0].isdigit(): continue

		(fid, protoport, ups, downs, gt) = line.split()
		up   = ups.split(',')[:param.n]
		down = downs.split(',')[:param.n]

		samples.append(([protoport] + up + down, gt))

	# test
	knc = HTClass()
	knc.load(model)

	# test
	(acc, ratio) = knc.score([x[0] for x in samples], [x[1] for x in samples])
	print("%.2f\t%.2f" % (acc * 100.0, ratio * 100.0))

if __name__ == "__main__":
	p = argparse.ArgumentParser(description='First packets size traffic classifier tester')
	p.add_argument('model', help='model file')
	p.add_argument('-f','--file', default="-", help='input file [stdin]')
	p.add_argument("-n", type=int, default=1, help="number of packets [1]")
	p.add_argument("--exe", help="exec given Python file first (e.g. for params)")
	args = p.parse_args()

	marg = open(args.model, "rb")

	if args.file == "-":
		farg = sys.stdin
	else:
		farg = open(args.file, "r")

	if args.exe:
		exec(open(args.exe).read())

	main(args, farg, marg)

