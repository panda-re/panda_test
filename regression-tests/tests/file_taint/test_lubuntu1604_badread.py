# test_lubuntu1604_badread.py
# Test the file_taint plugin with a 32-bit guest and a binary which makes a
# failing call to sys_read.
#
# Created:  30-OCT-2019

import os

import ptest
import tempfile

import tests.file_taint.common as common

TESTDIR = os.path.dirname(__file__)

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
RTL8139 = ptest.Device(ptest.Device.RTL8139, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 2048, NETDEV, RTL8139, vga=ptest.Qemu.CIRRUS)

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="input1.bin")

TAINTED_BRANCH = ptest.Plugin("tainted_branch")

OSI = ptest.Plugin("osi")
OSI_LINUX = ptest.Plugin("osi_linux", kconf_file=os.path.join("shared_configs",
    "lubuntu_kernelinfo.conf"))

_, PLOG1 = tempfile.mkstemp()
# This recording is from 59% to 61% of the full recording (which takes a LONG
# time to replay) - but the binary of interest is only run within this little
# snippet.  The binary of interest is very similar to
# linux_singleproc_singlefile.elf.
REPLAY1 = ptest.Replay("lubuntu1604-filetaint-badread_59to61", QEMU, OSI, OSI_LINUX,
    FILE_TAINT_INPUT1, TAINTED_BRANCH, os="linux-32-ubuntu-4.4.0-21-generic", plog=PLOG1)

def run():
    # Replay normally, and check for the results from the first (working)
    # sys_read.
    retcode = REPLAY1.run()
    if retcode != 0:
        REPLAY1.dump_console(stdout=True, stderr=True)
        return False

    if not common.linux_checkplog(PLOG1, 0x0804866E):
        return False

    # Now, verify that a warning was written out about sys_read returning an
    # error.
    stdout_file = REPLAY1.stdout()
    if ('file_taint linux_read_return_32: detected read failure, ignoring.' not
        in stdout_file.read()):
        print("expected warning about detected read failure")
        REPLAY1.dump_console(stdout=True)
        return False
        
    return True

def cleanup():
    pass
