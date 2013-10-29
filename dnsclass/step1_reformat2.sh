#!/bin/bash
# Simpler reformat

if [ $# -lt 1 ]; then
	echo "usage: $0 outdir < infile.arff" >&2
	exit 1
fi

OUTDIR="$1"
mkdir -p "$OUTDIR"

arff-select 2lpi_proto dns_name fc_dst_port fc_proto | tail -n +2 | grep -v ?dns_name \
	| sed -re 's;(.*)\t(.*)\t(.*)\t(.*);\1\t\2:\3/\4;g' > "$OUTDIR/data.txt"
wc -l "$OUTDIR/data.txt"
