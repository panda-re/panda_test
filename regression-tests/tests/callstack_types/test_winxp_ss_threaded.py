# test_winxp_ss_threaded.py
# Test the threaded stack_type option of the callstack_instr plugin with
# Windows XP OSI support.
#
# Created:  10-JUN-2019

import filecmp
import os

import ptest

INDENT_SPACES = "                 "
STRING_MATCHES_SUFFIX = "_string_matches.txt"
STRING_MATCHES_EXP_SUFFIX = "_string_matches_expected.txt"
OUTPUT_PREFIX = "winxp_ss_threaded"

STRINGSEARCH = ptest.Plugin("stringsearch", str="value", callers=128)
CALLSTACK = ptest.Plugin("callstack_instr", stack_type="threaded")

# setup for "-net nic -net user"
NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

# "-usbdevice tablet" is deprecated in favor of "-device usb-tablet -usb"
TABLET = ptest.Device(ptest.Device.USB_TABLET)

QEMU = ptest.Qemu(ptest.Qemu.I386, 500, NETDEV, E1000DEV, TABLET,
    options="-usb")

# use os.path.join so needn't worry about what the separator character is on
# this system
REPLAY_PATH = os.path.join("windowsxp", "wxpsp3_mtsf_morefns_90p")
TEST_DIR_PREFIX = os.path.join("tests", "callstack_types")

REPLAY_SS = ptest.Replay(REPLAY_PATH, QEMU, CALLSTACK, STRINGSEARCH,
    os="windows-32-xpsp3")

# created files that haven't been cleaned up yet
new_files = set()

# are all the files in new_files from tests that ran OK?
all_ok = False
    
def run():
    """
    Execute the test and return true if the test passed.
    """
    global all_ok
    
    # run the test with threaded stack_type specified
    retcode = REPLAY_SS.run()
    
    # need string matches file regardless of how things went
    sm_filename = os.path.join(TEST_DIR_PREFIX,
        OUTPUT_PREFIX + STRING_MATCHES_SUFFIX)
    os.rename(STRING_MATCHES_SUFFIX, sm_filename)
    new_files.add(sm_filename)
    
    # also helpful to keep stdout and stderr in case got wrong results
    stdout_filename = os.path.join(TEST_DIR_PREFIX, OUTPUT_PREFIX + ".stdout")
    new_files.add(stdout_filename)
    REPLAY_SS.copy_stdout(stdout_filename)
    stderr_filename = os.path.join(TEST_DIR_PREFIX, OUTPUT_PREFIX + ".stderr")
    new_files.add(stderr_filename)
    REPLAY_SS.copy_stderr(stderr_filename)
        
    if (retcode != 0):
        print(INDENT_SPACES + "***** ERROR EXECUTING PANDA *****")
        return False
    
    # verify that the string matches file has the expected content
    sm_expected_filename = os.path.join(TEST_DIR_PREFIX,
        OUTPUT_PREFIX + STRING_MATCHES_EXP_SUFFIX)
    if (not filecmp.cmp(sm_filename, sm_expected_filename)):
        print(INDENT_SPACES +
            "***** STRING MATCHES FILE NOT AS EXPECTED *****")
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
    