# test_debian64_max_labels.py
# Test the file_taint plugin maximum labels option using a 64-bit guest.
#
# Created:  25-OCT-2019

import os

import ptest
import tempfile

import tests.file_taint.common as common

TESTDIR = os.path.dirname(__file__)
REPLAY_PATH = os.path.join("debian64", "linux64_positional")

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

TABLET = ptest.Device(ptest.Device.USB_TABLET)

QEMU = ptest.Qemu(ptest.Qemu.X86_64, 2048, NETDEV, E1000DEV, TABLET,
    options="-usb")

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="positional.bin",
    pos=True, max_num_labels=2)

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
        REPLAY1.dump_console(stderr=True)
        return False

    found_branch = False
    found_labels = []
    try:
        with ptest.PlogReader(PLOG1) as plr:
            for i, m in enumerate(plr):
                if m.HasField("tainted_branch"):
                    for tq in m.tainted_branch.taint_query:
                        found_labels += tq.unique_label_set.label
                # block with the cmp for 0x1234
                if m.pc == 0x55CE0E42A983 and m.HasField("tainted_branch"):
                    found_branch = True
                # block with the cmp for 0x2345
                if m.pc == 0x55CE0E42AB3 and m.HasField("tainted_branch"):
                    print("0x55CE0E42AB3 should not have been reported")
                    return False
                if m.pc == 0x55CE0E42A9D7 and m.HasField("tainted_branch"):
                    print("0x55CE0E42A9D7 should not have been reported")
                    return False
    except:
        print("error")
    if not found_branch:
        print("expected branch not found")
        return False
    if set(found_labels) != set([0, 1]) or (2 in found_labels or 3 in found_labels):
        print("expected the following labels: {}".format([0, 1]))
        return False

    return True

def cleanup():
    pass
