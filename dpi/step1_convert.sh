#!/bin/bash
# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

BYTES=16

fup=""
fdown=""
for i in `seq 1 $BYTES`; do fup="$fup pl_${i}_up"; done
for i in `seq 1 $BYTES`; do fdown="$fdown pl_${i}_down"; done

arff-select fc_id fc_proto fc_dst_port $fup $fdown gt
