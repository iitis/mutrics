#!/bin/bash

DIR=`dirname $0`

[[ $# -lt 1 ]] && { echo "usage: $0 outdir [train-options]" >&2; exit 1; }

OUTDIR="$1"
shift
ARGS="$@"

echo "training on $OUTDIR/train.txt"
/usr/bin/python $DIR/libshorttext-tools/text-train.py \
	-P "$OUTDIR/converter" $ARGS \
	"$OUTDIR/train.svm" "$OUTDIR/model"

