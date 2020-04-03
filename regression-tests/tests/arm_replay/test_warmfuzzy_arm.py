import os
import tempfile

import ptest

# QEMU Options
DRIVE = ptest.Drive("/dev/null", "nulldrive")
DRIVE_DEVICE = ptest.Device(ptest.Device.SCSI_DISK, backend=DRIVE)
QEMU = ptest.Qemu(ptest.Qemu.ARM, 256, DRIVE, DRIVE_DEVICE, machine='versatilepb', cpu="arm1176")

# PANDA Options
REPLAY = ptest.Replay("warmfuzzy-arm-raspbian", QEMU)

def run():
    rc = REPLAY.run()
    if rc != 0:
        REPLAY.dump_console(stderr=True, stdout=True)
        return False
    return True

def cleanup():
    pass
