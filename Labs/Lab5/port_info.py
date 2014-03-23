import socket
mydstport = raw_input("Please enter port number: ")
port = int(mydstport)
print port

try:
	myservice = socket.getservbyport(port, "tcp")
	print "That service is: ", myservice
except:
	print port, "is not tracked by IANA"