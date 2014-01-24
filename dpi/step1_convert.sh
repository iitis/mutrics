#!/bin/bash

BYTES=16

fup=""
fdown=""
for i in `seq 1 $BYTES`; do fup="$fup pl_${i}_up"; done
for i in `seq 1 $BYTES`; do fdown="$fdown pl_${i}_down"; done

arff-select fc_id fc_proto fc_dst_port $fup $fdown gt
