# test_win2k_full.py
# Test the memorymap plugin when neither pcs nor instruction counts are used to
# identify the instructions of interest.  (This will result in information on
# all instructions being dumped.)  Note that the recording used
# (2k-filetaint-singleproc-singlefile) is one which used to crash when with an
# instruction count discrepancy error when all instructions were dumped.  This
# crash was due to a problem in wintrospection that was fixed as a part of
# creating the memorymap plugin, so it's nice to verify that problem is still
# gone too.
#
# Created:  11-SEP-2019

import datetime
import os
import filecmp

import ptest

INDENT_SPACES = "                 "

# some entries which have been separately verified; used to spot check results
# watch out for image_paths with "\n" in them!
EXPECTED_ITEMS = [
    "pc=0x77f8916a instr_count=1045318 process=CSRSS.EXE pid=168 tid=132 in_kernel=false image_name=ntdll.dll image_path=C:\WINNT\system32\\ntdll.dll image_base=0x77f80000",
    "pc=0x80064bb6 instr_count=1045699 process=CSRSS.EXE pid=168 tid=132 in_kernel=true image_name=hal.dll image_path=\WINNT\System32\hal.dll image_base=0x80062000",
    "pc=0x7c4ee08b instr_count=1046568 process=win_singleproc_ pid=944 tid=556 in_kernel=false image_name=KERNEL32.dll image_path=C:\WINNT\system32\KERNEL32.dll image_base=0x7c4e0000",
    "pc=0x80404213 instr_count=1192240 process=win_singleproc_ pid=944 tid=556 in_kernel=true image_name=ntoskrnl.exe image_path=\WINNT\System32\\ntoskrnl.exe image_base=0x80400000",
    "pc=0x80404241 instr_count=1192251 process=System pid=8 tid=44 in_kernel=true image_name=ntoskrnl.exe image_path=\WINNT\System32\\ntoskrnl.exe image_base=0x80400000",
    "pc=0x80064bfb instr_count=1192656 process=System pid=8 tid=44 in_kernel=true image_name=hal.dll image_path=\WINNT\System32\hal.dll image_base=0x80062000"
]

TEST_PREFIX = "win2k_full"
STDOUT_NAME = os.path.join("tests", "memorymap", TEST_PREFIX + ".stdout")
STDERR_NAME = os.path.join("tests", "memorymap", TEST_PREFIX + ".stderr")

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000 = ptest.Device(ptest.Device.E1000, backend=NETDEV)

QEMU = ptest.Qemu(ptest.Qemu.I386, 1024, NETDEV, E1000, vga=ptest.Qemu.CIRRUS)

MM = ptest.Plugin("memorymap")

REPLAY_MM = ptest.Replay("2k-filetaint-singleproc-singlefile", QEMU, MM,
    os="windows-32-2000")

allOK = False
new_files = set()

def run():
    global allOK
    
    # Run the scenario
    print(INDENT_SPACES +
        "This test takes about 10 minutes to run.  Started at:  " +
        str(datetime.datetime.now()))
    retcode = REPLAY_MM.run()
    
    REPLAY_MM.copy_stdout(STDOUT_NAME)
    new_files.add(STDOUT_NAME)
    
    if (retcode != 0):
        print(INDENT_SPACES + "***** ERROR EXECUTING PANDA *****")
        REPLAY_MM.copy_stderr(STDERR_NAME)
        new_files.add(STDERR_NAME)
        REPLAY_MM.dump_console(stdout=False, stderr=True)
        return False

    # first, verify got the same number of reports from memorymap as there are
    # guest instructions in the recording
    got_total = False
    total_instrs = 0
    mm_reports = 0
    checked = 0
    with open(STDOUT_NAME, 'r') as in_file:
        for line in in_file:
            line = line.strip()
            
            # the line that tells us how many instructions there are total may
            # appear sometime after the reports begin, so have to start counting
            # immediately
            if (line.startswith("pc=0x")):
                mm_reports = mm_reports + 1
                    
                # while we're in here, might as well spot check some lines too
                try:
                    ndx = EXPECTED_ITEMS.index(line)
                    checked = checked | (2**ndx)
                except ValueError:
                    pass
            elif ((not got_total) and line.endswith("total.")):
                last_colon = line.rfind(":")
                post_total = line.rfind("instrs")
                total_text = line[last_colon+1:post_total].strip()
                total_instrs = int(total_text, base=10)
                got_total = True
    
    if (not got_total):
        print(INDENT_SPACES + "***** COULD NOT FIND TOTAL INSTRUCTIONS *****")
        return False
    elif (mm_reports != total_instrs):
        print(INDENT_SPACES + "***** GOT " + str(mm_reports) +
            " REPORTS, EXPECTED " + str(total_instrs) + " *****")
        return False

    if (checked != 63):
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
