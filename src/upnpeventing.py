#!/usr/bin/env python3

## example script to send SOAP requests to a UPnP endpoint
## Copyright 2018-2023 Armijn Hemel
## Licensed under the MIT license
## SPDX-License-Identifier: MIT

import httplib
import os
import time
import xml.dom.minidom

eventsuburl = "/upnp/event/WANIPConnection"
hostip = "192.168.1.1"
hostport = 52869
headers = {"HOST": "", "CALLBACK": "", "NT": "upnp:event", "TIMEOUT": "Second-infinite"}

#for i in range(0,30000):
for i in range(0,100):
    # Host and optional port number
    conn = httplib.HTTPConnection("%s:%d" % ( hostip, hostport))

    # Assign dynamic headers with proper values
    headers["HOST"] = "%s:%d" % (hostip, hostport)

    #headers["CALLBACK"] = "<192.168.1.2/test>"
    headers["CALLBACK"] = "<BLA>"

    conn.putrequest("SUBSCRIBE", eventsuburl, skip_host=True, skip_accept_encoding=True)

    # Put all headers in order to the specifications
    conn.putheader("HOST", headers["HOST"])
    conn.putheader("CALLBACK", headers["CALLBACK"])
    conn.putheader("NT", headers["NT"])
    conn.putheader("TIMEOUT", headers["TIMEOUT"])
    conn.endheaders()

    # wait for a response and print it to the commandline
    response = conn.getresponse()
    print(i, response.status, response.reason, response.getheaders())
    #time.sleep(0.1)
