import os
import tempfile

import ptest

# QEMU Options
QEMU = ptest.Qemu(ptest.Qemu.X86_64, 4096, vga=ptest.Qemu.CIRRUS)

# PANDA Options
REPLAY = ptest.Replay("warmfuzzy-x64-win2k8r2", QEMU)

def run():
    rc = REPLAY.run()
    if rc != 0:
        REPLAY.dump_console(stderr=True, stdout=True)
        return False
    return True

def cleanup():
    pass
