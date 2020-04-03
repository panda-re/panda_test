# test_win2k_nondefcounter.py
# Test the replaymovie plugin using a guest with a GUI, with an instruction
# counter at a non-default location in the movie.
#
# Created:  22-AUG-2019
# Changed:  24-OCT-2019   Corrected erroneous printfs.

import filecmp
import glob
import os
import subprocess
from shutil import copyfile

import ptest

import tests.replaymovie.replaymoviecommon as rmcommon

FILE_PREFIX = "win2k_nondefcounter"

# use os.path.join so needn't worry about what the separator character is on
# this system
REPLAY_PATH = os.path.join("windows2k", "win2k_mtsf_morefns")
TEST_DIR_PREFIX = os.path.join("tests", "replaymovie")

# setup for "-net nic,model=ne2k_pci -net user"
NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
NE2KPCI = ptest.Device(ptest.Device.NE2K_PCI, backend=NETDEV)

# "-usbdevice tablet" is deprecated in favor of "-device usb-tablet -usb"
TABLET = ptest.Device(ptest.Device.USB_TABLET)

QEMU = ptest.Qemu(ptest.Qemu.I386, 512, NETDEV, NE2KPCI, TABLET,
    vga=ptest.Qemu.CIRRUS, options="-usb")

# this should put the counter above the command prompt window in the guest
MOVIE = ptest.Plugin("replaymovie", save_instruction_count=True, xfraction=0.5,
    yfraction=0.1)
REPLAY = ptest.Replay(REPLAY_PATH, QEMU, MOVIE)

# created files that haven't been cleaned up yet
new_files = set()

# are all the files in new_files from tests that ran OK?
all_ok = False
    
def run():
    """
    Execute the test and return true if the test passed.
    """
    global all_ok
    
    retcode = REPLAY.run()
    
    # keep stdout and stderr in case need to peruse for clues if fails later
    stdout_filename = os.path.join(TEST_DIR_PREFIX, FILE_PREFIX + ".stdout")
    new_files.add(stdout_filename)
    stderr_filename = os.path.join(TEST_DIR_PREFIX, FILE_PREFIX + ".stderr")
    new_files.add(stderr_filename)
    REPLAY.copy_stdout(stdout_filename)
    REPLAY.copy_stderr(stderr_filename)
    if (retcode != 0):
        print(rmcommon.INDENT_SPACES +
            "***** ERROR EXECUTING PANDA TO PRODUCE MOVIE FRAMES *****")
        # just delete the 101 ppm files, as too many to rename and keep around
        rmcommon.delete_ppms()
        return False
    
    # verify did get text file with instruction counter information
    counters_file = os.path.join("replay_movie_counters.txt")
    if (not os.path.exists(counters_file)):
        print(rmcommon.INDENT_SPACES + "***** REPLAYMOVIE DID NOT PRODUCE " +
            counters_file + " *****")
        rmcommon.delete_ppms()
        return False
        
    # always have to delete the counters file, to prevent a later test that
    # does not expect one from failing - so make a copy in case need it for
    # error checking this test
    counters_file_copy = os.path.join(TEST_DIR_PREFIX,
        FILE_PREFIX + counters_file)
    copyfile(counters_file, counters_file_copy)
    new_files.add(counters_file_copy)
    
    # verify did get the 101 ppm files (named replay_movie_000.ppm through
    # replay_movie_100.ppm, although this is just a warm-fuzzy check)
    # replaymovie puts them in the folder run from
    ppmlist = glob.glob("replay_movie_*.ppm")
    if (len(ppmlist) != 101):
        print(rmcommon.INDENT_SPACES + "***** FOUND " + str(len(ppmlist)) +
            " replay_movie_###.ppm FILES BUT EXPECTED 101 *****")
        rmcommon.delete_ppms()
        os.remove(counters_file)
        return False
    
    # execute <build_dir>../panda/panda/plugins/replaymovie/moviecounter.sh
    # it expects the input ppm files to be in the folder run from, and puts the
    # output file there too
    builddir = ptest.get_build_dir()
    moviescript=os.path.join(builddir, "..", "panda", "panda", "plugins",
        "replaymovie", "moviecounter.sh")
    try:
        stderrfile = open(stderr_filename, "a")
        retcode = subprocess.call(moviescript, stderr=stderrfile)
        if (retcode < 0):
            print(rmcommon.INDENT_SPACES +
                "***** UNEXPECTED TERMINATION OF moviecounter.sh *****")
            rmcommon.delete_ppms()
            os.remove(counters_file)
            return False
    except OSError as e:
        print(rmcommon.INDENT_SPACES +
            "***** ERROR EXECUTING moviecounter.sh *****")
        rmcommon.delete_ppms()
        os.remove(counters_file)
        return False
        
    # rename moviecounter.mp4 and store in new_files list
    moviepath = os.path.join(TEST_DIR_PREFIX, FILE_PREFIX + ".mp4")
    os.rename("moviecounter.mp4", moviepath)
    new_files.add(moviepath)
    
    # compare new moviecounter.mp4 with our good copy
    expected_movie = os.path.join(TEST_DIR_PREFIX,
        "win2k_nondefcounter_expected.mp4")
    if (not filecmp.cmp(moviepath, expected_movie)):
        print(rmcommon.INDENT_SPACES + "***** MOVIE FILE NOT AS EXPECTED *****")
        rmcommon.delete_ppms()
        os.remove(counters_file)
        return False
        
    # just delete the original 101 ppm files and the 101 created by
    # moviecounter.sh, and the original counters file
    rmcommon.delete_ppms()
    os.remove(counters_file)
            
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
            print(rmcommon.INDENT_SPACES + cur_file)
        print(rmcommon.INDENT_SPACES +
            "The above output files have not been deleted in hopes they cue " +
            "you in as to what went wrong.")
    