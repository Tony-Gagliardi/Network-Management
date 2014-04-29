'''
File: network.py
Created by Mark Dehus - TLEN 5410
Modified by Anthony Gagliardi
Modified: 27 April 2014
The purpose of this file is to spawn a virtual
network containing a single switch and four
connected hosts for ARP Cache Poisoning simulation
'''
'''
Initial code provided by Mark Dehus. 
It has been modified to match the topology 
necessary for my project.
'''

from mininet.net import Mininet
from mininet.node import OVSController, OVSKernelSwitch, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
    
def allfour():

    "Create an empty network and add nodes to it."

    net = Mininet(controller = OVSController, 
                    switch=OVSSwitch, autoSetMacs=True)

    info( '*** Adding controller\n')
    net.addController( 'c0' )

    info( '*** Adding hosts\n' )
    h1 = net.addHost( 'h1', ip='10.0.0.1' )
    h2 = net.addHost( 'h2', ip='10.0.0.2' )
    h3 = net.addHost( 'h3', ip='10.0.0.3' )
    h4 = net.addHost( 'h4', ip='10.0.0.4' )

    info( '*** Adding switch\n' )
    s1 = net.addSwitch( 's1' )

    info( '*** Creating links\n' )
    net.addLink( h1, s1)
    net.addLink( h2, s1)
    net.addLink( h3, s1)
    net.addLink( h4, s1)

    info( '*** Starting network\n')
    net.start()

    info( '*** Running CLI\n' )
    CLI( net )

    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    allfour()
