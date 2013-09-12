#!/usr/bin/env python3

import sys
import argparse
from Flow import *
from ClassTree import *

#########################################################################

def mutrics(farg):
	read_arff_header(farg)
	ct = ClassTree()

	for line in farg:
		line = line.strip()
		if not line[0:1].isdigit(): continue

		# classify
		f = Flow(line)
		(mod, proto, history) = ct.classify(f)
		f.register(mod, proto, history)

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
