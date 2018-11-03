'''
Create a socket that listens for incoming UDP broadcasts. Use a thread to listen for any incoming
messages so we don't block the code.
Then, broadcast a message.
Any other machines running this code will respond to the message.
We will get the broadcasted message, but ignore it because we check if it's from ourselves or not.
If we get a response from another machine running this code we'll show it.

Basically this is a simple program to find other machines on a network. Unlike ping, you don't need
to know the other machines IP address.
'''

import sys
from socket import *
import time
from threading import Thread

class Discovery(object):

    UDP_IP = "0.0.0.0"
    BROADCAST_IP = "192.168.255.255"
    UDP_PORT = 54545
    QUERY_END = " wants to know who is about."
    REPLY_END = " says 'Hello.'"
    RUN_TIME = 60 * 60  # Run for one hour

    def broadcast(self):
        from socket import *

        cs = socket(AF_INET, SOCK_DGRAM)
        cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        cs.sendto('Hello, network!', (BROADCAST_IP, 54545))


    def listener(self):
        while self.running:
            try:
                data, addr = self.listener.recvfrom(1024) # buffer size is 1024 bytes
                if (data.startswith(self.host) == False):  # Ignore our own messages
                    print "IN:", data
                    if (data.endswith(QUERY_END)):  # Respond if it's a Query broadcast
                        msg = self.host + REPLY_END
                        self.reciever = socket(AF_INET, SOCK_DGRAM)
                        self.reciever.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                        print "OUT:", msg
                        self.reciever.sendto(msg, (BROADCAST_IP, UDP_PORT))
            except timeout, e:
                self.idle += 1
            except error, e:
                # Something else happened, handle error, exit, etc.
                raise
            except exception, e:
                if len(msg) == 0:
                    print 'Server shutting down.'
                else:
                    print "Fatal problem:"
                    print e
                    raise

    def start(self):
        self.running = True
        self.host = gethostname()
        self.idle = 0

        self.listener = socket(AF_INET, SOCK_DGRAM) # UDP
        self.listener.bind((UDP_IP, UDP_PORT))

        self.listener.settimeout(15)

        self.thread = Thread(target=listener, args=())
        self.thread.start()

        msg = "{}:{}".format(self.host, QUERY_END)
        self.broadcast_sock = socket(AF_INET, SOCK_DGRAM)
        self.broadcast_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        print "OUT:", msg
        self.broadcast_sock.sendto(msg, (BROADCAST_IP, UDP_PORT))

        self.running = False