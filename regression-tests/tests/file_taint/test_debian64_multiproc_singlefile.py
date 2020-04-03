# test_debian64_multiproc_singlefile.py
# Test the file_taint plugin using a 64-bit guest and a binary that opens the
# same file in multiple processes.
#
# Created:  25-OCT-2019

import os

import ptest
import re
import tempfile

import tests.file_taint.common as common

TESTDIR = os.path.dirname(__file__)
REPLAY_PATH = os.path.join("debian64", "linux64_mp_sf")

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

TABLET = ptest.Device(ptest.Device.USB_TABLET)

QEMU = ptest.Qemu(ptest.Qemu.X86_64, 2048, NETDEV, E1000DEV, TABLET,
    options="-usb")

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="input1.bin")

TAINTED_BRANCH = ptest.Plugin("tainted_branch")

CONF_NAME = os.path.join("shared_configs", "debian_kernelinfo.conf")
OSI = ptest.Plugin("osi")
OSI_LINUX = ptest.Plugin("osi_linux", kconf_file=CONF_NAME,
    kconf_group="debian4.9_amd64")

_, PLOG1 = tempfile.mkstemp()
REPLAY1 = ptest.Replay(REPLAY_PATH, QEMU, OSI, OSI_LINUX, FILE_TAINT_INPUT1,
    TAINTED_BRANCH, os="linux-64-.+", plog=PLOG1)

def run():
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
    # Due to ASLR in the debian guest, the PC for the same block from each
    # process will be at different locations (you can verify using memorymap
    # that the image base is different in the two processes)
    found_branches = { 0x557041C7F930:False, 0x557509E09930:False }
    try:
        with ptest.PlogReader(PLOG1) as plr:
            for i, m in enumerate(plr):
                if (m.pc in found_branches.keys()) and m.HasField("tainted_branch"):
                    found_branches[m.pc] = True
    except:
        pass
    for k in found_branches:
        if (False == found_branches[k]):
            print("expected 0x%X to be reported" % (k))
            return False

    return True

def cleanup():
    pass
