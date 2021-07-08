import os

import ptest
import tempfile

import tests.file_taint.common as common

TESTDIR = os.path.dirname(__file__)

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
RTL8139 = ptest.Device(ptest.Device.RTL8139, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 2048, NETDEV, RTL8139, vga=ptest.Qemu.CIRRUS)

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="multifile1.bin")
FILE_TAINT_INPUT2 = ptest.Plugin("file_taint", filename="multifile2.bin")

TAINTED_BRANCH = ptest.Plugin("tainted_branch")

OSI = ptest.Plugin("osi")
OSI_LINUX = ptest.Plugin("osi_linux", kconf_file=os.path.join("shared_configs",
    "lubuntu_kernelinfo.conf"))

_, PLOG1 = tempfile.mkstemp()
REPLAY1 = ptest.Replay("lubuntu1604-filetaint-multifile-multiread", QEMU, OSI, OSI_LINUX,
    FILE_TAINT_INPUT1, TAINTED_BRANCH, os="linux-32-ubuntu-4.4.0-21-generic", plog=PLOG1)
_, PLOG2 = tempfile.mkstemp()
REPLAY2 = ptest.Replay("lubuntu1604-filetaint-multifile-multiread", QEMU, OSI, OSI_LINUX,
    FILE_TAINT_INPUT2, TAINTED_BRANCH, os="linux-32-ubuntu-4.4.0-21-generic", plog=PLOG2)

def run():
    retcode = REPLAY1.run()
    if retcode != 0:
        REPLAY1.dump_console(stderr=True)
        return False

    found_branches = { 0x080486F3: False, 0x0804871F: False }
    try:
        with ptest.PlogReader(PLOG1) as plr:
            for i, m in enumerate(plr):
                if (m.pc in found_branches.keys()) and m.HasField("tainted_branch"):
                    found_branches[m.pc] = True
                if m.pc == 0x0804874B and m.HasField("tainted_branch"):
                    print("0x0804874B should not have been reported")
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
                if m.pc == 0x0804874B and m.HasField("tainted_branch"):
                    found_branch = True 
                if m.pc in found_branches.keys() and m.HasField("tainted_branch"):
                    print("0x%X should not have been reported" % (m.pc))
                    return False
    except Exception as e:
        print(e)
    if not found_branch:
        print("expected 0x%X to be reported" % (0x0804874B))
        return False

    return True

def cleanup():
    pass
