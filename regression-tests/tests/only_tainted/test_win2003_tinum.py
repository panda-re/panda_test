# test_win2003_tinum.py
# Run the regression test for the issues fixed in issue 79.  These changes were
# to not have update_cb in taint2 update the masks on untainted data, and to
# not count untainted data as seen tainted data in tainted_instr.
#
# Created:  29-NOV-2018

import os
import re

import ptest

INDENT_SPACES = "                 "

STRINGSEARCH = ptest.Plugin("stringsearch", str="thieves", callers=128)
TSTRINGSEARCH = ptest.Plugin("tstringsearch")

# I believe these are the equivalent of "-net nic -net user"
NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

# darn Qemu won't let me specify 3G for guest memory like PANDA does
QEMU = ptest.Qemu(ptest.Qemu.I386, 3072, NETDEV, E1000DEV)

# use os.path.join so needn't worry about what the separator character is on
# this system
REPLAY_PATH = os.path.join("windows2003", "windows2003_yippy")

newFiles = set()
allOK = False

def DoReplay(filePrefix, limitNum):
    """
    Replay the recording, using the provided filePrefix for the output file
    prefixes.  Use the limitNum to limit the number of tainted 'instructions'
    seen by tainted_instr before it gives up.
    Return True if all went fine, and False if it did not.
    """

    tainted_instr = ptest.Plugin("tainted_instr", num=limitNum)
    replayTI = ptest.Replay(REPLAY_PATH, QEMU, STRINGSEARCH, TSTRINGSEARCH,
        tainted_instr)
    retcode = replayTI.run()
    
    # need to keep stdout and stderr just in case fails later on
    replayTI.copy_stdout(filePrefix + ".stdout")
    newFiles.add(filePrefix + ".stdout")
    replayTI.copy_stderr(filePrefix + ".stderr")
    newFiles.add(filePrefix + ".stderr")
    newFiles.add("_string_matches.txt")
    if (retcode != 0):
        print(INDENT_SPACES + "***** ERROR EXECUTING PANDA *****")
        replayTI.dump_console(stdout=False, stderr=True)
        return False
        
    return True

def GetRunsCount(filePrefix):
    """
    Search the PANDA console log file with the name filePrefix + ".stdout" for
    the number of taint reports, where consecutive reports for the same PC are
    counted as one run.  Return the value found.
    """
    
    maxRunsFound = 0
    with open(filePrefix + ".stdout", 'r') as inFile:
        consecRuns = 0
        prevPCLine = ""
        for line in inFile:
            if (line.startswith("  pc = 0x")):
                if (len(prevPCLine) > 0):
                    if (not (line in prevPCLine)):
                        maxRunsFound = maxRunsFound + 1
                        prevPCLine = line
                else:
                    maxRunsFound = maxRunsFound + 1
                    prevPCLine = line
                
    return maxRunsFound
                            
def run():
    """
    Execute the test and return true if the test passed.
    """

    global allOK
    
    numLimit = 10
    
    # first, replay the recording with a max of 20, to verify this is still a
    # valid scenario (0 means unlimited, but it could take QUITE some time to
    # run the recording to completion)
    bigLimitFilePrefix = "windows2003_tinum20"
    if (DoReplay(bigLimitFilePrefix, 20)):
        runsFound = GetRunsCount(bigLimitFilePrefix)
        if (runsFound <= numLimit):
            print(INDENT_SPACES +
                "INVALID SCENARIO - ONLY FOUND " +
                str(runsFound) + " TAINTED RUNS BUT NEED MORE THAN " +
                str(numLimit))
            return False
            
    # now, replay with the limit, to verify the limit was really used to end
    # the replay early
    smallLimitFilePrefix = "windows2003_tinum10"
    if (DoReplay(smallLimitFilePrefix, numLimit)):
        runsFound = GetRunsCount(smallLimitFilePrefix)
        if (runsFound > numLimit):
            print(INDENT_SPACES + "FOUND " + str(runsFound) +
                " TAINTED RUNS, WHICH IS ABOVE THE REQUESTED LIMIT OF " +
                str(numLimit))
            return False
            
    allOK = True
    return True
    
def cleanup():
    """
    A cleanup function called when the test completes regardless of whether or
    not the test passed.
    """
    
    global allOK

    if (allOK):
         while (len(newFiles) > 0):
             curFile = newFiles.pop()
             try:
                 os.remove(curFile)
             except IOError:
                 pass
    else:
         while (len(newFiles) > 0):
             curFile = newFiles.pop()
             print(INDENT_SPACES + curFile)
         print(INDENT_SPACES + "The above files have not been deleted in the " +
             "hope they will cue you in as to what went wrong.")
    