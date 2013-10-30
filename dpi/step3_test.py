#!/usr/bin/env python3

import sys
import argparse
import random
from HTClass import *

def main(P, src, model):
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

	# load model
	knc = HTClass()
	knc.load(model)

	# test
	(acc, ratio, err) = knc.score([x[0] for x in samples], [x[1] for x in samples])
	print("ok %.3f%%\tin %.3f%%\tof %d K total (%d errors)" %
		(acc * 100.0, ratio * 100.0, len(samples)/1000.0, err))

if __name__ == "__main__":
	p = argparse.ArgumentParser(description='First payload bytes traffic classifier')
	p.add_argument('model', help='model file')
	p.add_argument("-n", type=int, default=2, help="number of bytes [2]")
	p.add_argument("--exe", help="exec given Python file first (e.g. for params)")
	args = p.parse_args()

	if args.model: marg = open(args.model, "rb")
	else: marg = None

	if args.exe: exec(open(args.exe).read())

	main(args, sys.stdin, marg)

