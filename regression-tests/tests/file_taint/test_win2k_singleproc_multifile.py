import ptest
import tempfile

import tests.file_taint.common as common

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000 = ptest.Device(ptest.Device.E1000, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 1024, NETDEV, E1000, vga=ptest.Qemu.CIRRUS)

FILE_TAINT_INPUT1 = ptest.Plugin("file_taint", filename="input1.bin")
FILE_TAINT_INPUT2 = ptest.Plugin("file_taint", filename="input2.bin")
FILE_TAINT_INPUT3 = ptest.Plugin("file_taint", filename="should-not-be-tainted")

TAINTED_BRANCH = ptest.Plugin("tainted_branch")

_, PLOG1 = tempfile.mkstemp()
REPLAY1 = ptest.Replay("2k-filetaint-singleproc-multifile", QEMU,
    FILE_TAINT_INPUT1, TAINTED_BRANCH, os="windows-32-2000", plog=PLOG1)
_, PLOG2 = tempfile.mkstemp()
REPLAY2 = ptest.Replay("2k-filetaint-singleproc-multifile", QEMU,
    FILE_TAINT_INPUT2, TAINTED_BRANCH, os="windows-32-2000", plog=PLOG2)
_, PLOG3 = tempfile.mkstemp()
REPLAY3 = ptest.Replay("2k-filetaint-singleproc-multifile", QEMU,
    FILE_TAINT_INPUT3, TAINTED_BRANCH, os="windows-32-2000", plog=PLOG2)

def run():
    # Try the first file
    retcode = REPLAY1.run()
    if retcode != 0:
        return False

    foundbb = False
    with ptest.PlogReader(PLOG1) as plr:
        for i, m in enumerate(plr):
            # This basic block should have a conditional branch instruction
            # that depends on tainted data.
            if m.pc == 0x00401666 and m.HasField("tainted_branch"):
                foundbb = True
    if not foundbb:
        print("expected 0x00401666 to be reported in tainted branch")
        return False

    # Try the second file
    retcode = REPLAY2.run()
    if retcode != 0:
        return False

    foundbb = False
    with ptest.PlogReader(PLOG2) as plr:
        for i, m in enumerate(plr):
            # This basic block should have a conditional branch instruction
            # that depends on tainted data.
            if m.pc == 0x00401666 and m.HasField("tainted_branch"):
                foundbb = True
    if not foundbb:
        print("expected 0x00401666 to be reported in tainted branch")
        return False

    # Try to taint a file that we didn't open. The plog file should be empty.
    retcode = REPLAY3.run()
    if retcode != 0:
        return False

    foundbb = False
    try:
        with ptest.PlogReader(PLOG3) as plr:
            for i, m in enumerate(plr):
                # This basic block should have a conditional branch instruction
                # that depends on tainted data.
                if m.pc == 0x00401666 and m.HasField("tainted_branch"):
                    foundbb = True
    except:
        pass

    if foundbb:
        print("expected 0x00401666 not to be reported in tainted branch")
        return False

    return True

def cleanup():
    pass
