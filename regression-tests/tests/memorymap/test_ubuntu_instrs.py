# test_ubuntu_instrs.py
# Test the memorymap plugin when instruction counts are used to identify the
# instructions of interest.
#
# Created:  13-SEP-2019

import os
import filecmp

import ptest

INDENT_SPACES = "                 "

EXPECTED_ITEMS = [
    "pc=0xb764ee54 instr_count=6653621 process=iscsid pid=996 tid=996 in_kernel=false image_name=libc-2.23.so image_path=/lib/i386-linux-gnu/libc-2.23.so image_base=0xb7572000",
    "pc=0xb7732c2d instr_count=6653752 process=iscsid pid=996 tid=996 in_kernel=false image_name=[???] image_path=(null) image_base=0xb7732000",
    "pc=0x080dbbd0 instr_count=6659763 process=bash pid=1136 tid=1136 in_kernel=false image_name=bash image_path=/bin/bash image_base=0x08048000",
    "pc=0xc11c4d93 instr_count=7705320 process=linux_multithre pid=1153 tid=1153 in_kernel=false image_name=(unknown) image_path=(unknown) image_base=(unknown)",
    "pc=0xb76cce0f instr_count=18326247 process=linux_multithre pid=1153 tid=1156 in_kernel=false image_name=libc-2.23.so image_path=/lib/i386-linux-gnu/libc-2.23.so image_base=0xb75ea000",
    "pc=0xb77a6345 instr_count=21333671 process=linux_multithre pid=1153 tid=1155 in_kernel=false image_name=libpthread-2.23.so image_path=/lib/i386-linux-gnu/libpthread-2.23.so image_base=0xb77a0000",
    "pc=0xb769a7cc instr_count=21364855 process=linux_multithre pid=1153 tid=1153 in_kernel=false image_name=libc-2.23.so image_path=/lib/i386-linux-gnu/libc-2.23.so image_base=0xb75ea000"
]

TEST_PREFIX = "ubuntu_instrs"
STDOUT_NAME = os.path.join("tests", "memorymap", TEST_PREFIX + ".stdout")
STDERR_NAME = os.path.join("tests", "memorymap", TEST_PREFIX + ".stderr")
REPLAY_PATH = os.path.join("ubuntuserver", "linux_mt_sf")

CONF_NAME = os.path.join("shared_configs", "ubuntuserver_kernelinfo.conf")

OSI = ptest.Plugin("osi")
OSI_LINUX = ptest.Plugin("osi_linux", kconf_file=CONF_NAME,
    kconf_group="UbuntuServer")

# setup for "-net nic -net user"
NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 2048, NETDEV, E1000DEV)

MM = ptest.Plugin("memorymap",
    instr_counts="7705320-21364855-21333671-18326247-6659763-6653752-6653621")

REPLAY_MM = ptest.Replay(REPLAY_PATH, QEMU, OSI, OSI_LINUX, MM,
    os="linux-32-.+")

allOK = False
new_files = set()

def run():
    global allOK
    
    # Run the scenario
    retcode = REPLAY_MM.run()
    
    REPLAY_MM.copy_stdout(STDOUT_NAME)
    new_files.add(STDOUT_NAME)
    
    if (retcode != 0):
        print(INDENT_SPACES + "***** ERROR EXECUTING PANDA *****")
        REPLAY_MM.copy_stderr(STDERR_NAME)
        new_files.add(STDERR_NAME)
        REPLAY_MM.dump_console(stdout=False, stderr=True)
        return False

    # verify got expected number of reports, and they report the correct data
    checked = 0
    mm_reports = 0
    with open(STDOUT_NAME, 'r') as in_file:
        for line in in_file:
            line = line.strip()
            if (line.startswith("pc=0x")):
                mm_reports = mm_reports + 1
                try:
                    ndx = EXPECTED_ITEMS.index(line)
                    checked = checked | (2**ndx)
                except ValueError:
                    pass
    
    if (mm_reports != len(EXPECTED_ITEMS)):
        print(INDENT_SPACES + "***** UNEXPECTED REPORTS FOUND *****")
        return False
        
    if (checked != 127):
        print(INDENT_SPACES +
            "***** AT LEAST ONE OF THE EXPECTED ENTRIES WAS NOT FOUND *****")
        return False
        
    allOK = True
    return True

def cleanup():
    global allOK
    
    if (allOK):
        while (len(new_files) > 0):
            cur_file = new_files.pop()
            try:
                os.remove(cur_file)
            except OSError:
                pass        # empty statement
    else:
        # empty the set too
        while (len(new_files) > 0):
            cur_file = new_files.pop()
            print(INDENT_SPACES + cur_file)
        print(INDENT_SPACES +
            "The above output files have not been deleted in hopes they cue " +
            "you in as to what went wrong.")
