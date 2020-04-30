#!/usr/bin/env python3

import os
import sys
import subprocess
import wget

from panda import blocking, Panda

TEST_PROG_USR = "tt_ioctl_userspace"
TEST_PROG_MOD = "tt_ioctl_module.ko"
TEST_PROG_DIR = "dd_src"

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
HOST_PROG_DIR = os.path.join(CURR_DIR, TEST_PROG_DIR)
GUEST_PROG_DIR_RO = os.path.join(os.sep + "root", TEST_PROG_DIR)
GUEST_PROG_DIR_RW = os.path.join(os.sep + "root", "test", TEST_PROG_DIR)

QCOW = "bionic-server-cloudimg-amd64.qcow2"
BASE_URL = "http://panda-re.mit.edu/qcows/linux/ubuntu/1804/x86_64/"
QCOW_URL = BASE_URL + QCOW
HOST_QCOW_PATH = os.path.join(CURR_DIR, QCOW)

def host_download_qcow():
    if not os.path.isfile(HOST_QCOW_PATH):
        print("\nDownloading \'{}\'...".format(QCOW))
        wget.download(QCOW_URL)
        assert(os.path.isfile(HOST_QCOW_PATH))

@blocking
def run_in_guest():

    # Mount src in guest
    panda.revert_sync("root")
    panda.copy_to_guest(HOST_PROG_DIR)

    # Build kernel module in guest
    # If built on host, host-guest kernel version mismatch can cause module load errors
    build_cmds = [

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
        "mkdir test",
        "cp -a {} test".format(GUEST_PROG_DIR_RO),
        "cd {} && make clean && make".format(GUEST_PROG_DIR_RW),
    ]

    for cmd in build_cmds:
        print(panda.run_serial_cmd(cmd, no_timeout=True))

    # Load kernel module, run userspace program to talk to it
    print(panda.run_serial_cmd(
        "cd {} && insmod {} && ./{}".format(
            GUEST_PROG_DIR_RW,
            TEST_PROG_MOD,
            TEST_PROG_USR
        )
    ))

    # Logs
    print(panda.run_serial_cmd("dmesg | tail -30"))

    panda.end_analysis()

if __name__ == "__main__":

    host_download_qcow()

    panda = Panda(
        arch = "x86_64",
        qcow = HOST_QCOW_PATH,
        extra_args = "-nographic",
        expect_prompt = rb"root@ubuntu:.*",
        mem = "1G"
    )

    panda.queue_async(run_in_guest)
    panda.run()