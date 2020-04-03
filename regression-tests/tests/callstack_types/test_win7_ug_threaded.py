# test_win7_ug_threaded.py
# Test the unigrams plugin with the threaded stack_type option of the
# callstack_instr plugin.
#
# Created:  11-JUN-2019

import filecmp
import numpy as np
import os
import sys
import time
from struct import unpack

import ptest

STACKKIND_INDEX = 0
CALLER_INDEX = 1
PC_INDEX = 2
SID1_INDEX = 3
SID2_INDEX = 4
INKERNEL_INDEX = 5
HIST_INDEX = 6

def load_hist(f):
    ulong_size = unpack("<i", f.read(4))[0]
    ulong_fmt = '<u%d' % ulong_size
    stack_type_size = unpack("<i", f.read(4))[0]
    stack_type_fmt = '<u%d' % stack_type_size
    rectype = np.dtype( [ ('stackKind', stack_type_fmt), ('caller', ulong_fmt),
    ('pc', ulong_fmt), ('sidFirst', ulong_fmt), ('sidSecond', ulong_fmt),
    ('isKernelMode', '<u1'), ('hist', '<i4', 256) ] )
    data = np.fromfile(f, dtype=rectype)
    return data
    
def compare_unigrams(actual_filename, expected_filename):
    """
    Compare the unigrams in expected_filename with the corresponding recordds in
    actual_filename.  The former only contains records whose PCs are in the
    range of interest.  Both files should have their records in the same order.
    Return True if the selected records in the two files match, and False
    otherwise.  Also returns False if the expected output has a record that
    is not included in the actual output.
    """

    # the actual unigrams output files are too large for Git
    # as a result, the expected_filename is a subset of the expected output, but
    # in text format; only the records within the PC range expected are in the
    # expected_filename, and they are in the same order as in the original file
    
    # assume all will be OK
    they_match = True
    found_records_in_range = False
    
    # read as binary, to prevent attempts to treat as utf8
    unigrams1 = load_hist(open(actual_filename, 'rb'))
    unigrams1List = unigrams1.tolist()
    
    # the expected results file has line feeds in the middle of the records
    # (added by Python - I can't figure out how to make it STOP), so to form a
    # record I need to concatenate multiple lines together
    ug2records = []
    with open(expected_filename, 'r') as ifile:
        subrec_count = 0
        cur_record = ""
        for ug2_line in ifile:
            # there are always lines in a record
            cur_record = cur_record + " " + ug2_line.strip()
            subrec_count = subrec_count + 1
            if (subrec_count == 12):
                ug2records.append(cur_record)
                subrec_count = 0
                cur_record = ""
    ug1_index = 0
    for ug2_line in ug2records:
        # parse ug2_line into its parts ug2Kind, ug2caller, ug2pc, ug2sid1,
        #                                                       ug2sid2, ug2hist
        # format is "(<kind>L, <caller>L, <pc>L, <stack id1>L, <stack id2>L,
        #             <in kernel flag>,
        #             array([<256 integers separated by commas>], dtype=int32))"
        ug2_splits = ug2_line.split()
        split_index = 0
        itemS = ug2_splits[split_index][1:-2]
        split_index = split_index + 1
        ug2Kind = int(itemS)
        
        itemS = ug2_splits[split_index][0:-2]
        split_index = split_index + 1
        ug2caller = int(itemS)
        
        itemS = ug2_splits[split_index][0:-2]
        split_index = split_index + 1
        ug2pc = int(itemS)
        
        itemS = ug2_splits[split_index][0:-2]
        split_index = split_index + 1
        ug2sid1 = int(itemS)
        
        itemS = ug2_splits[split_index][0:-2]
        split_index = split_index + 1
        ug2sid2 = int(itemS)
 
        itemS = ug2_splits[split_index][0:-1]
        split_index = split_index + 1
        ug2inKernel= int(itemS)
       
        ug2hist = []
        itemS = ug2_splits[split_index][7:-1]
        split_index = split_index + 1
        ug2hist.append(int(itemS))
        for hist_index in range(254):
            itemS = ug2_splits[split_index][0:-1]
            split_index = split_index + 1
            ug2hist.append(int(itemS))
        itemS = ug2_splits[split_index][0:-2]
        split_index = split_index + 1
        ug2hist.append(int(itemS))

        # look for the next record from unigrams1 that matches this PC
        need_new_ug2 = False
        while ((not need_new_ug2) and (ug1_index < len(unigrams1List))):
            rec1 = unigrams1List[ug1_index]
            if (rec1[STACKKIND_INDEX] == ug2Kind):
                if (rec1[PC_INDEX] == ug2pc):
                    # must be within range of PCs care about, as all the PCs in
                    # the expected output are in range
                    found_records_in_range = True
                    need_new_ug2 = True
                    # do the other parts of the histogram index match?
                    if ((rec1[CALLER_INDEX] != ug2caller) or (rec1[SID1_INDEX]
                        != ug2sid1) or (rec1[SID2_INDEX] != ug2sid2) or
                        (rec1[INKERNEL_INDEX] != ug2inKernel)):
                        they_match = False
                    else:
                        # do the histograms themselves match?
                        hist1 = rec1[HIST_INDEX].tolist()
                        if (hist1 != ug2hist):
                            they_match = False
            else:
                # the two records weren't even generated for the same stack type
                they_match = False
            ug1_index = ug1_index + 1
        # if didn't find a match in actual file, then ran out before the
        # expected record was found
        if (not need_new_ug2):
            they_match = False
    if (not found_records_in_range):
        they_match = False
    return they_match
    
INDENT_SPACES = "                 "
OUTPUT_PREFIX = "win7_ug_threaded"
READ_OUTPUT = "unigram_mem_read_report.bin"
WRITE_OUTPUT = "unigram_mem_write_report.bin"
READ_OUTPUT_EXP = "unigram_mem_read_report_expected.bin"
WRITE_OUTPUT_EXP = "unigram_mem_write_report_expected.bin"

UNIGRAMS = ptest.Plugin("unigrams")
CALLSTACK = ptest.Plugin("callstack_instr", stack_type="threaded")

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

REPLAY_SS = ptest.Replay(REPLAY_PATH, QEMU, CALLSTACK, UNIGRAMS,
    os="windows-32-7")

# created files that haven't been cleaned up yet
new_files = set()

# are all the files in new_files from tests that ran OK?
all_ok = False
    
def run():
    """
    Execute the test and return true if the test passed.
    """
    global all_ok
    
    # create the unigrams output using the heuristic stack_type
    retcode = REPLAY_SS.run()
    
    # rename the output files
    read_filename = os.path.join(TEST_DIR_PREFIX,
        OUTPUT_PREFIX + "_" + READ_OUTPUT)
    os.rename(READ_OUTPUT, read_filename)
    new_files.add(read_filename)
    write_filename = os.path.join(TEST_DIR_PREFIX,
        OUTPUT_PREFIX + "_" + WRITE_OUTPUT)
    os.rename(WRITE_OUTPUT, write_filename)
    new_files.add(write_filename)
    
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
    
    # this is a hack, but unigrams (at least with threaded stack_type) can
    # produce different output even when rerun with same PANDA binary and
    # settings (they're quite consistent with asid stack type, which is the
    # only stack type that used to be supported, but not helpful for verifying
    # the stack ID portion of the unigrams output)
    # so far, those differences are always for PCs outside of the binary (so
    # they're in the OS or OS libraries somewhere)
    # the binary analyzed has addresses from 0x401000 through 0x402E79
    # as the expected output is a subset of the full output (as otherwise the
    # files are too big for git) which only includes records with PCs in that
    # range, we can rely on that to subset the actual data the same way
    # verify that the read output file has the expected content
    read_expected_filename = os.path.join(TEST_DIR_PREFIX,
        OUTPUT_PREFIX + "_" + READ_OUTPUT_EXP)
    if (not compare_unigrams(read_filename, read_expected_filename)):
        print(INDENT_SPACES +
            "***** READ OUTPUT FILE NOT AS EXPECTED *****")
        return False

    # verify that the write output file has the expected content
    write_expected_filename = os.path.join(TEST_DIR_PREFIX,
        OUTPUT_PREFIX + "_" + WRITE_OUTPUT_EXP)
    if (not compare_unigrams(write_filename, write_expected_filename)):
        print(INDENT_SPACES +
            "***** WRITE OUTPUT FILE NOT AS EXPECTED *****")
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
    
