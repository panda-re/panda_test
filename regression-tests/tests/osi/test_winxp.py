import os
import re

import ptest

TMP_STDOUT = "/tmp/winxpsp3-osi-test.stdout"

TARGET_PID = 808
TARGET_PPID = 1512

# Not all processes are checked since there are so many. I picked a few common
# processes to verify. Once we are sure we can get a handful, it seems like we
# wouldn't be gaining much by checking every single process because of the way
# the kernel structures are laid out (its just a linked list).
EXPECTED_PROCESS_LIST = {
    4: "System",
    308: "smss.exe",
    408: "csrss.exe",
    492: "services.exe",
    912: "svchost.exe",
    1740: "wuauclt.exe",
    1512: "explorer.exe",
    808: "procexp.exe"
}

# Not all entries are checked due to the way "osi_test" works. We could be more
# pedantic, but it would be more time consuming to execute - I don't think its
# worth it.
EXPECTED_DYLIB_ENTRIES = [
    (0x7C900000, 0xAF000, "ntdll.dll", "C:\\WINDOWS\\system32\\ntdll.dll"),
    (0x1E10000, 0x2c5000, "xpsp2res.dll", "C:\\WINDOWS\\system32\\xpsp2res.dll"),
    (0x77C10000, 0x58000, "msvcrt.dll", "C:\\WINDOWS\\system32\\msvcrt.dll"),
    (0x76F60000, 0x2C000, "WLDAP32.dll", "C:\\WINDOWS\\system32\\WLDAP32.dll"),
    (0x7C800000, 0xF6000, "kernel32.dll", "C:\\WINDOWS\\system32\\kernel32.dll")
]

EXPECTED_KERNEL_MODULE_ENTRIES = [
    (0x804D7000, 0x216680, "ntoskrnl.exe", "\\WINDOWS\\system32\\ntoskrnl.exe"),
    (0xF83CF000, 0x8d000, "Ntfs.sys", "Ntfs.sys"),
    (0xF73CA000, 0xA000, "PROCEXP152.SYS", "\\??\\C:\\WINDOWS\\system32\\Drivers\\PROCEXP152.SYS"),
    (0xF8818000, 0x7000, "fdc.sys", "\\SystemRoot\\System32\\DRIVERS\\fdc.sys"),
    (0xF8630000, 0xC000, "cirrus.sys", "\\SystemRoot\\System32\\DRIVERS\\cirrus.sys")
]

NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
RTL8139 = ptest.Device(ptest.Device.RTL8139, backend=NETDEV)
QEMU = ptest.Qemu(ptest.Qemu.I386, 512, RTL8139, NETDEV, vga=ptest.Qemu.CIRRUS)
OSI_TEST = ptest.Plugin("osi_test")
REPLAY = ptest.Replay("winxpsp3-osi-test", QEMU, OSI_TEST, os="windows-32-xpsp3")
 
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
