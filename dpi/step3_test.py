#!/usr/bin/env python3
# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

import sys
import argparse
import random
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
		pl_up = [int(x) for x in d[3:3+b]][0:P.i]
		pl_down = [int(x) for x in d[3+b:-1]][0:P.i]

		if pl_up[0] == -1 or pl_down[0] == -1: continue

		v = [proto,port] + pl_up + pl_down
		samples.append((v, gt))

	# load model
	cls = DT(verb=True)
	cls.load(model)

	# test
	(acc, ratio, err) = cls.score([x[0] for x in samples], [x[1] for x in samples])
	print("ok %.3f%%\tin %.3f%%\tof %d K total (%d errors)" %
		(acc * 100.0, ratio * 100.0, len(samples)/1000.0, err))

if __name__ == "__main__":
	p = argparse.ArgumentParser()
	p.add_argument('model', help='model file')
	p.add_argument("-i", type=int, default=8, help="number of bytes [8]")
	p.add_argument("--exe", help="exec given Python file first (e.g. for params)")
	args = p.parse_args()

	marg = open(args.model, "rb")
	if args.exe: exec(open(args.exe).read())

	main(args, sys.stdin, marg)

