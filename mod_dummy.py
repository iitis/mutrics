from ClassTree import *

def check(f):
	gt = f.data["lpi_proto"]
	return gt in ['TCP_Empty', 'Unknown']

def classify(f):
	#return f.data["lpi_proto"]
	return "SKIP"

ClassTree.register("dummy", check, classify)
