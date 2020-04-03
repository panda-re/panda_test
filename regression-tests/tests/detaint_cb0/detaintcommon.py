# detaintcommon.py
# Common code used to compare results for testing detaint_cb0 option.
#
# Created:  08-OCT-2018
# Changed:  30-JAN-2019   compare full string matches output, as ACE-35
#                         (formerly issue 33) is fixed
# Changed:  27-FEB-2019   use set instead of list in ExtractTaintReports, as it
#                         is more efficient, and we want to check more of file

import filecmp
import os
import re

import ptest

INDENT_SPACES = "                 "
STRING_MATCHES_SUFFIX = "_string_matches.txt"

STRINGSEARCH = ptest.Plugin("stringsearch", str="hello world", callers=128)
TSTRINGSEARCH = ptest.Plugin("tstringsearch")
TAINTED_INSTR = ptest.Plugin("tainted_instr")

# created files that haven't been cleaned up yet
newFiles = set()

# are all the files in newFiles from tests that ran OK?
allOK = False

def DoReplay(filePrefix, qemuOpts, replayPath, detaint):
    """
    Replay the recording in replayPath, with the detaint setting given,
    using the QEMU options given, and using the given file prefix for the
    standard out and standard error files.
    Also save the string matches file to a file with the same prefix.
    Return True if the replay finished OK, and False if it did not.
    """

    TAINT2 = ptest.Plugin("taint2", detaint_cb0=detaint)
    REPLAY_DETAINT = ptest.Replay(replayPath, qemuOpts, TAINT2, STRINGSEARCH,
        TSTRINGSEARCH, TAINTED_INSTR)
    retcode = REPLAY_DETAINT.run()
    stdoutFileName = filePrefix + ".stdout"
    newFiles.add(stdoutFileName)
    stderrFileName = filePrefix + ".stderr"
    newFiles.add(stderrFileName)
    REPLAY_DETAINT.copy_stdout(filePrefix + ".stdout")
    REPLAY_DETAINT.copy_stderr(filePrefix + ".stderr")
    stdoutFile = open(stdoutFileName, "r")
    stderrFile = open(stderrFileName, "r")
    if (retcode != 0):
        print(INDENT_SPACES + "***** ERROR EXECUTING PANDA *****")
        stderrFile.close()
        stdoutFile.close()
        stderrFile = open(stderrFile.name, "r")
        print(stderrFile.read())
        return False
        
    smFile = os.path.join("tests", "detaint_cb0", filePrefix + STRING_MATCHES_SUFFIX)
    os.rename(STRING_MATCHES_SUFFIX, smFile)
    newFiles.add(smFile)
    
    # make ready for next run
    stderrFile.close()
    stdoutFile.close()
        
    return True
        
def ExtractTaintReports(filePrefix, searchPattern):
    """
    Extract the taint reports (their number and the list of unique blocks)
    that match the given searchPattern from the stdout file with the given
    prefix.  Return a dictiony with the number of taint reports matching
    the pattern in numTaintReports, and a set of the unique tainted blocks found
    in taintedBlocks.
    """

    taintedBlocks = set()
    numTaintReports = 0
    with open(filePrefix + ".stdout", "r") as logFile:
        for line in logFile:
            line = line.strip()
            matchObj = re.search(searchPattern, line)
            if (matchObj != None):
                numTaintReports = numTaintReports + 1
                if (line not in taintedBlocks):
                    taintedBlocks.add(line)
    
    return {'numTaintReports':numTaintReports, 'taintedBlocks':taintedBlocks}
        
def DoComparison(filePrefix, qemuOpts, replayPath, searchPattern):
    """
    Compare the taint2 results of running the same replay with the detaint
    flag and without out.  Return True if the results with the flag have
    the appropriate blocks tainted, but fewer taint reports than occurred
    without the flag.  Return False otherwise.
    """
    
    global allOK
    
    allOK = False

    # first generate the results w/out detainting
    fullFilePrefixF = filePrefix + "_nodetaint"        
    DoReplay(fullFilePrefixF, qemuOpts, replayPath, False)
    preReports = ExtractTaintReports(fullFilePrefixF, searchPattern)
      
    # then generate the results with detainting
    fullFilePrefixT = filePrefix + "_detaint"
    DoReplay(fullFilePrefixT, qemuOpts, replayPath, True)
    postReports = ExtractTaintReports(fullFilePrefixT, searchPattern)
        
    # and finally see if they are correct
    
    # as the string matches file is output of stringsearch plugin, no taint is
    # involved; but seems a good idea to verify both runs are finding the string
    # in the same places
    fullFileF = os.path.join("tests", "detaint_cb0", fullFilePrefixF + STRING_MATCHES_SUFFIX)
    fullFileT = os.path.join("tests", "detaint_cb0", fullFilePrefixT + STRING_MATCHES_SUFFIX)
    if (not filecmp.cmp(fullFileF, fullFileT)):
        print(INDENT_SPACES +
            "DETAINTED AND NON-DETAINTED STRINGS MATCHES FILES ARE DIFFERENT")
        return False

    # verify that the detainted list is a subset of the tainted list
    if (postReports['taintedBlocks'] > preReports['taintedBlocks']):
        print(INDENT_SPACES +
            "DETAINTED TAINTED BLOCKS LIST NOT A SUBSET OF NON-DETAINTED LIST")
        return False
    
    # verify that the detainted list contains only the expected blocks
    expectedTaintedBlocks = set()
    with open(os.path.join("tests", "detaint_cb0",
        fullFilePrefixT + "_tainted_blocks_expected.txt"), "r") as expectFile:
        for line in expectFile:
            line = line.strip()
            expectedTaintedBlocks.add(line)
    if (postReports['taintedBlocks'] != expectedTaintedBlocks):
        print(INDENT_SPACES + "DETAINTED TAINTED BLOCKS LIST NOT CORRECT")
        # the expected results file is expected to already be sorted
        print(INDENT_SPACES + "Expected:" + str(expectedTaintedBlocks))
        print(INDENT_SPACES + "Got:" + str(sorted(postReports['taintedBlocks'])))
        return False
        
    # verify that the number of taint reports has decreased
    if (preReports['numTaintReports'] <= postReports['numTaintReports']):
        print(INDENT_SPACES + "NUMBER OF TAINT REPORTS DID NOT DECREASE")
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
