#
# DNS-Class
# TODO: target DNS flows
#

from ClassTree import *

def check(f):
	if "dns_name" in f.data and f.data["dns_name"][0] != '?':
		return True
	elif f.data["lpi_proto"] == "DNS":
		return True
	else:
		return False

def classify(f):
	dn = f.data["dns_name"]

	if f.data["lpi_proto"] == "DNS":
		return "DNS"
	elif dn[0:4] == "www.":
		return "WWW"
	else:
		return "Unknown"

ClassTree.register("dnsclass", check, classify)
