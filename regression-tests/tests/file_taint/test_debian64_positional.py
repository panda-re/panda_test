# test_debian64_positional.py
# Test the file_taint plugin start and ending positional options using a 64-bit
# guest.
#
# Created:  25-OCT-2019

import os

import ptest
import tempfile

import tests.file_taint.common as common

TESTDIR = os.path.dirname(__file__)
REPLAY_PATH = os.path.join("debian64", "linux64_positional")

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

TABLET = ptest.Device(ptest.Device.USB_TABLET)

QEMU = ptest.Qemu(ptest.Qemu.X86_64, 2048, NETDEV, E1000DEV, TABLET,
    options="-usb")

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="positional.bin",
    pos=True, start=0, end=3)
FILE_TAINT_INPUT2 = ptest.Plugin("file_taint", filename="positional.bin",
    pos=True, start=4, end=7)
FILE_TAINT_INPUT3 = ptest.Plugin("file_taint", filename="positional.bin",
    pos=True, start=8, end=11)

TAINTED_BRANCH = ptest.Plugin("tainted_branch")

CONF_NAME = os.path.join("shared_configs", "debian_kernelinfo.conf")
OSI = ptest.Plugin("osi")
OSI_LINUX = ptest.Plugin("osi_linux", kconf_file=CONF_NAME,
    kconf_group="debian4.9_amd64")

_, PLOG1 = tempfile.mkstemp()
REPLAY1 = ptest.Replay(REPLAY_PATH, QEMU, OSI, OSI_LINUX, FILE_TAINT_INPUT1,
    TAINTED_BRANCH, os="linux-64-.+", plog=PLOG1)
_, PLOG2 = tempfile.mkstemp()
REPLAY2 = ptest.Replay(REPLAY_PATH, QEMU, OSI, OSI_LINUX, FILE_TAINT_INPUT2,
    TAINTED_BRANCH, os="linux-64-.+", plog=PLOG2)
_, PLOG3 = tempfile.mkstemp()
REPLAY3 = ptest.Replay(REPLAY_PATH, QEMU, OSI, OSI_LINUX, FILE_TAINT_INPUT3,
    TAINTED_BRANCH, os="linux-64-.+", plog=PLOG3)

# block where compare with 0x1234
TAINTED_PC1 = 0x55CE0E42A983

# block where compare with 0x2345
TAINTED_PC2 = 0x55CE0E42A9B3

# block where compare with 0x3456
TAINTED_PC3 = 0x55CE0E42A9D7

def run():
    retcode = REPLAY1.run()
    if retcode != 0:
        REPLAY1.dump_console(stderr=True)
        return False

    found_branch = False
    found_labels = []
    try:
        with ptest.PlogReader(PLOG1) as plr:
            for i, m in enumerate(plr):
                if m.HasField("tainted_branch"):
                    for tq in m.tainted_branch.taint_query:
                        found_labels += tq.unique_label_set.label
                if m.pc == TAINTED_PC1 and m.HasField("tainted_branch"):
                    found_branch = True
                if m.pc == TAINTED_PC2 and m.HasField("tainted_branch"):
                    print("0x%X should not have been reported" % (TAINTED_PC2))
                    return False
                if m.pc == TAINTED_PC3 and m.HasField("tainted_branch"):
                    print("0x%X should not have been reported" % (TAINTED_PC3))
                    return False
    except:
        print("error")
    if not found_branch:
        print("expected branch at 0x%X not found" % TAINTED_PC1)
        return False
    if set(found_labels) != set([0, 1, 2, 3]):
        print("expected the following labels: {}".format([0, 1, 2, 3]))
        return False

    retcode = REPLAY2.run()
    if retcode != 0:
        REPLAY2.dump_console(stderr=True)
        return False

    found_branch = False
    found_labels = []
    try:
        with ptest.PlogReader(PLOG2) as plr:
            for i, m in enumerate(plr):
                if m.HasField("tainted_branch"):
                    for tq in m.tainted_branch.taint_query:
                        found_labels += tq.unique_label_set.label
                if m.pc == TAINTED_PC2 and m.HasField("tainted_branch"):
                    found_branch = True
                if m.pc == TAINTED_PC1 and m.HasField("tainted_branch"):
                    print("0x%X should not have been reported" % (TAINTED_PC1))
                    return False
                if m.pc == TAINTED_PC3 and m.HasField("tainted_branch"):
                    print("0x%X should not have been reported" % (TAINTED_PC3))
                    return False
    except:
        pass
    if not found_branch:
        print("expected branch at 0x%X not found" % (TAINTED_PC2))
        return False
    if set(found_labels) != set([4, 5, 6, 7]):
        print("expected the following labels: {}".format([4, 5, 6, 7]))
        return False

    retcode = REPLAY3.run()
    if retcode != 0:
        REPLAY3.dump_console(stderr=True)
        return False

    found_branch = False
    found_labels = []
    try:
        with ptest.PlogReader(PLOG3) as plr:
            for i, m in enumerate(plr):
                if m.HasField("tainted_branch"):
                    for tq in m.tainted_branch.taint_query:
                        found_labels += tq.unique_label_set.label
                if m.pc == TAINTED_PC3 and m.HasField("tainted_branch"):
                    found_branch = True
                if m.pc == TAINTED_PC1 and m.HasField("tainted_branch"):
                    print("0x%X should not have been reported" % (TAINTED_PC1))
                    return False
                if m.pc == TAINTED_PC2 and m.HasField("tainted_branch"):
                    print("0x%X should not have been reported" % (TAINTED_PC2))
                    return False
    except:
        pass
    if not found_branch:
        print("expected branch at 0x%X not found" % (TAINTED_PC3))
        return False
    if set(found_labels) != set([8, 9, 10, 11]):
        print("expected the following labels: {}".format([8, 9, 10, 11]))
        return False
    
    return True

def cleanup():
    pass
