from npkts import HTClass
from ClassTree import *

model = "./npkts/model"
n = 1

htc = HTClass.HTClass()
htc.load(open(model, "rb"))

def check(f):
	f = f.data
	if f["pks_1_up"] == "0" or f["pks_1_down"] == "0":
		return False
	else:
		return True

def classify(f):
	f = f.data
	pp = "%s/%s" % (f["fc_proto"], f["fc_dst_port"])

	up   = [str(f["pks_%d_up"%i])   for i in range(1,n+1)]
	down = [str(f["pks_%d_down"%i]) for i in range(1,n+1)]

	return htc.one([pp] + up + down)

ClassTree.register("npkts", check, classify)
