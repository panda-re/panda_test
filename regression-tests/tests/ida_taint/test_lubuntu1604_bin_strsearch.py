import csv
import os
import tempfile
import uuid
import sys

import ptest

TESTDIR = os.path.dirname(__file__)

STRINGSEARCH = ptest.Plugin("stringsearch", name=os.path.join(TESTDIR, 'searchdata'))
TSTRINGSEARCH = ptest.Plugin("tstringsearch")
IDA_TAINT2_CSV = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()) + ".csv")
IDA_TAINT2 = ptest.Plugin("ida_taint2", filename=IDA_TAINT2_CSV)
OSI_LINUX = ptest.Plugin("osi_linux", kconf_file=os.path.join("shared_configs",
    "lubuntu_kernelinfo.conf"))

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
RTL8139 = ptest.Device(ptest.Device.RTL8139, backend=NETDEV)


QEMU = ptest.Qemu(ptest.Qemu.I386, 2048, NETDEV, RTL8139, vga=ptest.Qemu.CIRRUS)
REPLAY_PATH = "idataint2_lubuntu1604"

REPLAY = ptest.Replay(REPLAY_PATH, QEMU, STRINGSEARCH, TSTRINGSEARCH,
    IDA_TAINT2, OSI_LINUX, os="linux-32-ubuntu-4.4.0-21-generic")

def run():
    """
    Execute the test and return true if the test passed.
    """

    # Run the replay. Make sure it doesn't fail.
    retcode = REPLAY.run()
    if retcode != 0:
        REPLAY.dump_console(stderr=True)
        return False

    # Now open the ida_taint2 csv file and make sure our expected basic block
    # is reported as depending on tainted data.
    result_file = open(IDA_TAINT2_CSV, "r")
    reader = csv.reader(result_file)
    next(reader, None)
    found_inst = False
    for row in reader:
        pid = int(row[1])
        pc = int(row[2], 16)
        label = int(row[3])
        # Our magic numbers:
        if pid == 1087 and pc == 0x804841C and label == 10: 
            found_inst = True
            break
    result_file.close()
    return found_inst

def cleanup():
    """
    A cleanup function called when the test completes reguardless of whether or
    not the test passed.
    """
    pass
