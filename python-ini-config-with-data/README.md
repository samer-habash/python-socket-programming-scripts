General Python Socket programming :

- The script is intended to listen and monitor the published multicast UDP binary data .
- NOTE that the multicast ip's are already defind globally - please check 
1) The scripts are made to check daily binary traffic upon some patterns and words.

Global Multicast Addresses :

        IPv4 Multicast addresses use the reserved class D address range:
        224.0.0.0 through 239.255.255.255
        
        NOTE: The addresses range between 224.0.0.0 and 224.0.0.255 is reserved for use by routing and maintenance protocols inside a network.
        
        Multi-Cast demo script can be get from https://github.com/python/cpython/blob/master/Tools/demo/mcast.py
        Usage example  : ~ python /mcast-latency.py -i multicast-ip  -p port -e $(hostname -i) &
        -i  multicast IP
        -p multicast port
        -e IP of the server that you are running the script.


2) The script checks if the multicast has no data at all for about 20 seconds , and if yes then it sends email then stop .

* Important :
Exaplanation of each file in the script :

        1- The script opens a multicast UDP channels in order to listen to the data traffic (The sender UDP multicast must be streaming)
        2- The script uses the socket programing of python (socket is a C library)
        3- The script will also extract and translate patterns and words upon its sequence in the binary traffic , it uses the "little endian byte order format"
        4- mcast-data-lost.py file :  This is the main script that do all the check ups and math for monitoring the traffic as explained above.
        5- MultiCast-IPs.ini file : This is the ini.file that contains the information for each server/host and IP/Port that is relevant to.

