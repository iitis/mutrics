from Cascade import *

def check(f):
	gt = f.data["lpi_proto"]
	return gt in ['TCP_Empty', 'Unknown']

def classify(f):
	#return f.data["lpi_proto"]
	return "SKIP"

Cascade.register("dummy", check, classify)
