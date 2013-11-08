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

		(fid, proto, port, gt) = line.split()

		k = "/".join([proto, port])
		samples.append((k, gt))

	# load model
	knc = HTClass()
	knc.load(model)

	# test
	(acc, ratio, err) = knc.score([x[0] for x in samples], [x[1] for x in samples])

	# print the result
	print("ok %.3f%%\tin %.3f%%\tof %g K total (%d errors)" %
		(acc * 100.0, ratio * 100.0, len(samples)/1000.0, err))

if __name__ == "__main__":
	p = argparse.ArgumentParser()
	p.add_argument('model', help='model file')
	p.add_argument('-f','--file', default="-", help='input file [stdin]')
	p.add_argument("--exe", help="exec given Python file first (e.g. for params)")
	args = p.parse_args()

	marg = open(args.model, "rb")

	if args.file == "-":
		farg = sys.stdin
	else:
		farg = open(args.file, "r")

	if args.exe: exec(open(args.exe).read())

	main(args, farg, marg)

