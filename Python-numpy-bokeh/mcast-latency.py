
#!usr/bin/env python
#
# Send/receive UDP multicast packets.
# Requires that your OS kernel supports IP multicast.
#
# Usage:
#   mcast -s (sender, IPv4)
#   mcast -s -6 (sender, IPv6)
#   mcast    (receivers, IPv4)
#   mcast  -6  (receivers, IPv6)
#   mcast -i <ip address> -p <port address>
#   mcast -h for help

PORT = port_number
MYGROUP_4 = 'multicast_group_ip'
MYGROUP_6 = 'ff15:7079:7468:6f6e:6465:6d6f:6d63:6173'
MYTTL = 64
MYINTERFACE = '0.0.0.0'

import os
import time
import struct
import socket
import sys
import getopt
import csv
import datetime

def main(argv):
        try:
           opts, args = getopt.getopt(argv,"6i:p:e:h:R")
        except getopt.GetoptError:
          print 'mcast-latency.py -i <ip adddress> -p <port> -e <ip address of interface to join>'
          sys.exit(2)
        for opt, arg in opts:
          if opt == '-h': 
              print 'mcast-latency.py -i <ip address> -p <port address> -e <ip address of interface to join> -h'
              sys.exit()
          elif opt in ("-e"):
                MYINTERFACE = arg
          elif opt in ("-i"):
               MYGROUP_4 = arg
               group = MYGROUP_4
               if opt in ("-6"):
                  MYGROUP_6 = arg
                  group = MYGROUP_6
          elif opt in ("-p"):
                MYPORT = arg
        try:
          group
        except NameError:
                  print 'mcast-latency.py -i <ip address> -p <port address> -e <ip address of interface to join> -h'
                  sys.exit()

        receiver(group,MYPORT,MYINTERFACE)

def receiver(group,MYPORT,MYINTERFACE):
    # Look up multicast group address in name server and find out IP version
    addrinfo = socket.getaddrinfo(group, None)[0]

    # Create a socket
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Allow multiple copies of this program on one machine
    # (not strictly needed)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind it to the port
    s.bind(('', int(MYPORT)))

    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    # Join group
    if addrinfo[0] == socket.AF_INET: # IPv4
                if MYINTERFACE is not None:
                         mreq = group_bin + socket.inet_aton(MYINTERFACE)
                         s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
                         imr = socket.inet_pton(socket.AF_INET, group) + socket.inet_aton(MYINTERFACE) + socket.inet_pton(socket.AF_INET, '1.1.1.1')
                         #s.setsockopt(socket.SOL_IP, socket.IP_ADD_SOURCE_MEMBERSHIP, imr)
                else:
                        mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
                        s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    else:
        mreq = group_bin + struct.pack('@I', 0)
        s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

    #Creat csv file
    timestr = time.strftime("%Y%m%d-%H:%M:%S")
    output_CSV = 'output_'+timestr+'.'+'csv'
    header = ["LogTime", "column1","column2","column3"]
    with open(output_CSV, mode='w') as csvfileheader:
	writer = csv.writer(csvfileheader)
	writer.writerow(header)
    print 	'\n', \
		'\n', \
	  "     CSV File", output_CSV,"has been created!" , '\n', \
	  "     By Default the republished messages is not included ", '\n',\

    # Loop, printing any data we receive
    while True:
	data = s.recvfrom(1500)
	#print data
	if not data:
	    print 'No data recieved by the socket , check IT'
	    break
	#incdata = repr(data) or
	incdata = data[0]
	# example of patter1
    # Usually the first bytes contains the network layer let's say it is 8 bytes and it depends on the network.
    patter1 = struct.unpack_from('=H', incdata[10:18])[0]
        tmicro = datetime.datetime.utcnow()
        #tmicro = datetime.datetime.utcnow().time()
	if (sys.argv[-1] != 'Flag1') and (patter1 == value1):
	    #Create condition for only Republished=False
	    column1=struct.unpack_from('=I',incdata[16:24])[0]
		column2=struct.unpack_from('=Q',incdata[24:32])[0]
		column3=struct.unpack_from('=Q',incdata[32:40])[0]

		with open(output_CSV, mode='a') as csvfile:
		    data = [tmicro,column1,column2,column3]
		    csv.writer(csvfile).writerow(data)
	  	    
	elif (sys.argv[-1] == 'Flag1') and (pattern1 == value2):
	    column1=struct.unpack_from('=I',incdata[16:24])[0]
		column2=struct.unpack_from('=Q',incdata[24:32])[0]
		column3=struct.unpack_from('=Q',incdata[32:40])[0]

	    with open(output_CSV, mode='a') as csvfile:
	       data = data = [tmicro,column1,column2,column3]
	       csv.writer(csvfile).writerow(data)

if __name__ == '__main__':
    main(sys.argv[1:])

