# test_ubuntu_rx2.py
# Run the second received packets tainted_net regression test.
#
# Created:  12-OCT-2018
# Changed:  16-OCT-2018   Adjust to new stdout/stderr file handling framework.
# Changed:  27-FEB-2019   Verify all the taint reports, now that the problem
#                         with inconsistent taint reports (ACE-22) is fixed.

import os
import re

import ptest

INDENT_SPACES = "                 "
TEST_PREFIX = "tainted_net_ubuntu_rx2"

TAINT2 = ptest.Plugin("taint2", detaint_cb0=True)
TAINTED_NET = ptest.Plugin("tainted_net", label_incoming_network=True)
TAINTED_INSTR = ptest.Plugin("tainted_instr")

# I believe these are the equivalent of "-net nic -net user"
NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

# darn Qemu won't let me specify 2G for guest memory like PANDA does
QEMU = ptest.Qemu(ptest.Qemu.I386, 2048, NETDEV, E1000DEV)

# use os.path.join so needn't worry about what the separator character is on
# this system
REPLAY_PATH = os.path.join("ubuntuserver", "ubuntu_client2")

STDOUT_NAME = TEST_PREFIX + ".stdout"
STDERR_NAME = TEST_PREFIX + ".stderr"

REPLAY_TN = ptest.Replay(REPLAY_PATH, QEMU, TAINT2, TAINTED_NET, TAINTED_INSTR)

allOK = False

def ExtractTaintedBlocks(fileName, searchPattern):
    """
    Return a set of the reports on the tainted blocks whose reports
    (in lower-case hex) match the pattern provided.  A "report" is a line that
    looks like "pc = 0x" and then some hex number.
    """

    taintedBlocks = set()
    with open(fileName, "r") as logFile:
        for line in logFile:
            line = line.strip()
            matchObj = re.search(searchPattern, line)
            if (matchObj != None):
                if (line not in taintedBlocks):
                    taintedBlocks.add(line)
    
    return taintedBlocks
    
def run():
    """
    Execute the test and return true if the test passed.
    """

    global allOK
    
    # first, replay the recording
    retcode = REPLAY_TN.run()
    
    # always need stdout, even on success
    REPLAY_TN.copy_stdout(STDOUT_NAME)
    if (retcode != 0):
        print(INDENT_SPACES + "***** ERROR EXECUTING PANDA *****")
        REPLAY_TN.copy_stderr(STDERR_NAME)
        RELPLAY_TN.dump_console(stdout=False, stderr=True)
        return False
    
    # now, check the results
    tbReports = ExtractTaintedBlocks(STDOUT_NAME, "pc = 0x")
    expectedTaintedBlocks = set()
    expectFileName = os.path.join("tests", "tainted_net", TEST_PREFIX +
        "_tainted_blocks_expected.txt")
    try:
        with open(expectFileName, "r") as expectFile:
            for line in expectFile:
                line = line.strip()
                expectedTaintedBlocks.add(line)
    except IOError:
        print(INDENT_SPACES + "ERROR READING " + expectFileName)
        REPLAY_TN.copy_stderr(STDERR_NAME)
        return False
        
    if (tbReports != expectedTaintedBlocks):
        print(INDENT_SPACES + "TAINTED BLOCKS LIST NOT CORRECT")
        # the expected results file is expected to already be sorted
        print(INDENT_SPACES + "Expected:" + str(expectedTaintedBlocks))
        print(INDENT_SPACES + "Got:" + str(sorted(tbReports)))
        REPLAY_TN.copy_stderr(STDERR_NAME)
        return False
    
    allOK = True
    return True
    
def cleanup():
    """
    A cleanup function called when the test completes regardless of whether or
    not the test passed.
    """
    
    global allOK

    if (allOK):
         os.remove(STDOUT_NAME)
         # framework will delete stderr temporary file
    else:
         print(INDENT_SPACES + STDOUT_NAME)
         print(INDENT_SPACES + STDERR_NAME)
         print(INDENT_SPACES + "The above files have not been deleted in the " +
             "hope they will cue you in as to what went wrong.")
    