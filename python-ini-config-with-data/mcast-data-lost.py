#!usr/bin/env python2
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
#   mcast -h for hepublisherResource

PORT = port_number
MYGROUP_4 = 'multicast_group_ip'
MYGROUP_6 = 'ff15:7079:7468:6f6e:6465:6d6f:6d63:6173'
MYTTL = 255
MYINTERFACE = '0.0.0.0'

import struct
import socket
import sys
import getopt
import datetime
from configparser import SafeConfigParser


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "6i:p:e:h:R")
    except getopt.GetoptError:
        print(
            'mcast-latency.py -i <ip adddress> -p <port> -e <ip address of interface to join> -h <Include Republished Messages> -R')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(
                'mcast-latency.py -i <ip address> -p <port address> -e <ip address of interface to join> -h <Include Republished Messages > -R')
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
        print(
            'mcast-latency.py -i <ip address> -p <port address> -e <ip address of interface to join> -hi <Include Republished Messages > -R')
        sys.exit()
    print(group, MYPORT, MYINTERFACE)

    receiver(group, MYPORT, MYINTERFACE)


def receiver(group, MYPORT, MYINTERFACE):
    # Look up multicast group address in name server and find out IP version
    global socketerror
    addrinfo = socket.getaddrinfo(group, None)[0]

    # Create a socket
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # setting timeout for the soket if it did not esablish
    # s.settimeout(10)

    # Allow multiple copies of this program on one machine
    # (not strictly needed)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind it to the port
    s.bind(('', int(MYPORT)))

    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    # Join group
    if addrinfo[0] == socket.AF_INET:  # IPv4
        if MYINTERFACE is not None:
            mreq = group_bin + socket.inet_aton(MYINTERFACE)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            imr = socket.inet_pton(socket.AF_INET, group) + socket.inet_aton(MYINTERFACE) + socket.inet_pton(
                socket.AF_INET, '1.1.1.1')
            # s.setsockopt(socket.SOL_IP, socket.IP_ADD_SOURCE_MEMBERSHIP, imr)
        else:
            mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    else:
        mreq = group_bin + struct.pack('@I', 0)
        s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

    # Touching file name Republished.log
    def truncate(logfile):
        with open(logfile, mode='w') as filelog:
            pass

    # Parsing the ini file config for Multicast IP's
    def parser_ini(ip, port):
        parser = SafeConfigParser()
        parser.read('MultiCast-IPs.ini')
        for section_name in parser.sections():
            for name, value in parser.items(section_name):
                if str(ip + ':' + port) == str(value):
                    publisherResource_Name = str(name).replace(',', "")
                    Host = str(section_name).replace(',', "")
                    #print(publisherResource_Name, Host)
                    return publisherResource_Name, Host

    def get_logfile(type, feed, server):
        if type == 'Repub':
            logfile = ('Republished_' + feed + '_' + server + '.log').replace(" ","")
            return logfile
        elif type == 'MC':
            repub_Log = ('Multicast-data-lost_' + feed + '_' + server + '.txt').replace(" ","")
            return repub_Log

    def issue_time():
        timestr = str(datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S.%f"))
        return timestr

    # EpublisherResourceased time check (stopwatch)
    Minutes = datetime.datetime.now() + datetime.timedelta(minutes=3)

    get_info = parser_ini(group, MYPORT)
    publisherResource = str(get_info[0])
    Host = str(get_info[1])
    #print(publisherResource, type(publisherResource), '\n', Host, type(Host))
    Logfile = get_logfile('Repub', publisherResource, Host)
    Repub_Log = get_logfile('MC', publisherResource, Host)
    

    if 'word1' in publisherResource:
        while True:
            try:
                # we should set the timeout before starting receiving the data or it will not work !
                s.settimeout(20)
                data = s.recvfrom(1500)
                # print(data)
                incdata = data[0]
                #print(incdata)
                #example of pattern1 with the bytes sequence in the binary data
                # Usually the first bytes contains the network layer let's say it is 8 bytes and it depends on the network.
                pattern1 = struct.unpack_from('=H', incdata[10:15])[0]

                if data:
                    if (pattern1 == word1-value1):
                        with open(Repub_Log, 'w+') as f:
                            body = "publisherResource Disconnected Alert ! ", \
                                   "The socket is disconnected for the following : ", '\n', "publisherResource Name :", str(publisherResource), \
                                   '\n', "Host : ", str(Host), '\n', \
                                   "Happened at UTC Time :", issue_time()
                            #print(body)
                            f.writelines(str(line) for line in body)
                            continue

                else:
                    with open(Repub_Log, 'w+') as f:
                        body = "Data Lost Alert ! ", \
                               "MultiCast Data Failure Or the socket is disconnected somehow the last 20 seconds : ", '\n', "publisherResource Name :", str(publisherResource), \
                               '\n', "Host : ", str(Host), '\n', \
                               "Happened approximately at of UTC Time :", issue_time()
                        print(body)
                        f.writelines(str(line) for line in body)
                        continue

            except (socket.error, socket.timeout) as socketerror:
                with open(Repub_Log, 'w+') as f:
                    body = "Socket Error Type : ", socketerror, '\n', \
                           "MultiCast Data Failure for the last 20 seconds : ", '\n', "publisherResource Name :", str(publisherResource), \
                           '\n', "Host : ", str(Host), '\n', \
                           "Happened approximately at UTC Time :", issue_time(), '\n', \
                           "Reasons: ",'\n', \
                              "1) Network has issues and we could not monitor the traffic from support2 server ",'\n', \
                              "       Please check from the support mcast scipt from other server ",'\n', \
                              "2) Real issue is happening"

                    print(body)
                    f.writelines(str(line) for line in body)

# Can add another word or more patterns and continue with the elif condition:
        #e.g : elif 'word2' in publisherResource:

if __name__ == '__main__':
    main(sys.argv[1:])
