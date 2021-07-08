import ptest
import re
import tempfile

import tests.file_taint.common as common

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000 = ptest.Device(ptest.Device.E1000, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 1024, NETDEV, E1000, vga=ptest.Qemu.CIRRUS)

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="input1.bin")

TAINTED_BRANCH = ptest.Plugin("tainted_branch")

_, PLOG1 = tempfile.mkstemp()
REPLAY1 = ptest.Replay("2k-filetaint-multiproc-singlefile", QEMU,
    FILE_TAINT_INPUT1, TAINTED_BRANCH, os="windows-32-2000", plog=PLOG1)

def run():
    # Run the replay
    retcode = REPLAY1.run()
    if retcode != 0:
        REPLAY1.dump_console(stdout=True, stderr=True)
        return False

    # Verify that there were two instances where the file was tained by
    # examining stdout.
    stdout_file = REPLAY1.stdout()
    matches = re.findall(
        r'^\*{3} applying (?:positional|uniform) taint labels \d+\.\.\d+ to buffer @ \d+ \*{3}$',
        stdout_file.read(), flags=re.MULTILINE)
    if len(matches) != 2:
        print("expected %d matches got %d\n", 2, len(matches))
        return False
    # See if our basic block showed up in the pandalog
    foundbb = False
    try:
        with ptest.PlogReader(PLOG1) as plr:
            for i, m in enumerate(plr):
                if m.pc == 0x004016A8 and m.HasField("tainted_branch"):
                    foundbb = True
    except:
        pass
    return foundbb

def cleanup():
    pass
