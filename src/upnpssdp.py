#! /usr/bin/python

## Sample code used for my SANE 2006 paper "UPnP: dead simple or simply deadly?"
## The script has been reworked to be a bit more modern.
## Copyright 2005 - 2018 Armijn Hemel
##
## Licensed under the MIT license
## SPDX-License-Identifier: MIT

import sys, errno, mimetools, struct, datetime, argparse
import socket
import threading
from StringIO import StringIO
from urlparse import urlsplit

##
## Portmapping: WANIPConnection UPnP device
##

host = "239.255.255.250"
#host = "10.0.0.162"
#host = "192.168.1.1"

##
## Some Axis Internet camera
##
#host = "216.231.170.182"

## class to send a single SSDP discovery message
class SSDPDiscovery:
	def __init__(self, verbose):
		self.sock=None
		self.verbose = verbose
	def discover(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.connect((host, 1900))
		self.msg = ""
		self.msg = self.msg + "M-SEARCH * HTTP/1.1\r\n"
		self.msg = self.msg + "HOST: 239.255.255.250:1900\r\n"
		self.msg = self.msg + "MAN: ssdp:discover\r\n"
		self.msg = self.msg + "MX: 10\r\n"
		self.msg = self.msg + "ST: ssdp:all\r\n"
		self.msg = self.msg + "\r\n"
		self.msg = self.msg + "\r\n"
		if self.verbose:
			print "Sending message: ", self.msg
			sys.stdout.flush()
		self.sock.send(self.msg)

## class to start a server that continuously listens for SSDP packets
class SSDPServer(threading.Thread):
	def __init__(self, logfilepath):
		self.logfile = logfilepath
		threading.Thread.__init__(self)
	def run(self):
		## create two sockets, add them to the broadcast group and
		## make sure that the address can be reused (Linux only, for BSD
		## you should use other options).
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1 )
		self.sock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock2.setsockopt( socket.SOL_SOCKET, socket.SO_BROADCAST, 1 )

		logfile = open(self.logfile, 'w+')
		logfile.write("logfile open\n")
		logfile.flush()

		self.sock.bind(('', 1900))
		self.sock2.bind(('', 1900))
		self.sock.connect((host, 1900))
		print "Sending discovery message on: %s, port %s " % self.sock.getpeername()
		print "Listening on: %s, port %s\n" % self.sock.getsockname()
		self.msg = ""
		self.msg = self.msg + "M-SEARCH * HTTP/1.1\r\n"
		self.msg = self.msg + "HOST: 239.255.255.250:1900\r\n"
		self.msg = self.msg + "MAN: ssdp:discover\r\n"
		self.msg = self.msg + "MX: 10\r\n"
		self.msg = self.msg + "ST: ssdp:all\r\n"
		self.msg = self.msg + "\r\n"
		self.msg = self.msg + "\r\n"
		logfile.write("sending msg\n")
		logfile.write(self.msg)
		self.sock.send(self.msg)
		logfile.write("message sent\n")
		logfile.flush()

		print "Listening...\n"
		sys.stdout.flush()

		mreq = struct.pack("4sl", socket.inet_aton("239.255.255.250"), socket.INADDR_ANY)
   		self.sock2.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
		while (1):
			print "Waiting for SSDP data at", datetime.datetime.utcnow().isoformat()
			sys.stdout.flush()
			(data, client) = self.sock2.recvfrom(1024)
			logfile.write(data)
			tempres = self.parsedata(data, client[0])
			self.filter_hosts(tempres)
			logfile.write(client[0])
			logfile.write("\n")
			logfile.flush()
			print
			sys.stdout.flush()

	def parsedata(self, data, client):
		headers = {}
		headers['HOSTIP'] = client
		counterheaders=0
                headerdata = StringIO(data)
		for i in headerdata:
			# skip the first element, it's the HTTP return code
			if counterheaders == 0:
				counterheaders+=1
				continue
			tempres = i.strip().split(':',1)

			# evil hack for \r\n at the end of the data
			if len(tempres[0]) == 0:
				counterheaders+=1
				continue
			headers[tempres[0].upper()] = tempres[1].strip()
			counterheaders+=1
		return headers

	## only show the interesting end points
	def filter_hosts(self, data):
		try:
			for profilename in ["WANIPConnection", "WANPPPConnection", "WANPOTSConnection"]:
				if profilename in data["ST"]:
					print "URL found", data["LOCATION"]
					sys.stdout.flush()
					break
		except KeyError:
			# there is no ST header, just an NT header
			for profilename in ["WANIPConnection", "WANPPPConnection", "WANPOTSConnection"]:
				if profilename in data["NT"]:
					print "URL found", data["LOCATION"]
					sys.stdout.flush()
					break

def main(argv):
	parser = argparse.ArgumentParser()

	## the following options are provided on the commandline
	parser.add_argument("-l", "--logfile", action="store", dest="logfile", help="path to logfile", metavar="LOGFILE")
	args = parser.parse_args()

	if args.logfile == None:
		parser.error("Logfile location missing")

	## first create a SSDPServer thread and start it, so it
	## listens on the right address + interface
	## TODO: more sanity checks for logfile location
	logfilepath = args.logfile
	ssdpserver = SSDPServer(logfilepath)
	ssdpserver.start()

if __name__ == "__main__":
        main(sys.argv)
