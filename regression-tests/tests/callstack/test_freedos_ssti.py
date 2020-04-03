# test_freedos_ssti.py
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

TEST_PREFIX = "freedos_ssti"
STDOUT_NAME = os.path.join("tests", "callstack", TEST_PREFIX + ".stdout")
STDERR_NAME = os.path.join("tests", "callstack", TEST_PREFIX + ".stderr")
SM_NAME = os.path.join("tests", "callstack", TEST_PREFIX + "_string_matches.txt")

QEMU = ptest.Qemu(ptest.Qemu.I386, 128)

CALLSTACK = ptest.Plugin("callstack_instr", verbose=True)
STRINGSEARCH = ptest.Plugin("stringsearch", str="hello world", callers=128)
TSTRINGSEARCH = ptest.Plugin("tstringsearch")
TAINTED_INSTR = ptest.Plugin("tainted_instr")
REPLAY_PATH = os.path.join("freedos", "freedos_hello32b2")

REPLAY_SS = ptest.Replay(REPLAY_PATH, QEMU, CALLSTACK, STRINGSEARCH,
    TSTRINGSEARCH, TAINTED_INSTR)

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

#    # it's hard to determine for sure that the situation that causes the logging
#    # of return addresses for Stopped blocks in the stacks that will be reported
#    # on, but we can at least determine that SOME Stopped block ended in a call
#    # this is done with help of the verbose option for the callstack_instr
#    # plugin, which outputs a warning whenever such an event occurs
#    with open(STDOUT_NAME, 'r') as inFile:
#        gotEOF = False
#        gotWarning = False
#        while ((not gotEOF) and (not gotWarning)):
#            curLine = inFile.readline()
#            lineLen = len(curLine)
#            if (not (lineLen == 0)):
#                curLine = curLine.strip()
#                if (curLine.startswith(STOPPED_WARNING_PREFIX)):
#                    gotWarning = True
#            else:
#                gotEOF = True
#                
#    if (not gotWarning):
#        print(INDENT_SPACES + "***** NOT A USEFUL RUN *****")
#        print(INDENT_SPACES + "No blocks ending in call instructions were Stopped")
#        print(INDENT_SPACES + "Try again")
#        return False
        
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
