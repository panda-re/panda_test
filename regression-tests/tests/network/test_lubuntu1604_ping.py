from scapy.all import *

import ptest
import os

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000 = ptest.Device(ptest.Device.E1000, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 2048, NETDEV, E1000, vga=ptest.Qemu.CIRRUS)

PCAP_FILE = "/tmp/test-netrec.pcap"
NETWORK_PLUGIN = ptest.Plugin("network", file=PCAP_FILE)

REPLAY = ptest.Replay("lubuntu1604-ping-test", QEMU, NETWORK_PLUGIN)

def run():
    retcode = REPLAY.run()
    if retcode != 0:
        REPLAY.dump_console(stderr=True)
        return False

    packets = rdpcap(PCAP_FILE)
    packet_count = 0
    expected_reply = None
    for pkt in packets:
        if ICMP in pkt and icmptypes[pkt.getlayer(ICMP).type] == "echo-request":
            if expected_reply != None:
                print("Error Missed the reply packet!")
                return False
            expected_reply = pkt.getlayer(Raw).load
        elif ICMP in pkt and icmptypes[pkt.getlayer(ICMP).type] == "echo-reply":
            if not expected_reply == pkt.getlayer(Raw).load:
                print("Error: Ping packet echo-reply mismatch!")
                return False
            expected_reply = None
        packet_count += 1
    if packet_count != 12:
        print("Error: Packet Count Mismatch!")
        return False

    return True

def cleanup():
    try:
        os.remove(PCAP_FILE)
    except:
        pass
