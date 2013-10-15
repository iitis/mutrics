#!/usr/bin/env python3

import sys
import ArffReader

ar = ArffReader.ArffReader(sys.stdin)

print("# ID\tDst IP:port\t\tLabel")

for f in ar:
	# ignore flows without ground truth
	if f["lpi_proto"] == "Unknown": continue

	print("{fc_id}\t{fc_dst_addr}\t{fc_dst_port}\t{lpi_proto}".format_map(f))
