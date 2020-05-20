#!/usr/bin/python3

import os
from os import path
from os import remove
import sys
import shutil
from sys import argv
from panda import blocking, Panda

thisdir = os.path.dirname(os.path.realpath(__file__))
os.system("mkdir -p " + os.path.join(thisdir,"cdrom"))
os.system("cd ../../taint_unit_test; export TARGET=\"TARGET_I386\" && make; cp bin/* " + os.path.join(thisdir,"cdrom") + "; cd ../tests/taint2; cp run_all_tests.sh " + os.path.join(thisdir,"cdrom") + ";")

@blocking
def run_in_guest():
    panda.revert_sync("root")
    panda.copy_to_guest(os.path.join(thisdir,"cdrom"))
    panda.load_plugin("taint2")

    panda.run_serial_cmd("./cdrom/turn_on_taint; ./cdrom/run_all_tests.sh", no_timeout=True)
    result = panda.finish_serial_cmd()
    print(result)
    panda.stop_run()

if __name__ == "__main__":
    # Single arg of arch, defaults to i386
    arch = "i386" if len(argv) <= 1 else argv[1]
    panda = Panda(
        arch = "i386",
        qcow = "/home/panda/regdir/qcows/wheezy_panda2.qcow2",
        extra_args = "-nographic",
        expect_prompt = rb"root@debian-i386:.*"
    )
    panda.queue_async(run_in_guest)
    panda.run()
