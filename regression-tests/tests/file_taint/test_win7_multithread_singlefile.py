import ptest
import tempfile

import tests.file_taint.common as common

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000 = ptest.Device(ptest.Device.E1000, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 2048, NETDEV, E1000, vga=ptest.Qemu.CIRRUS)

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="positional.bin")

TAINTED_BRANCH = ptest.Plugin("tainted_branch")

TAINT2 = ptest.Plugin("taint2", no_tp=True)

_, PLOG1 = tempfile.mkstemp()
REPLAY1 = ptest.Replay("7-filetaint-multithread-singlefile", QEMU,
    FILE_TAINT_INPUT1, TAINTED_BRANCH, TAINT2, os="windows-32-7", plog=PLOG1)

def run():
    retcode = REPLAY1.run()
    if retcode != 0:
        REPLAY1.dump_console()
        return False

    found_branches = { 0x401630: False, 0x40172E: False, 0x40182C: False }
    try:
        with ptest.PlogReader(PLOG1) as plr:
            for i, m in enumerate(plr):
                if m.pc in found_branches.keys() and m.HasField("tainted_branch"):
                    found_branches[m.pc] = True
    except Exception as e:
        print(e)
    for k in found_branches:
        if not found_branches[k]:
            print("expected 0x%X to be reported\n" % (k))
            return False

    return True

def cleanup():
    pass
