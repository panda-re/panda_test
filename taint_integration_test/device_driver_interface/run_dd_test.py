#!/usr/bin/env python3

import os
import sys
import subprocess
import wget

from panda import blocking, Panda

# Artifact setup
TEST_PROG_USR = "tt_ioctl_userspace"
TEST_PROG_MOD = "tt_ioctl_module.ko"
TEST_PROG_DIR = "dd_src"
HOST_PROG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), TEST_PROG_DIR)
GUEST_PROG_DIR = os.path.join(os.sep + "root", TEST_PROG_DIR)

# Since the kernel module is compiled on the host, guest kernel needs to be a reasonably close version
# Otherwise, will get "Error: could not insert module tt_ioctl_module.ko: Invalid module format"
COMPAT_QCOW = "ubuntu_1604_x86_64.qcow"
COMPAT_QCOW_URL = "http://panda-re.mit.edu/qcows/linux/ubuntu/1604/x86_64/" + COMPAT_QCOW
HOST_QCOW_PATH = os.path.join(HOST_PROG_DIR, COMPAT_QCOW)

def host_download_qcow():
    if not os.path.isfile(HOST_QCOW_PATH):
        print("Downloading \'{}\'...".format(COMPAT_QCOW))
        wget.download(COMPAT_QCOW_URL)
        assert(os.path.isfile(HOST_QCOW_PATH))

def host_build_test_progs():
    print("Building \'{}\' and \'{}\'...".format(TEST_PROG_USR, TEST_PROG_MOD))
    output = subprocess.check_output(
        ["make", "clean", "&&", "make"],
        shell=True,
        cwd=HOST_PROG_DIR
    )
    print(output.decode("utf-8"))
    assert(os.path.isfile(os.path.join(HOST_PROG_DIR, TEST_PROG_USR)))
    assert(os.path.isfile(os.path.join(HOST_PROG_DIR, TEST_PROG_MOD)))

@blocking
def run_in_guest(panda):

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

    host_download_qcow()
    host_build_test_progs()

    panda = Panda(
        arch = "x86_64",
        qcow = HOST_QCOW_PATH,
        args = "-nographic"
    )

    panda.queue_async(run_in_guest(panda))
    panda.run()