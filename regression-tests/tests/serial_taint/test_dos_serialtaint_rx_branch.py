import os
import tempfile

import ptest

# QEMU Options
CHARDEV = ptest.CharBackend(ptest.CharBackend.PIPE, "com5", path="/dev/null")
ISA_SERIAL = ptest.Device(ptest.Device.ISA_SERIAL, backend=CHARDEV, iobase=0x03F8, irq=4)
QEMU = ptest.Qemu(ptest.Qemu.I386, 64, CHARDEV, ISA_SERIAL)

# PANDA Options
SERIAL_TAINT = ptest.Plugin("serial_taint")
TAINTED_BRANCH = ptest.Plugin("tainted_branch")
_, PLOG = tempfile.mkstemp()
REPLAY = ptest.Replay("dos-serialtaint-rx-branch", QEMU, SERIAL_TAINT, TAINTED_BRANCH, plog=PLOG)

def run():
    rc = REPLAY.run()
    if rc:
        REPLAY.dump_console(stderr=True)
        return False
    found_branch = False
    try:
        with ptest.PlogReader(PLOG) as plr:
            for i, m in enumerate(plr):
                if m.HasField("tainted_branch") and m.pc == 0x2BD3:
                    found_branch = True
                    break
    except Exception as e:
        print(e)
        return False
    if not found_branch:
        print("expected to find branch at 0x2BD3")
        return False

    return True

def cleanup():
    os.remove(PLOG)

