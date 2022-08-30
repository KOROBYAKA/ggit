from sys import exit
from mininet.node import Host
from mininet.topo import Topo
from mininet.util import quietRun
from mininet.log import error



class VLANHost( Host ):
    "Host connected to VLAN interface"

    # pylint: disable=arguments-differ
    def config( self, vlan=100, **params ):
        """Configure VLANHost according to (optional) parameters:
           vlan: VLAN ID for default interface"""

        r = super( VLANHost, self ).config( **params )

        intf = self.defaultIntf()
        self.cmd( 'ifconfig %s inet 0' % intf )
        self.cmd( 'vconfig add %s %d' % ( intf, vlan ) )
        self.cmd( 'ifconfig %s.%d inet %s' % ( intf, vlan, params['ip'] ) )
        newName = '%s.%d' % ( intf, vlan )
        intf.name = newName
        self.nameToIntf[ newName ] = intf


        return r


hosts = { 'vlan': VLANHost }

class MyTopo( Topo ):
    def build( self, k=4, n=1, vlanBase=100 ):
        s1 = self.addSwitch( 's1' )
        for i in range( k ):
            vlan = vlanBase + i
        name = 'hA'
        hA = self.addHost( name, cls=VLANHost, vlan=vlan )
        self.addLink( hA, s1)

        hB = self.addHost( 'hB')
        self.addLink( hB, s1 )
        self.addLink(hB, s1)
        self.addLink(hB, s1)
        self.addLink(hB, s1)




topos = { 'mytopo': ( lambda: MyTopo() ) }