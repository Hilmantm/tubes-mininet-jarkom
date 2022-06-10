from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
import os
import time
from datetime import datetime

# class NetworkTopology(Topo):

#     def build(self, **_opts):

#         # Konfigurasi host
#         host_a = self.addHost('hostA', ip="192.168.20.2/24", defaultRoute="192.168.20.1")
#         host_b = self.addHost('hostB', ip="192.168.50.2/24", defaultRoute="192.168.50.1")

#         # Konfigurasi router
#         router_1 = self.addHost('router1', ip="192.168.1.1/24")
#         router_2 = self.addHost('router2', ip="192.168.2.1/24")
#         router_3 = self.addHost('router3', ip="192.168.3.1/24")
#         router_4 = self.addHost('router4', ip="192.168.4.1/24")

#         #Mendefinisikan bandwidth (/Mbps)
#         bandwidth1 = {'bw':1}
#         bandwidth2 = {'bw':0.5}

#         # add link host
#         self.addLink(router_1, host_a, intfName1 = 'router1-eth0', intfName2 = 'hostA-eth0', cls=TCLink, **bandwidth1)
#         self.addLink(router_2, host_a, intfName1 = 'router2-eth0', intfName2 = 'hostA-eth1', cls=TCLink, **bandwidth1)
#         self.addLink(router_3, host_b, intfName1 = 'router3-eth0', intfName2 = 'hostB-eth0', cls=TCLink, **bandwidth1)
#         self.addLink(router_4, host_b, intfName1 = 'router4-eth0', intfName2 = 'hostB-eth1', cls=TCLink, **bandwidth1)

#         # add link router
#         self.addLink(router_1, router_3, intfName1 = 'router1-eth1', intfName2 = 'router3-eth1', cls=TCLink, **bandwidth2)
#         self.addLink(router_1, router_4, intfName1 = 'router1-eth2', intfName2 = 'router4-eth1', cls=TCLink, **bandwidth1)
#         self.addLink(router_2, router_4, intfName1 = 'router2-eth2', intfName2 = 'router4-eth2', cls=TCLink, **bandwidth2)
#         self.addLink(router_2, router_3, intfName1 = 'router2-eth1', intfName2 = 'router3-eth2', cls=TCLink, **bandwidth1)
#         self.build()

# def run():
#     net = Mininet(topo=NetworkTopology())
#     net.start()

# setLogLevel('info')
# run()

def configNetwork():

    # Run Mininet
    net = Mininet( link=TCLink )
    
    # Add Router
    net.addHost( 'r1', ip='192.168.1.1/24' )
    net.addHost( 'r2', ip='192.168.2.1/24' )
    net.addHost( 'r3', ip='192.168.3.1/24' )
    net.addHost( 'r4', ip='192.168.4.1/24' )
    
    # Add Host h0,h1,h2,h3
    net.addHost("ha", ip="192.168.20.2/24", defaultRoute="via 192.168.20.1")
    net.addHost("hb", ip="192.168.50.2/24", defaultRoute="via 192.168.50.1")
    

    # Add Link
    net.addLink( net[ 'ha' ], net[ 'r1' ], intfName2='r1-eth0', bw=1 ) 
    net.addLink( net[ 'ha' ], net[ 'r2' ], intfName2='r2-eth0', bw=1 )

    # Stop Network
    net.stop()

if __name__ == '__main__':
    os.system('mn -c')
    os.system( 'clear' )
    setLogLevel( 'info' )
    coonfigNetwork()
