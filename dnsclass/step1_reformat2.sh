#!/bin/bash
# Simpler reformat

OUTDIR="$1"
GT="${2:-gt}"

if { [[ -z "$OUTDIR" ]] || [[ "$OUTDIR" = "-h" ]]; }; then
	echo "usage: $0 outdir < infile.arff" >&2
	exit 1
fi

mkdir -p "$OUTDIR"
arff-select "$GT" dns_name fc_dst_port fc_proto | tail -n +2 | grep -v ?dns_name \
	| sed -re 's;(.*)\t(.*)\t(.*)\t(.*);\1\t\2:\3/\4;g' > "$OUTDIR/data.txt"
wc -l "$OUTDIR/data.txt"
