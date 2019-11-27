# noqa: E501, W291
from cloudinit import net

from cloudinit.tests.helpers import (CiTestCase, mock)

IFCONFIG_FREEBSD = """vtnet0: flags=8843<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> metric 0 mtu 1500
        options=6c07bb<RXCSUM,TXCSUM,VLAN_MTU,VLAN_HWTAGGING,JUMBO_MTU,VLAN_HWCSUM,TSO4,TSO6,LRO,VLAN_HWTSO,LINKSTATE,RXCSUM_IPV6,TXCSUM_IPV6>
        ether 52:54:00:50:b7:0d
re0.33: flags=8943<UP,BROADCAST,RUNNING,PROMISC,SIMPLEX,MULTICAST> metric 0 mtu 1500
        options=80003<RXCSUM,TXCSUM,LINKSTATE>
        ether 80:00:73:63:5c:48
        groups: vlan 
        vlan: 33 vlanpcp: 0 parent interface: re0
        media: Ethernet autoselect (1000baseT <full-duplex,master>)
        status: active
        nd6 options=21<PERFORMNUD,AUTO_LINKLOCAL>
lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> metric 0 mtu 16384
        options=680003<RXCSUM,TXCSUM,LINKSTATE,RXCSUM_IPV6,TXCSUM_IPV6>
"""


class TestInterfacesByMac(CiTestCase):

    @mock.patch('cloudinit.util.subp')
    @mock.patch('cloudinit.util.is_FreeBSD')
    def test_get_interfaces_by_mac(self, mock_is_FreeBSD, mock_subp):
        mock_is_FreeBSD.return_value = True
        mock_subp.return_value = (IFCONFIG_FREEBSD, 0)
        a = net.get_interfaces_by_mac()
        assert a == {
                "vtnet0": "52:54:00:50:b7:0d",
                "re0.33": "80:00:73:63:5c:48"}
