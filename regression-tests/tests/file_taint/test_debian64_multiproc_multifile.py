# test_debian64_multiproc_multifile.py
# Test the file_taint plugin using a 64-bit guest and a binary that uses
# multiple processes to read different files.
#
# Created:  25-OCT-2019

import os

import ptest
import tempfile

import tests.file_taint.common as common

TESTDIR = os.path.dirname(__file__)
REPLAY_PATH = os.path.join("debian64", "linux64_mp_mf")

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

TABLET = ptest.Device(ptest.Device.USB_TABLET)

QEMU = ptest.Qemu(ptest.Qemu.X86_64, 2048, NETDEV, E1000DEV, TABLET,
    options="-usb")

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="input1.bin")
FILE_TAINT_INPUT2 = ptest.Plugin("file_taint", filename="input2.bin")
FILE_TAINT_INPUT3 = ptest.Plugin("file_taint", filename="should-not-be-tainted")

TAINTED_BRANCH = ptest.Plugin("tainted_branch")

CONF_NAME = os.path.join("shared_configs", "debian_kernelinfo.conf")
OSI = ptest.Plugin("osi")
OSI_LINUX = ptest.Plugin("osi_linux", kconf_file=CONF_NAME,
    kconf_group="debian4.9_amd64")

_, PLOG1 = tempfile.mkstemp()
REPLAY1 = ptest.Replay(REPLAY_PATH, QEMU, OSI, OSI_LINUX, FILE_TAINT_INPUT1,
    TAINTED_BRANCH, os="linux-64-.+", plog=PLOG1)
_, PLOG2 = tempfile.mkstemp()
REPLAY2 = ptest.Replay(REPLAY_PATH, QEMU, OSI, OSI_LINUX, FILE_TAINT_INPUT2,
    TAINTED_BRANCH, os="linux-64-.+", plog=PLOG2)
_, PLOG3 = tempfile.mkstemp()
REPLAY3 = ptest.Replay(REPLAY_PATH, QEMU, OSI, OSI_LINUX, FILE_TAINT_INPUT3,
    TAINTED_BRANCH, os="linux-64-.+", plog=PLOG3)

# due to ASLR, the 64-bit debian guest loads the binary into each process at a
# different base address, resulting in the tainted branch of interest being at
# a different location; the memorymap plugin and a little arithmetic can verify
# that these PCs identify the same block
PROC1_PC = 0x55E6F41B1930
PROC2_PC = 0x5609FB13E930

def run():
    # Try with a file that the binary was executed with in the first process
    retcode = REPLAY1.run()
    if retcode != 0:
        REPLAY1.dump_console(stdout=True, stderr=True)
        return False

    if not common.linux_checkplog(PLOG1, PROC1_PC):
        return False

    # Try the second process
    retcode = REPLAY2.run()
    if retcode != 0:
        REPLAY2.dump_console(stdout=True, stderr=True)
        return False
    if not common.linux_checkplog(PLOG2, PROC2_PC):
        return False

    # Try with a file we didn't open in either process
    retcode = REPLAY3.run()
    if retcode != 0:
        REPLAY3.dump_console(stdout=True, stderr=True)
        return False
    try:        
        if common.linux_checkplog(PLOG3, PROC1_PC):
            return False
    except:
        pass
    try:        
        if common.tainted_branch_in_plog(PLOG3):
            return False
    except:
        pass
    
    return True

def cleanup():
    pass
