#!/usr/bin/env python3

import sys
import argparse
import random
from kNN import *

def main(P, src, model):
	samples = []

	# read data
	for line in src:
		line = line.strip()
		if not line[0].isdigit(): continue

		(fid, proto, port, up, down, gt) = line.split()
		up   = int(up)
		down = int(down)

		samples.append(([up, down], gt))

	# load model
	cls = kNN(k=P.k)
	cls.load(model)

	# test
	(acc, ratio, err) = cls.score([x[0] for x in samples], [x[1] for x in samples])
	print("ok %.3f%%\tin %.3f%%\tof %d K total (%d errors)" %
		(acc * 100.0, ratio * 100.0, len(samples)/1000.0, err))

if __name__ == "__main__":
	p = argparse.ArgumentParser(description='First packets size traffic classifier tester')
	p.add_argument('model', help='model file')
	p.add_argument("-k", type=int, default=3, help="number of neighbors [3]")
	p.add_argument("--exe", help="exec given Python file first (e.g. for params)")
	args = p.parse_args()

	marg = open(args.model, "rb")
	if args.exe: exec(open(args.exe).read())

	main(args, sys.stdin, marg)

