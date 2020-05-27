#!/usr/bin/python3

import os
from os import path
from os import remove
import sys
import shutil
from sys import argv
from panda import blocking, Panda

thisdir = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    panda = Panda(
        arch = "i386",
        qcow = "/home/panda/regdir/qcows/wheezy_panda2.qcow2",
        extra_args = "-nographic",
        expect_prompt = rb"root@debian-i386:.*"
    )

    panda.load_plugin("taint2")
    panda.run_replay("taint2_tests")
