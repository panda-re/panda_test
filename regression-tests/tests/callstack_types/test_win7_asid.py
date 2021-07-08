# test_win7_asid.py
# Test the asid stack_type option of the callstack_instr plugin.  This includes
# both explicitly setting the stack_type, and it being implicitly selected
# because the -os switch was not used.
#
# Created:  06-JUN-2019

import filecmp
import os

import ptest

INDENT_SPACES = "                 "
STRING_MATCHES_SUFFIX = "_string_matches.txt"

STRINGSEARCH = ptest.Plugin("stringsearch", str="value", callers=128)

# setup for "-net nic -net user"
NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

# "-usbdevice tablet" is deprecated in favor of "-device usb-tablet -usb"
TABLET = ptest.Device(ptest.Device.USB_TABLET)

QEMU = ptest.Qemu(ptest.Qemu.I386, 4096, NETDEV, E1000DEV, TABLET,
    options="-usb")

# use os.path.join so needn't worry about what the separator character is on
# this system
REPLAY_PATH = os.path.join("windows7", "win7_mtsf_morefns_89p")
TEST_DIR_PREFIX = os.path.join("tests", "callstack_types")
    
# created files that haven't been cleaned up yet
new_files = set()

# are all the files in new_files from tests that ran OK?
all_ok = False

def do_replay(file_prefix, callstack_plugin):
    """
    Replay the recording using the given callstack_instr plugin, using the given
    file prefix for the standard out and standard error files, and for the
    string matches file prefix.
    Returns True if the replay finished OK, and False if it did not.
    """

    replay_ss = ptest.Replay(REPLAY_PATH, QEMU, STRINGSEARCH, callstack_plugin)
    retcode = replay_ss.run()
    stdout_filename = os.path.join(TEST_DIR_PREFIX, file_prefix + ".stdout")
    new_files.add(stdout_filename)
    stderr_filename = os.path.join(TEST_DIR_PREFIX, file_prefix + ".stderr")
    new_files.add(stderr_filename)
    replay_ss.copy_stdout(stdout_filename)
    replay_ss.copy_stderr(stderr_filename)
    stdout_file = open(stdout_filename, "r")
    stderr_file = open(stderr_filename, "r")
    if (retcode != 0):
        print(INDENT_SPACES + "***** ERROR EXECUTING PANDA *****")
        stderr_file.close()
        stdout_file.close()
        stderr_file = open(stderr_file.name, "r")
        print(stderr_file.read())
        return False
        
    sm_file = os.path.join(TEST_DIR_PREFIX, file_prefix + STRING_MATCHES_SUFFIX)
    os.rename(STRING_MATCHES_SUFFIX, sm_file)
    new_files.add(sm_file)
    
    # make ready for next run
    stderr_file.close()
    stdout_file.close()
        
    return True
    
def run():
    """
    Execute the test and return true if the test passed.
    """
    global all_ok
    
    # run the test with no stack_type specified
    callstack_no_type = ptest.Plugin("callstack_instr")
    retcode = do_replay("win7_asid_notype", callstack_no_type)
    if (not retcode):
        return False
        
    # verify that the string matches file produced is for stack_type=asid
    # as of 06-JUN-2019, there are 3 formats of stack IDs:
    #    asid:       "(asid=0x<hex number>)"
    #    heuristic:  "(asid=0x<hex number>, sp=0x<hex number>)"
    #    threaded:   "(processID=0x<hex number>, threadID=0x<hex number>)"
    sm_notype_filename = os.path.join(TEST_DIR_PREFIX,
        "win7_asid_notype" + STRING_MATCHES_SUFFIX)
    with open(sm_notype_filename, "r") as sm_file:
        for line in sm_file:
            if (("(asid=0x" not in line) or (", sp=0x" in line)):
                print(INDENT_SPACES + "***** DEFAULT TYPE NOT asid *****")
                return False
                    
    # run the test with an explicit stack_type of asid
    callstack_asid = ptest.Plugin("callstack_instr", stack_type="asid")
    retcode = do_replay("win7_asid", callstack_asid)
    if (not retcode):
        return False
    
    # verify that the string matches files produced from each run are identical
    sm_asid_filename = os.path.join(TEST_DIR_PREFIX,
        "win7_asid" + STRING_MATCHES_SUFFIX)
    if (not filecmp.cmp(sm_notype_filename, sm_asid_filename)):
        print(INDENT_SPACES +
            "***** IMPLICIT AND EXPLICIT asid STRING MATCHES FILES " +
            "ARE DIFFERENT *****")
        return False

    all_ok = True
    return True
    
def cleanup():
    """
    A cleanup function called when the test completes regardless of whether or
    not the test passed.
    """
    global all_ok
    
    if (all_ok):
        while (len(new_files) > 0):
            cur_file = new_files.pop()
            try:
                os.remove(cur_file)
            except OSError:
                pass
    else:
        while (len(new_files) > 0):
            cur_file = new_files.pop()
            print(INDENT_SPACES + cur_file)
        print(INDENT_SPACES +
            "The above output files have not been deleted in hopes they cue " +
            "you in as to what went wrong.")
    