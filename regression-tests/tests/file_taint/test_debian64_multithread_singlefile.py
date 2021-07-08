# test_debian64_multithread_singlefile.py
# Test the file_taint plugin using a 64-bit guest and a binary that opens the
# same file in 3 different threads.
#
# Created:  25-OCT-2019

import os

import ptest
import tempfile

import tests.file_taint.common as common

TESTDIR = os.path.dirname(__file__)
REPLAY_PATH = os.path.join("debian64", "linux64_mt_sf")

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

TABLET = ptest.Device(ptest.Device.USB_TABLET)

QEMU = ptest.Qemu(ptest.Qemu.X86_64, 2048, NETDEV, E1000DEV, TABLET,
    options="-usb")

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="positional.bin")

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
        REPLAY1.dump_console()
        return False

    # these 3 PCs are the addresses of the blocks in process_value1,
    # process_value2 and process_value3 where the comparison is made against
    # 0x1234, 0x2345 and 0x3456 respectively
    found_branches = { 0x555CDC5F3A7E: False, 0x555CDC5F3B53: False, 0x555CDC5F3C28: False }
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
