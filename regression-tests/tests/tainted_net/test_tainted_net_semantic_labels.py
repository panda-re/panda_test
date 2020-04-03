# test_tainted_net_ace.py

import os
import re

import ptest

INDENT_SPACES = "                 "
TEST_PREFIX = "tainted_net_semantic_labels"

TAINTED_NET = ptest.Plugin("tainted_net", label_incoming_network=True, semantic=True, packets="84", bytes="1-3:5", ip_proto="6", ip_src="192.168.100.1", ip_dst="192.168.100.60", eth_type="0x0800")

# I believe these are the equivalent of "-net nic -net user"
NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 1024, NETDEV, E1000DEV, vga="cirrus")

# use os.path.join so needn't worry about what the separator character is on
# this system
REPLAY_PATH = "test_tainted_net_semantic_labels"

STDOUT_NAME = TEST_PREFIX + ".stdout"
STDERR_NAME = TEST_PREFIX + ".stderr"
IDA_TAINT_FILE = "ida_taint2.csv"
IDA_TAINT_SEMANTIC_LABELS_FILE = "ida_taint2.csv.semantic_labels"

def remove_file(filename):
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass

remove_file(STDOUT_NAME)
remove_file(STDERR_NAME)
remove_file(IDA_TAINT_FILE)
remove_file(IDA_TAINT_SEMANTIC_LABELS_FILE)

REPLAY_TN = ptest.Replay(REPLAY_PATH, QEMU, TAINTED_NET, os="linux-32-redhat:2.4.18-14")

allOK = False

SEMANTIC_LABELS_FILE_EXPECTED_CONTENTS = [ \
    "1,84-1", \
    "2,84-2", \
    "3,84-3", \
    "4,84-5"  \
     ]

IDA_TAINT_FILE_EXPECTED_CONTENTS = [ \
    "process name,pid,pc,label", \
    "(kernel),0,0xf88cd489,1", \
    "(kernel),0,0xf88cd489,2", \
    "(kernel),0,0xf88cd489,3", \
    "(kernel),0,0xf88cd489,4", \
    "(kernel),0,0xc01f97fd,1", \
    "(kernel),0,0xc01f97fd,2", \
    "(kernel),0,0xc01f97fd,3", \
    "(kernel),0,0xc01f97fd,4", \
    "(kernel),0,0xc01f97ff,4"  \
    ]

def verify_file(file_name, expected):
    i = 0
    with open(file_name) as f:
        for line in f:
            if (i == len(expected)):
                print ("File: " + file_name)
                print ("Expected: " + str(len(expected)) + " lines")
                print ("Got: >" + str(i) + " lines")
                return False
            if(line.strip() != expected[i]):
                print ("File: " + file_name)
                print ("Line: " + str(i+1))
                print ("Expected: " + expected[i])
                print ("Got: " + line.strip())
                return False
            i+=1
    if (i != len(expected)):
        print ("File: " + file_name)
        print ("Expected " + str(len(expected)) + " lines")
        print ("Got " + str(i) + " lines")
        return False
    return True

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

    if (not verify_file(IDA_TAINT_SEMANTIC_LABELS_FILE, SEMANTIC_LABELS_FILE_EXPECTED_CONTENTS) or not verify_file(IDA_TAINT_FILE, IDA_TAINT_FILE_EXPECTED_CONTENTS)):
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
        remove_file(IDA_TAINT_FILE)
        remove_file(IDA_TAINT_SEMANTIC_LABELS_FILE)
    else:
        print(INDENT_SPACES + STDOUT_NAME)
        print(INDENT_SPACES + STDERR_NAME)
        print(INDENT_SPACES + IDA_TAINT_FILE)
        print(INDENT_SPACES + IDA_TAINT_SEMANTIC_LABELS_FILE)
        print(INDENT_SPACES + "The above files have not been deleted in the " +
            "hope they will cue you in as to what went wrong.")
    
