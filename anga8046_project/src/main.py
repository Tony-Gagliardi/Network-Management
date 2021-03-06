'''
File: main.py
Created by Anthony Gagliardi - TLEN 5410
Creation Date: 17 April 2014
Modified: 29 April 2014
The purpose of this project is to monitor ARP
traffic over an internal network and identify possible
malicious activity so that network adminstrators
can be notified.

Note: To simulate ARP poisoning, I will be using a scapy
function called 'arpcachepoison' that I found from:
oss.netboxblue.com/pug/scapy.html
'''
from scapy.all import *
import smtplib
import datetime

# This is the dictonary that will be used for
# determining initial network toplogy information
pairings = {}

def send_email(mac, ip):
	'''
	The send_email function is used for sending emails to the
	network adminstrator when malicious activity is detected 
	on the network.
	Note: For help with the smtp library and formatting I referenced an example
	at this address:
	# http://stackoverflow.com/questions/64505/sending-mail-from-python-using-smtp
	
	Parameters:
		mac(string) - Mac address of malicious user
		ip(string) - Ip of user who's traffic is now being redirected
	'''

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.set_debuglevel(0)
	server.starttls()
	server.login('netman2014tr@gmail.com', 'netman2014')

	date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )

	
	subject = "[Urgent] Malicious Activity Detected"
	message_text = ('Malicious ARP traffic has been detected!\n' +
						'Malicious users MAC: '+ mac + '\n' 
							'Victims IP: '+ ip)	
	msg = ("From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" 
            % ( 'netman2014tr@gmail.com', 'netman2014tr@gmail.com', 
        		subject, date, message_text ))	

	server.sendmail('netman2014tr@gmail.com', 'netman2014tr@gmail.com', msg)
	server.quit()

def parse_packet(pkt, pairings):
	'''
	The parse_packet function analyzes packet data to see if there is 
	malicious activity on the network. If the packet is not yet in the
	dictionary and it is on the internal subnet of '10.x.x.x', then we add
	the IP/MAC pair to the dictionary so we can look out for changes in the
	future. In a way, this script is a lot like SSH in that, you better
	hope the inital information you receive is right and not an attack.

	Parameters:
		pkt(Packet) - The ARP packet for examination
		pairings(Dictionary) - Known MAC/IP pairs on the network
	'''
	flag = pairings.get(pkt.psrc)
	if flag == None and pkt.psrc.startswith('10.') == True:
		pairings[pkt.psrc] = pkt.hwsrc
		print "Adding IP/MAC pair to table"
	elif flag == None and pkt.psrc.startswith('10.') == False:
		print "Ignoring packet: out of network range..."
	else: 
		if pairings[pkt.psrc] == pkt.hwsrc:
			print 'No malicious behavior'
		else:
			print'!!!Malicious activity detected!!!...emailing administrator'
			send_email(pkt.hwsrc, pkt.psrc)

def static_monitor(pkt):
	'''
	The static_monitor function is used to parse ARP traffic
	on the network and give the neccesary details to the parse_packet
	function
	NOTE: I used the tutorial and similar code to the examples found
	at: 
	http://www.scmdt.mmu.ac.uk/blossom/downloads/byDoing/PythonScriptingwithScapyLab.pdf

	Parameters:
		pkt(Packet) - The ARP packet for examination
	'''
	if ARP in pkt and pkt[ARP].op in (1,2): #who-has or is-at
		parings = parse_packet(pkt, pairings) 
		return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%") 

def main():
	'''
	The main function takes user input to determine what type of network
	is being used. Currently, dynamic is unimplemented. For the static
	network, I sniff out only ARP packets on the network, and then run
	the static_monitor function on them. That is the purpose of 'prn' in
	the sniff function.
	'''
	network = raw_input("Please enter static or dynamic for network type: ")
	if network == 'dynamic':
		pass

 	if network == 'static':
		sniff(prn=static_monitor, filter="arp", store=0)


if __name__ == '__main__':
	main()