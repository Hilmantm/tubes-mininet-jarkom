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

    def build(self, **opts):

        # Konfigurasi host
        host_a = self.addHost('hostA', ip="192.168.20.2", defaultRoute="192.168.20.1")
        host_b = self.addHost('hostB', ip="192.168.50.2", defaultRoute="192.168.50.1")

        # Konfigurasi router
        router_1 = self.addRouter('router1', cls=LinuxRouter, ip="192.168.1.1/24")
        router_2 = self.addRouter('router2', cls=LinuxRouter, ip="192.168.2.1/24")
        router_3 = self.addRouter('router3', cls=LinuxRouter, ip="192.168.3.1/24")
        router_4 = self.addRouter('router4', cls=LinuxRouter, ip="192.168.4.1/24")
        
