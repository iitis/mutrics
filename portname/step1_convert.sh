#!/bin/bash
# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

GT="${1:-gt}"

arff-select fc_id fc_proto fc_dst_port dns_name $GT \
	| grep -v '?dns_name'
