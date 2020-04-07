#!/usr/bin/python

import os
import sys
import subprocess as sp

thisdir = os.path.dirname(os.path.realpath(__file__))
td = os.path.realpath(thisdir + "/../..")
sys.path.append(td)

from ptest_utils import *

os.system("mkdir -p " + thisdir + "/taint2_logs")
os.system("rm " + thisdir+"/taint2_logs/*")

run_test_debian("-panda taint2 ", 'cde',"i386")
os.system("mv " + tmpoutdir + "/taint2_log " + thisdir + "/taint2_logs/taint2_log_e")

run_test_debian("-panda taint2 ", 'cd4',"i386")
os.system("mv " + tmpoutdir + "/taint2_log " + thisdir + "/taint2_logs/taint2_log_4")

run_test_debian("-panda taint2 ", 'cd5',"i386")
os.system("mv " + tmpoutdir + "/taint2_log " + thisdir + "/taint2_logs/taint2_log_5")

run_test_debian("-panda taint2 ", 'cd6',"i386")
os.system("mv " + tmpoutdir + "/taint2_log " + thisdir + "/taint2_logs/taint2_log_6")

run_test_debian("-panda taint2 ", 'cd7',"i386")
os.system("mv " + tmpoutdir + "/taint2_log " + thisdir + "/taint2_logs/taint2_log_7")

run_test_debian("-panda taint2 ", 'cd8',"i386")
os.system("mv " + tmpoutdir + "/taint2_log " + thisdir + "/taint2_logs/taint2_log_8")

run_test_debian("-panda taint2 ", 'cd9',"i386")
os.system("mv " + tmpoutdir + "/taint2_log " + thisdir + "/taint2_logs/taint2_log_9")

run_test_debian("-panda taint2 ", 'cd10',"i386")
os.system("mv " + tmpoutdir + "/taint2_log " + thisdir + "/taint2_logs/taint2_log_10")

run_test_debian("-panda taint2 ", 'cd11',"i386")
os.system("mv " + tmpoutdir + "/taint2_log " + thisdir + "/taint2_logs/taint2_log_11")

os.system("mv " + thisdir+"/taint2_logs/* " + tmpoutdir)

os.system("rmdir " + thisdir+"/taint2_logs")

sys.exit(0)
