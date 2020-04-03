import csv
import os
import tempfile
import uuid
import sys

import ptest

TESTDIR = os.path.dirname(__file__)

STRINGSEARCH_DEAD_DATA = ptest.Plugin("stringsearch", name=os.path.join(TESTDIR, 'dead'))
STRINGSEARCH_LIVE_DATA = ptest.Plugin("stringsearch", name=os.path.join(TESTDIR, 'live'))
TSTRINGSEARCH = ptest.Plugin("tstringsearch", pos=True)
TAINTED_BRANCH = ptest.Plugin("tainted_branch", liveness=True)

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
RTL8139 = ptest.Device(ptest.Device.RTL8139, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 2048, NETDEV, RTL8139, vga=ptest.Qemu.CIRRUS)
REPLAY_PATH = "lubuntu1604_tb_liveness"

PLOG_FILE_DEAD = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
REPLAY_DEAD = ptest.Replay(REPLAY_PATH, QEMU, STRINGSEARCH_DEAD_DATA, TSTRINGSEARCH, TAINTED_BRANCH, plog=PLOG_FILE_DEAD)
PLOG_FILE_LIVE = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
REPLAY_LIVE = ptest.Replay(REPLAY_PATH, QEMU, STRINGSEARCH_LIVE_DATA, TSTRINGSEARCH, TAINTED_BRANCH, plog=PLOG_FILE_LIVE)

def run():
    """
    Execute the test and return true if the test passed.
    """
 
    # Run the replay searching for the dead data. Make sure it doesn't fail.
    retcode = REPLAY_DEAD.run()
    if retcode != 0:
        REPLAY_DEAD.dump_console()
        return False

    # Now read the pandalog file, verify that no labels are live.
    with ptest.PlogReader(PLOG_FILE_DEAD) as plr:
        for i, m in enumerate(plr):
            if m.HasField('label_liveness'):
                return False

    # Run the replay searching for the live data. Make sure it doesn't fail.
    retcode = REPLAY_LIVE.run()
    if retcode != 0:
        REPLAY_LIVE.dump_console()
        return False

    # Now read the pandalog file, verify that our live data is indeed marked as
    # live.
    labels = {0: 0, 1: 0, 2: 0, 3: 0}
    with ptest.PlogReader(PLOG_FILE_LIVE) as plr:
        for i, m in enumerate(plr):
            if m.HasField('label_liveness'):
                labels[m.label_liveness.label] = m.label_liveness.count

    # The only labels in our output should be in the interval [0, 3] and the count
    # should be one.
    for key, val in labels.items():
        if val != 1 or key < 0 or key > 3:
            return False
  
    return True

def cleanup():
    """
    A cleanup function called when the test completes reguardless of whether or
    not the test passed.
    """
    pass
