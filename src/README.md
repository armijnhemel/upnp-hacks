# How to use

1. make sure your firewall is not blocking UDP port 1900
2. run the following program:

```
$ python upnpssdp.py -l /path/to/logfile
```

The script will send a SSDP discover request and listen to replies on UDP port
`1900`. If there are any responses it will process and filter them to see if
there are any of the interesting profiles from the Internet Gateway Device
(IGD) profile.

The raw responses (all UPnP data that is sent on the UPnP broadcast address)
will be logged in the logfile.
