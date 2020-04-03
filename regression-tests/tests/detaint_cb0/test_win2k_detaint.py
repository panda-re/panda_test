# test_win2k_detaint.py
# Test taint2's detaint_cb0 option on a recording made of a 32-bit binary
# running under Windows 2000.
#
# Created:  09-OCT-2018
# Changed:  27-FEB-2019   Verify more results, now that problem with
#                         inconsistent taint reports (ACE-22) is fixed.

import datetime
import os
import re

import ptest

import tests.detaint_cb0.detaintcommon as dtcommon

# I believe these are the equivalent of "-net nic,model=ne2k_pci -net user"
NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
NE2KPCI = ptest.Device(ptest.Device.NE2K_PCI, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 512, NETDEV, NE2KPCI, vga=ptest.Qemu.CIRRUS)

# use os.path.join so needn't worry about what the separator character is on
# this system
REPLAY_PATH = os.path.join("windows2k", "win2k_hellostb")

def run():
    """
    Execute the test and return true if the test passed.
    """

    print(dtcommon.INDENT_SPACES +
        "This test takes about 16 minutes to run.  Started at:  " +
        str(datetime.datetime.now()))
    retcode = dtcommon.DoComparison("win2k", QEMU, REPLAY_PATH, "pc = 0x")
    if (not retcode):
        return False
        
    return True
    
def cleanup():
    """
    A cleanup function called when the test completes regardless of whether or
    not the test passed.
    """

    dtcommon.cleanup()
    