# test_win2003_card_lazyshad.py
# Run the maximum taint cardinality regression test when the taint is
# in a LazyShad.  Network taint uses a LazyShad.
#
# Created:  26-OCT-2018

import os
import re

import ptest

INDENT_SPACES = "                 "

TAINTED_NET = ptest.Plugin("tainted_net", label_incoming_network=True, pos=True)
TAINTED_INSTR = ptest.Plugin("tainted_instr", num=60000)

# I believe these are the equivalent of "-net nic -net user"
NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

# darn Qemu won't let me specify 3G for guest memory like PANDA does
QEMU = ptest.Qemu(ptest.Qemu.I386, 3072, NETDEV, E1000DEV)

# use os.path.join so needn't worry about what the separator character is on
# this system
REPLAY_PATH = os.path.join("windows2003", "windows2003_surfwww")

newFiles = set()
allOK = False

def DoReplay(filePrefix, maxCard):
    """
    Replay the recording with maxCard as the maximum taint cardinality.
    Use the provided filePrefix for the output file prefixes.  There will be
    PANDA log file output in filePrefix+".plog".
    Return True if all went fine, and False if it did not.
    """

    plogName = filePrefix + ".plog"
    taint2 = ptest.Plugin("taint2", max_taintset_card=maxCard)
    replayTN = ptest.Replay(REPLAY_PATH, QEMU, taint2, TAINTED_NET,
        TAINTED_INSTR, plog=plogName)
    retcode = replayTN.run()
    newFiles.add(plogName)
    
    # need to keep stdout and stderr just in case fails later on
    replayTN.copy_stdout(filePrefix + ".stdout")
    newFiles.add(filePrefix + ".stdout")
    replayTN.copy_stderr(filePrefix + ".stderr")
    newFiles.add(filePrefix + ".stderr")
    if (retcode != 0):
        print(INDENT_SPACES + "***** ERROR EXECUTING PANDA *****")
        replayTN.dump_console(stdout=False, stderr=True)
        return False
        
    return True

def GetMaxCard(filePrefix):
    """
    Search the PANDA log file with the name filePrefix + ".plog" for the maximum
    taint set cardinality.  Return the value found.
    """
    
    maxCardFound = 0
    with ptest.PlogReader(filePrefix + ".plog") as plr:
        for msgNo, msg in enumerate(plr):
            fieldInfoList = msg.ListFields()
            # for each item in list, item 0 is the FieldDescriptor, item 1 is
            # its value
            # not every message has the tainted_instr field of interest, so
            # HasField can't be used to find the messages of interest (it just
            # checks to see if the field has something in it, and will throw an
            # exception if the field doesn't even exist)
            for fieldInfo in fieldInfoList:
                if (fieldInfo[0].name == "tainted_instr"):
                    tiFieldInfoList = fieldInfo[1].ListFields()
                    for tiFieldInfo in tiFieldInfoList:
                        if (tiFieldInfo[0].name == "taint_query"):
                            # the taint_query is a repeated field
                            for curTQ in tiFieldInfo[1]:
                                # the unique_label_set within it is optional
                                tqFieldInfoList = curTQ.ListFields()
                                for tqFieldInfo in tqFieldInfoList:
                                    if (tqFieldInfo[0].name == "unique_label_set"):
                                        # the label within it is repeated
                                        curCard = 0
                                        for curLabel in tqFieldInfo[1].label:
                                            curCard = curCard + 1
                                        if (curCard > maxCardFound):
                                            maxCardFound = curCard
                
    return maxCardFound
    
                            
def run():
    """
    Execute the test and return true if the test passed.
    """

    global allOK
    
    maxCard = 100
    
    # first, replay the recording with no maximum, to verify this is still a
    # valid scenario
    noMaxFilePrefix = "windows2003_maxcard_none_lazyshad"
    if (DoReplay(noMaxFilePrefix, 0)):
        maxFound = GetMaxCard(noMaxFilePrefix)
        if (maxFound <= maxCard):
            print(INDENT_SPACES +
                "INVALID SCENARIO - NO CARDINALITY FOUND ABOVE " +
                str(maxCard) + " (MAXIMUM CARDINALITY FOUND IS " +
                str(maxFound) + ")")
            return False
            
    # now, replay with the limit, to verify the cardinality was really limited
    # when the cardinality EXCEEDS the limit, the taint is removed by taint2, so
    # the limit itself may appear in valid output
    maxFilePrefix = "windows2003_maxcard_100_lazyshad"
    if (DoReplay(maxFilePrefix, maxCard)):
        maxFound = GetMaxCard(maxFilePrefix)
        if (maxFound > maxCard):
            print(INDENT_SPACES + "FOUND MAXIMUM CARDINALITY OF " +
                str(maxFound) + " WHICH IS ABOVE THE REQUESTED MAXIMUM OF " +
                str(maxCard))
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
    