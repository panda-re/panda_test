import os

import ptest
import tempfile

import tests.file_taint.common as common

TESTDIR = os.path.dirname(__file__)

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
RTL8139 = ptest.Device(ptest.Device.RTL8139, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 2048, NETDEV, RTL8139, vga=ptest.Qemu.CIRRUS)

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="positional.bin",
    pos=True, start=0, end=3)
FILE_TAINT_INPUT2 = ptest.Plugin("file_taint", filename="positional.bin",
    pos=True, start=4, end=7)
FILE_TAINT_INPUT3 = ptest.Plugin("file_taint", filename="positional.bin",
    pos=True, start=8, end=11)

TAINTED_BRANCH = ptest.Plugin("tainted_branch")

OSI = ptest.Plugin("osi")
OSI_LINUX = ptest.Plugin("osi_linux", kconf_file=os.path.join("shared_configs",
    "lubuntu_kernelinfo.conf"))

_, PLOG1 = tempfile.mkstemp()
REPLAY1 = ptest.Replay("lubuntu1604-filetaint-positional", QEMU, OSI, OSI_LINUX,
    FILE_TAINT_INPUT1, TAINTED_BRANCH, os="linux-32-ubuntu-4.4.0-21-generic", plog=PLOG1)
_, PLOG2 = tempfile.mkstemp()
REPLAY2 = ptest.Replay("lubuntu1604-filetaint-positional", QEMU, OSI, OSI_LINUX,
    FILE_TAINT_INPUT2, TAINTED_BRANCH, os="linux-32-ubuntu-4.4.0-21-generic", plog=PLOG2)
_, PLOG3 = tempfile.mkstemp()
REPLAY3 = ptest.Replay("lubuntu1604-filetaint-positional", QEMU, OSI, OSI_LINUX,
    FILE_TAINT_INPUT3, TAINTED_BRANCH, os="linux-32-ubuntu-4.4.0-21-generic", plog=PLOG3)

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
                if m.pc == 0x080486C3 and m.HasField("tainted_branch"):
                    found_branch = True
                if m.pc == 0x080486EF and m.HasField("tainted_branch"):
                    print("0x080486EF should not have been reported")
                    return False
                if m.pc == 0x0804871B and m.HasField("tainted_branch"):
                    print("0x0804871B should not have been reported")
                    return False
    except:
        print("error")
    if not found_branch:
        print("expected branch at 0x080486C3 not found")
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
                if m.pc == 0x080486EF and m.HasField("tainted_branch"):
                    found_branch = True
                if m.pc == 0x080486C3 and m.HasField("tainted_branch"):
                    print("0x080486C3 should not have been reported")
                    return False
                if m.pc == 0x0804871B and m.HasField("tainted_branch"):
                    print("0x0804871B should not have been reported")
                    return False
    except:
        pass
    if not found_branch:
        print("expected branch at 0x080486EF not found")
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
                if m.pc == 0x0804871B and m.HasField("tainted_branch"):
                    found_branch = True
                if m.pc == 0x080486C3 and m.HasField("tainted_branch"):
                    print("0x080486C3 should not have been reported")
                    return False
                if m.pc == 0x080486EF and m.HasField("tainted_branch"):
                    print("0x080486EF should not have been reported")
                    return False
    except:
        pass
    if not found_branch:
        print("expected branch at 0x0804871B not found")
        return False
    if set(found_labels) != set([8, 9, 10, 11]):
        print("expected the following labels: {}".format([8, 9, 10, 11]))
        return False

    return True

def cleanup():
    pass
