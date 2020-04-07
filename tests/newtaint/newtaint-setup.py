#!/usr/bin/python

import os
import subprocess as sp
import sys
import re
import shutil

#from expect import *

thisdir = os.path.dirname(os.path.realpath(__file__))
td = os.path.realpath(thisdir + "/../..")
sys.path.append(td)

from ptest_utils import *

newtaintpath = os.path.join(thisdir, "tests", "newtaint")
replaypath = os.path.join(thisdir, "tests", "replays")

os.system("rm -rf " + os.path.join(newtaintpath,"panda_test"))
os.system("rm -rf " + replaypath)

gitclonestring = "git clone https://github.com/panda-re/panda_test " + os.path.join(newtaintpath,"panda_test")

os.system(gitclonestring)
os.mkdir(replaypath)
os.mkdir(os.path.join(replaypath, "cde"))
os.mkdir(os.path.join(replaypath, "cde", "cdrom"))
os.mkdir(os.path.join(replaypath, "cd4"))
os.mkdir(os.path.join(replaypath, "cd4", "cdrom"))
os.mkdir(os.path.join(replaypath, "cd5"))
os.mkdir(os.path.join(replaypath, "cd5", "cdrom"))
os.mkdir(os.path.join(replaypath, "cd6"))
os.mkdir(os.path.join(replaypath, "cd6", "cdrom"))
os.mkdir(os.path.join(replaypath, "cd7"))
os.mkdir(os.path.join(replaypath, "cd7", "cdrom"))
os.mkdir(os.path.join(replaypath, "cd8"))
os.mkdir(os.path.join(replaypath, "cd8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cd9"))
os.mkdir(os.path.join(replaypath, "cd9", "cdrom"))
os.mkdir(os.path.join(replaypath, "cd10"))
os.mkdir(os.path.join(replaypath, "cd10", "cdrom"))
os.mkdir(os.path.join(replaypath, "cd11"))
os.mkdir(os.path.join(replaypath, "cd11", "cdrom"))

tutpath = os.path.join(newtaintpath, "panda_test", "taint_unittest")

os.system("cd " + tutpath + " && ./build.sh")
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cde", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cd4", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cd5", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cd6", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cd7", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cd8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cd9", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cd10", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cd11", "cdrom"))

guestcmde = "guest:cde || cd " + os.path.join(replaypath, "cde", "cdrom") + " && ./turn_on_taint && ./eax_test"
guestcmd4 = "guest:cd4 || cd " + os.path.join(replaypath, "cd4", "cdrom") + " && ./turn_on_taint && ./test4"
guestcmd5 = "guest:cd5 || cd " + os.path.join(replaypath, "cd5", "cdrom") + " && ./turn_on_taint && ./test5"
guestcmd6 = "guest:cd6 || cd " + os.path.join(replaypath, "cd6", "cdrom") + " && ./turn_on_taint && ./test6"
guestcmd7 = "guest:cd7 || cd " + os.path.join(replaypath, "cd7", "cdrom") + " && ./turn_on_taint && ./test7"
guestcmd8 = "guest:cd8 || cd " + os.path.join(replaypath, "cd8", "cdrom") + " && ./turn_on_taint && ./test8"
guestcmd9 = "guest:cd9 || cd " + os.path.join(replaypath, "cd9", "cdrom") + " && ./turn_on_taint && ./test9"
guestcmd10 = "guest:cd10 || cd " + os.path.join(replaypath, "cd10", "cdrom") + " && ./turn_on_taint && ./test10"
guestcmd11 = "guest:cd11 || cd " + os.path.join(replaypath, "cd11", "cdrom") + " && ./turn_on_taint && ./test11"

try:
    record_debian(guestcmde, "cde", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cd4", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd5, "cd5", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd6, "cd6", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd7, "cd7", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd8, "cd8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd9, "cd9", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd10, "cd10", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd11, "cd11", "i386")
except:
    print("ok")

sys.exit(0)
