import socket
myip = raw_input("Please enter IP: ")

try:
	myname = socket.gethostbyaddr(myip)
	print "My DNS name is: ", myname[0]
except socket.herror, ex:
	print myip, "doesn't have a reverse record."
