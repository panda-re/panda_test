# test_debian64_pcs.py
# Test the memorymap plugin with a 64-bit guest.
#
# Created:  18-SEP-2019

import os
import filecmp

import ptest

INDENT_SPACES = "                 "

# some entries which have been separately verified; used to spot check results
EXPECTED_ITEMS = [
    "pc=0xffffffff8120d1c9 instr_count=583632 process=linux_multithre pid=789 tid=789 in_kernel=false image_name=(unknown) image_path=(unknown) image_base=(unknown)",
    "pc=0x00007f24fca00c20 instr_count=668951 process=linux_multithre pid=789 tid=789 in_kernel=false image_name=ld-2.24.so image_path=/lib/x86_64-linux-gnu/ld-2.24.so image_base=0x00007f24fca00000",
    "pc=0x00007f24fc52cac1 instr_count=1269232 process=linux_multithre pid=789 tid=789 in_kernel=false image_name=libc-2.24.so image_path=/lib/x86_64-linux-gnu/libc-2.24.so image_base=0x00007f24fc444000",
    "pc=0x00007f24fc52cac1 instr_count=1294578 process=linux_multithre pid=789 tid=790 in_kernel=false image_name=libc-2.24.so image_path=/lib/x86_64-linux-gnu/libc-2.24.so image_base=0x00007f24fc444000",
    "pc=0x00007f24fc52cac1 instr_count=1318398 process=linux_multithre pid=789 tid=789 in_kernel=false image_name=libc-2.24.so image_path=/lib/x86_64-linux-gnu/libc-2.24.so image_base=0x00007f24fc444000",
    "pc=0x00007f24fc52cac1 instr_count=1341140 process=linux_multithre pid=789 tid=789 in_kernel=false image_name=libc-2.24.so image_path=/lib/x86_64-linux-gnu/libc-2.24.so image_base=0x00007f24fc444000",
    "pc=0x00007f24fc52cac1 instr_count=1344485 process=linux_multithre pid=789 tid=792 in_kernel=false image_name=libc-2.24.so image_path=/lib/x86_64-linux-gnu/libc-2.24.so image_base=0x00007f24fc444000",
    "pc=0x00007f24fc52cac1 instr_count=1346662 process=linux_multithre pid=789 tid=791 in_kernel=false image_name=libc-2.24.so image_path=/lib/x86_64-linux-gnu/libc-2.24.so image_base=0x00007f24fc444000",
    "pc=0x00007f7c33442100 instr_count=2421531 process=xfce4-terminal pid=776 tid=776 in_kernel=false image_name=libglib-2.0.so.0.5000.3 image_path=/lib/x86_64-linux-gnu/libglib-2.0.so.0.5000.3 image_base=0x00007f7c333b2000",
    "pc=0x00007f7c338e6c93 instr_count=2421635 process=xfce4-terminal pid=776 tid=776 in_kernel=false image_name=libgobject-2.0.so.0.5000.3 image_path=/usr/lib/x86_64-linux-gnu/libgobject-2.0.so.0.5000.3 image_base=0x00007f7c338d5000"
]

EXPECTED_COUNTS = dict([
        ('pc=0x00007f24fca00c20', 1),
        ('pc=0x00007f24fc52cac1', 6),
        ('pc=0xffffffff8120d1c9', 1),
        ('pc=0x000000008120d1cd', 0),
        ('pc=0x00007f7c33442100', 120),
        ('pc=0x00007f7c338e6c93', 4)
])

TEST_PREFIX = "debian64_pcs"
STDOUT_NAME = os.path.join("tests", "memorymap", TEST_PREFIX + ".stdout")
STDERR_NAME = os.path.join("tests", "memorymap", TEST_PREFIX + ".stderr")
REPLAY_PATH = os.path.join("debian64", "linux64_mt_sf_83to85")

CONF_NAME = os.path.join("shared_configs", "debian_kernelinfo.conf")

OSI = ptest.Plugin("osi")
OSI_LINUX = ptest.Plugin("osi_linux", kconf_file=CONF_NAME,
    kconf_group="debian4.9_amd64")

# setup for "-net nic -net user"
NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000DEV = ptest.Device(ptest.Device.E1000, backend=NETDEV)

TABLET = ptest.Device(ptest.Device.USB_TABLET)

QEMU = ptest.Qemu(ptest.Qemu.X86_64, 2048, NETDEV, E1000DEV, TABLET,
    options="-usb")

# includes cases of omitting leading 0s, 8-leading-fs case, and a no-match case
# on purpose
MM = ptest.Plugin("memorymap",
    pcs="0x00007f24fca00c20-0x7f24fc52cac1-0xffffffff8120d1c9-0x8120d1cd-0x00007f7c33442100-0x00007f7c338e6c93")

REPLAY_MM = ptest.Replay(REPLAY_PATH, QEMU, OSI, OSI_LINUX, MM,
    os="linux-64-.+")

actual_counts = dict([
        ('pc=0x00007f24fca00c20', 0),
        ('pc=0x00007f24fc52cac1', 0),
        ('pc=0xffffffff8120d1c9', 0),
        ('pc=0x000000008120d1cd', 0),
        ('pc=0x00007f7c33442100', 0),
        ('pc=0x00007f7c338e6c93', 0)
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
                    cur_count = actual_counts[line[0:21]]
                    actual_counts[line[0:21]] = cur_count + 1
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
            "***** AT LEAST ONE OF THE EXPECTED ENTRIES WAS NOT FOUND (flags=" +
            str(checked) + ") *****")
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
