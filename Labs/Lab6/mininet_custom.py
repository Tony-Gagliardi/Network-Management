'''
Initial code provided by Mark Dehus. 
It has been modified to match the topology 
specified in the lab 6 writeup.
Modified by Anthony Gagliardi and Saman Samadian
'''

from mininet.net import Mininet
from mininet.node import  RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def allfour():

    "Create an empty network and add nodes to it."

    net = Mininet( controller=RemoteController, switch=OVSKernelSwitch, 
                        autoSetMacs=True)

    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    info( '*** Adding hosts\n' )
    h1 = net.addHost( 'h1', ip='10.0.0.1' )
    h2 = net.addHost( 'h2', ip='10.0.0.2' )
    h3 = net.addHost( 'h3', ip='10.0.0.3' )
    h4 = net.addHost( 'h4', ip='10.0.0.4' )

    info( '*** Adding switch\n' )
    s1 = net.addSwitch( 's1' )
    s2 = net.addSwitch( 's2' )
    s3 = net.addSwitch( 's3' )
    s4 = net.addSwitch( 's4' )

    info( '*** Creating links\n' )
    net.addLink( h1, s1)
    net.addLink( h2, s2 )
    net.addLink( s1, s2 )
    net.addLink( s2, s3 )
    net.addLink( s3, s4 )
    net.addLink( h3, s3 )
    net.addLink( h4, s4 )

    info( '*** Starting network\n')
    net.start()

    info( '*** Running CLI\n' )
    CLI( net )

    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    allfour()
