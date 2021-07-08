# test_ubuntu64_multifile_multiread.py
# Test the file_taint plugin using a 64-bit guest and a binary that reads
# multiple files.
#
# Created:  25-OCT-2019

import os

import ptest
import tempfile

import tests.file_taint.common as common

TESTDIR = os.path.dirname(__file__)
REPLAY_PATH = os.path.join("ubuntuserver64", "linux64_mf_mr")

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.X86_64, 2048, NETDEV, E1000DEV)

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="multifile1.bin")
FILE_TAINT_INPUT2 = ptest.Plugin("file_taint", filename="multifile2.bin")

TAINTED_BRANCH = ptest.Plugin("tainted_branch")

# this guest gets its OSI configuration from the default file in osi_linux

_, PLOG1 = tempfile.mkstemp()
REPLAY1 = ptest.Replay(REPLAY_PATH, QEMU, FILE_TAINT_INPUT1, TAINTED_BRANCH,
    os="linux-64-ubuntu:4.4.0-154-generic", plog=PLOG1)
_, PLOG2 = tempfile.mkstemp()
REPLAY2 = ptest.Replay(REPLAY_PATH, QEMU, FILE_TAINT_INPUT2, TAINTED_BRANCH,
    os="linux-64-ubuntu:4.4.0-154-generic", plog=PLOG2)

BRANCH3_PC = 0x4008F9

def run():
    retcode = REPLAY1.run()
    if retcode != 0:
        REPLAY1.dump_console(stderr=True)
        return False

    found_branches = { 0x4008AD: False, 0x4008D9: False }
    try:
        with ptest.PlogReader(PLOG1) as plr:
            for i, m in enumerate(plr):
                if (m.pc in found_branches.keys()) and m.HasField("tainted_branch"):
                    found_branches[m.pc] = True
                if m.pc == BRANCH3_PC and m.HasField("tainted_branch"):
                    print("0x%X should not have been reported" % (BRANCH3_PC))
                    return False
    except Exception as e:
        print(e)
    for k in found_branches:
        if found_branches[k] == False:
            print("expected 0x%X to be reported" % (k))
            return False

    retcode = REPLAY2.run()
    if retcode != 0:
        REPLAY2.dump_console(stderr=True)
        return False

    found_branch = False
    try:
        with ptest.PlogReader(PLOG2) as plr:
            for i, m in enumerate(plr):
                if m.pc == BRANCH3_PC and m.HasField("tainted_branch"):
                    found_branch = True 
                if m.pc in found_branches.keys() and m.HasField("tainted_branch"):
                    print("0x%X should not have been reported" % (m.pc))
                    return False
    except Exception as e:
        print(e)
    if not found_branch:
        print("expected 0x%X to be reported" % (BRANCH3_PC))
        return False

    return True

def cleanup():
    pass
