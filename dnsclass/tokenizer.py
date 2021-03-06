#!/usr/bin/env python
# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

import re

### <yuck!>
import sys
from os import path
sys.path.insert(0, path.dirname(__file__))
### </yuck!>

import tldextract
import params as P

def do_segment(word):
	if len(word) > 0:
		return [word]
	else:
		return []

	###########
	# (from segment import segment)
	ret = []
	if P.tok.seg > 0 and len(word) > P.tok.seg:
		for token in segment(word):
			if len(token) > 1: ret.append(token)
	elif len(word) > 0:
		ret.append(word)
	return ret
	###########


def get_flow_features(domain):
	ret = []
	text = domain.strip()

	i = text.rfind(':')
	if i > 0:
		s = text[i:]
		j = s.find('/')
	
		if j > 0:
			ret.append(s[:j]) # port
			ret.append(s[j:]) # proto
		else:
			ret.append(s[:j]) # port
	
	return ret

def tokenizer(domain):
	ret = []
	text = domain.lower().strip()

	# parse the domain
	r = tldextract.extract(text)

	# subdomain: only letters
	if len(r.subdomain):
		# change digits to 'N'
		sd = re.sub('[0-9]', 'N', r.subdomain)
		sd = re.sub('(N+)', '\\1.', sd)

		for word in re.split("[^a-zN]+", sd):
			if len(word) == 0:
				continue
			elif word.isdigit():
				ret.append("N" * len(word))
			else:
				ret.extend(do_segment(word))

	# domain: no dashes
	for word in r.domain.split("-"):
		ret.extend(do_segment(word))

	# TLD: no dots
	if P.tok.tlds:
		for token in r.tld.split("."):
			if len(token) > 0: ret.append(token)

	# flow features
	if P.tok.flow:
		ret.extend(get_flow_features(domain))

	if P.tok.max > 0:
		ret = ret[-P.tok.max:]

	#print "%s -> %s" % (domain.strip(), ret)
	return ret

