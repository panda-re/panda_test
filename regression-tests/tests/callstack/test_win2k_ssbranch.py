# test_win2k_ssbranch.py
# Test the changes made to resolve issue ACE-35 (formerly NG GitHub issue 33).
# The problem was that the callstack_instr plugin, when its after_block_exec
# callback was notified that a block had been executed and that block ended in
# a call statement, was putting the return address of the call on the stack,
# even if the block had actually been stopped before it was executed.  When the
# block was run again, the return address would be put on the stack again.  If
# the stack was requested while inside the function, there would be two return
# addresses on the stack instead of just one.  If the stack was requested after
# having returned from the function, there would still be one return address on
# the stack as (most likely) the block starting with the return address would
# only have attempted execution once.
#
# Created:  30-JAN-2019

import os
import filecmp

import ptest

INDENT_SPACES = "                 "

STOPPED_WARNING_PREFIX = "callstack_instr not adding Stopped caller to stack:"

TEST_PREFIX = "win2k_ssbranch"
STDOUT_NAME = os.path.join("tests", "callstack", TEST_PREFIX + ".stdout")
STDERR_NAME = os.path.join("tests", "callstack", TEST_PREFIX + ".stderr")
SM_NAME = os.path.join("tests", "callstack", TEST_PREFIX + "_string_matches.txt")

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000 = ptest.Device(ptest.Device.E1000, backend=NETDEV)

# the -llvm option causes the problem of interest to occur more often
QEMU = ptest.Qemu(ptest.Qemu.I386, 1024, NETDEV, E1000, vga=ptest.Qemu.CIRRUS, options="-llvm")

CALLSTACK = ptest.Plugin("callstack_instr", verbose=True)
STRINGSEARCH = ptest.Plugin("stringsearch", str="branch", callers=128)

REPLAY_SS = ptest.Replay("2k-filetaint-singleproc-singlefile", QEMU,
    CALLSTACK, STRINGSEARCH)

allOK = False

def run():
    global allOK
    
    # Run the scenario
    retcode = REPLAY_SS.run()
    
    # need the stdout and string matches output regardless of results
    REPLAY_SS.copy_stdout(STDOUT_NAME)
    os.rename("_string_matches.txt", SM_NAME)
    
    if (retcode != 0):
        print(INDENT_SPACES + "***** ERROR EXECUTING PANDA *****")
        REPLAY_SS.copy_stderr(STDERR_NAME)
        REPLAY_SS.dump_console(stdout=False, stderr=True)
        return False

    if (not filecmp.cmp(SM_NAME, os.path.join("tests", "callstack",
        TEST_PREFIX + "_string_matches_expected.txt"))):
        print(INDENT_SPACES + "***** CALLSTACKS NOT AS EXPECTED *****")
        return False

    allOK = True
    return True

def cleanup():
    global allOK
    
    if (allOK):
        os.remove(STDOUT_NAME)
        os.remove(SM_NAME)
    else:
        print(INDENT_SPACES + STDOUT_NAME)
        print(INDENT_SPACES + STDERR_NAME)
        print(INDENT_SPACES + SM_NAME)
        print(INDENT_SPACES + "The above files have not been deleted in the " +
            "hope they will cue you in as to what went wrong.")
