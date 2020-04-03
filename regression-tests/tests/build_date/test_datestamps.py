# test_datestamps.py
# Verify that all the available PANDA builds report the same build date in
# response to "--version" and "--help".
#
# Created:  30-OCT-2019

import os
import subprocess

import ptest

INDENT_SPACES = "                 "

TEST_DIR_PREFIX = os.path.join("tests", "build_date")

# the build dates found by various means
build_dates = set()

# created files that haven't been cleaned up yet
new_files = set()

# are all the files in new_files from tests that ran OK?
all_ok = False

def extract_build_date(stdout_name):
    global build_dates
    
    # extract the build date from the version output
    found_build_date = False
    with open(stdout_name, "r") as sofile:
        for line in sofile:
            line = line.strip()
            if (line.startswith("Build date ")):
                found_build_date = True
                build_dates.add(line)
                break
    if (not found_build_date):
        print(INDENT_SPACES +
            "***** BUILD DATE NOT FOUND *****")
        return False
        
    return True
        
def extract_dates(arch):
    global new_files
    global build_dates
    
    # I don't really need the RAM, but QEMU won't construct w/out one
    cur_qemu = ptest.Qemu(arch, 2048)
    
    cmdline = cur_qemu.cmdline(monitor=False)
    panda_cmdline = os.path.join(ptest.get_build_dir(), cmdline[0])
    
    # execute PANDA with the version option
    stdout_name = str(arch) + "_version.stdout"
    stdout_file = open(stdout_name, 'w')
    retcode = subprocess.call([panda_cmdline, "-version"], stdout=stdout_file)
    new_files.add(stdout_name)
    if (retcode != 0):
        print(INDENT_SPACES + "***** ERROR EXECUTING PANDA FOR " + str(arch) +
            " *****")
        return False
    gotdate = extract_build_date(stdout_name)
    if (not gotdate):
        return False

    # execute PANDA with the help option
    stdout_name = str(arch) + "_help.stdout"
    stdout_file = open(stdout_name, 'w')
    retcode = subprocess.call([panda_cmdline, "-help"], stdout=stdout_file)
    new_files.add(stdout_name)
    if (retcode != 0):
        print(INDENT_SPACES + "***** ERROR EXECUTING PANDA FOR " + str(arch) +
            " *****")
        return False
    gotdate = extract_build_date(stdout_name)
    if (not gotdate):
        return False
        
    return True
        
def run():
    """
    Execute the test and return true if the test passed.
    """
    global all_ok
    global build_dates
    
    retcode = extract_dates(ptest.Qemu.I386)
    if (not retcode):
        return False
        
    retcode = extract_dates(ptest.Qemu.X86_64)
    if (not retcode):
        return False
        
    retcode = extract_dates(ptest.Qemu.PPC)
    if (not retcode):
        return False
        
    retcode = extract_dates(ptest.Qemu.ARM)
    if (not retcode):
        return False
    
    if (len(build_dates) != 1):
        print(INDENT_SPACES + "***** ALL BUILD DATES ARE NOT IDENTICAL *****")
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
    