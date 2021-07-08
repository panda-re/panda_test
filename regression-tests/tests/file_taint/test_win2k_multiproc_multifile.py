import ptest
import tempfile

import tests.file_taint.common as common

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
RTL8139 = ptest.Device(ptest.Device.RTL8139, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 1024, NETDEV, RTL8139, vga=ptest.Qemu.CIRRUS)

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="input1.bin")
FILE_TAINT_INPUT2 = ptest.Plugin("file_taint", filename="input2.bin")
FILE_TAINT_INPUT3 = ptest.Plugin("file_taint", filename="should-not-be-tainted")

TAINTED_BRANCH = ptest.Plugin("tainted_branch")

_, PLOG1 = tempfile.mkstemp()
REPLAY1 = ptest.Replay("2k-filetaint-multiproc-multifile", QEMU,
    FILE_TAINT_INPUT1, TAINTED_BRANCH, os="windows-32-2000", plog=PLOG1)
_, PLOG2 = tempfile.mkstemp()
REPLAY2 = ptest.Replay("2k-filetaint-multiproc-multifile", QEMU,
    FILE_TAINT_INPUT2, TAINTED_BRANCH, os="windows-32-2000", plog=PLOG2)
_, PLOG3 = tempfile.mkstemp()
REPLAY3 = ptest.Replay("2k-filetaint-multiproc-multifile", QEMU,
    FILE_TAINT_INPUT3, TAINTED_BRANCH, os="windows-32-2000", plog=PLOG2)

def run():
    # Try the first process
    retcode = REPLAY1.run()
    if retcode != 0:
        return False

    if not common.win_checkplog(PLOG1):
        return False

    # Try the second process
    retcode = REPLAY2.run()
    if retcode != 0:
        return False
    if not common.win_checkplog(PLOG2):
        return False

    # Try to taint a file that we didn't open. The plog file should be empty.
    retcode = REPLAY3.run()
    if retcode != 0:
        return False
    try:
        common.win_checkplog(PLOG3)
        return False
    except:
        pass

    return True

def cleanup():
    pass
