import os
import tempfile

import ptest

# QEMU Options
QEMU = ptest.Qemu(ptest.Qemu.PPC, 1024)

# PANDA Options
REPLAY = ptest.Replay("warmfuzzy-ppc-lubuntu", QEMU)

def run():
    rc = REPLAY.run()
    if rc != 0:
        REPLAY.dump_console(stderr=True, stdout=True)
        return False
    return True

def cleanup():
    pass
