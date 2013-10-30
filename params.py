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
	"Gnutella",
	"HalfLife",
	"Jabber",
	"Kademlia",
	"Kaspersky",
	"Mail",
	"NTP",
	"RTMP",
	"Skype",
	"SQL",
	"SSDP",
	"SSH",
	"Steam",
	"STUN",
	"Teredo",
	"Teamviewer",
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
from mod_dpi import *

# init modules
dnsclass = mod_dnsclass("./dnsclass/data/model")
portsize = mod_portsize("./portsize/data/model")
dstip = mod_dstip("./dstip/data/model")
dpi = mod_dpi("./dpi/data/model")
npkts = mod_npkts("./npkts/data/model2_tcp", "./npkts/data/model2_udp")

# register
Cascade.register(dstip)
Cascade.register(dnsclass)
Cascade.register(portsize)
Cascade.register(dpi)
Cascade.register(npkts)
