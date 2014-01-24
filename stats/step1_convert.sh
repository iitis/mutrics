#!/bin/bash

up="bs_min_size_up bs_avg_size_up bs_max_size_up bs_std_size_up bs_min_iat_up bs_avg_iat_up bs_max_iat_up bs_std_iat_up"
down="bs_min_size_down bs_avg_size_down bs_max_size_down bs_std_size_down bs_min_iat_down bs_avg_iat_down bs_max_iat_down bs_std_iat_down"

arff-select fc_id fc_proto fc_dst_port $up $down gt
