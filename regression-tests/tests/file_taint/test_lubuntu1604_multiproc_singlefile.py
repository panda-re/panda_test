import os

import ptest
import re
import tempfile

import tests.file_taint.common as common

TESTDIR = os.path.dirname(__file__)

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
RTL8139 = ptest.Device(ptest.Device.RTL8139, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 2048, NETDEV, RTL8139, vga=ptest.Qemu.CIRRUS)

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="input1.bin")

TAINTED_BRANCH = ptest.Plugin("tainted_branch")

OSI = ptest.Plugin("osi")
OSI_LINUX = ptest.Plugin("osi_linux", kconf_file=os.path.join("shared_configs", "lubuntu_kernelinfo.conf"))

_, PLOG1 = tempfile.mkstemp()
REPLAY1 = ptest.Replay("lubuntu1604-filetaint-multiproc-singlefile", QEMU,
    OSI, OSI_LINUX, FILE_TAINT_INPUT1, TAINTED_BRANCH, os="linux-32-ubuntu-4.4.0-21-generic", plog=PLOG1)

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
                if m.pc == 0x804863E and m.HasField("tainted_branch"):
                    foundbb = True
    except:
        pass
    return foundbb

def cleanup():
    pass
