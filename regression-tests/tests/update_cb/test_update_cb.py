# test_update_cb.py
# Run the update_cb_switch regression test.  Note that this test is not executed
# using PANDA, as it's too darned hard to find examples of all the situations
# need to test to verify the bit twiddling in update_cb is done properly.
#
# Created:  08-NOV-2018

import os
import subprocess

import ptest

INDENT_SPACES = "                 "

STDOUT_NAME = "test_update_cb.stdout"

BINARY_NAME = "update_cb_switch"
EXPECTED_RESULTS_NAME = "update_cb_switch_results.txt"

allOK = False
outputFiles = set()
    
def run():
    """
    Execute the test and return true if the test passed.
    """

    global allOK
    global outputFiles
    
    # first, verify that the necessary files exist
    buildDir = ptest.get_build_dir()
    testerDir = os.path.join(buildDir, "..", "panda", "panda", "plugins",
        "taint2", "tests", "update_cb_switch")
    try:
        testerFiles = os.listdir(testerDir)
        gotBinary = False
        gotExpectedResults = False
        for curFile in testerFiles:
            if (curFile == BINARY_NAME):
                gotBinary = True
            elif (curFile == EXPECTED_RESULTS_NAME):
                gotExpectedResults = True
    except FileNotFoundError:
        print(INDENT_SPACES + testerDir + ' NOT FOUND')
        return False
    if (not (gotBinary and gotExpectedResults)):
        print(INDENT_SPACES + BINARY_NAME + ' AND/OR ' + EXPECTED_RESULTS_NAME +
            ' FILES NOT FOUND IN ' + testerDir)
        print(INDENT_SPACES + '   Did you forget to make ' + BINARY_NAME + '?')
        return False
        
    update_cb_cmdline = os.path.join(testerDir, BINARY_NAME)
    expectedResultsFullName = os.path.join(testerDir, EXPECTED_RESULTS_NAME)
    
    # now, run the update_cb_switch test executable, sending current results
    stdoutFile = open(STDOUT_NAME, 'w')
    retcode = subprocess.call(update_cb_cmdline, stdout=stdoutFile)
    outputFiles.add(STDOUT_NAME)
    if (retcode != 0):
        print(INDENT_SPACES + "***** ERROR EXECUTING " + BINARY_NAME + " *****")
        print(INDENT_SPACES + "   Return Code = " + str(retcode))
        return False
    
    # now, check the results
    expectedResults = []
    try:
        with open(expectedResultsFullName, "r") as expectFile:
            for line in expectFile:
                line = line.strip()
                expectedResults.append(line)
    except IOError:
        print(INDENT_SPACES + "ERROR READING " + expectedResultsFullName)
        return False
        
    actualResults = []
    try:
        with open(STDOUT_NAME, "r") as actualsFile:
            for line in actualsFile:
                line = line.strip()
                actualResults.append(line)
    except IOError:
        print(INDENT_SPACES + "ERROR READING " + STDOUT_NAME)
        return False
        
    if (actualResults != expectedResults):
        print(INDENT_SPACES + "EXPECTED AND ACTUAL RESULTS DIFFER")
        return False
    
    allOK = True
    return True
    
def cleanup():
    """
    A cleanup function called when the test completes regardless of whether or
    not the test passed.
    """
    
    global allOK
    global outputFiles

    if (allOK):
        while (len(outputFiles) > 0):
            curFile = outputFiles.pop()
            try:
                os.remove(curFile)
            except IOError:
                pass
    else:
        origLen = len(outputFiles)
        while (len(outputFiles) > 0):
            curFile = outputFiles.pop()
            print(INDENT_SPACES + curFile)
        if (origLen > 0):
            print(INDENT_SPACES + "The above files have not been deleted in " +
                "the hope they will cue you in as to what went wrong.")
    