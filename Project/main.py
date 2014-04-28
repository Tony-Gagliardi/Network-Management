'''
File: main.py
Created by Anthony Gagliardi - TLEN 5410
Creation Date: 17 April 2014
Modified: 17 April 2014
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
	The send_email function is used for sending emails based on the 
	specified id, which is of type string. trap_data is the line of code
	in the trap data where our keywords were found, and interface is the
	return value of the get_interface function, and it provides the emails
	subject line with a specific interface.
	---NOTICE---
	For help with the smtp library and formatting we referenced an example
	at this address:
	# http://stackoverflow.com/questions/64505/sending-mail-from-python-using-smtp
	'''

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.set_debuglevel(0)
	server.starttls()
	server.login('netman2014tr@gmail.com', 'netman2014')

	date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )

	
	subject = "[Urgent] Malicious Activity Detected"
	message_text = ('Malicious ARP traffic has been detected at ' + mac + ' ' + ip)	
	msg = ("From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" 
            % ( 'netman2014tr@gmail.com', 'netman2014tr@gmail.com', 
        		subject, date, message_text ))	

	server.sendmail('netman2014tr@gmail.com', 'netman2014tr@gmail.com', msg)
	server.quit()

def parse_packet(pkt, pairings):
	flag = pairings.get(pkt.psrc)
	if flag == None and pkt.psrc.startswith('10.') == True:
		pairings[pkt.psrc] = pkt.hwsrc
		print "Adding IP/MAC pair to table"
	elif flag == None and pkt.psrc.startswith('10.') == False:
		print "Ignoring packet out of network range..."
	else: 
		if pairings[pkt.psrc] == pkt.hwsrc:
			print 'No malicious behaviour'
		else:
			print'Malicious activity detected...emailing administrator'
			send_email(pkt.hwsrc, pkt.psrc)

def static_monitor(pkt):
	'''
	NOTE: I used the tutorial and similar code to the examples found
	at: 
	http://www.scmdt.mmu.ac.uk/blossom/downloads/byDoing/PythonScriptingwithScapyLab.pdf
	'''
	if ARP in pkt and pkt[ARP].op in (1,2): #who-has or is-at
		parings = parse_packet(pkt, pairings) 
		return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%") 

def main():
	network = raw_input("Please enter static or dynamic for network type: ")
	if network == 'dynamic':
		pass

 	if network == 'static':
		sniff(prn=static_monitor, filter="arp", store=0)


if __name__ == '__main__':
	main()