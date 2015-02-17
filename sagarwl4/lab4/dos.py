import socket

# addressing information of target
IPADDR = '192.168.101.74'
PORTNUM = 31337
 
# enter the data content of the UDP packet as hex
PACKETDATA = 'sagarwl4'
 
# initialize a socket, think of it as a cable
# SOCK_DGRAM specifies that this is UDP
 
# connect the socket, think of it as connecting the cable to the address location
#s.connect((IPADDR, PORTNUM))
 
# send the command
for i in range(1100):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
	s.connect((IPADDR, PORTNUM))
	s.send(PACKETDATA)
	s.recv(1024)
	s.close()
