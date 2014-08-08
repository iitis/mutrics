#!/usr/bin/env python3
# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

import sys
import argparse
from Flow import *
from Cascade import *
from BKS import *
from Stats import *
from arff_tools import ArffReader

#########################################################################

def waterfall(dump, dumpl, limit, fmt, cstats, stats):
	# init modules
	src = ArffReader.ArffReader(sys.stdin)
	dst = sys.stdout
	cs = Cascade()
	st = Stats()

	# setup proto filter
	if hasattr(P, "skip"):
		check = lambda gt: gt not in P.skip
	elif hasattr(P, "select"):
		check = lambda gt: gt in P.select
	else:
		check = lambda: True

	# arff header?
	if fmt == "arff":
		src.printh(nodata=True, dst=dst)
		dst.write("%% Multilevel Traffic Classifier: Waterfall approach\n")
		dst.write("% waterfall_module: classifier that contributed the answer\n")
		dst.write("% waterfall_proto: the identified protocol\n")
		dst.write("@attribute waterfall_module string\n")
		dst.write("@attribute waterfall_proto string\n\n")
		dst.write("@data\n")

	# go!
	for d in src:
		# check if gt is enabled
		gt = d[P.gtcol]
		if not check(gt): continue

		# parse and classify
		f = Flow(src, d, gt)
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
		f.write(fmt, dst)
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

def bks(limit, fmt, cstats, stats, train, test):
	src = ArffReader.ArffReader(sys.stdin)
	dst = sys.stdout
	cs = BKS()
	st = Stats()

	# setup proto filter
	if hasattr(P, "skip"):
		check = lambda gt: gt not in P.skip
	elif hasattr(P, "select"):
		check = lambda gt: gt in P.select
	else:
		check = lambda: True

	# arff header?
	if fmt == "arff":
		src.printh(nodata=True, dst=dst)
		dst.write("%% Multilevel Traffic Classifier: BKS approach\n")
		dst.write("% bks_proto: the identified protocol\n")
		dst.write("@attribute bks_proto string\n\n")
		dst.write("@data\n")

	# load a model?
	if test:
		cs.train_load(test)

	# go!
	for d in src:
		# check if gt is enabled
		gt = d[P.gtcol]
		if not check(gt): continue

		# parse and pass to classifiers
		f = Flow(src, d, gt)
		s = cs.ask(f)

		if train:
			cs.train(s, f.gt)
		else:
			cs.classify(f, s)

			# print it to the user?
			if limit:
				if f.isunk():
					if "unk" not in limit: continue
				elif "ans" not in limit:
					if f.isok()  and "ok"  not in limit: continue
					if f.iserr() and "err" not in limit: continue

			# print and count
			f.write(fmt, dst)
			st.count(f)

	# finish training
	if train:
		cs.train_finish()
		cs.train_store(train)

	# algo stats?
	if cstats:
		print("BKS statistics")
		print("==============")
		print(cs.get_stats())

	# stats?
	if stats:
		if train:
			cs.train_show()
		else:
			print("Performance statistics")
			print("======================")
			print(st.get_cm())

#########################################################################

def main():
	# parse arguments
	p = argparse.ArgumentParser(description='Multilevel Traffic Classifier')

	p.add_argument("--exe", default='./params.py', help="exec given Python file first (e.g. for params)")
	p.add_argument("--gt", help="column with ground-truth")
	p.add_argument("--dump", nargs=1, help="dump given flows of a particular module (e.g. dnsclass:Unk+Err)")
	p.add_argument("--limit", nargs=1, help="limit output to given flows (e.g. Unk+Err)")
	p.add_argument("-f","--format", choices=['txt', 'arff', 'none'], default='txt', help="output format")
	p.add_argument("-a","--algo", choices=['waterfall', 'bks'], default='waterfall', help="ensemble method")
	p.add_argument('-s','--stats', action='store_true', help="print performance statistics")
	p.add_argument('-c','--cstats', action='store_true', help="print algorithm statistics")
	p.add_argument('-q','--quiet', action='store_true', help="equivalent of --format=none")

	p.add_argument('-T','--train', type=argparse.FileType('wb'), help="train given model (BKS)")
	p.add_argument('-E','--test',  type=argparse.FileType('rb'), help="test given model (BKS)")

	args = p.parse_args()

	if args.quiet: args.format = "none"

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

	# params
	if args.exe: exec(open(args.exe).read())
	if args.gt: P.gtcol = args.gt

	if args.algo == "waterfall":
		waterfall(dump, dumpl, limit, args.format, args.cstats, args.stats)
	elif args.algo == "bks":
		bks(limit, args.format, args.cstats, args.stats, args.train, args.test)

if __name__ == "__main__": main()
