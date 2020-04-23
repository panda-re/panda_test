#!/usr/bin/env python3

import os
import sys
import subprocess

from panda import blocking, Panda

TEST_PROG_USR = "tt_ioctl_userspace"
TEST_PROG_MOD = "tt_ioctl_module.ko"
TEST_PROG_DIR = "dd_src"
HOST_PROG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), TEST_PROG_DIR)
GUEST_PROG_DIR = os.path.join(os.sep + "root", TEST_PROG_DIR)

# No arguments, x86_64. Otherwise argument should be guest arch.
generic_type = sys.argv[1] if len(sys.argv) > 1 else "x86_64"
panda = Panda(generic=generic_type)

def host_build_test_progs():
    output = subprocess.check_output(
        ["make", "clean", "&&", "make"],
        shell=True,
        cwd=HOST_PROG_DIR
    )
    print(output.decode("utf-8"))
    assert(os.path.isfile(os.path.join(HOST_PROG_DIR, TEST_PROG_USR)))
    assert(os.path.isfile(os.path.join(HOST_PROG_DIR, TEST_PROG_MOD)))

@blocking
def run_in_guest():

    # Mount test src/binaries in guest
    panda.revert_sync("root")
    panda.copy_to_guest(HOST_PROG_DIR)

    # Load kernel module, run userspace program to talk to it
    print(panda.run_serial_cmd("uname -r"))
    print(panda.run_serial_cmd(
        "cd {} && insmod {} && ./{}".format(
            GUEST_PROG_DIR,
            TEST_PROG_MOD,
            TEST_PROG_USR
        )
    ))

    panda.end_analysis()

if __name__ == "__main__":
    host_build_test_progs()
    panda.queue_async(run_in_guest)
    panda.run()