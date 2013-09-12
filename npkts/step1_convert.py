#!/usr/bin/env python3

import sys
import ArffReader

ar = ArffReader.ArffReader(sys.stdin)

print("# ID\tProto/Port\tUp\t\tDown\t\tLabel")

for f in ar:
	# ignore flows without ground truth
	if f["lpi_proto"] == "Unknown": continue

	# ignore flows for which this method does not apply
	if f["pks_1_up"] == "0" or f["pks_1_down"] == "0": continue

	s1 = "{pks_1_up},{pks_2_up},{pks_3_up},{pks_4_up},{pks_5_up}".format_map(f)
	s2 = "{pks_1_down},{pks_2_down},{pks_3_down},{pks_4_down},{pks_5_down}".format_map(f)

	print("{f[fc_id]}\t{f[fc_proto]}/{f[fc_dst_port]}\t{up}\t{down}\t{f[lpi_proto]}\t".format(up=s1, down=s2, f=f))
