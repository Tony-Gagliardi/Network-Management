import netsnmp
import time
from time import gmtime, strftime
import matplotlib.pyplot as plot_lib

class Router(object):
    def __init__(self, ip):
        '''
        Initialization method for our Router, all we need to initialize
        with is a session.
        '''
        self.session = netsnmp.Session(DestHost = ip,
                                    Community = 'public', Version = 1)


    def update(self):
        '''
        The update method pulls a list of interfaces from the device 
        and displays them to the user so they can choose which interface
        to monitor, it also gets the inital count of dropped packets. It
        returns a list containing the interface requested by the user
        and the initial count.
        '''
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

        print "List of Interfaces ---"

        packet_drops = []

        for i in range(0, ifnumber_result):
            self.session.getnext(getters)
            print ifdescr.tag[-1], ': ', ifdescr.val
            packet_drops.append(ifoutdiscards.val)
        if_request = raw_input('Please enter the interface to monitor: ')
        if if_request == '7':
            count = packet_drops[int(if_request) - 2]
        else:
            count = packet_drops[int(if_request) - 1]
            print 'Monitoring starts at ', strftime("%H:%M %p")
            result_list = [ if_request, count]
            print 'Current dropped packets is ', count
            return result_list

    def calculate_difference(self, current_count, previous_count,
                                 i, total, original_count):
        '''
        The calculate_difference method calculates the number
        of dropped packets over a 60 second interval. It returns
        the cummulative total of dropped packets so that we can
        check for an SLA violation after every 5 minutes.
        '''
        if i == 0:
            drop_count = int(current_count) - int(original_count)
        else:
            drop_count = int(current_count) - int(previous_count)
        print drop_count,'dropped packets'
        if drop_count <= 100:
            pass
        if drop_count > 100:
            print ('!!! Warning !!! Dropped packets exceeded 100 '
                    + 'within 5 minutes at ' + strftime("%H:%M %p"))

        if i == 0:
            total = drop_count
        elif i == 4:
            total += drop_count
            if total > 500:
                print '!!! Critical !!! SLA Violation'
                print "5 minutes has passed...Resetting the counter"
            else:
                print 'SLA met...NO violation occured'
                print "5 minutes has passed...Resetting the counter"
        else:
            total += drop_count
        return total

    def monitor(self, interface, loop_count):
        '''
        The monitor method gets the current number
        of discarded packets on an interface. It returns
        the current number of dropped packets by the device
        over its lifetime, so that we can calculate the 
        drop count over specific intervals.
        '''
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

def main():
    ip = raw_input('Please enter IP of SNMP Device: ')
    router = Router(ip)
    result = router.update()
    # iterator for keeping track of which interval we are on
    i = 0
    total = 0
    original_count = result[1]
    run_time = int(raw_input("Enter number of minutes to monitor (0 for indefinite): "))
    if run_time == 0:
        print "Graph is unavailable during indefinite monitoring"
        while True:
            time.sleep(60)
            if i == 0:
                previous_count = total
            else:
                previous_count = current_count
            current_count = router.monitor(result[0], i)
            # total is initially zero, but for all other iterations
            # total will be the value returned by the calculate_difference
            # method
            total = router.calculate_difference(current_count,
                        previous_count, i, total, original_count)
            i += 1
            # resetting stuff after 5 minutes
            if i % 5 == 0 and i != 0:
                i = 0
                total = 0
                original_count = current_count
    else:
        print "Graph can be found upon exit in script folder named packets.png"
        current_time = time.time()
        run_timesec = run_time * 60
        plot_list = []
        while True:
            if (time.time() - (current_time)) >= run_timesec:
                plot_lib.plot(plot_list)
                plot_lib.ylabel('Total packets dropped by device')
                plot_lib.xlabel('Time % 60')
                plot_lib.savefig('packets.png')
                break
            else:
                time.sleep(60)
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
            plot_list.append(current_count)

if __name__ == '__main__':
    main()