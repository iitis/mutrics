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

		b = int((len(d)-4) / 2)
		szup = [int(x) for x in d[3:3+b]][0:P.i]
		szdown = [int(x) for x in d[3+b:-1]][0:P.i]

		if szup[0] == 0 or szdown[0] == 0: continue

		v = [proto,port] + szup + szdown
		samples.append((v, gt))

	# load model
	#cls = kNN(k=P.k, verb=True)
	#cls = kNN(k=P.k)
	cls = DT()
	cls.load(model)

	# test
	(acc, ratio, err) = cls.score([x[0] for x in samples], [x[1] for x in samples])
	print("ok %.3f%%\tin %.3f%%\tof %d K total (%d errors)" %
		(acc * 100.0, ratio * 100.0, len(samples)/1000.0, err))

if __name__ == "__main__":
	p = argparse.ArgumentParser(description='First packets size traffic classifier tester')
	p.add_argument('model', help='model file')
	p.add_argument("-i", type=int, default=1, help="number of packets [1]")
	p.add_argument("-k", type=int, default=3, help="number of neighbors [3]")
	p.add_argument("--exe", help="exec given Python file first (e.g. for params)")
	args = p.parse_args()

	marg = open(args.model, "rb")
	if args.exe: exec(open(args.exe).read())

	main(args, sys.stdin, marg)

