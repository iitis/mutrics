#!/bin/bash
# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

up="pks_1_up pks_2_up pks_3_up pks_4_up pks_5_up"
down="pks_1_down pks_2_down pks_3_down pks_4_down pks_5_down"

#arff-select fc_id fc_proto fc_dst_port $up $down gt
arff-select fc_id fc_proto fc_dst_port $up $down lpi_proto
