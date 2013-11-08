################################################
##### GENERAL
################################################
global P; P = lambda:0

P.gtcol = "2lpi_proto"

#P.skip = ["Unknown", "TCP_Empty", "SNMP", "Radius", "Syslog"]
P.select = [
	"BitTorrent",
	"DNS",
	"eMule",
	"Jabber",
	"Kademlia",
	"Kaspersky",
	"Mail",
	"NTP",
	"Skype",
	"SSH",
	"Steam",
	"STUN",
	"WWW",
]

################################################
##### MODULES
################################################

from mod_dnsclass import *
from mod_portsize import *
from mod_dstip import *
from mod_npkts import *
from mod_dpi import *
from mod_port import *

# init modules
dstip = mod_dstip("./dstip/data/model")
dnsclass = mod_dnsclass("./dnsclass/data/model")
portsize = mod_portsize("./portsize/data/model")
npkts = mod_npkts("./npkts/data/model")
dpi = mod_dpi("./dpi/data/model")
port = mod_port("./port/data/model")

# register
Cascade.register(dstip)
Cascade.register(dnsclass)
Cascade.register(portsize)
Cascade.register(npkts)
Cascade.register(dpi)
Cascade.register(port)
