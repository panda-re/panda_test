import ptest

def win_checkplog(plog_file):
    """
    Check the pandalog for the Windows versions of the tests.
    """
    with ptest.PlogReader(plog_file) as plr:
        for i, m in enumerate(plr):
            # This basic block should have a conditional branch instruction
            # that depends on tainted data.
            if m.pc == 0x004016A8 and m.HasField("tainted_branch"):
                return True
    return False

def linux_checkplog(plog_file, expected_pc=0x804863E):
    """
    Check the pandalog for the Linux versions of the tests.  The default
    expected_pc is appropriate for use with the lubuntu1604 tests.  Other guests
    can override what the pc which is expected to be reported by tainted_branch.
    """
    with ptest.PlogReader(plog_file) as plr:
        for i, m in enumerate(plr):
            # This basic block should have a conditional branch instruction
            # that depends on tainted data.
            if m.pc == expected_pc and m.HasField("tainted_branch"):
                return True
    return False

def tainted_branch_in_plog(plog_file):
    """
    Determine whether or not the plog file contains tainted branches.
    """
    with ptest.PlogReader(plog_file) as plr:
        for i, m in enumerate(plr):
            if m.hasField("tainted_branch"):
                return True
    return False
    