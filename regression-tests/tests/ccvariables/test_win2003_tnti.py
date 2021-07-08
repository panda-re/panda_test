# test_win2003_tnti.py
# Run a regression test using a Windows 2003 recording to look for the problem
# with inconsistent taint reports due to i386 condition code variable
# calculations done when entering or exiting cpu_exec (see ACE-22).
#
# Created:  06-MAY-2019
#

import datetime
import os

import ptest

INDENT_SPACES = "                 "
TEST_PREFIX = "win2003_tnti"

TAINTED_NET = ptest.Plugin("tainted_net", label_incoming_network=True)
TAINTED_INSTR = ptest.Plugin("tainted_instr")

# I believe these are the equivalent of "-net nic -net user"
NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

# darn Qemu won't let me specify 3G for guest memory like PANDA does
QEMU = ptest.Qemu(ptest.Qemu.I386, 3072, NETDEV, E1000DEV)

# use os.path.join so needn't worry about what the separator character is on
# this system
REPLAY_PATH = os.path.join("windows2003", "windows2003_client")

STDOUT_NAME = TEST_PREFIX + ".stdout"
STDERR_NAME = TEST_PREFIX + ".stderr"

REPLAY_TN = ptest.Replay(REPLAY_PATH, QEMU, TAINTED_NET, TAINTED_INSTR)

allOK = False

def ExtractTaintedInfo(fileName):
    """
    Return a dictionary mapping the address of each tainted block to the number
    of times a taint report for it occurred in the file.
    """

    taintedInfo = dict()
    with open(fileName, "r") as logFile:
        for line in logFile:
            line = line.strip()
            if (line.startswith("pc = 0x")):
                # extract the address portion without the hex specifier
                eqPos = line.index("=")
                addrHex = line[eqPos+4:]
                addrHex = addrHex.zfill(8)
                if (addrHex in taintedInfo):
                    taintedInfo[addrHex] = taintedInfo[addrHex] + 1
                else:
                    taintedInfo[addrHex] = 1
    
    return taintedInfo
    
def run():
    """
    Execute the test and return true if the test passed.
    """

    global allOK
    
    # really, the only sure way to verify the problem with i386 condition code
    # variables is fixed is to run with taint2_debug built in, and taint2: debug
    # on, so one can verify that a block was Stopped that calls a condition code
    # helper function that generates taint, and that the expected number of
    # taint reports are generated from the helper
    # but, as we don't run regression tests with taint2_debug built in, this is
    # the best we can do
    
    print(INDENT_SPACES +
        "This test takes about 5 minutes to run.  Started at:  " +
        str(datetime.datetime.now()))
        
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
    tbReports = ExtractTaintedInfo(STDOUT_NAME)
    expectedTaintReports = dict()
    expectFileName = os.path.join("tests", "ccvariables", TEST_PREFIX +
        "_tainted_info_expected.txt")
    try:
        with open(expectFileName, "r") as expectFile:
            for line in expectFile:
                line = line.strip()
                # first is the address, 8 hex characters with 0x prefix
                # then is the number of times it was reported
                addrHex = line[2:10]
                blockCountS = line[10:].strip()
                expectedTaintReports[addrHex] = int(blockCountS)
    except IOError:
        print(INDENT_SPACES + "ERROR READING " + expectFileName)
        REPLAY_TN.copy_stderr(STDERR_NAME)
        return False
    
    # yes, python lets you compare dictionaries for equality
    if (tbReports != expectedTaintReports):
        print(INDENT_SPACES + "TAINT REPORTS LIST NOT CORRECT")
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
    