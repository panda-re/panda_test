import os
import re

import ptest

TMP_STDOUT = "/tmp/win7-osi-test.stdout"

TARGET_PID = 3592 
TARGET_PPID = 1440 

# Not all processes are checked since there are so many. I picked a few common
# processes to verify. Once we are sure we can get a handful, it seems like we
# wouldn't be gaining much by checking every single process because of the way
# the kernel structures are laid out (its just a linked list).
EXPECTED_PROCESS_LIST = {
    4: "System",
    248: "smss.exe",
    324: "csrss.exe",
    480: "services.exe",
    684: "svchost.exe",
    1180: "dwm.exe",
    1440: "explorer.exe",
    3592: "procexp.exe"
}

# Not all entries are checked due to the way "osi_test" works. We could be more
# pedantic, but it would be more time consuming to execute - I don't think its
# worth it.
EXPECTED_DYLIB_ENTRIES = [
    (0x77690000, 0x13C000, "ntdll.dll", "C:\\Windows\\SYSTEM32\\ntdll.dll"),
    (0x75B80000, 0x6000, "NSI.dll", "C:\\Windows\\system32\\NSI.dll"),
    (0x758F0000, 0x2D000, "Wintrust.dll", "C:\\Windows\\system32\\Wintrust.dll"),
    (0x74190000, 0xFB000, "WindowsCodecs.dll", "C:\\Windows\\system32\\WindowsCodecs.dll"),
    (0x71470000, 0x18000, "NTDSAPI.dll", "C:\\Windows\\system32\\NTDSAPI.dll")
]

EXPECTED_KERNEL_MODULE_ENTRIES = [
    (0x8280D000, 0x404000, "ntoskrnl.exe", "\\SystemRoot\\system32\\ntoskrnl.exe"),
    (0x89B27000, 0x8000, "rdprefmp.sys", "\\SystemRoot\\system32\\drivers\\rdprefmp.sys"),
    (0x89777000, 0x11000, "termdd.sys", "\\SystemRoot\\system32\\DRIVERS\\termdd.sys"),
    (0x8998A000, 0x3F000, "volsnap.sys", "\\SystemRoot\\system32\\drivers\\volsnap.sys"),
    (0x89A16000, 0x32000, "fvevol.sys", "\\SystemRoot\\System32\\DRIVERS\\fvevol.sys")
]

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
E1000 = ptest.Device(ptest.Device.E1000, backend=NETDEV)
QEMU = ptest.Qemu(ptest.Qemu.I386, 2048, E1000, NETDEV, vga=ptest.Qemu.CIRRUS)
OSI_TEST = ptest.Plugin("osi_test")
REPLAY = ptest.Replay("win7-osi-test", QEMU, OSI_TEST, os="windows-32-7")
 
def run():
    retcode = REPLAY.run()
    if retcode != 0:
        REPLAY.dump_console(stdout=True, stderr=True)
        return False
    REPLAY.copy_stdout(TMP_STDOUT)

    lines = []

    process_table = {}
    dylib_table = []
    kernmod_table = []

    # Extract osi_test data when the current process is procexp.exe.
    stdout = open(TMP_STDOUT, "r")
    cp_regex = re.compile("Current process: procexp.exe")
    end_regex = re.compile("-------------------------------------------------")
    for line in stdout:
        if cp_regex.search(line):
            lines.append(line)
            break

    # Fill the process table
    ps_list_regex = re.compile("Process list")
    fill_process_table = False
    for line in stdout:
        toks = line.split()
        if fill_process_table and len(toks) == 0:
            break
        if fill_process_table:
            process_table[int(toks[1])] = toks[0]
        if ps_list_regex.search(line):
            fill_process_table = True

    # Fill Memory Mapping Table
    dyn_lib_regex = re.compile("Dynamic libraries list")
    fill_dyn_lib_table = False
    for line in stdout:
        if dyn_lib_regex.search(line):
            fill_dyn_lib_table = True
        elif fill_dyn_lib_table:
            toks = line.split()
            if len(toks) == 0:
                break
            dylib_entry = (int(toks[0], 16), int(toks[1]), toks[2], toks[3])
            dylib_table.append(dylib_entry)

    # Fill kernel module table
    kern_mod_regex = re.compile("Kernel module list")
    fill_kern_mod_table = False
    for line in stdout:
        if kern_mod_regex.search(line):
            fill_kern_mod_table = True
        elif fill_kern_mod_table:
            toks = line.split()
            if len(toks) == 0:
                break
            kernmod_entry = (int(toks[0], 16), int(toks[1]), toks[2], toks[3])
            kernmod_table.append(kernmod_entry)

    # find the end of the output
    for line in stdout:
        if end_regex.search(line):
            break
        lines.append(line)  
    stdout.close()

    # Check the current PID
    current_pid_regex = re.compile("PID:%d" % (TARGET_PID))
    ok = True in map(lambda line: current_pid_regex.search(line) != None, lines)
    if not ok:
        print("Could not find expected process ID!")
        return False

    # Check the parent PID
    parent_pid_regex = re.compile("PPID:%d" % (TARGET_PPID))
    ok = True in map(lambda line: parent_pid_regex.search(line) != None, lines)
    if not ok:
        print("Could not find expected parent process ID!")
        return False

    # Check the process table entries
    for k, v in EXPECTED_PROCESS_LIST.items():
        if k not in process_table or process_table[k] != v:
            print("expected %d:%s to be in the process table" % (k, v))
            return False

    # Check the memory mapping\libraries.
    for entry in EXPECTED_DYLIB_ENTRIES:
        if entry not in dylib_table:
            print("expected %s to be in the dynamic library table" % (entry,))
            return False

    # Check the kernel modules
    for entry in EXPECTED_KERNEL_MODULE_ENTRIES:
        if entry not in kernmod_table:
            print("expected %s to be in the kernel module table" % (entry,))
            return False

    return True
 
def cleanup():
    os.remove(TMP_STDOUT)
