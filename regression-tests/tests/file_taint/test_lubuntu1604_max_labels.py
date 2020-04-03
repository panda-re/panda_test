import os

import ptest
import tempfile

import tests.file_taint.common as common

TESTDIR = os.path.dirname(__file__)

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
RTL8139 = ptest.Device(ptest.Device.RTL8139, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 2048, NETDEV, RTL8139, vga=ptest.Qemu.CIRRUS)

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="positional.bin",
    pos=True, max_num_labels=2)

TAINTED_BRANCH = ptest.Plugin("tainted_branch")

OSI = ptest.Plugin("osi")
OSI_LINUX = ptest.Plugin("osi_linux", kconf_file=os.path.join("shared_configs",
    "lubuntu_kernelinfo.conf"))

_, PLOG1 = tempfile.mkstemp()
REPLAY1 = ptest.Replay("lubuntu1604-filetaint-positional", QEMU, OSI, OSI_LINUX,
    FILE_TAINT_INPUT1, TAINTED_BRANCH, os="linux-32-ubuntu-4.4.0-21-generic", plog=PLOG1)

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
        print("expected branch not found")
        return False
    if set(found_labels) != set([0, 1]) or (2 in found_labels or 3 in found_labels):
        print("expected the following labels: {}".format([0, 1]))
        return False

    return True

def cleanup():
    pass
