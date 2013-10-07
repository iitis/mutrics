################################################
##### GENERAL
################################################
global P; P = lambda:0

P.skip = ["Unknown", "TCP_Empty", "SNMP", "Radius", "Syslog"]

################################################
##### MODULES
################################################

from mod_dummy import *
from mod_dnsclass import *
from mod_npkts import *

########## 0. temporary
# emits "SKIP" for empty flows and unknowns
mod = mod_dummy()
Cascade.register(mod)

########## 1. DNS-Class
# Requires flow name
mod = mod_dnsclass("./dnsclass/asnet1/model")
Cascade.register(mod)

########## 2. npkts
# Requires pkt size from both sides >0
mod = mod_npkts("./npkts/model2", 1)
Cascade.register(mod)
