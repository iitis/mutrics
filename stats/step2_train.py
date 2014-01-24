#!/usr/bin/env python3

import sys
import argparse
import random
from DT import *

def main(P, src, dst):
	samples = []
	total = 0

	# read data
	for line in src:
		line = line.strip()
		if not line[0].isdigit(): continue
		total += 1

		d = line.split()
		proto = 1 if d[1] == "TCP" else 2
		port = int(d[2])
		gt = d[-1]

		stats = [int(x) for x in d[3:-1]]
		if stats[4] == 0 or stats[12] == 0: continue

		v = [proto,port] + stats
		samples.append((v, gt))

	print("read %d samples out of %d total (%.2f)" % (len(samples), total, 1.0*len(samples)/total))

	# take random samples
	if P.t > 0:
		samples = random.sample(samples, P.t+P.T)
		train = samples[:P.t]
		test = samples[P.t:]
	else:
		train = samples
		test = []

	# train
	knc = DT()
	knc.fit([x[0] for x in train], [x[1] for x in train])

	# test
	if len(test) > 0:
		(acc, ratio, err) = knc.score([x[0] for x in test], [x[1] for x in test])
		print("ok %.3f%%\tin %.3f%%\tof %d K total (%d errors)" %
			(acc * 100.0, ratio * 100.0, len(test)/1000.0, err))

	# store model
	if dst: knc.store(dst)

if __name__ == "__main__":
	p = argparse.ArgumentParser()
	p.add_argument('model', nargs='?', help='output file')
	p.add_argument("-t", type=int, default=0, help="number of training patterns [0=all]")
	p.add_argument("-T", type=int, default=0, help="number of testing patterns [0=none]")
	p.add_argument("--exe", help="exec given Python file first (e.g. for params)")
	args = p.parse_args()

	if args.model: marg = open(args.model, "wb")
	else: marg = None

	if args.exe: exec(open(args.exe).read())

	main(args, sys.stdin, marg)
