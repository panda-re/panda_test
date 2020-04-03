# test_ubuntu_pcs.py
# Test the memorymap plugin when pcs are used to identify the instructions of
# interest.  The pcs are specified in hexadecimal, octal, and decimal, to verify
# all radices are handled properly.
#
# Created:  13-SEP-2019

import os
import filecmp

import ptest

INDENT_SPACES = "                 "

# some entries which have been separately verified; used to spot check results
EXPECTED_ITEMS = [
    "pc=0xb7732c2d instr_count=54667 process=iscsid pid=996 tid=996 in_kernel=false image_name=[???] image_path=(null) image_base=0xb7732000",
    "pc=0xb7732c2d instr_count=194952 process=iscsid pid=996 tid=996 in_kernel=false image_name=[???] image_path=(null) image_base=0xb7732000",
    "pc=0x080dbbd0 instr_count=6659763 process=bash pid=1136 tid=1136 in_kernel=false image_name=bash image_path=/bin/bash image_base=0x08048000",
    "pc=0xb76cce0f instr_count=14217492 process=linux_multithre pid=1153 tid=1154 in_kernel=false image_name=libc-2.23.so image_path=/lib/i386-linux-gnu/libc-2.23.so image_base=0xb75ea000",
    "pc=0xb77a6352 instr_count=14217505 process=linux_multithre pid=1153 tid=1154 in_kernel=false image_name=libpthread-2.23.so image_path=/lib/i386-linux-gnu/libpthread-2.23.so image_base=0xb77a0000",
    "pc=0xb76cce0f instr_count=18326247 process=linux_multithre pid=1153 tid=1156 in_kernel=false image_name=libc-2.23.so image_path=/lib/i386-linux-gnu/libc-2.23.so image_base=0xb75ea000",
    "pc=0xb77a6352 instr_count=18326260 process=linux_multithre pid=1153 tid=1156 in_kernel=false image_name=libpthread-2.23.so image_path=/lib/i386-linux-gnu/libpthread-2.23.so image_base=0xb77a0000",
    "pc=0xc143aac4 instr_count=20748535 process=linux_multithre pid=1153 tid=1155 in_kernel=false image_name=(unknown) image_path=(unknown) image_base=(unknown)",
    "pc=0xb76cce0f instr_count=21333661 process=linux_multithre pid=1153 tid=1155 in_kernel=false image_name=libc-2.23.so image_path=/lib/i386-linux-gnu/libc-2.23.so image_base=0xb75ea000",
    "pc=0xb77a6352 instr_count=21333674 process=linux_multithre pid=1153 tid=1155 in_kernel=false image_name=libpthread-2.23.so image_path=/lib/i386-linux-gnu/libpthread-2.23.so image_base=0xb77a0000"
]

EXPECTED_COUNTS = dict([
        ('pc=0xb7732c2d', 37),
        ('pc=0x080dbbd0', 1),
        ('pc=0xb76cce0f', 3),
        ('pc=0xb77a6352', 3),
        ('pc=0xc143aac4', 406144)
])

TEST_PREFIX = "ubuntu_pcs"
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

# 3077778477 = 0xb7732c2d
# 026733147017 = 0xb76cce0f
MM = ptest.Plugin("memorymap",
    pcs="0x080dbbd0-3077778477-0Xc143aac4-026733147017-0xb77a6352")

REPLAY_MM = ptest.Replay(REPLAY_PATH, QEMU, OSI, OSI_LINUX, MM,
    os="linux-32-.+")

actual_counts = dict([
        ('pc=0xb7732c2d', 0),
        ('pc=0x080dbbd0', 0),
        ('pc=0xb76cce0f', 0),
        ('pc=0xb77a6352', 0),
        ('pc=0xc143aac4', 0)
])

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

    # verify got expected number of reports (remember, a particular PC may
    # be executed at more than one guest instruction count)
    # also spot check several of the entries that have been separately verified
    checked = 0
    extras_found = 0
    with open(STDOUT_NAME, 'r') as in_file:
        for line in in_file:
            line = line.strip()
            if (line.startswith("pc=0x")):
                try:
                    ndx = EXPECTED_ITEMS.index(line)
                    checked = checked | (2**ndx)
                except ValueError:
                    pass
                try:
                    cur_count = actual_counts[line[0:13]]
                    actual_counts[line[0:13]] = cur_count + 1
                except KeyError:
                    extras_found = extras_found + 1
    
    if (extras_found != 0):
        print(INDENT_SPACES + "***** REPORTS FOR UNEXPECTED PCS FOUND *****")
        return False
        
    # make sure got exactly the right number for each PC requested
    for cur_key, expected_count in EXPECTED_COUNTS.items():
        try:
            actual_count = actual_counts[cur_key]
            if (actual_count != expected_count):
                print(INDENT_SPACES + "***** GOT " + str(actual_count) + 
                    " REPORTS FOR PC " + cur_key + ", EXPECTED " + 
                    str(expected_count) + " *****")
                return False
        except KeyError:
            print(INDENT_SPACES + "***** PROGRAMMING ERROR *****")
            return False
        
    if (checked != 1023):
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
