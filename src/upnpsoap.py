#!/usr/bin/python

# example script to send SOAP requests to a UPnP endpoint
# Copyright 2005 - 2018 Armijn Hemel
# Licensed under the MIT license
# SPDX-License-Identifier: MIT

import os
import time
import xml.dom.minidom
from SOAPpy import *

# There are many different end points. Here are a few ones that
# were observd in the wild.
# Some of the documentation was added in 2017 and details
# have been lost in the mists of time.

# Unknown stack
# ZyXel
# endpoint = "http://192.168.1.1/UD/?3"

# Speedtouch
#endpoint = "http://10.0.0.138/upnp/control/wanpppcpppoa"

# Broadcom stack, part of the end point address generated
# Linksys WRT54G
# Linksys WRT54GS
# Some ASUS devices
#endpoint = "http://192.168.1.1:5431/uuid:0014-bf09-551c0200b2dc/WANIPConnection:1"
#endpoint = "http://192.168.1.1:5431/uuid:0014-bf09-551c020099dc/WANIPConnection:1"

# Unknown stack
# Linksys BEFW
#endpoint = "http://192.168.1.1:2468/WANIPConnection"

# Unknown stack
# Netgear
#endpoint = "http://192.168.1.1/Public_UPNP_C3"

# Linux IGD
# Netgear
#endpoint = "http://192.168.1.1:49152/upnp/control/WANIPConn1"

# AVM
#endpoint = "http://192.168.178.1:49000/upnp/control/WANIPConn1"

# COMPAL
endpoint = 'http://192.168.0.1:5000/ctl/IPConn'

# the different profiles
# profilename = 'WANPPPConnection
profilename = 'WANIPConnection'

# the SOAP name space (for SOAPpy)
namespace = "urn:schemas-upnp-org:service:%s:1" % profilename

# the different actions
getexternalipaddress = "urn:schemas-upnp-org:service:%s:1#GetExternalIPAddress" % profilename
addportmapping = "urn:schemas-upnp-org:service:%s:1#AddPortMapping" % profilename
deleteportmapping = "urn:schemas-upnp-org:service:%s:1#DeletePortMapping" % profilename
getgenericportmappingentry = "urn:schemas-upnp-org:service:%s:1#GetGenericPortMappingEntry" % profilename
getnatrsipstatus = "urn:schemas-upnp-org:service:%s:1#GetNATRSIPStatus" % profilename
getportmappingnumberofentries = "urn:schemas-upnp-org:service:%s:1#GetPortMappingNumberOfEntries" % profilename

# noroot needed for ZyXEL
#server = SOAPProxy(endpoint, namespace, noroot=1)
server = SOAPProxy(endpoint, namespace)

server.Config.debug = 1

# own IP address, hardcoded for now
ownip = '192.168.0.10'

# first get the external IP address
try:
    print "external IP", server._sa(getexternalipaddress).GetExternalIPAddress()
except:
    print "endpoint not valid or UPnP not enabled"
    sys.exit(1)

# print all existing portmappings
i = 0
bound = 0
while(i < bound):
    response = ""
    try:
        response = server._sa(getgenericportmappingentry).GetGenericPortMappingEntry(NewPortMappingIndex=i)
    except:
        i = i+1
        break
    print "portmapping %d: " % i, response
    i = i+1

# add a port mapping, then delete it

print "add portmapping"
response = server._sa(addportmapping).AddPortMapping(NewRemoteHost="", NewExternalPort=8022, NewProtocol="TCP", NewInternalPort=22, NewInternalClient=ownip, NewEnabled=1, NewPortMappingDescription="evil h4x0rz", NewLeaseDuration=0)
print response
print "delete portmapping"

try:
    server._sa(deleteportmapping).DeletePortMapping(NewRemoteHost="", NewExternalPort=22, NewProtocol="TCP")
except:
    pass


# some more things for different profiles

#server2 = SOAPProxy("http://10.0.0.138/upnp/control/lanhcm", "urn:schemas-upnp-org:service:LANDevice:1")
#getdnsservers = "urn:schemas-upnp-org:service:LANDevice:1#GetDNSServers"
#getdomainname = "urn:schemas-upnp-org:service:LANDevice:1#GetDomainName"
#setdomainname = "urn:schemas-upnp-org:service:LANDevice:1#SetDomainName"
#getsubnetmask = "urn:schemas-upnp-org:service:LANDevice:1#GetSubnetMask"
#setsubnetmask = "urn:schemas-upnp-org:service:LANDevice:1#SetSubnetMask"
#getiprouterslist = "urn:schemas-upnp-org:service:LANDevice:1#GetIPRoutersList"
#setiprouter = "urn:schemas-upnp-org:service:LANDevice:1#SetIPRouter"

#print "DNS:", server2._sa(getdnsservers).GetDNSServers()
#print "domainname:", server2._sa(getdomainname).GetDomainName()
#print server2._sa(setdomainname).SetDomainName(NewDomainName="blaat")
#print server2._sa(getdomainname).GetDomainName()
#print server2._sa(getsubnetmask).GetSubnetMask()
#print server2._sa(setsubnetmask).SetSubnetMask(NewSubnetMask="255.0.0.0")
#print server2._sa(getiprouterslist).GetIPRoutersList()
#print server2._sa(setiprouter).SetIPRouter(NewIPRouters="10.0.0.138")

print "NAT enabled:", server._sa(getnatrsipstatus).GetNATRSIPStatus()[1]
