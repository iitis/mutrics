#!/usr/bin/env python3

import sys
import argparse
from Flow import *
from Cascade import *
from Stats import *

#########################################################################

def mutrics(src, dst, dump, dumpl, limit, fmt, cstats, stats):
	# read the ARFF header
	Flow.read_arff_header(src)

	# init modules
	cs = Cascade()
	st = Stats()

	# go!
	for line in src:
		line = line.strip()
		if not line[0:1].isdigit(): continue

		# read the flow and check it
		f = Flow(line)
		if f.gt in P.skip: continue

		# classify
		show = cs.classify(f, dump, dumpl)

		# print it to the user?
		if not show:
			continue
		if limit:
			if f.isunk():
				if "unk" not in limit: continue
			elif "ans" not in limit:
				if f.isok()  and "ok"  not in limit: continue
				if f.iserr() and "err" not in limit: continue

		# print and count
		f.write(dst, fmt)
		st.count(f)

	# cascade stats?
	if cstats:
		if fmt != "none": print("")
		print("Cascade statistics")
		print("==================")
		print(cs.get_stats())

	# perf stats?
	if stats:
		if cstats: print("")
		print("Performance statistics")
		print("======================")
		print(st.get_cm())

#########################################################################

def main():
	# parse arguments
	p = argparse.ArgumentParser(description='Multilevel Traffic Classifier')

	p.add_argument('input', nargs='?',
		type=argparse.FileType('r'), default=sys.stdin, help='input file in ARFF format [stdin]')
	p.add_argument('output', nargs='?',
		type=argparse.FileType('w'), default=sys.stdout, help='output file [stdout]')
	p.add_argument("--exe", default='./params.py', help="exec given Python file first (e.g. for params)")
	p.add_argument("--dump", nargs=1, help="dump given flows of a particular module (e.g. dnsclass:Unk+Err)")
	p.add_argument("--limit", nargs=1, help="limit output to given flows (e.g. Unk+Err)")
	p.add_argument("-f","--format", choices=['txt', 'arff', 'none'], default='txt', help="output format")
	p.add_argument('-s','--stats', action='store_true', help="print performance statistics")
	p.add_argument('-c','--cstats', action='store_true', help="print cascade statistics")

	args = p.parse_args()

	# dumping
	dump = None
	dumpl = []
	if args.dump:
		try:
			(dump, v) = [x.strip().lower() for x in args.dump[0].split(":")]
			dumpl = [x.strip().lower() for x in v.split("+")]
		except:
			dump = (args.dump[0].split(":")[0]).strip().lower()
			dumpl = ["ans"]

	# limits
	if args.limit:
		limit = [x.strip().lower() for x in args.limit[0].split("+")]
	else:
		limit = None

	# params.py
	if args.exe:
		exec(open(args.exe).read())

	mutrics(args.input, args.output, dump, dumpl, limit, args.format, args.cstats, args.stats)

if __name__ == "__main__": main()
