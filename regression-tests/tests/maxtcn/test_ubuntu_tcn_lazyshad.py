# test_ubuntu_tcn_lazyshad.py
# Run the maximum taint compute number (TCN) regression test when the taint is
# in a LazyShad.  Network taint uses a LazyShad.
#
# Created:  22-OCT-2018

import os
import re

import ptest

INDENT_SPACES = "                 "

TAINTED_NET = ptest.Plugin("tainted_net", label_incoming_network=True)
TAINTED_INSTR = ptest.Plugin("tainted_instr", num=23000)

# I believe these are the equivalent of "-net nic -net user"
NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

# darn Qemu won't let me specify 2G for guest memory like PANDA does
QEMU = ptest.Qemu(ptest.Qemu.I386, 2048, NETDEV, E1000DEV)

# use os.path.join so needn't worry about what the separator character is on
# this system
REPLAY_PATH = os.path.join("ubuntuserver", "ubuntu_client")

newFiles = set()
allOK = False

def DoReplay(filePrefix, maxTCN):
    """
    Replay the recording with maxTCN as the maximum taint compute number.
    Use the provided filePrefix for the output file prefixes.  There will be
    PANDA log file output in filePrefix+".plog".
    Return True if all went fine, and False if it did not.
    """

    plogName = filePrefix + ".plog"
    taint2 = ptest.Plugin("taint2", max_taintset_compute_number=maxTCN)
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

def GetMaxTCN(filePrefix):
    """
    Search the PANDA log file with the name filePrefix + ".plog" for the maximum
    taint computer number.  Return the value found.
    """
    
    maxTCNFound = 0
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
                                if (curTQ.tcn > maxTCNFound):
                                    maxTCNFound = curTQ.tcn
                
    return maxTCNFound
    
                            
def run():
    """
    Execute the test and return true if the test passed.
    """

    global allOK
    
    maxTCN = 99
    
    # first, replay the recording with no maximum, to verify this is still a
    # valid scenario
    noMaxFilePrefix = "ubuntu_maxtcn_none_lazyshad"
    if (DoReplay(noMaxFilePrefix, 0)):
        maxFound = GetMaxTCN(noMaxFilePrefix)
        if (maxFound <= maxTCN):
            print(INDENT_SPACES + "INVALID SCENARIO - NO TCNS FOUND ABOVE " +
                str(maxTCN))
            return False
            
    # now, replay with the limit, to verify the TCN was really limited
    # when the TCN EXCEEDS the limit, the taint is removed by taint2, so the
    # limit itself may appear in valid output
    maxFilePrefix = "ubuntu_maxtcn_99_lazyshad"
    if (DoReplay(maxFilePrefix, maxTCN)):
        maxFound = GetMaxTCN(maxFilePrefix)
        if (maxFound > maxTCN):
            print(INDENT_SPACES + "FOUND MAXIMUM TCN OF " + str(maxFound) +
                " WHICH IS ABOVE THE REQUESTED MAXIMUM OF " + str(maxTCN))
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
    