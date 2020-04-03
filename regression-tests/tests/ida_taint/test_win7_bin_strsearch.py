import csv
import os
import tempfile
import uuid

import ptest

TESTDIR = os.path.dirname(__file__)

STRINGSEARCH = ptest.Plugin("stringsearch", name=os.path.join(TESTDIR, 'searchdata'))
TSTRINGSEARCH = ptest.Plugin("tstringsearch")
IDA_TAINT2_CSV = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()) + ".csv")
IDA_TAINT2 = ptest.Plugin("ida_taint2", filename=IDA_TAINT2_CSV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 2048, vga=ptest.Qemu.CIRRUS)

REPLAY_PATH = "idataint2_win7"

REPLAY = ptest.Replay(REPLAY_PATH, QEMU, STRINGSEARCH, TSTRINGSEARCH, IDA_TAINT2, os="windows-32-7")

STDOUT_FILE = open(os.path.join(tempfile.gettempdir(), str(uuid.uuid4())), 'w')
STDERR_FILE = open(os.path.join(tempfile.gettempdir(), str(uuid.uuid4())), 'w')

def run():
    """
    Execute the test and return true if the test passed.
    """

    # Run the replay. Make sure it doesn't fail.
    retcode = REPLAY.run()
    if retcode != 0:
        return False

    # Now open the ida_taint2 csv file and make sure our expected basic block
    # is reported as depending on tainted data.
    result_file = open(IDA_TAINT2_CSV, "r")
    reader = csv.reader(result_file)
    next(reader, None)
    found_bb = False
    for row in reader:
        pid = int(row[1])
        pc = int(row[2], 16)
        label = int(row[3])
        # Our magic numbers:
        if pid == 1392 and pc == 0x0040157E and label == 10:
            found_bb = True
            break
    result_file.close()
    return found_bb

def cleanup():
    """
    A cleanup function called when the test completes reguardless of whether or
    not the test passed.
    """
    STDOUT_FILE.close()
    STDERR_FILE.close()
    try:
        os.remove(IDA_TAINT2_CSV)
        os.remove(STDOUT_FILE.name)
        os.remove(STDERR_FILE.name)
    except OSError:
        pass
