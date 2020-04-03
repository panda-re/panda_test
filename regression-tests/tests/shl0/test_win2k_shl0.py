# test_win2k_shl0.py
# Test the changes made to how taint2 propagates taint on an LLVM SHL 0 (shift
# left 0, which does nothing) instruction using a recording made of a 32-bit
# binary running under Windows 2000.
#
# Created:  10-OCT-2018
# Changed:  03-DEC-2018   Tweak expected results to account for changes in
#                         how taint propagates.

import os
import re

import ptest

import tests.shl0.shl0common as shlcommon

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

    # Note block 0x1671ea0 has taint in it from more instructions than SHL 0.
    # The only way to tell for sure how much of it is from an SHL 0 that has
    # only some of its input bytes tainted is to run PANDA with TAINT2DEBUG, and
    # compare the taint2 debug lines with the LLVM for the block to see which
    # reports go with which LLVM instruction.  As we rarely build with
    # TAINT2DEBUG on, we can't do that during regression testing.
    retcode = shlcommon.DoComparison("win2k", QEMU, REPLAY_PATH,
        "0x1671ea0", 17)
    if (not retcode):
        return False
        
    return True
    
def cleanup():
    """
    A cleanup function called when the test completes regardless of whether or
    not the test passed.
    """

    shlcommon.cleanup()
    