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
    net.addHost("r1")
    net.addHost("r2")
    net.addHost("r3")
    net.addHost("r4")
    
    # Add Host ha, hb
    net.addHost("ha")
    net.addHost("hb")

    # Add Link
    net.addLink( net[ 'ha' ], net[ 'r1' ], intfName1='ha-eth0', intfName2='r1-eth0', cls=TCLink, bw=1 ) # NET 1
    net.addLink( net[ 'r1' ], net[ 'r3' ], intfName1='r1-eth1', intfName2='r3-eth1', cls=TCLink, bw=0.5 ) # NET 2
    net.addLink( net[ 'r3' ], net[ 'hb' ], intfName1='r3-eth0', intfName2='hb-eth0', cls=TCLink, bw=1 ) # NET 3
    net.addLink( net[ 'hb' ], net[ 'r4' ], intfName1='hb-eth1', intfName2='r4-eth1', cls=TCLink, bw=1 ) # NET 4
    net.addLink( net[ 'r4' ], net[ 'r2' ], intfName1='r4-eth0', intfName2='r2-eth0', cls=TCLink, bw=0.5 ) # NET 5
    net.addLink( net[ 'ha' ], net[ 'r2' ], intfName1='ha-eth1', intfName2='r2-eth1', cls=TCLink, bw=1 ) # NET 6
    net.addLink( net[ 'r1' ], net[ 'r4' ], intfName1='r1-eth2', intfName2='r4-eth2', cls=TCLink, bw=1 ) # NET 7
    net.addLink( net[ 'r2' ], net[ 'r3' ], intfName1='r2-eth2', intfName2='r3-eth2', cls=TCLink, bw=1 ) # NET 8

    net.build()

    # config ip into interface
    # ha
    net['ha'].cmd('ifconfig ha-eth0 0')
    net['ha'].cmd('ifconfig ha-eth1 0')
    net['ha'].cmd('ifconfig ha-eth0 192.168.0.1 netmask 255.255.255.0')
    net['ha'].cmd('ifconfig ha-eth1 192.168.5.1 netmask 255.255.255.0')

    # hb
    net['hb'].cmd('ifconfig hb-eth0 0')
    net['hb'].cmd('ifconfig hb-eth1 0')
    net['hb'].cmd('ifconfig hb-eth0 192.168.2.2 netmask 255.255.255.0')
    net['hb'].cmd('ifconfig hb-eth1 192.168.3.1 netmask 255.255.255.0')

    # r1
    net['r1'].cmd('ifconfig r1-eth0 0')
    net['r1'].cmd('ifconfig r1-eth1 0')
    net['r1'].cmd('ifconfig r1-eth2 0')
    net['r1'].cmd('ifconfig r1-eth0 192.168.0.2 netmask 255.255.255.0')
    net['r1'].cmd('ifconfig r1-eth1 192.168.1.1 netmask 255.255.255.0')
    net['r1'].cmd('ifconfig r1-eth2 192.168.6.1 netmask 255.255.255.0')

    # r2
    net['r2'].cmd('ifconfig r2-eth0 0')
    net['r2'].cmd('ifconfig r2-eth1 0')
    net['r2'].cmd('ifconfig r2-eth2 0')
    net['r2'].cmd('ifconfig r2-eth0 192.168.4.2 netmask 255.255.255.0')
    net['r2'].cmd('ifconfig r2-eth1 192.168.5.2 netmask 255.255.255.0')
    net['r2'].cmd('ifconfig r2-eth2 192.168.7.1 netmask 255.255.255.0')

    # r3
    net['r3'].cmd('ifconfig r3-eth0 0')
    net['r3'].cmd('ifconfig r3-eth1 0')
    net['r3'].cmd('ifconfig r3-eth2 0')
    net['r3'].cmd('ifconfig r3-eth0 192.168.2.1 netmask 255.255.255.0')
    net['r3'].cmd('ifconfig r3-eth1 192.168.1.2 netmask 255.255.255.0')
    net['r3'].cmd('ifconfig r3-eth2 192.168.7.2 netmask 255.255.255.0')

    # r4
    net['r4'].cmd('ifconfig r4-eth0 0')
    net['r4'].cmd('ifconfig r4-eth1 0')
    net['r4'].cmd('ifconfig r4-eth2 0')
    net['r4'].cmd('ifconfig r4-eth0 192.168.4.1 netmask 255.255.255.0')
    net['r4'].cmd('ifconfig r4-eth1 192.168.3.2 netmask 255.255.255.0')
    net['r4'].cmd('ifconfig r4-eth2 192.168.6.2 netmask 255.255.255.0')


    # Start IP Forward on Router
    net[ 'r1' ].cmd( 'sysctl net.ipv4.ip_forward=1' )
    net[ 'r2' ].cmd( 'sysctl net.ipv4.ip_forward=1' )
    net[ 'r3' ].cmd( 'sysctl net.ipv4.ip_forward=1' )
    net[ 'r4' ].cmd( 'sysctl net.ipv4.ip_forward=1' )

    # Static routing
    # 2 table karena terdapat 2 interface
    # ha
    net['ha'].cmd('ip rule add from 192.168.0.1 table 1')
    net['ha'].cmd('ip rule add from 192.168.5.1 table 2')
    net['ha'].cmd('ip route add 192.168.0.0/24 dev ha-eth0 scope link table 1')
    net['ha'].cmd('ip route add default via 192.168.0.2 dev ha-eth0 table 1')
    net['ha'].cmd('ip route add 192.168.5.0/24 dev ha-eth1 scope link table 2')
    net['ha'].cmd('ip route add default via 192.168.5.2 dev ha-eth1 table 2')
    net['ha'].cmd('ip route add default scope global nexthop via 192.168.0.2 dev ha-eth0')

    # hb
    net['hb'].cmd('ip rule add from 192.168.2.2 table 1')
    net['hb'].cmd('ip rule add from 192.168.3.1 table 2')
    net['hb'].cmd('ip route add 192.168.2.0/24 dev hb-eth0 scope link table 1')
    net['hb'].cmd('ip route add default via 192.168.2.1 dev hb-eth0 table 1')
    net['hb'].cmd('ip route add 192.168.3.0/24 dev hb-eth1 scope link table 2')
    net['hb'].cmd('ip route add default via 192.168.3.2 dev hb-eth1 table 2')
    net['hb'].cmd('ip route add default scope global nexthop via 192.168.3.2 dev hb-eth1')

    # r1
    net['r1'].cmd('route add -net 192.168.2.0/24 gw 192.168.1.2')
    net['r1'].cmd('route add -net 192.168.3.0/24 gw 192.168.6.2')
    net['r1'].cmd('route add -net 192.168.4.0/24 gw 192.168.6.2')
    net['r1'].cmd('route add -net 192.168.5.0/24 gw 192.168.6.2')
    net['r1'].cmd('route add -net 192.168.7.0/24 gw 192.168.1.2')

    # r2
    net['r2'].cmd('route add -net 192.168.0.0/24 gw 192.168.7.2')
    net['r2'].cmd('route add -net 192.168.1.0/24 gw 192.168.7.2')
    net['r2'].cmd('route add -net 192.168.2.0/24 gw 192.168.7.2')
    net['r2'].cmd('route add -net 192.168.3.0/24 gw 192.168.4.1')
    net['r2'].cmd('route add -net 192.168.6.0/24 gw 192.168.4.1')

    # r3
    net['r3'].cmd('route add -net 192.168.0.0/24 gw 192.168.1.1')
    net['r3'].cmd('route add -net 192.168.3.0/24 gw 192.168.7.1')
    net['r3'].cmd('route add -net 192.168.4.0/24 gw 192.168.7.1')
    net['r3'].cmd('route add -net 192.168.5.0/24 gw 192.168.7.1')
    net['r3'].cmd('route add -net 192.168.6.0/24 gw 192.168.1.1')

    # r4
    net['r4'].cmd('route add -net 192.168.0.0/24 gw 192.168.6.1')
    net['r4'].cmd('route add -net 192.168.1.0/24 gw 192.168.6.1')
    net['r4'].cmd('route add -net 192.168.2.0/24 gw 192.168.6.1')
    net['r4'].cmd('route add -net 192.168.5.0/24 gw 192.168.4.2')
    net['r4'].cmd('route add -net 192.168.7.0/24 gw 192.168.4.2')

    net.start()

    # ping all host
    info('\n', net.ping(), '\n')

    CLI(net)

    # Stop Network
    # net.stop()

if __name__ == '__main__':
    os.system('mn -c')
    os.system( 'clear' )
    setLogLevel( 'info' )
    configNetwork()
