Project Summary
===============
The purpose of this project is to monitor ARP traffic on a network
and notify administrators when malicious activity is detected.

Goals Achieved
--------------
Goal 1 - Use python's flowd library to parse all network traffic supplied byNetFlow and extract ARP replies

    I was able to complete this goal, but I approached it a little
different than specified in the proposal. Instead of using Netflow data
and extracting ARP packets, I was able to use the python module called
Scapy, which is designed for security scripts like this one. Ironically,
it only took three lines of code to 'sniff' ARP packets on the network
using this module.

Goal 2 - Generate a tool for preventing attacks in a network with statically assigned IP Addresses.

    I was able to complete this goal. I essentially built a dictionary
that determines correct internal MAC/IP pairs. If any change is made to these pairings, the network administrator is notified because this is a clear
indication of malicious activity.

Goals Still In-Progress
-----------------------
Goal 3 - Modify the tool for preventing attacks in a network with dynamically assigned IP Addresses (eg. An internal DHCP Server).

    This goal is still in progress because of limitations of mininet. I can't seem to find a way to get mininet hosts to talk to a DHCP server to obtain their IP Addresses. If I had that working, I have a very specific strategy for completing this goal, which as follows:

    1. Use Scapy's sniff function to detect any ARP traffic on the network.
    2. Exactly the same as the static network, invoke a function on the
        packet that determines whether or not the MAC/IP pair has been
        modified.
    3. Now, instead of immediately notifying the administrator via 
        email, compare the MAC/IP pair found with the current MAC/IP pair
        residing in the DHCP server's configuration files to see if they 
        match. If not, notify the adminstrator.

Lessons Learned
-----------------------
1. Scapy is an incredibly powerful and useful tool for network related tasks, especially those related to security and packet sniffing.

2. Staying true to the project timeline is very important.

3. ARP traffic is a lot more prevalent than I thought. 
