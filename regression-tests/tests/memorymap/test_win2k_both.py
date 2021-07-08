# test_win2k_both.py
# Test the memorymap plugin when both pcs and instruction counts are used to
# identify the instructions of interest.
#
# Created:  12-SEP-2019

import os
import filecmp

import ptest

INDENT_SPACES = "                 "

# some entries which have been separately verified; used to spot check results
# watch out for image_paths with "\n" in them!
EXPECTED_ITEMS = [
    "pc=0xbff858aa instr_count=20404 process=System pid=8 tid=40 in_kernel=true image_name=atapi.sys image_path=atapi.sys image_base=0xbff83000",
    "pc=0xbff858ac instr_count=20405 process=System pid=8 tid=40 in_kernel=true image_name=atapi.sys image_path=atapi.sys image_base=0xbff83000",
    "pc=0xbff858ac instr_count=60396 process=System pid=8 tid=40 in_kernel=true image_name=atapi.sys image_path=atapi.sys image_base=0xbff83000",
    "pc=0xbfeee8ba instr_count=410033 process=System pid=8 tid=40 in_kernel=true image_name=Ntfs.sys image_path=Ntfs.sys image_base=0xbfeee000",
    "pc=0xbfeee8bd instr_count=410034 process=System pid=8 tid=40 in_kernel=true image_name=Ntfs.sys image_path=Ntfs.sys image_base=0xbfeee000",
    "pc=0xbfeee8bf instr_count=410035 process=System pid=8 tid=40 in_kernel=true image_name=Ntfs.sys image_path=Ntfs.sys image_base=0xbfeee000",
    "pc=0xa0084e6e instr_count=1334882 process=CSRSS.EXE pid=168 tid=196 in_kernel=true image_name=win32k.sys image_path=\??\C:\WINNT\system32\win32k.sys image_base=0xa0000000",
    "pc=0x80064fd2 instr_count=2668000 process=(no current process) pid=NA tid=0 in_kernel=true image_name=hal.dll image_path=\WINNT\System32\hal.dll image_base=0x80062000",
    "pc=0xa007f14c instr_count=5010203 process=CSRSS.EXE pid=168 tid=192 in_kernel=true image_name=win32k.sys image_path=\??\C:\WINNT\system32\win32k.sys image_base=0xa0000000",
    "pc=0xa0088c71 instr_count=10048002 process=explorer.exe pid=744 tid=756 in_kernel=true image_name=win32k.sys image_path=\??\C:\WINNT\system32\win32k.sys image_base=0xa0000000",
    "pc=0xbff858aa instr_count=10197247 process=win_mt_sf_moref pid=412 tid=644 in_kernel=true image_name=atapi.sys image_path=atapi.sys image_base=0xbff83000",
    "pc=0xbff858b4 instr_count=10197250 process=win_mt_sf_moref pid=412 tid=644 in_kernel=true image_name=atapi.sys image_path=atapi.sys image_base=0xbff83000",
    "pc=0xbff858b2 instr_count=10207411 process=win_mt_sf_moref pid=412 tid=644 in_kernel=true image_name=atapi.sys image_path=atapi.sys image_base=0xbff83000",
    "pc=0xbfeee8bd instr_count=12858321 process=System pid=8 tid=24 in_kernel=true image_name=Ntfs.sys image_path=Ntfs.sys image_base=0xbfeee000",
    "pc=0x80069a0f instr_count=12877472 process=System pid=8 tid=24 in_kernel=true image_name=hal.dll image_path=\WINNT\System32\hal.dll image_base=0x80062000"
]

TEST_PREFIX = "win2k_both"
STDOUT_NAME = os.path.join("tests", "memorymap", TEST_PREFIX + ".stdout")
STDERR_NAME = os.path.join("tests", "memorymap", TEST_PREFIX + ".stderr")
REPLAY_PATH = os.path.join("windows2k", "win2k_mtsf_morefns")

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
NE2KPCI = ptest.Device(ptest.Device.NE2K_PCI, backend=NETDEV)

TABLET = ptest.Device(ptest.Device.USB_TABLET)

QEMU = ptest.Qemu(ptest.Qemu.I386, 512, NETDEV, NE2KPCI, TABLET,
    vga=ptest.Qemu.CIRRUS, options="-usb")

# note that 0xbf858ac does not correspond to a guest instruction address
MM = ptest.Plugin("memorymap",
    pcs="0xbfeee8ba-0xbfeee8bd-0xbfeee8bf-0x80069a0f-0xbff858aa-0xbf858ac-0xbff858b2-0xbff858b4",
    instr_counts="20405-60396-1334882-2668000-5010203-10048002")

REPLAY_MM = ptest.Replay(REPLAY_PATH, QEMU, MM, os="windows-32-2000")

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
    expected_reports = 864
    mm_reports = 0
    
    # also spot check several of the entries that have been separately verified
    checked = 0
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
    
    if (mm_reports != expected_reports):
        print(INDENT_SPACES + "***** GOT " + str(mm_reports) +
            " REPORTS, EXPECTED " + str(expected_reports) + " *****")
        return False

    if (checked != 32767):
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
