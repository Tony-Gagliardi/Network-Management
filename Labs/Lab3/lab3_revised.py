import netsnmp
import time

class Router(object):
    def __init__(self, ip):
        self.session = netsnmp.Session(DestHost = ip,
                                    Community = 'public', Version = 1)

    def __str__(self):
        print ip

    def update(self,ip):
        ifindex = netsnmp.Varbind('.1.3.6.1.2.1.2.2.1.1')
        ifdescr = netsnmp.Varbind('.1.3.6.1.2.1.2.2.1.2')
        ifoutdiscards = netsnmp.Varbind('.1.3.6.1.2.1.2.2.1.19')
        ifnumber = netsnmp.Varbind('.1.3.6.1.2.1.2.1.0')

        ifnumber_result = int(self.session.get(netsnmp.VarList(ifnumber))[0])

        getters = netsnmp.VarList()
        getters.append(ifindex)
        getters.append(ifdescr)
        getters.append(ifoutdiscards)
        getters.append(ifnumber)

        packet_drops = []

        for i in range(0, ifnumber_result):
            self.session.getnext(getters)
            # print ifindex.tag, ifindex.iid, ifindex.val
            print ifdescr.tag[-1], ': ', ifdescr.val
            packet_drops.append(ifoutdiscards.val)
            # print packet_drops
        if_request = raw_input('Please enter the interface to monitor: ')
        if if_request == '7':
            count = packet_drops[int(if_request) - 2]
        else:
            count = packet_drops[int(if_request) - 1]
            time_struct = time.localtime()
            print 'At', time_struct.tm_hour, time_struct.tm_min
            print 'Current dropped packets is ', count
            result_list = []
            result_list.append(if_request)
            result_list.append(count)
            return result_list

    def calculate_difference(self, current_count, previous_count,
                                 i, total, original_count):
        local_time = time.localtime()
        if i == 0:
            drop_count = int(current_count) - int(original_count)
        else:
            drop_count = int(current_count) - int(previous_count)
        print drop_count, 'dropped packets'
        if drop_count <= 100:
            pass
        if drop_count > 100:
            print ('!!! Warning !!! Dropped packets exceeded 20 percent SLA '
                    + 'within 5 minutes at, ' + str(local_time.tm_hour) + ':' +
                    str(local_time.tm_min))
        if i == 0:
            total = drop_count
        elif i == 4:
            total += drop_count
            if total > 500:
                print '!!! Critical !!! SLA Violation'
            else:
                print 'SLA met'
        else: 
            total += drop_count
        return total

    def monitor(self, interface, loop_count):
        spec_interface = '.1.3.6.1.2.1.2.2.1.19.' + interface
        ifoutdiscards = netsnmp.Varbind(spec_interface)
        getdiscards = netsnmp.VarList()
        getdiscards.append(ifoutdiscards)
        counter = self.session.get(getdiscards)
        if loop_count == 0:
            print '60 Seconds Monitoring: ', counter[0]
        if loop_count == 1:
            print '120 Seconds Monitoring: ', counter[0]
        if loop_count == 2:
            print '180 Seconds Monitoring: ', counter[0]
        if loop_count == 3:
            print '240 Seconds Monitoring: ', counter[0]
        if loop_count == 4:
            print '300 Seconds Monitoring: ', counter[0]
        return counter[0]


if __name__ == '__main__':
    def main():
        ip = raw_input('Please enter IP of SNMP Device: ')
        router = Router(ip)
        result = router.update(ip)
        i = 0
        total = 0
        original_count = result[1]
        while True:
            time.sleep(20)
            if i == 0:
                previous_count = total
            else:
                previous_count = current_count
            current_count = router.monitor(result[0], i)
            total = router.calculate_difference(current_count, 
                        previous_count, i, total, original_count)
            i += 1
            if i % 5 == 0 and i != 0:
                i = 0
                total = 0
                original_count = current_count

main()