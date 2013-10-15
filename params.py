################################################
##### GENERAL
################################################
global P; P = lambda:0

#P.skip = ["Unknown", "TCP_Empty", "SNMP", "Radius", "Syslog"]
P.select = [
	"Ares",
	"BitTorrent",
	"eMule",
	"Gnutella",
	"HalfLife",
	"Jabber",
	"Kademlia",
	"Kaspersky",
	"Mail",
	"NTP",
	"RTMP",
	"SIP",
	"Skype",
	"SQL",
	"SSDP",
	"SSH",
	"Steam",
	"STUN",
	"Teamviewer",
	"Teredo",
	"WWW",
	"XboxLive",
]

################################################
##### MODULES
################################################

from mod_dnsclass import *
from mod_npkts import *
from mod_dstip import *

# init modules
dnsclass = mod_dnsclass("./dnsclass/model/model")
npkts = mod_npkts("./npkts/data/model")
dstip = mod_dstip("./dstip/data/model")

# register
Cascade.register(dstip)
Cascade.register(npkts)
Cascade.register(dnsclass)
