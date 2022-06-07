from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
import os
import time
from datetime import datetime

class NetworkTopology(Topo):

    def build(self, **_opts):

        # Konfigurasi host
        host_a = self.addHost('hostA', ip="192.168.20.2/24", defaultRoute="192.168.20.1")
        host_b = self.addHost('hostB', ip="192.168.50.2/24", defaultRoute="192.168.50.1")

        # Konfigurasi router
        router_1 = self.addNode('router1', ip="192.168.1.1/24")
        router_2 = self.addNode('router2', ip="192.168.2.1/24")
        router_3 = self.addNode('router3', ip="192.168.3.1/24")
        router_4 = self.addNode('router4', ip="192.168.4.1/24")

        #Mendefinisikan bandwidth (/Mbps)
        bandwidth1 = {'bw':1}
        bandwidth2 = {'bw':0.5}

        # add link host
        self.addLink(router_1, host_a, intfName1 = 'router1-eth0', intfName2 = 'hostA-eth0', cls=TCLink, **bandwidth1)
        self.addLink(router_2, host_a, intfName1 = 'router2-eth0', intfName2 = 'hostA-eth1', cls=TCLink, **bandwidth1)
        self.addLink(router_3, host_b, intfName1 = 'router3-eth0', intfName2 = 'hostB-eth0', cls=TCLink, **bandwidth1)
        self.addLink(router_4, host_b, intfName1 = 'router4-eth0', intfName2 = 'hostB-eth1', cls=TCLink, **bandwidth1)

        # add link router
        self.addLink(router_1, router_3, intfName1 = 'router1-eth1', intfName2 = 'router3-eth1', cls=TCLink, **bandwidth2)
        self.addLink(router_1, router_4, intfName1 = 'router1-eth2', intfName2 = 'router4-eth1', cls=TCLink, **bandwidth1)
        self.addLink(router_2, router_4, intfName1 = 'router2-eth2', intfName2 = 'router4-eth2', cls=TCLink, **bandwidth2)
        self.addLink(router_2, router_3, intfName1 = 'router2-eth1', intfName2 = 'router3-eth2', cls=TCLink, **bandwidth1)
        self.build()

def run():
    net = Mininet(topo=NetworkTopology())
    net.start()

setLogLevel('info')
run()
