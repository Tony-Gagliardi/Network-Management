import netsnmp
import time

def monitor_interface(num_drops, interface, session, ifoutdiscards):
	time_struct = time.localtime()
	print 'At', time_struct.tm_hour, time_struct.tm_min, 'the'
	print 'current interface packet drop count is ', num_drops[interface - 1]
	while (True):
		i = 0
		time.sleep(60)



if __name__ == '__main__':
	def main():
		ip = raw_input('Please enter IP of SNMP Device: ')
		session = netsnmp.Session(DestHost = ip, 
									Community = 'public', Version = 1)
		ifindex = netsnmp.Varbind('.1.3.6.1.2.1.2.2.1.1')
		ifdescr = netsnmp.Varbind('.1.3.6.1.2.1.2.2.1.2')
		ifoutdiscards = netsnmp.Varbind('.1.3.6.1.2.1.2.2.1.19')
		ifnumber = netsnmp.Varbind('.1.3.6.1.2.1.2.1.0')

		ifnumber_result = int(session.get(netsnmp.VarList(ifnumber))[0])

		getters = netsnmp.VarList()
		getters.append(ifindex)
		getters.append(ifdescr)
		getters.append(ifoutdiscards)
		getters.append(ifnumber)

		packet_drops = []

		for i in range(0, ifnumber_result):
			session.getnext(getters)
			# print ifindex.tag, ifindex.iid, ifindex.val
			print ifdescr.tag[-1], ': ', ifdescr.val
			packet_drops.append(ifoutdiscards.val)
			print packet_drops
		if_request = int(raw_input('Please enter the interface to monitor: '))
		monitor_interface(packet_drops, if_request, session, ifoutdiscards)
		# print ifnumber_result
main()