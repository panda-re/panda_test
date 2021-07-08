# test_debian64_32bitbinary.py
# Test the file_taint plugin on a recording of a 32-bit binary taken in a 64-bit
# guest.
#
# Created:  25-OCT-2019

import os

import ptest
import tempfile

import tests.file_taint.common as common

TESTDIR = os.path.dirname(__file__)
REPLAY_PATH = os.path.join("debian64", "linux32bitbinary_sp_sf")

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
    # Try with a file that the binary was executed with
    retcode = REPLAY1.run()
    if retcode != 0:
        REPLAY1.dump_console(stdout=True, stderr=True)
        return False

    # But, as it is a 32-bit binary, none of the system calls that file_taint
    # needs should have been identified - instead there should be warnings in
    # the log about finding 32-bit system calls.
    stderr_file = REPLAY1.stderr()
    if ('32-bit system call (int 0x80) found in 64-bit replay - ignoring' not in stderr_file.read()):
        print("expected warnings about 32-bit system calls")
        return False
    
    # The plog should be empty, as none of the system calls related to the
    # input1.bin file should have been identified.
    try:
        if (common.tainted_branch_in_plog(PLOG1)):
            return False
    except:
        pass

    return True

def cleanup():
    pass
