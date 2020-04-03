import ptest
import tempfile

import tests.file_taint.common as common

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000 = ptest.Device(ptest.Device.E1000, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 2048, NETDEV, E1000, vga=ptest.Qemu.CIRRUS)

TAINT2 = ptest.Plugin("taint2", no_tp=True)

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="positional.bin",
    pos=True, start=0, end=3)
FILE_TAINT_INPUT2 = ptest.Plugin("file_taint", filename="positional.bin",
    pos=True, start=4, end=7)
FILE_TAINT_INPUT3 = ptest.Plugin("file_taint", filename="positional.bin",
    pos=True, start=8, end=11)

TAINTED_BRANCH = ptest.Plugin("tainted_branch")

_, PLOG1 = tempfile.mkstemp()
REPLAY1 = ptest.Replay("7-filetaint-positional", QEMU,
    FILE_TAINT_INPUT1, TAINTED_BRANCH, TAINT2, os="windows-32-7", plog=PLOG1)
_, PLOG2 = tempfile.mkstemp()
REPLAY2 = ptest.Replay("7-filetaint-positional", QEMU,
    FILE_TAINT_INPUT2, TAINTED_BRANCH, TAINT2, os="windows-32-7", plog=PLOG2)
_, PLOG3 = tempfile.mkstemp()
REPLAY3 = ptest.Replay("7-filetaint-positional", QEMU,
    FILE_TAINT_INPUT3, TAINTED_BRANCH, TAINT2, os="windows-32-7", plog=PLOG3)

def run():
    retcode = REPLAY1.run()
    if retcode != 0:
        REPLAY1.dump_console()
        return False

    found_branch = False
    found_labels = []
    try:
        with ptest.PlogReader(PLOG1) as plr:
            for i, m in enumerate(plr):
                if m.HasField("tainted_branch"):
                    for tq in m.tainted_branch.taint_query:
                        found_labels += tq.unique_label_set.label
                if m.pc == 0x00401790 and m.HasField("tainted_branch"):
                    found_branch = True
                if m.pc == 0x004017B5 and m.HasField("tainted_branch"):
                    print("0x004017B5 should not have been reported")
                    return False
                if m.pc == 0x004017DA and m.HasField("tainted_branch"):
                    print("0x004017DA should not have been reported")
                    return False
    except:
        print("error")
    if not found_branch:
        print("expected branch not found")
        return False
    if set(found_labels) != set([0, 1, 2, 3]):
        print("expected the following labels: {}".format([0, 1, 2, 3]))
        return False

    retcode = REPLAY2.run()
    if retcode != 0:
        REPLAY2.dump_console()
        return False

    found_branch = False
    found_labels = []
    try:
        with ptest.PlogReader(PLOG2) as plr:
            for i, m in enumerate(plr):
                if m.HasField("tainted_branch"):
                    for tq in m.tainted_branch.taint_query:
                        found_labels += tq.unique_label_set.label
                if m.pc == 0x004017B5 and m.HasField("tainted_branch"):
                    found_branch = True
                if m.pc == 0x00401790 and m.HasField("tainted_branch"):
                    print("0x00401790 should not have been reported")
                    return False
                if m.pc == 0x004017DA and m.HasField("tainted_branch"):
                    print("0x004017DA should not have been reported")
                    return False
    except:
        pass
    if not found_branch:
        print("expected branch not found")
        return False
    if set(found_labels) != set([4, 5, 6, 7]):
        print("expected the following labels: {}".format([4, 5, 6, 7]))
        return False

    retcode = REPLAY3.run()
    if retcode != 0:
        REPLAY3.dump_console()
        return False

    found_branch = False
    found_labels = []
    try:
        with ptest.PlogReader(PLOG3) as plr:
            for i, m in enumerate(plr):
                if m.HasField("tainted_branch"):
                    for tq in m.tainted_branch.taint_query:
                        found_labels += tq.unique_label_set.label
                if m.pc == 0x004017DA and m.HasField("tainted_branch"):
                    found_branch = True
                if m.pc == 0x004017B5 and m.HasField("tainted_branch"):
                    print("0x004017B5 should not have been reported")
                    return False
                if m.pc == 0x00401790 and m.HasField("tainted_branch"):
                    print("0x00401790 should not have been reported")
                    return False
    except:
        pass
    if not found_branch:
        print("expected branch not found")
        return False
    if set(found_labels) != set([8, 9, 10, 11]):
        print("expected the following labels: {}".format([8, 9, 10, 11]))
        return False

    return True

def cleanup():
    pass
