# test_win2k_tp_threaded.py
# Test the textprinter plugin with the threaded stack type option of the
# callstack_instr plugin.
#
# Created:  10-JUN-2019

import filecmp
import os

import ptest

INDENT_SPACES = "                 "
OUTPUT_PREFIX = "win2k_tp_threaded"

REPLAY_PATH = os.path.join("windows2k", "win2k_mtsf_morefns")
TEST_DIR_PREFIX = os.path.join("tests", "callstack_types")
READ_TP_FILENAME = "read_tap_buffers.txt.gz"
WRITE_TP_FILENAME = "write_tap_buffers.txt.gz"
READ_TP_EXPECTED_FILENAME = "win2k_tp_threaded_read_expected.txt.gz"
WRITE_TP_EXPECTED_FILENAME = "win2k_tp_threaded_write_expected.txt.gz"

TEXTPRINTER = ptest.Plugin("textprinter")
CALLSTACK = ptest.Plugin("callstack_instr", stack_type="threaded")

# setup for "-net nic,model=ne2k_pci -net user"
NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
NE2KPCI = ptest.Device(ptest.Device.NE2K_PCI, backend=NETDEV)

# "-usbdevice tablet" is deprecated in favor of "-device usb-tablet -usb"
TABLET = ptest.Device(ptest.Device.USB_TABLET)

QEMU = ptest.Qemu(ptest.Qemu.I386, 512, NETDEV, NE2KPCI, TABLET,
    vga=ptest.Qemu.CIRRUS, options="-usb")

REPLAY_TP = ptest.Replay(REPLAY_PATH, QEMU, CALLSTACK, TEXTPRINTER,
    os="windows-32-2000")

# created files that haven't been cleaned up yet
new_files = set()

# are all the files in new_files from tests that ran OK?
all_ok = False
    
def run():
    """
    Execute the test and return true if the test passed.
    """
    global all_ok
    
    # textprinter expects tap_points.txt input file to be in the directory run
    # from, but we are not there (yet)
    in_wd = os.getcwd()
    os.chdir(TEST_DIR_PREFIX)
    
    # run the test with threaded stack type
    retcode = REPLAY_TP.run()
    
    # text printer output goes to files with fixed names
    read_op_filename = os.path.join(TEST_DIR_PREFIX, READ_TP_FILENAME)
    new_files.add(read_op_filename)
    write_op_filename = os.path.join(TEST_DIR_PREFIX, WRITE_TP_FILENAME)
    new_files.add(write_op_filename)
    
    # also helpful to keep stdout and stderr in case got wrong results
    stdout_filename = os.path.join(TEST_DIR_PREFIX, OUTPUT_PREFIX + ".stdout")
    new_files.add(stdout_filename)
    REPLAY_TP.copy_stdout(OUTPUT_PREFIX + ".stdout")
    stderr_filename = os.path.join(TEST_DIR_PREFIX, OUTPUT_PREFIX + ".stderr")
    new_files.add(stderr_filename)
    REPLAY_TP.copy_stderr(OUTPUT_PREFIX + ".stderr")
        
    if (retcode != 0):
        print(INDENT_SPACES + "***** ERROR EXECUTING PANDA *****")
        os.chdir(in_wd)
        return False
    
    # verify that the tap buffers output files have the expected content
    # this seems a lot simpler than duplicating the activities of PANDA's
    # split_taps.py script, especially as some of that output is still not human
    # readable
    if (not filecmp.cmp(READ_TP_FILENAME, READ_TP_EXPECTED_FILENAME)):
        print(INDENT_SPACES +
            "***** READ TAP BUFFERS FILE NOT AS EXPECTED *****")
        os.chdir(in_wd)
        return False
    if (not filecmp.cmp(WRITE_TP_FILENAME, WRITE_TP_EXPECTED_FILENAME)):
        print(INDENT_SPACES +
            "***** WRITE TAP BUFFERS FILE NOT AS EXPECTED *****")
        os.chdir(in_wd)
        return False
        
    os.chdir(in_wd)
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
    