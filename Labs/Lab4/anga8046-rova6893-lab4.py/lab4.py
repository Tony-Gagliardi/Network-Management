import netsnmp as snmp
import time
import lab1
import smtplib
import datetime


def send_email(id, trap_data, interface):
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

	if id == 'up' or id == 'down':
		subject = '[ Notifier ] Interface ' + interface[-1] + ' Status'

	if id == 'traffic_low':
		subject = "[ Notifier ] Traffic falling threshold reached"

	if id == 'traffic_high':
		subject = "[ Notifier ] Traffic rising threshold reached"

	message_text = trap_data	
	msg = ("From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" 
            % ( 'netman2014tr@gmail.com', 'netman2014tr@gmail.com', 
        		subject, date, message_text ))	

	server.sendmail('netman2014tr@gmail.com', 'netman2014tr@gmail.com', msg)
	server.quit()

def get_interface():
	'''
	The get_interface function takes no parameters and is invoked when
	a particular keyword is found in the trap data, all it does is 
	recursively examine the trap data for the specific interface 
	and returns it.
	'''
	running = True
	while running:
		next_line = raw_input()
		if 'ifDescr' in next_line:
			next_line = next_line.split(" ")
			return next_line
		else:
			continue
	return 'Unknown Interface'

def trap_check(trap_data):
	'''
	The trap_check function recursively examines
	each line of the entire trap message for a particular
	keyword or phrase and then invokes the send_email function
	based on the keywords that it found.
	'''
	IPList = ['198.51.100.1']
	
	if 'linkUp' in trap_data:
		interface = get_interface()
		send_email('up', trap_data, interface)

	if 'linkDown' in trap_data:
		interface = get_interface()
		send_email('down', trap_data, interface)

	if 'enterprises.9.9.43.2.0.1' in trap_data:
		lab1.fetch_config(IPList)

	if 'mib-2.16.0.1' in trap_data:
		send_email('traffic_high', trap_data, 0)

	if 'mib-2.16.0.2' in trap_data:
		send_email('traffic_low', trap_data, 0)

def main():
	'''
	The main function takes in an entire trap
	message one line at a time and sends it to the 
	trap_check function for evaluation.
	'''
	running = True
	output = open('/tmp/traps', 'a')
	while running:
		try:
			input = raw_input()
			trap_check(input)
			output.write(input + "\n")
		except EOFError:
			running = False
	output.close()

if __name__ == '__main__':
	main()

