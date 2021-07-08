# test_ubuntu_ssti.py
# Use a recording from an ubuntu guest to test the changes made to resolve issue
# ACE-42 - LLVM frames not properly As running a test long enough to exhibit
# this problem can take a few hours, this test just examines the LLVM created by
# the taint2 plugin to verify the LLVM frame clearing code is in place.
#
# Created:  21-FEB-2019
# Changed:  05-JUN-2019   Don't dump stderr on PANDA error, as it is TOO long

import os
from enum import Enum

import ptest

import tests.clear_frames.framechecker as framechecker

INDENT_SPACES = "                 "

TEST_PREFIX = "ubuntu_ssti"
STDOUT_NAME = os.path.join("tests", "clear_frames", TEST_PREFIX + ".stdout")
STDERR_NAME = os.path.join("tests", "clear_frames", TEST_PREFIX + ".stderr")

# -net nic -net user
NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 2048, NETDEV, E1000DEV, options="-d llvm_ir")

STRINGSEARCH = ptest.Plugin("stringsearch", str="Buynak", callers=128)
TSTRINGSEARCH = ptest.Plugin("tstringsearch")
TAINTED_INSTR = ptest.Plugin("tainted_instr", num=5)
REPLAY_PATH = os.path.join("ubuntuserver", "ubuntu_sortinput")

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
