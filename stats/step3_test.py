#!/usr/bin/env python3

import sys
import argparse
import random
#from kNN import *
from DT import *

def main(P, src, model):
	samples = []

	# read data
	for line in src:
		line = line.strip()
		if not line[0].isdigit(): continue

		d = line.split()
		proto = 1 if d[1] == "TCP" else 2
		port = int(d[2])
		gt = d[-1]

		stats = [int(x) for x in d[3:-1]]
		if stats[4] == 0 or stats[12] == 0: continue

		v = [proto,port] + stats
		samples.append((v, gt))

	# load model
	cls = DT()
	cls.load(model)
	cls.algo.set_params(n_jobs=-1)

	# test
	(acc, ratio, err) = cls.score([x[0] for x in samples], [x[1] for x in samples])
	print("ok %.3f%%\tin %.3f%%\tof %d K total (%d errors)" %
		(acc * 100.0, ratio * 100.0, len(samples)/1000.0, err))

if __name__ == "__main__":
	p = argparse.ArgumentParser(description='First packets size traffic classifier tester')
	p.add_argument('model', help='model file')
	p.add_argument("--exe", help="exec given Python file first (e.g. for params)")
	args = p.parse_args()

	marg = open(args.model, "rb")
	if args.exe: exec(open(args.exe).read())

	main(args, sys.stdin, marg)

