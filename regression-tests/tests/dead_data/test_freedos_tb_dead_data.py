import csv
import os
import tempfile
import uuid
import re
import sys

import ptest

TESTDIR = os.path.dirname(__file__)

STRINGSEARCH_DEAD = ptest.Plugin("stringsearch", str="Abnormal program")
TSTRINGSEARCH = ptest.Plugin("tstringsearch", pos=True)
TAINTED_BRANCH = ptest.Plugin("tainted_branch", liveness=True)

QEMU = ptest.Qemu(ptest.Qemu.I386, 128, vga=ptest.Qemu.CIRRUS)
REPLAY_PATH = "freedos_tb_liveness"

PLOG_FILE_DEAD = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
REPLAY_DEAD = ptest.Replay(REPLAY_PATH, QEMU, STRINGSEARCH_DEAD, TSTRINGSEARCH,
    TAINTED_BRANCH, plog=PLOG_FILE_DEAD)

def run():
    """
    Execute the test and return true if the test passed.
    """

    # Run the replay searching for the dead data. Make sure it doesn't fail.
    retcode = REPLAY_DEAD.run()
    if retcode != 0:
        REPLAY_DEAD.dump_console()
        return False

    # Verify that the string was tainted.
    matched = False
    with REPLAY_DEAD.stdout() as f:
        for _, line in enumerate(f):
            mo = re.search("tstringsearch: ascii = \[Abnormal program\]", line)
            if mo != None:
                matched = True
    if not matched:
        return False

    # Now read the pandalog file, verify that no labels are live.
    with ptest.PlogReader(PLOG_FILE_DEAD) as plr:
        for i, m in enumerate(plr):
            if m.HasField('label_liveness'):
                return False

    return True

def cleanup():
    """
    A cleanup function called when the test completes reguardless of whether or
    not the test passed.
    """
    pass
