# Author: Pawel Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2014 IITiS PAN <http://www.iitis.pl/>
# Licensed under GNU GPL v3

def pc(num, total):
	if num == 0: return '0%'
	if num == total: return '100%'

	s = "%.1f%%" % (100.0 * num / total)
	if s == '0.0%':
		return '<0.1%'
	elif s == '100.0%':
		return '99.9%'
	else:
		return s

def fc(num):
	return "{:,}".format(int(num))

def int2str(num):
	sbl = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	base = len(sbl)

	ret = ''
	num, rem = divmod(num, base)
	while num:
		ret = sbl[rem] + ret
		num, rem = divmod(num, base)

	return sbl[rem] + ret
