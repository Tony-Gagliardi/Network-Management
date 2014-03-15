class Switch(object):
    def __init__(self, name, address, forwardtable = None):
        '''
        The Switch constructor initializes default attributes
        for a Switch.
        '''
        if forwardtable == None:
            self.forwardtable = {}
        # Ports is a ports list that we will use for simulating
        # connections between devices
        self.ports = list()
        self.name = name
        # MAC Address
        self.address = address

    def connect(self, indevice):
        '''
        The Switch connect method is a simulated
        connection between a switch and some device,
        all it does is add the device the Switch's ports
        list
        '''
        self.ports.append(indevice)

    def receive(self, inpacket, sender):
        '''
        The Switch receive method is a simulated accept
        of a packet, where the switch forwards or broadcasts
        depending on its CAM table. Because of the limitation of
        software, we are passing in the last known sender/invoker 
        to the receive call, which isn't a true implementation
        of Ethernet.
        '''
        if inpacket.dst in self.forwardtable:
            self.learn(inpacket, sender)
            self.forward(inpacket)
        else:
            print "Destination not in CAM table, broadcasting..."
            self.learn(inpacket, sender)
            self.broadcast(inpacket, sender)
                 
    def broadcast(self, inpacket, sender):
        '''
        The Switch broadcast method is invoked whenever a Switch's
        CAM table doesn't contain the destination specified in the data
        packet, it 'sends' the packet on all outgoing ports, expect for
        the one which the packet came in on
        '''
        for index, port in enumerate(self.ports):
            if port != sender:
                port.receive(inpacket, self)
            else:
                continue
    
    def learn (self, inpacket, sender):
        '''
        The Switch learn method is invoked whenever a packet
        is recieved. It simply updates the CAM table with 
        the senders information
        '''
        for index, item in enumerate(self.ports):
            if sender == item:
                self.forwardtable[inpacket.src] = index               
                    
    def forward(self, inpacket):
        '''
        The Switch forward method is invoked whenever a Switch's
        CAM table contains the destination specified in the data
        packet, it 'unicasts' the packet on the port which the Switch
        knows to reach the destination.
        '''
        self.ports[self.forwardtable[inpacket.dst]].receive(inpacket, self)     

    def __repr__(self):
        '''
        Useful method for debugging, allows us to print outgoing
        the name of a certain Switch object.
        '''
        return self.name

class Host(object):
    def __init__(self, name, address):
        '''
        The host constructor initializes default
        attributes for a Host.
        '''
        self.name = name
        self.address = address
        self.connection = None

    def connect(self, indevice):
        '''
        The Host connect method simulates a connection
        between a host and a switch by keeping track
        of the particular switch that a given host is 
        connected to.
        '''
        self.connection = indevice

    def receive(self, inpacket, sender):
        '''
        The Host receive method checks to make sure
        that a received packet was intended for itself,
        and then prints the payload.
        '''
        if self.address == inpacket.dst:
            print (self.name + ' received packet ' + '"' + inpacket.payload + 
                '"' + ' from ' + inpacket.src)

    def send(self, indst):
        '''
        The Host send method simulates sending a data packet
        with a specified payload by invoking receive on the 
        connected switch
        '''
        packet = Packet(self.address, indst.address,
            raw_input("Enter Message to be sent from " + self.name 
                + ' to ' + indst.name + ': '))
        self.connection.receive(packet, self)

    def __repr__(self):
        '''
        Useful method for debugging, allows us to print outgoing
        the name of a certain Host object.
        '''
        return self.name

class Packet(object):
    def __init__(self, src, dst, payload):
        '''
        The Packet constructor initializes default
        attributes for a data packet. 
        '''
        self.src = src
        self.dst = dst
        self.payload = payload

def main():
    h0 = Host('h0', '00')
    h1 = Host('h1', '01')
    s0 = Switch('s0', '10')
    s1 = Switch('s1', '11')
    h2 = Host('h2', '02')
    h3 = Host('h3', '03')
    s2 = Switch('s2', '12')
    h4 = Host('h4' , '04')
    h5 = Host('h5' , '05')
    h0.connect(s0)
    h1.connect(s0)
    s0.connect(h0)
    print "h0 connecting to s0"
    s0.connect(h1)
    print "h1 connecting to s0"
    s0.connect(s1)
    s1.connect(s0)
    print "s0 connecting to s1"
    h2.connect(s1)
    h3.connect(s1)
    s1.connect(h2)
    print "h2 connecting to s1"
    s1.connect(h3)
    print "h3 connecting to s1"
    s2.connect(s1)
    s1.connect(s2)
    print "s1 connecting to s2"
    h4.connect(s2)
    h5.connect(s2)
    s2.connect(h4)
    print "h4 connecting to s2"
    s2.connect(h5)
    print "h5 connecting to s2"


    loop = True
    while (loop == True):
        hostdict = {'h0': h0, 'h1': h1, 'h2' : h2, 'h3': h3, 'h4' : h4 ,'h5' : h5}
        srchost = raw_input("Which host would you like to send from?: ")
        dsthost = raw_input("Which host would you like to send to?: ")
        hostdict[srchost].send(hostdict[dsthost])
        response = raw_input("Enter '0' to examine CAM tables, '1' to examine Port Lists or 'exit' to quit: ")
        if response == '0':
            print 's0 forwarding table is' , s0.forwardtable
            print 's1 forwarding table is' , s1.forwardtable
            print 's2 forwarding table is' , s2.forwardtable
        elif response == '1':
            print 's0 port list is' , s0.ports
            print 's1 port list is' , s1.ports
            print 's2 port list is' , s2.ports

        elif response == 'exit':
            loop = False
            continue
        else:
            print ("Command not understood, please try again")
            
if __name__ == '__main__':
    main()
