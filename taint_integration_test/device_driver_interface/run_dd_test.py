#!/usr/bin/env python3

import os
import sys
import subprocess
import wget
import shutil
from pathlib import Path

from panda import blocking, Panda

TEST_PROG_USR = "tt_ioctl_userspace"
TEST_PROG_MOD = "tt_ioctl_module.ko"
TEST_PROG_DIR = "dd_src"
TEST_HDR_DIR  = "taint_include"
TEST_HDR_FILE = "taint.h"

CURR_DIR = Path(__file__).parent.absolute()
HOST_PROG_DIR = CURR_DIR.joinpath(TEST_PROG_DIR)
HOST_HDR_FILE = CURR_DIR.parent.parent.joinpath(TEST_HDR_DIR, TEST_HDR_FILE)

QCOW = "bionic-server-cloudimg-amd64.qcow2"
BASE_URL = "http://panda-re.mit.edu/qcows/linux/ubuntu/1804/x86_64/"
QCOW_URL = BASE_URL + QCOW
HOST_QCOW_PATH = CURR_DIR.joinpath(QCOW)

def host_download_qcow():
    print(HOST_QCOW_PATH)
    if not HOST_QCOW_PATH.is_file():
        print("\nDownloading \'{}\'...".format(QCOW))
        wget.download(QCOW_URL)
        assert(HOST_QCOW_PATH.is_file())

@blocking
def run_in_guest():

    # Mount src in guest
    panda.revert_sync("root")
    shutil.copy2(HOST_HDR_FILE, HOST_PROG_DIR)
    panda.copy_to_guest(str(HOST_PROG_DIR))
    HOST_PROG_DIR.joinpath(TEST_HDR_FILE).unlink()

    # Build kernel module in guest
    # If built on host, host-guest kernel version mismatch can cause module load errors
    build_cmds = [

        # Setup relevant files to mirror panda_test relative pathing
        "mkdir taint_include",
        "mkdir test_1",
        "cd test_1",
        "mkdir test_2",
        "cd -",
        "cp -r ./{} test_1/test_2".format(TEST_PROG_DIR),
        "mv ./test_1/test_2/{}/{} ./taint_include".format(TEST_PROG_DIR, TEST_HDR_FILE),

        # Networking
        "hwclock -s",
        "dhclient -v -4",

        # Packages
        "killall apt apt-get",
        "rm /var/lib/apt/lists/lock",
        "rm /var/cache/apt/archives/lock",
        "rm /var/lib/dpkg/lock*",
        "dpkg --configure -a",
        "apt-get clean",
        "apt-get update",
        "apt-get install -y make build-essential linux-headers-$(uname -r)",

        # Build
        "cd ./test_1/test_2/{} && make clean && make".format(TEST_PROG_DIR),
    ]

    for cmd in build_cmds:
        print(panda.run_serial_cmd(cmd, no_timeout=True))

    print(panda.run_serial_cmd("insmod {}".format(TEST_PROG_MOD), no_timeout=True))
    print(panda.run_serial_cmd("./{}".format(TEST_PROG_USR), no_timeout=True))

    '''
    # Load kernel module, run userspace program to talk to it
    print(panda.run_serial_cmd(
        "insmod {} && ./{}".format(
            TEST_PROG_MOD,
            TEST_PROG_USR
        ),
        no_timeout=True
    ))
    '''

    # Logs
    print(panda.run_serial_cmd("dmesg | tail -30"))

    panda.end_analysis()

if __name__ == "__main__":

    host_download_qcow()

    panda = Panda(
        arch = "x86_64",
        qcow = str(HOST_QCOW_PATH),
        extra_args = "-nographic",
        expect_prompt = rb"root@ubuntu:.*",
        mem = "1G"
    )

    panda.queue_async(run_in_guest)
    panda.run()
