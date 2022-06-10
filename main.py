from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info
import os
import time
from datetime import datetime

def configNetwork():

    # Run Mininet
    net = Mininet( link=TCLink )
    
    # Add Router
    net.addHost( 'r1', ip='192.168.1.1/24' )
    net.addHost( 'r2', ip='192.168.2.1/24' )
    net.addHost( 'r3', ip='192.168.3.1/24' )
    net.addHost( 'r4', ip='192.168.4.1/24' )
    
    # Add Host ha, hb
    net.addHost("ha", ip="192.168.1.2/24", defaultRoute="via 192.168.1.1")
    net.addHost("hb", ip="192.168.2.2/24", defaultRoute="via 192.168.2.1")
    

    # Add Link
    net.addLink( net[ 'ha' ], net[ 'r1' ], intfName2='r1-eth0', bw=1 ) 
    net.addLink( net[ 'ha' ], net[ 'r3' ], intfName2='r3-eth0', bw=1 )
    net.addLink( net[ 'hb' ], net[ 'r2' ], intfName2='r2-eth0', bw=1 )
    net.addLink( net[ 'hb' ], net[ 'r4' ], intfName2='r4-eth0', bw=1 )

    net.addLink( net[ 'r1' ], net[ 'r2' ], intfName2='r2-eth1', bw=0.5 )
    net.addLink( net[ 'r1' ], net[ 'r4' ], intfName2='r4-eth1', bw=1 )
    net.addLink( net[ 'r3' ], net[ 'r2' ], intfName2='r2-eth2', bw=1 )
    net.addLink( net[ 'r3' ], net[ 'r4' ], intfName2='r4-eth2', bw=0.5 )


    # add IP Address for host A
    net[ 'ha' ].cmd( 'ip addr add 192.168.1.2/24 brd + dev ha-eth0' )
    net[ 'ha' ].cmd( 'ip addr add 192.168.2.2/24 brd + dev ha-eth1' )

    # add IP Address for host B
    net[ 'ha' ].cmd( 'ip addr add 192.168.3.1/24 brd + dev hb-eth0' )
    net[ 'ha' ].cmd( 'ip addr add 192.168.3.2/24 brd + dev hb-eth1' )

    # add IP Address for router 1
    net[ 'r1' ].cmd( 'ip addr add 192.168.1.1/24 brd + dev r1-eth0' )
    net[ 'r1' ].cmd( 'ip addr add 192.168.2.1/24 brd + dev r1-eth1' )
    net[ 'r1' ].cmd( 'ip addr add 192.168.4.1/24 brd + dev r1-eth2' )

    # add IP Address for router 2
    net[ 'r2' ].cmd( 'ip addr add 192.168.2.1/24 brd + dev r2-eth0' )
    net[ 'r2' ].cmd( 'ip addr add 192.168.1.1/24 brd + dev r2-eth1' )
    net[ 'r2' ].cmd( 'ip addr add 192.168.3.1/24 brd + dev r2-eth2' )

    # add IP Address for router 3
    net[ 'r3' ].cmd( 'ip addr add 192.168.3.1/24 brd + dev r3-eth0' )
    net[ 'r3' ].cmd( 'ip addr add 192.168.2.1/24 brd + dev r3-eth1' )
    net[ 'r3' ].cmd( 'ip addr add 192.168.4.1/24 brd + dev r3-eth2' )

    # add IP Address for router 4
    net[ 'r4' ].cmd( 'ip addr add 192.168.4.1/24 brd + dev r4-eth0' )
    net[ 'r4' ].cmd( 'ip addr add 192.168.1.1/24 brd + dev r4-eth1' )
    net[ 'r4' ].cmd( 'ip addr add 192.168.3.1/24 brd + dev r4-eth2' )

    # Start IP Forward on Router
    net[ 'r1' ].cmd( 'sysctl net.ipv4.ip_forward=1' )
    net[ 'r2' ].cmd( 'sysctl net.ipv4.ip_forward=1' )
    net[ 'r3' ].cmd( 'sysctl net.ipv4.ip_forward=1' )
    net[ 'r4' ].cmd( 'sysctl net.ipv4.ip_forward=1' )

    net.start()

    # ping all host
    info('\n', net.ping(), '\n')

    # Stop Network
    net.stop()

if __name__ == '__main__':
    os.system('mn -c')
    os.system( 'clear' )
    setLogLevel( 'info' )
    configNetwork()
