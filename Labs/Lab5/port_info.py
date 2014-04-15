''' Code provided by Mark Dehus in the Lab 5 writeup 
	This program finds the info from IANA about a particular port.
'''


import socket
mydstport = raw_input("Please enter port number: ")
port = int(mydstport)
print port

try:
	myservice = socket.getservbyport(port, "tcp")
	print "That service is: ", myservice
except:
	print port, "is not tracked by IANA"