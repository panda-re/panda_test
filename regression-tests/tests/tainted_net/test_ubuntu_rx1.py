# test_ubuntu_rx1.py
# Run the first received packets tainted_net regression test.
#
# Created:  12-OCT-2018
# Changed:  16-OCT-2018   Adjust to Nathan's new way of dealing with stdout and
#                         stderr files.

import os
import re

import ptest

INDENT_SPACES = "                 "
TEST_PREFIX = "tainted_net_ubuntu_rx1"

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
REPLAY_PATH = os.path.join("ubuntuserver", "ubuntu_client")

STDOUT_NAME = TEST_PREFIX + ".stdout"
STDERR_NAME = TEST_PREFIX + ".stderr"
PLOG_NAME = TEST_PREFIX + ".plog"

REPLAY_TN = ptest.Replay(REPLAY_PATH, QEMU, TAINT2, TAINTED_NET, TAINTED_INSTR,
    plog=PLOG_NAME)

allOK = False

def run():
    """
    Execute the test and return true if the test passed.
    """

    global allOK
    
    # first, replay the recording
    retcode = REPLAY_TN.run()
    if (retcode != 0):
        print(INDENT_SPACES + "***** ERROR EXECUTING PANDA *****")
        REPLAY_TN.copy_stdout(STDOUT_NAME)
        REPLAY_TN.copy_stderr(STDERR_NAME)
        REPLAY_TN.dump_console(stdout=False, stderr=True)
        return False
    
    # now, check the results
    # the PLOG file should contain at least one callstack containing the address
    # 0x8048b05 (but note that PLOG uses decimal for all numbers, so 134515461)
    hexAddrS = "0x8048b05"                 # for ease of human readability
    decAddr = int(hexAddrS[2:], base=16)   # int also handles longs in Python 3
    foundOne = False
    with ptest.PlogReader(PLOG_NAME) as plr:
        for msgNo, msg in enumerate(plr):
            fieldInfoList = msg.ListFields()
            # for each item in list, item 0 is the FieldDescriptor, item 1 is
            # its value
            # not every message has the tainted_instr field of interest, so
            # HasField can't be used to find the messages of interest (it just
            # checks to see if the field has something in it, and will throw an
            # exception if the field doesn't even exist)
            for fieldInfo in fieldInfoList:
                if (fieldInfo[0].name == "tainted_instr"):
                    # the tainted_instr field is a message too, as is the
                    # call_stack field within tainted_instr
                    for curAddr in msg.tainted_instr.call_stack.addr:
                        if (curAddr == decAddr):
                            foundOne = True
                            break
    if (not foundOne):
        print(INDENT_SPACES + "FOUND NO CALLSTACKS WITH ADDRESS " + hexAddrS +
            " (" + str(decAddr) + ")")
        REPLAY_TN.copy_stdout(STDOUT_NAME)
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
         # won't have personal copies of stdout and stderr unless errored out
         os.remove(PLOG_NAME)
    else:
         print(INDENT_SPACES + STDOUT_NAME)
         print(INDENT_SPACES + STDERR_NAME)
         print(INDENT_SPACES + PLOG_NAME)
         print(INDENT_SPACES + "The above files have not been deleted in the " +
             "hope they will cue you in as to what went wrong.")
    