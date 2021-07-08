import ptest
import tempfile
import re

import tests.file_taint.common as common

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000 = ptest.Device(ptest.Device.E1000, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 1024, NETDEV, E1000, vga=ptest.Qemu.CIRRUS)

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="input1.bin")

TAINTED_BRANCH = ptest.Plugin("tainted_branch")

_, PLOG1 = tempfile.mkstemp()
REPLAY1 = ptest.Replay("2k-filetaint-async", QEMU,
    FILE_TAINT_INPUT1, TAINTED_BRANCH, os="windows-32-2000", plog=PLOG1)

def run():
    # Try the first process
    retcode = REPLAY1.run()
    if retcode != 0:
        REPLAY1.dump_console(stdout=True, stderr=True)
        return False

    stdout = REPLAY1.stdout()
    matches = re.findall(r'^file_taint read return: detected async read return, ignoring$', stdout.read(), flags=re.MULTILINE)
    if len(matches) != 1:
        print("expected %d matches got $d\n", 1, len(matches))
        return False

    return True

def cleanup():
    pass
