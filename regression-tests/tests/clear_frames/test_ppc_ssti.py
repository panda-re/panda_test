# test_ppc_ssti.py
# Use a recording from a ppc guest to test the changes made to resolve issue
# ACE-42 - LLVM frames not properly.  As running a test long enough to exhibit
# this problem can take over an hour, this test just examines the LLVM created
# by the taint2 plugin to verify the LLVM frame clearing code is in place.
#
# Created:  21-FEB-2019
# Changed:  05-JUN-2019   Don't dump stderr on PANDA error, as it is TOO long

import os
from enum import Enum

import ptest

import tests.clear_frames.framechecker as framechecker

INDENT_SPACES = "                 "

TEST_PREFIX = "ppc_ssti"
STDOUT_NAME = os.path.join("tests", "clear_frames", TEST_PREFIX + ".stdout")
STDERR_NAME = os.path.join("tests", "clear_frames", TEST_PREFIX + ".stderr")

QEMU = ptest.Qemu(ptest.Qemu.PPC, 1024, options="-d llvm_ir")

STRINGSEARCH = ptest.Plugin("stringsearch", str="package", callers=128)
TSTRINGSEARCH = ptest.Plugin("tstringsearch")
TAINTED_INSTR = ptest.Plugin("tainted_instr", num=1500)
REPLAY_PATH = os.path.join("ppc", "ppc_catgrep")

REPLAY_SSTI = ptest.Replay(REPLAY_PATH, QEMU, STRINGSEARCH, TSTRINGSEARCH,
    TAINTED_INSTR)

# did this regression test pass or not?
allOK = False

                            
def run():
    global allOK
    
    # Run the scenario
    retcode = REPLAY_SSTI.run()
    
    # need the stderr output regardless of results
    REPLAY_SSTI.copy_stderr(STDERR_NAME)
    
    if (retcode != 0):
        print(INDENT_SPACES + "***** ERROR EXECUTING PANDA *****")
        REPLAY_SSTI.copy_stdout(STDOUT_NAME)
        return False

    checkCode = framechecker.CheckLLVMFrames(STDERR_NAME)
    if (framechecker.LLVMFrameStatus.FRAMES_OK != checkCode):
        print(INDENT_SPACES + "***** ERRROR " + str(checkCode) + " *****")
        return False

    allOK = True
    return True

def cleanup():
    global allOK
    
    os.remove("_string_matches.txt")
    if (allOK):
        os.remove(STDERR_NAME)
    else:
        print(INDENT_SPACES + STDOUT_NAME)
        print(INDENT_SPACES + STDERR_NAME)
        print(INDENT_SPACES + "The above files have not been deleted in the " +
            "hope they will cue you in as to what went wrong.")
