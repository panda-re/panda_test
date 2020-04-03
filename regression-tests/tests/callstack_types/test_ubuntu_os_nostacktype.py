# test_ubuntu_os_nostacktype.py
# Test the threaded stack_type of the callstack_instr plugin by having it be
# implicitly selected by specifying the -os switch.  (There is already another
# regression test that explicitly selects the threaded stack_type.)
#
# Created:  07-JUN-2019
# Changed:  07-OCT-2019   Use shared kernel config files.

import os
import tempfile

import ptest

INDENT_SPACES = "                 "
FILE_PREFIX = "ubuntu_os_nostacktype"

# use os.path.join so needn't worry about what the separator character is on
# this system
REPLAY_PATH = os.path.join("ubuntuserver", "linux_mt_sf")
TEST_DIR_PREFIX = os.path.join("tests", "callstack_types")

TAINTED_INSTR = ptest.Plugin("tainted_instr")
FILE_TAINT = ptest.Plugin("file_taint", filename="positional.bin", pos=True)
OSI = ptest.Plugin("osi")
OSI_LINUX = ptest.Plugin("osi_linux", kconf_file=os.path.join("shared_configs",
    "ubuntuserver_kernelinfo.conf"), kconf_group="UbuntuServer")

# setup for "-net nic -net user"
NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 2048, NETDEV, E1000DEV)
_, PLOG1 = tempfile.mkstemp()
REPLAY_TI = ptest.Replay(REPLAY_PATH, QEMU, FILE_TAINT, OSI, OSI_LINUX,
    TAINTED_INSTR, os="linux-32-.+", plog=PLOG1)

# created files that haven't been cleaned up yet
new_files = set()

# are all the files in new_files from tests that ran OK?
all_ok = False
    
def run():
    """
    Execute the test and return true if the test passed.
    """
    global all_ok
    
    retcode = REPLAY_TI.run()
    stdout_filename = os.path.join(TEST_DIR_PREFIX, FILE_PREFIX + ".stdout")
    new_files.add(stdout_filename)
    stderr_filename = os.path.join(TEST_DIR_PREFIX, FILE_PREFIX + ".stderr")
    new_files.add(stderr_filename)
    REPLAY_TI.copy_stdout(stdout_filename)
    REPLAY_TI.copy_stderr(stderr_filename)
    if (retcode != 0):
        print(INDENT_SPACES + "***** ERROR EXECUTING PANDA *****")
        # if it didn't run, there probably isn't a plog file to look at
        return False
    
    # verify that the callstack_instr plugin used threaded stack_type
    is_threaded = False
    with open(stdout_filename) as stdout_file:
        for line in stdout_file:
            line = line.strip()
            if (line == "callstack_instr:  setting up threaded stack_type"):
                is_threaded = True
                break
    if (not is_threaded):
        print(INDENT_SPACES +
            "***** WRONG stack_type USED BY callstack_instr *****")
        return False
        
    # verify that the verifiable callstacks (ie. ones can check in gdb) are
    # correct
    # create dictionary of info on callstacks whose PCs were validated with gdb
    # (well, mostly, as gdb doesn't notice calls made to functions that weren't
    # compiled to use ebp for the stack, but PANDA does)
    # key is the PC, value is the callstack (most recent entries first)
    pc_a = 134514871
    pc_b = 134514639
    pc_c = 3078287487
    validated_info = dict()
    validated_info[pc_a] = [3078251157, 3077378142]
    validated_info[pc_b] = [3078251157, 3077378142]
    validated_info[pc_c] = [3078287487, 134514837, 3078251157, 3077378142]
    # there are actually 3 valid callstacks for PC 3078287487, one each for when
    # in process_value1, process_value2 or process_value3
    pv1_cs = [3078287487, 134514605, 3078251157, 3077378142]
    pv3_cs = [3078287487, 134515069, 3078251157, 3077378142]
    verified_info = dict()
    verified_info[pc_a] = False
    verified_info[pc_b] = False
    verified_info[pc_c] = False
    pv1_verified = False
    pv3_verified = False
    
    mismatch_found = False
    with ptest.PlogReader(PLOG1) as plr:
        for msg_no, msg in enumerate(plr):
            field_info_list = msg.ListFields()
            # for each item in list, item 0 is the FieldDescriptor, item 1 is
            # its value
            # not every message has the tainted_instr field of interest, so
            # HasField can't be used to find the messages of interest (it just
            # checks to see if the field has something in it, and will throw an
            # exception if the field doesn't even exist)
            cur_index = 0
            pc_index = -1
            ti_index = -1
            for field_info in field_info_list:
                if (field_info[0].name == "pc"):
                    # is the PC for this record of interest?
                    if (field_info[1] in validated_info):
                        pc_index = cur_index
                elif (field_info[0].name == "tainted_instr"):
                    ti_index = cur_index
                cur_index = cur_index + 1
            # if have both PC of interest and a tainted_instr that goes with it,
            # drill down into the taintedInstr>callStack>addr and verify it is
            # good
            if ((pc_index > -1) and (ti_index > -1)):
                ti_field_info = field_info_list[ti_index]
                ti_field_info_list = ti_field_info[1].ListFields()
                for ti_field_info in ti_field_info_list:
                    if (ti_field_info[0].name == "call_stack"):
                        cs_field_info_list = ti_field_info[1].ListFields()
                        for cs_field_info in cs_field_info_list:
                            # should be just the one addr subfield
                            cur_pc = field_info_list[pc_index][1]
                            if (cs_field_info[1] == validated_info[cur_pc]):
                                verified_info[cur_pc] = True
                            elif (cur_pc == pc_c):
                                if (cs_field_info[1] == pv1_cs):
                                    pv1_verified = True
                                elif (cs_field_info[1] == pv3_cs):
                                    pv3_verified = True
                                else:
                                    mismatch_found = True
                            else:
                                mismatch_found = True
    if (mismatch_found):
        print(INDENT_SPACES + "***** MISMATCHED CALLSTACK(S) FOUND *****")
        return False
    elif ((False in verified_info.values()) or (not pv1_verified) or (not pv3_verified)):
        print(INDENT_SPACES + "***** EXPECTED CALLSTACK MISSING *****")
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
    