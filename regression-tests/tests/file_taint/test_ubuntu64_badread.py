# test_ubuntu64_badread.py
# Test the file_taint plugin using a 64-bit guest and a binary that reads a
# single file in a single process, and also tries a read that will fail.
#
# Created:  30-OCT-2019

import os

import ptest
import tempfile

import tests.file_taint.common as common

TESTDIR = os.path.dirname(__file__)

# this binary does the same thing as linux_singleproc_singlefile, but then also
# performs a read that will fail
REPLAY_PATH = os.path.join("ubuntuserver64", "linux64_badread")

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.X86_64, 2048, NETDEV, E1000DEV)

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="input1.bin")

TAINTED_BRANCH = ptest.Plugin("tainted_branch")

# this guest gets its OSI configuration from the default file in osi_linux

_, PLOG1 = tempfile.mkstemp()
REPLAY1 = ptest.Replay(REPLAY_PATH, QEMU, FILE_TAINT_INPUT1, TAINTED_BRANCH,
    os="linux-64-ubuntu:4.4.0-154-generic", plog=PLOG1)

TAINTED_PC = 0x400857

def run():
    # Try with a file that the binary was executed with
    retcode = REPLAY1.run()
    if retcode != 0:
        REPLAY1.dump_console(stdout=True, stderr=True)
        return False

    if not common.linux_checkplog(PLOG1, TAINTED_PC):
        return False

    # Now, verify that a warning was written out about sys_read returning an
    # error.
    stdout_file = REPLAY1.stdout()
    if ('file_taint linux_read_return_64: detected read failure, ignoring.' not
        in stdout_file.read()):
        print("expected warning about detected read failure")
        REPLAY1.dump_console(stdout=True)
        return False

    return True

def cleanup():
    pass
