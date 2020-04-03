# test_win2k_nocounter.py
# Test the replaymovie plugin using a guest with a GUI, and explicitly asking
# for no instruction counter information.
#
# Created:  22-AUG-2019
# Changed:  24-OCT-2019   Corrected erroneous printfs.

import filecmp
import glob
import os
import subprocess

import ptest

import tests.replaymovie.replaymoviecommon as rmcommon

FILE_PREFIX = "win2k_nocounter"

# use os.path.join so needn't worry about what the separator character is on
# this system
REPLAY_PATH = os.path.join("windows2k", "win2k_mtsf_morefns")
TEST_DIR_PREFIX = os.path.join("tests", "replaymovie")

# setup for "-net nic,model=ne2k_pci -net user"
NETDEV = ptest.NetBackend(ptest.NetBackend.USER, "net0")
NE2KPCI = ptest.Device(ptest.Device.NE2K_PCI, backend=NETDEV)

# "-usbdevice tablet" is deprecatedin favor of "-device usb-tablet -usb"
TABLET = ptest.Device(ptest.Device.USB_TABLET)

QEMU = ptest.Qemu(ptest.Qemu.I386, 512, NETDEV, NE2KPCI, TABLET,
    vga=ptest.Qemu.CIRRUS, options="-usb")

# explicitly request no instruction counter information
MOVIE = ptest.Plugin("replaymovie", save_instruction_count=False)
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
    
    # verify did not get text file with instruction counter information
    counters_file = os.path.join("replay_movie_counters.txt")
    if (os.path.exists(counters_file)):
        print(rmcommon.INDENT_SPACES + "***** UNEXPECTEDLY FOUND " +
            counters_file + " *****")
        new_files.add(counters_file)
        rmcommon.delete_ppms()
        return False
        
    # verify did get the 101 ppm files (named replay_movie_000.ppm through
    # replay_movie_100.ppm, although this is just a warm-fuzzy check)
    # replaymovie puts them in the folder run from
    ppmlist = glob.glob("replay_movie_*.ppm")
    if (len(ppmlist) != 101):
        print(rmcommon.INDENT_SPACES + "***** FOUND " + str(len(ppmlist)) +
            " replay_movie_###.ppm FILES BUT EXPECTED 101 *****")
        rmcommon.delete_ppms()
        return False
    
    # execute <build_dir>../panda/panda/plugins/replaymovie/movie.sh
    # it expects the input ppm files to be in the folder run from, and puts the
    # output file there too
    builddir = ptest.get_build_dir()
    moviescript=os.path.join(builddir, "..", "panda", "panda", "plugins",
        "replaymovie", "movie.sh")
    try:
        stderrfile = open(stderr_filename, "a")
        retcode = subprocess.call(moviescript, stderr=stderrfile)
        if (retcode < 0):
            print(rmcommon.INDENT_SPACES +
                "***** UNEXPECTED TERMINATION OF movie.sh *****")
            rmcommon.delete_ppms()
            return False
    except OSError as e:
        print(rmcommon.INDENT_SPACES + "***** ERROR EXECUTING movie.sh *****")
        rmcommon.delete_ppms()
        return False
        
    # rename replay.mp4 and store in new_files list
    moviepath = os.path.join(TEST_DIR_PREFIX, FILE_PREFIX + ".mp4")
    os.rename("replay.mp4", moviepath)
    new_files.add(moviepath)
    
    # compare new replay.mp4 with our good copy
    expected_movie = os.path.join(TEST_DIR_PREFIX,
        "win2k_nocounter_expected.mp4")
    if (not filecmp.cmp(moviepath, expected_movie)):
        print(rmcommon.INDENT_SPACES + "***** MOVIE FILE NOT AS EXPECTED *****")
        rmcommon.delete_ppms()
        return False
        
    # just delete the 101 ppm files
    rmcommon.delete_ppms()
            
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
    