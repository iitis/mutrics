#!/bin/bash
# Reformat ARFF to LibShortText format
# http://www.csie.ntu.edu.tw/~cjlin/libshorttext/doc/libshorttext.html#installation-and-data-format
#
# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3
#

DIR="`dirname $0`"

if [ $# -lt 2 ]; then
	echo "usage: $0 outdir protos.txt arff-file1..." >&2
	exit 1
fi

OUTDIR="$1"
PROTOS="$2"
shift 2
FILES="$@"

protos=`paste -sd '|' $PROTOS`
mkdir -p $OUTDIR

for file in $FILES; do
	name="`basename $file`"
	name="${name%.arff}"

	echo "$name..." >&2
	tail -n +105 $file \
		| egrep -v ',(\?dns_name|Unknown|TCP_Empty),' \
		| cut -d, -f 4,8,39,41 \
		| sed -r \
			-e "/,$protos$/!d" \
			-e 's;^(.*),(.*),(.*),(.*)$;\4\t\3:\2/\1;g'
done > $OUTDIR/data.txt

wc -l $OUTDIR/data.txt
