import os
import tempfile

import ptest

# QEMU Options
NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
RTL8139 = ptest.Device(ptest.Device.RTL8139, backend=NETDEV)
CHARDEV = ptest.CharBackend(ptest.CharBackend.PIPE, "com5", path="/dev/null")
PCI_SERIAL = ptest.Device(ptest.Device.PCI_SERIAL, backend=CHARDEV)
QEMU = ptest.Qemu(ptest.Qemu.I386, 2048, NETDEV, RTL8139, CHARDEV, PCI_SERIAL, vga=ptest.Qemu.CIRRUS)

# PANDA Options
SERIAL_TAINT = ptest.Plugin("serial_taint")
TAINTED_BRANCH = ptest.Plugin("tainted_branch")
_, PLOG = tempfile.mkstemp()
REPLAY = ptest.Replay("lubuntu1604-serialtaint-rx-branch", QEMU, SERIAL_TAINT, TAINTED_BRANCH, plog=PLOG)

def run():
    rc = REPLAY.run()
    if rc:
        REPLAY.dump_console(stderr=True)
        return False
    found_branch = False
    try:
        with ptest.PlogReader(PLOG) as plr:
            for i, m in enumerate(plr):
                if m.HasField("tainted_branch") and m.pc == 0x8048609:
                    found_branch = True
                    break
    except Exception as e:
        print(e)
        return False
    if not found_branch:
        print("expected to find branch at 0x004016AF")
        return False

    return True

def cleanup():
    os.remove(PLOG)

