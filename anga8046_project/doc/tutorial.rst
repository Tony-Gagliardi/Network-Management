Simple Tutorial
===============

To run this project, follow the following steps:

1. Launch mininet by running the 'network.py' file.
2. Open a terminal on host 1 by typing 'xterm h1' in the mininet console.
3. Launch the packet sniffer by running the 'main.py' file.
4. In the xterm for h1, ping host h2 for a couple of seconds.
5. Navigate to the scapy python file and run it with 'sudo python scapy'
6. In the scapy interpreter, run 'arpcachepoison(10.0.0.1, 10.0.0.2)'
7. This will simulate a malicious user trying to spoof h2's MAC.
8. Check the email specified for the network administrator, in it there 
    should be a notification.
