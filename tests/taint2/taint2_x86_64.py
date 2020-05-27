#!/usr/bin/python3

import os
from os import path
from os import remove
import sys
import shutil
import wget
from sys import argv
from panda import blocking, Panda

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
QCOW = "bionic-server-cloudimg-amd64.qcow2"
BASE_URL = "http://panda-re.mit.edu/qcows/linux/ubuntu/1804/x86_64/"
QCOW_URL = BASE_URL + QCOW
HOST_QCOW_PATH = os.path.join(CURR_DIR, QCOW)

thisdir = os.path.dirname(os.path.realpath(__file__))
os.system("mkdir -p " + os.path.join(thisdir,"cdrom"))
os.system("cd ../../taint_unit_test; export TARGET=\"TARGET_X86_64\" && make; cp bin/* " + os.path.join(thisdir,"cdrom") + "; cd ../tests/taint2; cp run_all_tests.sh " + os.path.join(thisdir,"cdrom") + ";")

def host_download_qcow():
    if not os.path.isfile(HOST_QCOW_PATH):
        print("\nDownloading \'{}\'...".format(QCOW))
        wget.download(QCOW_URL)
        assert(os.path.isfile(HOST_QCOW_PATH))

@blocking
def run_in_guest():
    panda.revert_sync("root")
    panda.copy_to_guest(os.path.join(thisdir,"cdrom"))
    panda.load_plugin("taint2")

    panda.run_serial_cmd("./cdrom/turn_on_taint; ./cdrom/run_all_tests.sh")
    panda.stop_run()

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
