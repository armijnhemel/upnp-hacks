from httplib import HTTPConnection

httpc = HTTPConnection('10.0.0.138')
#httpc = HTTPConnection('192.168.1.1:5431')

headers = {"HOST": "10.0.0.138",
   "CALLBACK": "<http://10.0.0.163:22/notify>",
   "TIMEOUT": "Second-1800",
   "NT": "upnp:event"
   }

httpc.request("SUBSCRIBE", "/upnp/event/wanpppcpppoa", headers=headers)
#httpc.request("SUBSCRIBE", "/uuid:0014-bf09-551c020099dc/WANPPPConnection:1", headers=headers)

r1 = httpc.getresponse()

print(r1.status, r1.reason)
