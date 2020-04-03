import ptest
import tempfile

import tests.file_taint.common as common

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000 = ptest.Device(ptest.Device.E1000, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 1024, NETDEV, E1000, vga=ptest.Qemu.CIRRUS)

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="positional.bin",
    pos=True, max_num_labels=2)

TAINTED_BRANCH = ptest.Plugin("tainted_branch")

_, PLOG1 = tempfile.mkstemp()
REPLAY1 = ptest.Replay("2k-filetaint-positional", QEMU,
    FILE_TAINT_INPUT1, TAINTED_BRANCH, os="windows-32-2000", plog=PLOG1)

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
    if set(found_labels) != set([0, 1]) or (2 in found_labels or 3 in found_labels):
        print("expected the following labels: {}".format([0, 1]))
        return False

    return True

def cleanup():
    pass
