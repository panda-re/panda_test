#!/usr/bin/python3

import os
import argparse
import wget
import subprocess
from pathlib import Path

from panda import blocking, Panda

CURR_DIR = Path(__file__).parent.absolute()
X86_QCOW_URL = "https://panda-re.mit.edu/qcows/linux/ubuntu/1604/x86/ubuntu_1604_x86.qcow"
X64_QCOW_URL = "https://panda-re.mit.edu/qcows/linux/ubuntu/1804/x86_64/bionic-server-cloudimg-amd64-noaslr-nokaslr.qcow2"

# TODO: update this to be cleaner: use python3 Path (pathlib) and subprocess
def prepare_cdrom_iso(build_target):
    os.system("mkdir -p " + os.path.join(CURR_DIR,"cdrom"))
    os.system("cd ../../taint_unit_test;\
        export TARGET=\"" + build_target + "\" && make;\
        cp bin/* " + os.path.join(CURR_DIR,"cdrom") + ";\
        cd ../tests/taint2;\
        cp run_all_tests.sh " + os.path.join(CURR_DIR,"cdrom") + ";")

def host_download_qcow(qcow_url):
    qcow_name = qcow_url.split("/")[-1]
    host_qcow_path = CURR_DIR.joinpath(qcow_name)
    if not host_qcow_path.is_file():
        print("\nDownloading \'{}\'...".format(qcow_name))
        wget.download(qcow_url, out=str(CURR_DIR))
        assert(host_qcow_path.is_file())
    return host_qcow_path

@blocking
def run_in_guest_record():
    panda.record_cmd("./cdrom/turn_on_taint; ./cdrom/run_all_tests.sh",
        copy_directory=os.path.join(CURR_DIR,"cdrom"),
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
        test_expect_prompt = rb"root@ubuntu:.*"
        test_mem = "128M"
        test_qcow = Path("/home/panda/regdir/qcows/ubuntu_1604_x86.qcow")
        if not (test_qcow.exists() and test_qcow.is_file):
            test_qcow = host_download_qcow(X86_QCOW_URL)

    elif args.arch == "x86_64":
        build_target = "TARGET_X86_64"
        test_mem = "1G"
        test_expect_prompt = rb"root@ubuntu:.*"
        test_qcow = Path("/home/panda/regdir/qcows/bionic-server-cloudimg-amd64-noaslr-nokaslr.qcow2")
        if not (test_qcow.exists() and test_qcow.is_file):
            test_qcow = host_download_qcow(X64_QCOW_URL)

    # TODO: not yet supported, need hypercall update in taint.h
    #elif args.arch == "arm":
    #    build_target = "TARGET_ARM"
    #    test_mem = "256M"
    #    test_expect_prompt = rb"root@ubuntu:.*"
    #    test_qcow="/home/panda/regdir/qcows/arm_wheezy.qcow2"

    else:
        raise RuntimeError("Invalid architecture for taint2 unit tests!")

    # Panda prep
    if args.mode != "check":
        panda = Panda(
            arch = args.arch,
            qcow = str(test_qcow),
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
        panda.load_plugin("taint2")
        panda.run_replay("taint2_tests")

    elif args.mode == "check":
        expected_log = CURR_DIR.joinpath("taint2_log")
        assert(expected_log.is_file())

        with open(expected_log, 'r') as f:
            log_lines = [l for l in f.readlines() if l.strip()]
            for l in log_lines:
                print(l)
                if "fail" in l:
                    raise RuntimeError("Taint2 unit test failure")

        print("Taint2 unit test passed!")
    else:
        raise RuntimeError("Invalid mode for taint2 unit tests!")()