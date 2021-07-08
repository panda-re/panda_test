import ptest
import tempfile

import tests.file_taint.common as common

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000 = ptest.Device(ptest.Device.E1000, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 1024, NETDEV, E1000, vga=ptest.Qemu.CIRRUS)

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="multifile1.bin")
FILE_TAINT_INPUT2 = ptest.Plugin("file_taint", filename="multifile2.bin")

TAINTED_BRANCH = ptest.Plugin("tainted_branch")

_, PLOG1 = tempfile.mkstemp()
REPLAY1 = ptest.Replay("2k-filetaint-multifile-multiread", QEMU,
    FILE_TAINT_INPUT1, TAINTED_BRANCH, os="windows-32-2000", plog=PLOG1)
_, PLOG2 = tempfile.mkstemp()
REPLAY2 = ptest.Replay("2k-filetaint-multifile-multiread", QEMU,
    FILE_TAINT_INPUT2, TAINTED_BRANCH, os="windows-32-2000", plog=PLOG2)

def run():
    retcode = REPLAY1.run()
    if retcode != 0:
        REPLAY1.dump_console()
        return False

    found_branches = { 0x004017EF: False, 0x00401814: False }
    try:
        with ptest.PlogReader(PLOG1) as plr:
            for i, m in enumerate(plr):
                if (m.pc == 0x004017EF or m.pc == 0x00401814) and m.HasField("tainted_branch"):
                    found_branches[m.pc] = True
                if m.pc == 0x00401839 and m.HasField("tainted_branch"):
                    print("0x00401839 should not have been reported")
                    return False
    except Exception as e:
        print(e)
    for k in found_branches:
        if found_branches[k] == False:
            print("expected 0x%X to be reported" % (k))
            return False

    retcode = REPLAY2.run()
    if retcode != 0:
        REPLAY2.dump_console()
        return False

    found_branch = False
    try:
        with ptest.PlogReader(PLOG2) as plr:
            for i, m in enumerate(plr):
                if m.pc == 0x00401839 and m.HasField("tainted_branch"):
                    found_branch = True 
                if m.pc == 0x004017EF and m.HasField("tainted_branch"):
                    print("0x004017EF should not have been reported")
                    return False
                if m.pc == 0x00401814 and m.HasField("tainted_branch"):
                    print("0x00401814 should not have been reported")
                    return False
    except Exception as e:
        print(e)
    if not found_branch:
        print("expected 0x%X to be reported" % (0x00401839))
        return False

    return True

def cleanup():
    pass
