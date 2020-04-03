# test_ubuntu_tx.py
# Run the transmitted packets tainted_net regression test.
#
# Created:  10-OCT-2018
# Changed:  16-OCT-2018   Adjust to new stdout/stderr file handling framework.

import os
import re

import ptest

INDENT_SPACES = "                 "
STRING_MATCHES_SUFFIX = "_string_matches.txt"
TEST_PREFIX = "tainted_net_ubuntu_tx"

TAINT2 = ptest.Plugin("taint2", detaint_cb0=True)
STRINGSEARCH = ptest.Plugin("stringsearch", str="quick")
TSTRINGSEARCH = ptest.Plugin("tstringsearch")
TAINTED_NET = ptest.Plugin("tainted_net", query_outgoing_network=True, file=TEST_PREFIX + ".csv")

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

REPLAY_TN = ptest.Replay(REPLAY_PATH, QEMU, TAINT2, STRINGSEARCH, TSTRINGSEARCH,
    TAINTED_NET)

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
    # the only lines in the csv file that don't contain "NULL" should be the
    # column headers, and consecutive lines whose Datum spell out quick and have
    # a taint of 10 (ie, first line ends with "q, 10", second ends "u, 10", etc)
    status = 0                       # haven't started matching quick yet
    try:
        with open(TEST_PREFIX + ".csv", "r") as csvFile:
            for line in csvFile:
                line = line.strip()
                # the header is "Address","Datum","Labels"
                if (not (", NULL" in line) and not ("Datum" in line)):
                    if (status == 0):
                        if (line.endswith(",q, 10")):
                            status = 1
                        else:
                            status = -1
                    elif (status == 1):
                        if (line.endswith(",u, 10")):
                            status = 2
                        else:
                            status = -1
                    elif (status == 2):
                        if (line.endswith(",i, 10")):
                            status = 3
                        else:
                            status = -1
                    elif (status == 3):
                        if (line.endswith(",c, 10")):
                            status = 4
                        else:
                            status = -1
                    elif (status == 4):
                        if (line.endswith(",k, 10")):
                            status = 5
                        else:
                            status = -1
                    else:
                        status = -1
    except IOError:
        print(INDENT_SPACES + "***** ERROR READING " + TEST_PREFIX +
            ".csv *****")
        REPLAY_TN.copy_stdout(STDOUT_NAME)
        REPLAY_TN.copy_stderr(STDERR_NAME)
        return False
        
    if (status != 5):
        print(INDENT_SPACES + "WRONG OR MISSING TAINTED DATA")
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
         # the framework will delete the temporary stdout & stderr files
         os.remove(STRING_MATCHES_SUFFIX)
         os.remove(TEST_PREFIX + ".csv")
    else:
         print(INDENT_SPACES + STDOUT_NAME)
         print(INDENT_SPACES + STDERR_NAME)
         print(INDENT_SPACES + STRING_MATCHES_SUFFIX)
         print(INDENT_SPACES + TEST_PREFIX + ".csv")
         print(INDENT_SPACES + "The above files have not been deleted in the " +
             "hope they will cue you in as to what went wrong.")
    