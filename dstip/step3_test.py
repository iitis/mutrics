#!/usr/bin/env python3
# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

import sys
import argparse
import random
from HTClass import *

def main(P, src, model):
	samples = []

	# read data
	for line in src:
		line = line.strip()
		if not line[0].isdigit(): continue

		(fid, addr, port, gt) = line.split()
		samples.append((str([addr, port]), gt))

	# load model
	knc = HTClass()
	knc.load(model)

	# test
	(acc, ratio, err) = knc.score([x[0] for x in samples], [x[1] for x in samples])

	# print the result
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
