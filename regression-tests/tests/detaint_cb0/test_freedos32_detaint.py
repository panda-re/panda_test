# test_freedos32_detaint.py
# Test taint2's detaint_cb0 option on a recording made of a 32-bit binary
# running under FreeDOS.
#
# Created:  08-OCT-2018
# Changed:  27-FEB-2019   Verify more results, now that problem with
#                         inconsistent taint reports (ACE-22) is fixed.

import os
import re

import ptest

import tests.detaint_cb0.detaintcommon as dtcommon

QEMU = ptest.Qemu(ptest.Qemu.I386, 128)

# use os.path.join so needn't worry about what the separator character is on
# this system
REPLAY_PATH = os.path.join("freedos", "freedos_hello32b2")

def run():
    """
    Execute the test and return true if the test passed.
    """

    retcode = dtcommon.DoComparison("freedos32", QEMU, REPLAY_PATH, "pc = 0x")
    if (not retcode):
        return False
        
    return True
    
def cleanup():
    """
    A cleanup function called when the test completes regardless of whether or
    not the test passed.
    """

    dtcommon.cleanup()
    