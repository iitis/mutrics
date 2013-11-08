################################################
##### GENERAL
################################################
global P; P = lambda:0

P.gtcol = "2lpi_proto"

#P.skip = ["Unknown", "TCP_Empty", "SNMP", "Radius", "Syslog"]
P.select = [
	"Ares",
	"BitTorrent",
	"DNS",
	"eMule",
	"Jabber",
	"Kademlia",
	"Kaspersky",
	"Mail",
	"NTP",
	"Skype",
	"SQL",
	"SSDP",
	"SSH",
	"Steam",
	"STUN",
	"Teredo",
	"WWW",
	"XboxLive",
]

################################################
##### MODULES
################################################

from mod_dnsclass import *
from mod_portsize import *
from mod_dstip import *
from mod_npkts import *

# init modules
dstip = mod_dstip("./dstip/data/model")
dnsclass = mod_dnsclass("./dnsclass/data/model")
portsize = mod_portsize("./portsize/data/model")
npkts = mod_npkts("./npkts/data/model")

# register
Cascade.register(dstip)
Cascade.register(dnsclass)
Cascade.register(portsize)
Cascade.register(npkts)
