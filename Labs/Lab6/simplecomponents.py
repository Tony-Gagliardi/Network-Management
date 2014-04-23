'''  Implements two basic network elements, a SimpleHub and a SimpleSwitch.
     Some code was reused from the POX L2_pairs implementation.
'''
from pox.core import core
import pox.openflow.libopenflow_01 as of

class SimpleHub(object):
    def __init__(self):
        self.logger = core.getLogger()
        core.openflow.addListeners(self)

    def broadcast(self, event):
        ''' Instructs the switch that caused the event to be raised to simply
            broadcast the received packet out on all ports, execpt the one it
            came in on.

            Arguments:
                event: The event passed in from POX.
            
        '''
        message = of.ofp_packet_out(data=event.ofp)
        message.actions.append(of.ofp_action_output(port=of.OFPP_ALL))
        event.connection.send(message)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        self.logger.info("Got a packet from %s to %s", packet.src, packet.dst)
        self.broadcast(event)


class SimpleSwitch(object):
    def __init__(self):
        self.logger = core.getLogger()
        self.mac_table = {}
        core.openflow.addListeners(self)

    def forward(self, event, packet):
        destination_port = self.mac_table[(event.connection, packet.dst)]

        # Create a flow rule in the direction from sender to recipient
        # that maps to the port it came in on.
        message = of.ofp_flow_mod()
        message.match.dl_dst = packet.src
        message.match.dl_src = packet.dst
        message.actions.append(of.ofp_action_output(port = event.port))
        event.connection.send(message)

        # Create a flow rule for the recipient to the sender, and instruct
        # The switch to forward the packet that came in.
        message = of.ofp_flow_mod()
        message.data = event.ofp
        message.match.dl_src = packet.src
        message.match.dl_dst = packet.dst
        message.actions.append(of.ofp_action_output(port=destination_port))
        event.connection.send(message)
        self.logger.info("Installing %s <-> %s" % (packet.src, packet.dst))

    def _handle_PacketIn(self, event):
        packet = event.parsed
        self.logger.info("Got a packet from %s to %s", 
                         packet.src, packet.dst)
        
        # Learn the source
        self.mac_table[(event.connection, packet.src)] = event.port
        self.logger.info("Added (%s, %s) at %s to the mac table", 
                         event.connection, packet.src, event.port)

        try:
            self.logger.info("Trying to forward")
            self.forward(event, packet)
        except KeyError:
            self.logger.info("Broadcasting instead")
            # We don't know where the recipient is yet
            self.broadcast(event)

    def broadcast(self, event):
        ''' Instructs the switch that caused the event to be raised to simply
            broadcast the received packet out on all ports, execpt the one it
            came in on.

            Arguments:
                event: The event passed in from POX.
            
        '''
        message = of.ofp_packet_out(data=event.ofp)
        message.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(message)


def launch():
    #core.registerNew(SimpleHub)
    core.registerNew(SimpleSwitch)
