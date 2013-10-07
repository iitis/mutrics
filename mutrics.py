#!/usr/bin/env python3

import sys
import argparse
from Flow import *
from Cascade import *

#########################################################################

def mutrics(farg):
	read_arff_header(farg)
	ct = Cascade()

	for line in farg:
		line = line.strip()
		if not line[0:1].isdigit(): continue

		# read the flow and check it
		f = Flow(line)
		if f.gt in P.skip: continue

		# classify
		(mod, proto, history) = ct.classify(f)
		f.classify(mod, proto, history)

		# write
		print(f.txt())

def read_arff_header(farg):
	for line in farg:
		line = line.strip()

		if line[0:11] == '@attribute ':
			field = line.split()[1]
			Flow.add_field(field)
		elif line[0:5] == '@data':
			return

#########################################################################

def main():
	p = argparse.ArgumentParser(description='Multilevel, Modular Traffic Classifier')
	p.add_argument('file', nargs='?', help='input file in ARFF format [stdin]')
	p.add_argument("--exe", default='./params.py', help="exec given Python file first (e.g. for params)")
	args = p.parse_args()

	if not args.file:
		farg = sys.stdin
	else:
		farg = open(args.file, "r")

	if args.exe: exec(open(args.exe).read())
	mutrics(farg)

if __name__ == "__main__": main()
