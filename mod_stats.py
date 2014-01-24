# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

from stats import DT

class mod_stats:
	def __init__(self, model, i=5):
		self.i = i
		self.cls = DT.DT()
		self.cls.load(open(model, "rb"))
		self.cls.algo.set_params(n_jobs=1)

		self.keys = [
			"bs_min_size_up",   "bs_avg_size_up",   "bs_max_size_up",   "bs_std_size_up",
			"bs_min_iat_up",    "bs_avg_iat_up",    "bs_max_iat_up",    "bs_std_iat_up",
			"bs_min_size_down", "bs_avg_size_down", "bs_max_size_down", "bs_std_size_down",
			"bs_min_iat_down",  "bs_avg_iat_down",  "bs_max_iat_down",  "bs_std_iat_down"
		]

	def check(self, f):
		return "pks_1_up" in f.data

	def classify(self, f):
		proto  = 1 if f["fc_proto"] == "TCP" else 2
		port   = int(f["fc_dst_port"])
		ss     = [int(f[k]) for k in self.keys]

		v = [proto, port] + ss
		return self.cls.one(v)
