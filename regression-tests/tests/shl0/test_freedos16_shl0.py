# test_freedos16_shl0.py
# Test the changes made to how taint2 propagates taint on an LLVM SHL 0 (shift
# left 0, which does nothing) instruction using a recording made of a 16-bit binary
# running under FreeDOS.
#
# Created:  10-OCT-2018
# Changed:  03-DEC-2018   Adjust expected results to account for recent changes.

import os
import re

import ptest

import tests.shl0.shl0common as shlcommon

QEMU = ptest.Qemu(ptest.Qemu.I386, 128)

# use os.path.join so needn't worry about what the separator character is on
# this system
REPLAY_PATH = os.path.join("freedos", "freedos_hello16b2")

def run():
    """
    Execute the test and return true if the test passed.
    """

    # Note block 0x2c4c has taint in it from more instructions than SHL 0.
    # The only way to tell for sure how much of it is from an SHL 0 that has
    # only some of its input bytes tainted is to run PANDA with TAINT2DEBUG, and
    # compare the taint2 debug lines with the LLVM for the block to see which
    # reports go with which LLVM instruction.  As we rarely build with
    # TAINT2DEBUG on, we can't do that during regression testing.
    retcode = shlcommon.DoComparison("freedos16", QEMU, REPLAY_PATH,
        "0x2c4c", 17)
    if (not retcode):
        return False
        
    return True
    
def cleanup():
    """
    A cleanup function called when the test completes regardless of whether or
    not the test passed.
    """

    shlcommon.cleanup()
    