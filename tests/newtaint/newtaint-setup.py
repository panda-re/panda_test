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

os.mkdir(os.path.join(replaypath, "cdad"))
os.mkdir(os.path.join(replaypath, "cdad", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdaf"))
os.mkdir(os.path.join(replaypath, "cdaf", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdau8"))
os.mkdir(os.path.join(replaypath, "cdau8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdau16"))
os.mkdir(os.path.join(replaypath, "cdau16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdau32"))
os.mkdir(os.path.join(replaypath, "cdau32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdau64"))
os.mkdir(os.path.join(replaypath, "cdau64", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdas8"))
os.mkdir(os.path.join(replaypath, "cdas8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdas16"))
os.mkdir(os.path.join(replaypath, "cdas16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdas32"))
os.mkdir(os.path.join(replaypath, "cdas32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdas64"))
os.mkdir(os.path.join(replaypath, "cdas64", "cdrom"))

os.mkdir(os.path.join(replaypath, "cdsd"))
os.mkdir(os.path.join(replaypath, "cdsd", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdsf"))
os.mkdir(os.path.join(replaypath, "cdsf", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdsu8"))
os.mkdir(os.path.join(replaypath, "cdsu8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdsu16"))
os.mkdir(os.path.join(replaypath, "cdsu16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdsu32"))
os.mkdir(os.path.join(replaypath, "cdsu32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdsu64"))
os.mkdir(os.path.join(replaypath, "cdsu64", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdss8"))
os.mkdir(os.path.join(replaypath, "cdss8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdss16"))
os.mkdir(os.path.join(replaypath, "cdss16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdss32"))
os.mkdir(os.path.join(replaypath, "cdss32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdss64"))
os.mkdir(os.path.join(replaypath, "cdss64", "cdrom"))

os.mkdir(os.path.join(replaypath, "cdmd"))
os.mkdir(os.path.join(replaypath, "cdmd", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdmf"))
os.mkdir(os.path.join(replaypath, "cdmf", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdmu8"))
os.mkdir(os.path.join(replaypath, "cdmu8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdmu16"))
os.mkdir(os.path.join(replaypath, "cdmu16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdmu32"))
os.mkdir(os.path.join(replaypath, "cdmu32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdmu64"))
os.mkdir(os.path.join(replaypath, "cdmu64", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdms8"))
os.mkdir(os.path.join(replaypath, "cdms8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdms16"))
os.mkdir(os.path.join(replaypath, "cdms16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdms32"))
os.mkdir(os.path.join(replaypath, "cdms32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdms64"))
os.mkdir(os.path.join(replaypath, "cdms64", "cdrom"))

os.mkdir(os.path.join(replaypath, "cddd"))
os.mkdir(os.path.join(replaypath, "cddd", "cdrom"))
os.mkdir(os.path.join(replaypath, "cddf"))
os.mkdir(os.path.join(replaypath, "cddf", "cdrom"))
os.mkdir(os.path.join(replaypath, "cddu8"))
os.mkdir(os.path.join(replaypath, "cddu8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cddu16"))
os.mkdir(os.path.join(replaypath, "cddu16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cddu32"))
os.mkdir(os.path.join(replaypath, "cddu32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cddu64"))
os.mkdir(os.path.join(replaypath, "cddu64", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdds8"))
os.mkdir(os.path.join(replaypath, "cdds8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdds16"))
os.mkdir(os.path.join(replaypath, "cdds16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdds32"))
os.mkdir(os.path.join(replaypath, "cdds32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdds64"))
os.mkdir(os.path.join(replaypath, "cdds64", "cdrom"))

os.mkdir(os.path.join(replaypath, "cdmodu8"))
os.mkdir(os.path.join(replaypath, "cdmodu8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdmodu16"))
os.mkdir(os.path.join(replaypath, "cdmodu16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdmodu32"))
os.mkdir(os.path.join(replaypath, "cdmodu32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdmodu64"))
os.mkdir(os.path.join(replaypath, "cdmodu64", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdmods8"))
os.mkdir(os.path.join(replaypath, "cdmods8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdmods16"))
os.mkdir(os.path.join(replaypath, "cdmods16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdmods32"))
os.mkdir(os.path.join(replaypath, "cdmods32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdmods64"))
os.mkdir(os.path.join(replaypath, "cdmods64", "cdrom"))

os.mkdir(os.path.join(replaypath, "cdbwnu8"))
os.mkdir(os.path.join(replaypath, "cdbwnu8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwnu16"))
os.mkdir(os.path.join(replaypath, "cdbwnu16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwnu32"))
os.mkdir(os.path.join(replaypath, "cdbwnu32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwnu64"))
os.mkdir(os.path.join(replaypath, "cdbwnu64", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwns8"))
os.mkdir(os.path.join(replaypath, "cdbwns8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwns16"))
os.mkdir(os.path.join(replaypath, "cdbwns16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwns32"))
os.mkdir(os.path.join(replaypath, "cdbwns32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwns64"))
os.mkdir(os.path.join(replaypath, "cdbwns64", "cdrom"))

os.mkdir(os.path.join(replaypath, "cdbwau8"))
os.mkdir(os.path.join(replaypath, "cdbwau8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwau16"))
os.mkdir(os.path.join(replaypath, "cdbwau16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwau32"))
os.mkdir(os.path.join(replaypath, "cdbwau32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwau64"))
os.mkdir(os.path.join(replaypath, "cdbwau64", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwas8"))
os.mkdir(os.path.join(replaypath, "cdbwas8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwas16"))
os.mkdir(os.path.join(replaypath, "cdbwas16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwas32"))
os.mkdir(os.path.join(replaypath, "cdbwas32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwas64"))
os.mkdir(os.path.join(replaypath, "cdbwas64", "cdrom"))

os.mkdir(os.path.join(replaypath, "cdbwou8"))
os.mkdir(os.path.join(replaypath, "cdbwou8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwou16"))
os.mkdir(os.path.join(replaypath, "cdbwou16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwou32"))
os.mkdir(os.path.join(replaypath, "cdbwou32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwou64"))
os.mkdir(os.path.join(replaypath, "cdbwou64", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwos8"))
os.mkdir(os.path.join(replaypath, "cdbwos8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwos16"))
os.mkdir(os.path.join(replaypath, "cdbwos16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwos32"))
os.mkdir(os.path.join(replaypath, "cdbwos32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwos64"))
os.mkdir(os.path.join(replaypath, "cdbwos64", "cdrom"))

os.mkdir(os.path.join(replaypath, "cdbwxu8"))
os.mkdir(os.path.join(replaypath, "cdbwxu8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwxu16"))
os.mkdir(os.path.join(replaypath, "cdbwxu16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwxu32"))
os.mkdir(os.path.join(replaypath, "cdbwxu32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwxu64"))
os.mkdir(os.path.join(replaypath, "cdbwxu64", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwxs8"))
os.mkdir(os.path.join(replaypath, "cdbwxs8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwxs16"))
os.mkdir(os.path.join(replaypath, "cdbwxs16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwxs32"))
os.mkdir(os.path.join(replaypath, "cdbwxs32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwxs64"))
os.mkdir(os.path.join(replaypath, "cdbwxs64", "cdrom"))

os.mkdir(os.path.join(replaypath, "cdbwslu8"))
os.mkdir(os.path.join(replaypath, "cdbwslu8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwslu16"))
os.mkdir(os.path.join(replaypath, "cdbwslu16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwslu32"))
os.mkdir(os.path.join(replaypath, "cdbwslu32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwslu64"))
os.mkdir(os.path.join(replaypath, "cdbwslu64", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwsls8"))
os.mkdir(os.path.join(replaypath, "cdbwsls8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwsls16"))
os.mkdir(os.path.join(replaypath, "cdbwsls16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwsls32"))
os.mkdir(os.path.join(replaypath, "cdbwsls32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwsls64"))
os.mkdir(os.path.join(replaypath, "cdbwsls64", "cdrom"))

os.mkdir(os.path.join(replaypath, "cdbwsru8"))
os.mkdir(os.path.join(replaypath, "cdbwsru8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwsru16"))
os.mkdir(os.path.join(replaypath, "cdbwsru16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwsru32"))
os.mkdir(os.path.join(replaypath, "cdbwsru32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwsru64"))
os.mkdir(os.path.join(replaypath, "cdbwsru64", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwsrs8"))
os.mkdir(os.path.join(replaypath, "cdbwsrs8", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwsrs16"))
os.mkdir(os.path.join(replaypath, "cdbwsrs16", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwsrs32"))
os.mkdir(os.path.join(replaypath, "cdbwsrs32", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdbwsrs64"))
os.mkdir(os.path.join(replaypath, "cdbwsrs64", "cdrom"))

os.mkdir(os.path.join(replaypath, "cdmalloc"))
os.mkdir(os.path.join(replaypath, "cdmalloc", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdmemset"))
os.mkdir(os.path.join(replaypath, "cdmemset", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdmemcpy"))
os.mkdir(os.path.join(replaypath, "cdmemcpy", "cdrom"))
os.mkdir(os.path.join(replaypath, "cd11"))
os.mkdir(os.path.join(replaypath, "cd11", "cdrom"))

os.mkdir(os.path.join(replaypath, "cdlabel"))
os.mkdir(os.path.join(replaypath, "cdlabel", "cdrom"))


tutpath = os.path.join(newtaintpath, "panda_test", "taint_unittest")

os.system("cd " + tutpath + " && ./build.sh")
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cde", "cdrom"))

os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdad", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdaf", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdau8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdau16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdau32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdau64", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdas8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdas16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdas32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdas64", "cdrom"))

os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdsd", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdsf", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdsu8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdsu16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdsu32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdsu64", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdss8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdss16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdss32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdss64", "cdrom"))

os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmd", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmf", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmu8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmu16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmu32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmu64", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdms8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdms16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdms32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdms64", "cdrom"))

os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cddd", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cddf", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cddu8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cddu16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cddu32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cddu64", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdds8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdds16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdds32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdds64", "cdrom"))

os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmodu8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmodu16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmodu32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmodu64", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmods8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmods16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmods32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmods64", "cdrom"))

os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwnu8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwnu16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwnu32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwnu64", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwns8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwns16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwns32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwns64", "cdrom"))

os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwau8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwau16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwau32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwau64", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwas8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwas16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwas32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwas64", "cdrom"))

os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwou8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwou16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwou32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwou64", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwos8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwos16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwos32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwos64", "cdrom"))

os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwxu8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwxu16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwxu32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwxu64", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwxs8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwxs16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwxs32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwxs64", "cdrom"))

os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwslu8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwslu16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwslu32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwslu64", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwsls8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwsls16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwsls32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwsls64", "cdrom"))

os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwsru8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwsru16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwsru32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwsru64", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwsrs8", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwsrs16", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwsrs32", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdbwsrs64", "cdrom"))

os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmalloc", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmemset", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmemcpy", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cd11", "cdrom"))

os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdlabel", "cdrom"))


guestcmde = "guest:cde || cd " + os.path.join(replaypath, "cde", "cdrom") + " && ./turn_on_taint && ./eax_test"

guestcmdad = "guest:cdad || cd " + os.path.join(replaypath, "cdad", "cdrom") + " && ./turn_on_taint && ./add_double"
guestcmdaf = "guest:cdaf || cd " + os.path.join(replaypath, "cdaf", "cdrom") + " && ./turn_on_taint && ./add_float"
guestcmdau8 = "guest:cdau8 || cd " + os.path.join(replaypath, "cdau8", "cdrom") + " && ./turn_on_taint && ./add_uint8"
guestcmdau16 = "guest:cdau16 || cd " + os.path.join(replaypath, "cdau16", "cdrom") + " && ./turn_on_taint && ./add_uint16"
guestcmdau32 = "guest:cdau32 || cd " + os.path.join(replaypath, "cdau32", "cdrom") + " && ./turn_on_taint && ./add_uint32"
guestcmdau64 = "guest:cdau64 || cd " + os.path.join(replaypath, "cdau64", "cdrom") + " && ./turn_on_taint && ./add_uint64"
guestcmdas8 = "guest:cdas8 || cd " + os.path.join(replaypath, "cdas8", "cdrom") + " && ./turn_on_taint && ./add_sint8"
guestcmdas16 = "guest:cdas16 || cd " + os.path.join(replaypath, "cdas16", "cdrom") + " && ./turn_on_taint && ./add_sint16"
guestcmdas32 = "guest:cdas32 || cd " + os.path.join(replaypath, "cdas32", "cdrom") + " && ./turn_on_taint && ./add_sint32"
guestcmdas64 = "guest:cdas64 || cd " + os.path.join(replaypath, "cdas64", "cdrom") + " && ./turn_on_taint && ./add_sint64"

guestcmdsd = "guest:cdsd || cd " + os.path.join(replaypath, "cdsd", "cdrom") + " && ./turn_on_taint && ./sub_double"
guestcmdsf = "guest:cdsf || cd " + os.path.join(replaypath, "cdsf", "cdrom") + " && ./turn_on_taint && ./sub_float"
guestcmdsu8 = "guest:cdsu8 || cd " + os.path.join(replaypath, "cdsu8", "cdrom") + " && ./turn_on_taint && ./sub_uint8"
guestcmdsu16 = "guest:cdsu16 || cd " + os.path.join(replaypath, "cdsu16", "cdrom") + " && ./turn_on_taint && ./sub_uint16"
guestcmdsu32 = "guest:cdsu32 || cd " + os.path.join(replaypath, "cdsu32", "cdrom") + " && ./turn_on_taint && ./sub_uint32"
guestcmdsu64 = "guest:cdsu64 || cd " + os.path.join(replaypath, "cdsu64", "cdrom") + " && ./turn_on_taint && ./sub_uint64"
guestcmdss8 = "guest:cdss8 || cd " + os.path.join(replaypath, "cdss8", "cdrom") + " && ./turn_on_taint && ./sub_sint8"
guestcmdss16 = "guest:cdss16 || cd " + os.path.join(replaypath, "cdss16", "cdrom") + " && ./turn_on_taint && ./sub_sint16"
guestcmdss32 = "guest:cdss32 || cd " + os.path.join(replaypath, "cdss32", "cdrom") + " && ./turn_on_taint && ./sub_sint32"
guestcmdss64 = "guest:cdss64 || cd " + os.path.join(replaypath, "cdss64", "cdrom") + " && ./turn_on_taint && ./sub_sint64"

guestcmdmd = "guest:cdmd || cd " + os.path.join(replaypath, "cdmd", "cdrom") + " && ./turn_on_taint && ./mul_double"
guestcmdmf = "guest:cdmf || cd " + os.path.join(replaypath, "cdmf", "cdrom") + " && ./turn_on_taint && ./mul_float"
guestcmdmu8 = "guest:cdmu8 || cd " + os.path.join(replaypath, "cdmu8", "cdrom") + " && ./turn_on_taint && ./mul_uint8"
guestcmdmu16 = "guest:cdmu16 || cd " + os.path.join(replaypath, "cdmu16", "cdrom") + " && ./turn_on_taint && ./mul_uint16"
guestcmdmu32 = "guest:cdmu32 || cd " + os.path.join(replaypath, "cdmu32", "cdrom") + " && ./turn_on_taint && ./mul_uint32"
guestcmdmu64 = "guest:cdmu64 || cd " + os.path.join(replaypath, "cdmu64", "cdrom") + " && ./turn_on_taint && ./mul_uint64"
guestcmdms8 = "guest:cdms8 || cd " + os.path.join(replaypath, "cdms8", "cdrom") + " && ./turn_on_taint && ./mul_sint8"
guestcmdms16 = "guest:cdms16 || cd " + os.path.join(replaypath, "cdms16", "cdrom") + " && ./turn_on_taint && ./mul_sint16"
guestcmdms32 = "guest:cdms32 || cd " + os.path.join(replaypath, "cdms32", "cdrom") + " && ./turn_on_taint && ./mul_sint32"
guestcmdms64 = "guest:cdms64 || cd " + os.path.join(replaypath, "cdms64", "cdrom") + " && ./turn_on_taint && ./mul_sint64"

guestcmddd = "guest:cddd || cd " + os.path.join(replaypath, "cddd", "cdrom") + " && ./turn_on_taint && ./div_double"
guestcmddf = "guest:cddf || cd " + os.path.join(replaypath, "cddf", "cdrom") + " && ./turn_on_taint && ./div_float"
guestcmddu8 = "guest:cddu8 || cd " + os.path.join(replaypath, "cddu8", "cdrom") + " && ./turn_on_taint && ./div_uint8"
guestcmddu16 = "guest:cddu16 || cd " + os.path.join(replaypath, "cddu16", "cdrom") + " && ./turn_on_taint && ./div_uint16"
guestcmddu32 = "guest:cddu32 || cd " + os.path.join(replaypath, "cddu32", "cdrom") + " && ./turn_on_taint && ./div_uint32"
guestcmddu64 = "guest:cddu64 || cd " + os.path.join(replaypath, "cddu64", "cdrom") + " && ./turn_on_taint && ./div_uint64"
guestcmdds8 = "guest:cdds8 || cd " + os.path.join(replaypath, "cdds8", "cdrom") + " && ./turn_on_taint && ./div_sint8"
guestcmdds16 = "guest:cdds16 || cd " + os.path.join(replaypath, "cdds16", "cdrom") + " && ./turn_on_taint && ./div_sint16"
guestcmdds32 = "guest:cdds32 || cd " + os.path.join(replaypath, "cdds32", "cdrom") + " && ./turn_on_taint && ./div_sint32"
guestcmdds64 = "guest:cdds64 || cd " + os.path.join(replaypath, "cdds64", "cdrom") + " && ./turn_on_taint && ./div_sint64"

guestcmdmodu8 = "guest:cdmodu8 || cd " + os.path.join(replaypath, "cdmodu8", "cdrom") + " && ./turn_on_taint && ./mod_uint8"
guestcmdmodu16 = "guest:cdmodu16 || cd " + os.path.join(replaypath, "cdmodu16", "cdrom") + " && ./turn_on_taint && ./mod_uint16"
guestcmdmodu32 = "guest:cdmodu32 || cd " + os.path.join(replaypath, "cdmodu32", "cdrom") + " && ./turn_on_taint && ./mod_uint32"
guestcmdmodu64 = "guest:cdmodu64 || cd " + os.path.join(replaypath, "cdmodu64", "cdrom") + " && ./turn_on_taint && ./mod_uint64"
guestcmdmods8 = "guest:cdmods8 || cd " + os.path.join(replaypath, "cdmods8", "cdrom") + " && ./turn_on_taint && ./mod_sint8"
guestcmdmods16 = "guest:cdmods16 || cd " + os.path.join(replaypath, "cdmods16", "cdrom") + " && ./turn_on_taint && ./mod_sint16"
guestcmdmods32 = "guest:cdmods32 || cd " + os.path.join(replaypath, "cdmods32", "cdrom") + " && ./turn_on_taint && ./mod_sint32"
guestcmdmods64 = "guest:cdmods64 || cd " + os.path.join(replaypath, "cdmods64", "cdrom") + " && ./turn_on_taint && ./mod_sint64"

guestcmdbwnu8 = "guest:cdbwnu8 || cd " + os.path.join(replaypath, "cdbwnu8", "cdrom") + " && ./turn_on_taint && ./bwnot_uint8"
guestcmdbwnu16 = "guest:cdbwnu16 || cd " + os.path.join(replaypath, "cdbwnu16", "cdrom") + " && ./turn_on_taint && ./bwnot_uint16"
guestcmdbwnu32 = "guest:cdbwnu32 || cd " + os.path.join(replaypath, "cdbwnu32", "cdrom") + " && ./turn_on_taint && ./bwnot_uint32"
guestcmdbwnu64 = "guest:cdbwnu64 || cd " + os.path.join(replaypath, "cdbwnu64", "cdrom") + " && ./turn_on_taint && ./bwnot_uint64"
guestcmdbwns8 = "guest:cdbwns8 || cd " + os.path.join(replaypath, "cdbwns8", "cdrom") + " && ./turn_on_taint && ./bwnot_sint8"
guestcmdbwns16 = "guest:cdbwns16 || cd " + os.path.join(replaypath, "cdbwns16", "cdrom") + " && ./turn_on_taint && ./bwnot_sint16"
guestcmdbwns32 = "guest:cdbwns32 || cd " + os.path.join(replaypath, "cdbwns32", "cdrom") + " && ./turn_on_taint && ./bwnot_sint32"
guestcmdbwns64 = "guest:cdbwns64 || cd " + os.path.join(replaypath, "cdbwns64", "cdrom") + " && ./turn_on_taint && ./bwnot_sint64"

guestcmdbwau8 = "guest:cdbwau8 || cd " + os.path.join(replaypath, "cdbwau8", "cdrom") + " && ./turn_on_taint && ./bwand_uint8"
guestcmdbwau16 = "guest:cdbwau16 || cd " + os.path.join(replaypath, "cdbwau16", "cdrom") + " && ./turn_on_taint && ./bwand_uint16"
guestcmdbwau32 = "guest:cdbwau32 || cd " + os.path.join(replaypath, "cdbwau32", "cdrom") + " && ./turn_on_taint && ./bwand_uint32"
guestcmdbwau64 = "guest:cdbwau64 || cd " + os.path.join(replaypath, "cdbwau64", "cdrom") + " && ./turn_on_taint && ./bwand_uint64"
guestcmdbwas8 = "guest:cdbwas8 || cd " + os.path.join(replaypath, "cdbwas8", "cdrom") + " && ./turn_on_taint && ./bwand_sint8"
guestcmdbwas16 = "guest:cdbwas16 || cd " + os.path.join(replaypath, "cdbwas16", "cdrom") + " && ./turn_on_taint && ./bwand_sint16"
guestcmdbwas32 = "guest:cdbwas32 || cd " + os.path.join(replaypath, "cdbwas32", "cdrom") + " && ./turn_on_taint && ./bwand_sint32"
guestcmdbwas64 = "guest:cdbwas64 || cd " + os.path.join(replaypath, "cdbwas64", "cdrom") + " && ./turn_on_taint && ./bwand_sint64"

guestcmdbwou8 = "guest:cdbwou8 || cd " + os.path.join(replaypath, "cdbwou8", "cdrom") + " && ./turn_on_taint && ./bwor_uint8"
guestcmdbwou16 = "guest:cdbwou16 || cd " + os.path.join(replaypath, "cdbwou16", "cdrom") + " && ./turn_on_taint && ./bwor_uint16"
guestcmdbwou32 = "guest:cdbwou32 || cd " + os.path.join(replaypath, "cdbwou32", "cdrom") + " && ./turn_on_taint && ./bwor_uint32"
guestcmdbwou64 = "guest:cdbwou64 || cd " + os.path.join(replaypath, "cdbwou64", "cdrom") + " && ./turn_on_taint && ./bwor_uint64"
guestcmdbwos8 = "guest:cdbwos8 || cd " + os.path.join(replaypath, "cdbwos8", "cdrom") + " && ./turn_on_taint && ./bwor_sint8"
guestcmdbwos16 = "guest:cdbwos16 || cd " + os.path.join(replaypath, "cdbwos16", "cdrom") + " && ./turn_on_taint && ./bwor_sint16"
guestcmdbwos32 = "guest:cdbwos32 || cd " + os.path.join(replaypath, "cdbwos32", "cdrom") + " && ./turn_on_taint && ./bwor_sint32"
guestcmdbwos64 = "guest:cdbwos64 || cd " + os.path.join(replaypath, "cdbwos64", "cdrom") + " && ./turn_on_taint && ./bwor_sint64"

guestcmdbwxu8  = "guest:cdbwxu8  || cd " + os.path.join(replaypath, "cdbwxu8", "cdrom")  + " && ./turn_on_taint && ./bwxor_uint8"
guestcmdbwxu16 = "guest:cdbwxu16 || cd " + os.path.join(replaypath, "cdbwxu16", "cdrom") + " && ./turn_on_taint && ./bwxor_uint16"
guestcmdbwxu32 = "guest:cdbwxu32 || cd " + os.path.join(replaypath, "cdbwxu32", "cdrom") + " && ./turn_on_taint && ./bwxor_uint32"
guestcmdbwxu64 = "guest:cdbwxu64 || cd " + os.path.join(replaypath, "cdbwxu64", "cdrom") + " && ./turn_on_taint && ./bwxor_uint64"
guestcmdbwxs8  = "guest:cdbwxs8  || cd " + os.path.join(replaypath, "cdbwxs8", "cdrom")  + " && ./turn_on_taint && ./bwxor_sint8"
guestcmdbwxs16 = "guest:cdbwxs16 || cd " + os.path.join(replaypath, "cdbwxs16", "cdrom") + " && ./turn_on_taint && ./bwxor_sint16"
guestcmdbwxs32 = "guest:cdbwxs32 || cd " + os.path.join(replaypath, "cdbwxs32", "cdrom") + " && ./turn_on_taint && ./bwxor_sint32"
guestcmdbwxs64 = "guest:cdbwxs64 || cd " + os.path.join(replaypath, "cdbwxs64", "cdrom") + " && ./turn_on_taint && ./bwxor_sint64"

guestcmdbwslu8  = "guest:cdbwslu8  || cd " + os.path.join(replaypath, "cdbwslu8", "cdrom")  + " && ./turn_on_taint && ./bwsl_uint8"
guestcmdbwslu16 = "guest:cdbwslu16 || cd " + os.path.join(replaypath, "cdbwslu16", "cdrom") + " && ./turn_on_taint && ./bwsl_uint16"
guestcmdbwslu32 = "guest:cdbwslu32 || cd " + os.path.join(replaypath, "cdbwslu32", "cdrom") + " && ./turn_on_taint && ./bwsl_uint32"
guestcmdbwslu64 = "guest:cdbwslu64 || cd " + os.path.join(replaypath, "cdbwslu64", "cdrom") + " && ./turn_on_taint && ./bwsl_uint64"
guestcmdbwsls8  = "guest:cdbwsls8  || cd " + os.path.join(replaypath, "cdbwsls8", "cdrom")  + " && ./turn_on_taint && ./bwsl_sint8"
guestcmdbwsls16 = "guest:cdbwsls16 || cd " + os.path.join(replaypath, "cdbwsls16", "cdrom") + " && ./turn_on_taint && ./bwsl_sint16"
guestcmdbwsls32 = "guest:cdbwsls32 || cd " + os.path.join(replaypath, "cdbwsls32", "cdrom") + " && ./turn_on_taint && ./bwsl_sint32"
guestcmdbwsls64 = "guest:cdbwsls64 || cd " + os.path.join(replaypath, "cdbwsls64", "cdrom") + " && ./turn_on_taint && ./bwsl_sint64"

guestcmdbwsru8  = "guest:cdbwsru8  || cd " + os.path.join(replaypath, "cdbwsru8", "cdrom")  + " && ./turn_on_taint && ./bwsr_uint8"
guestcmdbwsru16 = "guest:cdbwsru16 || cd " + os.path.join(replaypath, "cdbwsru16", "cdrom") + " && ./turn_on_taint && ./bwsr_uint16"
guestcmdbwsru32 = "guest:cdbwsru32 || cd " + os.path.join(replaypath, "cdbwsru32", "cdrom") + " && ./turn_on_taint && ./bwsr_uint32"
guestcmdbwsru64 = "guest:cdbwsru64 || cd " + os.path.join(replaypath, "cdbwsru64", "cdrom") + " && ./turn_on_taint && ./bwsr_uint64"
guestcmdbwsrs8  = "guest:cdbwsrs8  || cd " + os.path.join(replaypath, "cdbwsrs8", "cdrom")  + " && ./turn_on_taint && ./bwsr_sint8"
guestcmdbwsrs16 = "guest:cdbwsrs16 || cd " + os.path.join(replaypath, "cdbwsrs16", "cdrom") + " && ./turn_on_taint && ./bwsr_sint16"
guestcmdbwsrs32 = "guest:cdbwsrs32 || cd " + os.path.join(replaypath, "cdbwsrs32", "cdrom") + " && ./turn_on_taint && ./bwsr_sint32"
guestcmdbwsrs64 = "guest:cdbwsrs64 || cd " + os.path.join(replaypath, "cdbwsrs64", "cdrom") + " && ./turn_on_taint && ./bwsr_sint64"

guestcmdmalloc = "guest:cdmalloc || cd " + os.path.join(replaypath, "cdmalloc", "cdrom") + " && ./turn_on_taint && ./malloc"
guestcmdmemset = "guest:cdmemset || cd " + os.path.join(replaypath, "cdmemset", "cdrom") + " && ./turn_on_taint && ./memset"
guestcmdmemcpy = "guest:cdmemcpy || cd " + os.path.join(replaypath, "cdmemcpy", "cdrom") + " && ./turn_on_taint && ./memcpy"
guestcmd11 = "guest:cd11 || cd " + os.path.join(replaypath, "cd11", "cdrom") + " && ./turn_on_taint && ./test11"

guestcmdlabel = "guest:cdlabel || cd " + os.path.join(replaypath, "cdlabel", "cdrom") + " && ./turn_on_taint && ./label"



try:
    record_debian(guestcmde, "cde", "i386")
except:
    print("ok")



try:
    record_debian(guestcmdad, "cdad", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdaf, "cdaf", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdau8, "cdau8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdau16, "cdau16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdau32, "cdau32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdau64, "cdau64", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdas8, "cdas8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdas16, "cdas16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdas32, "cdas32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdas64, "cdas64", "i386")
except:
    print("ok")



try:
    record_debian(guestcmdsd, "cdsd", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdsf, "cdsf", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdsu8, "cdsu8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdsu16, "cdsu16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdsu32, "cdsu32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdsu64, "cdsu64", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdss8, "cdss8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdss16, "cdss16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdss32, "cdss32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdss64, "cdss64", "i386")
except:
    print("ok")



try:
    record_debian(guestcmdmd, "cdmd", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdmf, "cdmf", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdmu8, "cdmu8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdmu16, "cdmu16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdmu32, "cdmu32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdmu64, "cdmu64", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdms8, "cdms8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdms16, "cdms16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdms32, "cdms32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdms64, "cdms64", "i386")
except:
    print("ok")



try:
    record_debian(guestcmddd, "cddd", "i386")
except:
    print("ok")
try:
    record_debian(guestcmddf, "cddf", "i386")
except:
    print("ok")
try:
    record_debian(guestcmddu8, "cddu8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmddu16, "cddu16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmddu32, "cddu32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmddu64, "cddu64", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdds8, "cdds8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdds16, "cdds16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdds32, "cdds32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdds64, "cdds64", "i386")
except:
    print("ok")



try:
    record_debian(guestcmdmodu8, "cdmodu8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdmodu16, "cdmodu16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdmodu32, "cdmodu32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdmodu64, "cdmodu64", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdmods8, "cdmods8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdmods16, "cdmods16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdmods32, "cdmods32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdmods64, "cdmods64", "i386")
except:
    print("ok")



try:
    record_debian(guestcmdbwnu8, "cdbwnu8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwnu16, "cdbwnu16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwnu32, "cdbwnu32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwnu64, "cdbwnu64", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwns8, "cdbwns8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwns16, "cdbwns16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwns32, "cdbwns32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwns64, "cdbwns64", "i386")
except:
    print("ok")



try:
    record_debian(guestcmdbwau8, "cdbwau8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwau16, "cdbwau16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwau32, "cdbwau32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwau64, "cdbwau64", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwas8, "cdbwas8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwas16, "cdbwas16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwas32, "cdbwas32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwas64, "cdbwas64", "i386")
except:
    print("ok")



try:
    record_debian(guestcmdbwou8, "cdbwou8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwou16, "cdbwou16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwou32, "cdbwou32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwou64, "cdbwou64", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwos8, "cdbwos8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwos16, "cdbwos16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwos32, "cdbwos32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwos64, "cdbwos64", "i386")
except:
    print("ok")



try:
    record_debian(guestcmdbwxu8, "cdbwxu8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwxu16, "cdbwxu16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwxu32, "cdbwxu32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwxu64, "cdbwxu64", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwxs8, "cdbwxs8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwxs16, "cdbwxs16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwxs32, "cdbwxs32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwxs64, "cdbwxs64", "i386")
except:
    print("ok")



try:
    record_debian(guestcmdbwslu8, "cdbwslu8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwslu16, "cdbwslu16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwslu32, "cdbwslu32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwslu64, "cdbwslu64", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwsls8, "cdbwsls8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwsls16, "cdbwsls16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwsls32, "cdbwsls32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwsls64, "cdbwsls64", "i386")
except:
    print("ok")



try:
    record_debian(guestcmdbwsru8, "cdbwsru8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwsru16, "cdbwsru16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwsru32, "cdbwsru32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwsru64, "cdbwsru64", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwsrs8, "cdbwsrs8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwsrs16, "cdbwsrs16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwsrs32, "cdbwsrs32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdbwsrs64, "cdbwsrs64", "i386")
except:
    print("ok")



try:
    record_debian(guestcmdmalloc, "cdmalloc", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdmemset, "cdmemset", "i386")
except:
    print("ok")
try:
    record_debian(guestcmdmemcpy, "cdmemcpy", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd11, "cd11", "i386")
except:
    print("ok")



try:
    record_debian(guestcmdlabel, "cdlabel", "i386")
except:
    print("ok")



sys.exit(0)
