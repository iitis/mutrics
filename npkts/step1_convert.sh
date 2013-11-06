#!/bin/bash

up="pks_1_up pks_2_up pks_3_up pks_4_up pks_5_up"
down="pks_1_down pks_2_down pks_3_down pks_4_down pks_5_down"

arff-select fc_id fc_proto fc_dst_port $up $down 2lpi_proto
