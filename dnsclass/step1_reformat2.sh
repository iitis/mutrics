#!/bin/bash
# Simpler reformat
#
# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

if [ $# -lt 1 ]; then
	echo "usage: $0 outdir < infile.arff" >&2
	exit 1
fi

OUTDIR="$1"
mkdir -p "$OUTDIR"

arff-select lpi_proto dns_name fc_dst_port fc_proto | tail -n +2 | grep -v ?dns_name \
	| sed -re 's;(.*)\t(.*)\t(.*)\t(.*);\1\t\2:\3/\4;g' > "$OUTDIR/data.txt"
wc -l "$OUTDIR/data.txt"
