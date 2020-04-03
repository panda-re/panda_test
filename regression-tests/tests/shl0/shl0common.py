# shl0common.py
# Common code used to compare results for testing the changes made to taint2 to
# not copy taint to all bytes when doing shift left by 0.
#
# Created:  10-OCT-2018

import os
import re

import ptest

INDENT_SPACES = "                 "
STRING_MATCHES_SUFFIX = "_string_matches.txt"

STRINGSEARCH = ptest.Plugin("stringsearch", str="hello world")
TSTRINGSEARCH = ptest.Plugin("tstringsearch")
TAINTED_INSTR = ptest.Plugin("tainted_instr")
TAINT2 = ptest.Plugin("taint2")

# created files that haven't been cleaned up yet
newFiles = set()

# are all the files in newFiles from tests that ran OK?
allOK = False

def DoReplay(filePrefix, qemuOpts, replayPath):
    """
    Replay the recording in replayPath, using the QEMU options given, and using
    the given file prefix for the standard out and standard error files.
    Also discard the string matches file as it is not needed later.
    Return True if the replay finished OK, and False if it did not.
    """

    REPLAY_DETAINT = ptest.Replay(replayPath, qemuOpts, TAINT2, STRINGSEARCH,
        TSTRINGSEARCH, TAINTED_INSTR)
    retcode = REPLAY_DETAINT.run()
    stdoutFileName = filePrefix + ".stdout"
    REPLAY_DETAINT.copy_stdout(stdoutFileName)
    newFiles.add(stdoutFileName)
    stderrFileName = filePrefix + ".stderr"
    REPLAY_DETAINT.copy_stderr(stderrFileName)
    newFiles.add(stderrFileName)
    if (retcode != 0):
        print(INDENT_SPACES + "***** ERROR EXECUTING PANDA *****")
        REPLAY_DETAINT.dump_console(stdout=False, stderr=True)
        return False
        
    # we're not testing the stringsearch plugin, so no point keeping its output
    os.remove(STRING_MATCHES_SUFFIX)
    
    return True
        
def ExtractTaintReports(filePrefix, searchPattern):
    """
    Extract the number of taint reports matching the given searchPattern.
    """

    numTaintReports = 0
    with open(filePrefix + ".stdout", "r") as logFile:
        for line in logFile:
            line = line.strip()
            matchObj = re.search(searchPattern, line)
            if (matchObj != None):
                numTaintReports = numTaintReports + 1
    
    return numTaintReports
        
def DoComparison(filePrefix, qemuOpts, replayPath, shl0Block, expectReports):
    """
    Run taint2 on the given replay, checking the given block contains the number
    of taint reports specified by expectReports.
    The block named by shl0Block should be one containing a "SHL 0" LLVM
    instruction whose input has only SOME of its bytes tainted.  It must be
    given in lower-case hex with the "0x" prefix.
    Before the SHL0 adjustments, taint2 would cause the taint on a SHL 0 to be
    smudged across all bytes of the output.  Now, the output should have the
    same bytes tainted as the input.  Return True if the expected number of
    taint reports exist in the given block.  Return False otherwise.
    """
    
    global allOK
    
    allOK = False
      
    # generate the results
    fullFilePrefix = filePrefix + "_postshl0"
    DoReplay(fullFilePrefix, qemuOpts, replayPath)
    searchPattern = "pc = " + shl0Block
    numReports = ExtractTaintReports(fullFilePrefix, searchPattern)
        
    # and finally see if got the right number of taint reports in the block
    if (numReports != expectReports):
        print(INDENT_SPACES + "WRONG NUMBER OF TAINT REPORTS IN BLOCK " + shl0Block)
        print(INDENT_SPACES + "Expected:" + str(expectReports))
        print(INDENT_SPACES + "Got:" + str(numReports))
        return False
       
    allOK = True
    return True

def cleanup():
    if (allOK):
        while (len(newFiles) > 0):
            curFile = newFiles.pop()
            try:
                os.remove(curFile)
            except OSError:
                pass        # empty statement
    else:
        # empty the set, so ready for use next time around
        while (len(newFiles) > 0):
            curFile = newFiles.pop()
            print(INDENT_SPACES + curFile)
        print(INDENT_SPACES +
            "The above output files have not been deleted in hopes they cue you in as to what went wrong.")
