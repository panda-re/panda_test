#!/usr/bin/python3

import os
import argparse
from pandare import blocking, Panda

thisdir = os.path.dirname(os.path.realpath(__file__))

# TODO: update this to be cleaner and use python3 Path (pathlib)
def prepare_cdrom_iso(build_target):
    os.system("mkdir -p " + os.path.join(thisdir,"cdrom"))
    os.system("cd ../../taint_unit_test;\
        export TARGET=\"" + build_target + "\" && make;\
        cp bin/* " + os.path.join(thisdir,"cdrom") + ";\
        cd ../tests/taint2;\
        cp run_all_tests.sh " + os.path.join(thisdir,"cdrom") + ";")

@blocking
def run_in_guest_record():
    panda.record_cmd("./cdrom/run_all_tests.sh",
        copy_directory=os.path.join(thisdir,"cdrom"),
        iso_name="cdrom.iso",
        recording_name="taint2_tests",
        snap_name="root"
    )
    panda.stop_run()

if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser(description="Create or replay a recording for taint2 unit tests")
    arg_parser.add_argument(
            '--arch',
            type=str,
            help="Architecture to test, one of: i386, x86_64, arm",
            default="i386",
    )
    arg_parser.add_argument(
            '--mode',
            type=str,
            help="Mode, one of: record, replay",
            default="record",
    )
    args = arg_parser.parse_args()

    # Arch selection
    if args.arch == "i386":
        build_target = "TARGET_I386"
        test_expect_prompt = rb"root@debian-i386:.*"
        test_qcow="/home/panda/regdir/qcows/wheezy_panda2.qcow2"
        test_mem = "128M"

    elif args.arch == "x86_64":
        build_target = "TARGET_X86_64"
        test_expect_prompt = rb"root@ubuntu:.*"
        test_qcow="/home/panda/regdir/qcows/bionic-server-cloudimg-amd64-noaslr-nokaslr.qcow2"
        test_mem = "1G"

    # TODO: not yet supported, need hypercall update in taint.h
    #elif args.arch == "arm":
    #    build_target = "TARGET_ARM"
    #    test_expect_prompt = rb"root@ubuntu:.*"
    #    test_qcow="/home/panda/regdir/qcows/arm_wheezy.qcow2"
    #    test_mem = "256M"

    else:
        raise RuntimeError("Invalid architecture for taint2 unit tests!")

    # Panda prep
    panda = Panda(
        arch = args.arch,
        qcow = test_qcow,
        extra_args = "-nographic",
        expect_prompt = test_expect_prompt,
        mem = test_mem
    )

    # Mode selection
    if args.mode == "record":
        prepare_cdrom_iso(build_target)
        panda.queue_async(run_in_guest_record)
        panda.run()

    elif args.mode == "replay":
        panda.load_plugin("taint2", args={"enable_hypercalls": True})
        panda.run_replay("taint2_tests")

    else:
        raise RuntimeError("Invalid mode for taint2 unit tests!")
