# test_ubuntu64_singleproc_multifile.py
# Test the file_taint plugin using a 64-bit guest and a binary that opens
# different files in the same process.
#
# Created:  25-OCT-2019

import os

import ptest
import tempfile

import tests.file_taint.common as common

TESTDIR = os.path.dirname(__file__)
REPLAY_PATH = os.path.join("ubuntuserver64", "linux64_sp_mf")

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.X86_64, 2048, NETDEV, E1000DEV)

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="input1.bin")
FILE_TAINT_INPUT2 = ptest.Plugin("file_taint", filename="input2.bin")
FILE_TAINT_INPUT3 = ptest.Plugin("file_taint", filename="should-not-be-tainted")

TAINTED_BRANCH = ptest.Plugin("tainted_branch")

# this guest gets its OSI configuration from the default file in osi_linux

_, PLOG1 = tempfile.mkstemp()
REPLAY1 = ptest.Replay(REPLAY_PATH, QEMU, FILE_TAINT_INPUT1, TAINTED_BRANCH,
    os="linux-64-ubuntu:4.4.0-154-generic", plog=PLOG1)
_, PLOG2 = tempfile.mkstemp()
REPLAY2 = ptest.Replay(REPLAY_PATH, QEMU, FILE_TAINT_INPUT2, TAINTED_BRANCH,
    os="linux-64-ubuntu:4.4.0-154-generic", plog=PLOG2)
_, PLOG3 = tempfile.mkstemp()
REPLAY3 = ptest.Replay(REPLAY_PATH, QEMU, FILE_TAINT_INPUT3, TAINTED_BRANCH,
    os="linux-64-ubuntu:4.4.0-154-generic", plog=PLOG3)

TAINTED_PC = 0x400783

def run():
    # Try the first file
    retcode = REPLAY1.run()
    if retcode != 0:
        REPLAY1.dump_console(stdout=True,stderr=True)
        return False

    foundbb = False
    with ptest.PlogReader(PLOG1) as plr:
        for i, m in enumerate(plr):
            # This basic block should have a conditional branch instruction
            # that depends on tainted data.
            if m.pc == TAINTED_PC and m.HasField("tainted_branch"):
                foundbb = True
    if not foundbb:
        print("expected 0x%X to be reported in tainted branch" % (TAINTED_PC))
        return False

    # Try the second file
    retcode = REPLAY2.run()
    if retcode != 0:
        return False

    foundbb = False
    with ptest.PlogReader(PLOG2) as plr:
        for i, m in enumerate(plr):
            # This basic block should have a conditional branch instruction
            # that depends on tainted data.
            if m.pc == TAINTED_PC and m.HasField("tainted_branch"):
                foundbb = True
    if not foundbb:
        print("expected 0x%X to be reported in tainted branch" % (TAINTED_PC))
        return False

    # Try to taint a file that we didn't open. The plog file should be empty.
    retcode = REPLAY3.run()
    if retcode != 0:
        return False

    foundbb = False
    try:
        with ptest.PlogReader(PLOG3) as plr:
            for i, m in enumerate(plr):
                # This basic block should have a conditional branch instruction
                # that depends on tainted data (if we'd searched for the right
                # file)
                if m.pc == TAINTED_PC and m.HasField("tainted_branch"):
                    foundbb = True
    except:
        pass

    if foundbb:
        print("expected 0x%X not to be reported in tainted branch" % (TAINTED_PC))
        return False

    return True

def cleanup():
    pass
