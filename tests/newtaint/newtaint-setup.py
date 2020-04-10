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

os.mkdir(os.path.join(replaypath, "cdmalloc"))
os.mkdir(os.path.join(replaypath, "cdmalloc", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdmemset"))
os.mkdir(os.path.join(replaypath, "cdmemset", "cdrom"))
os.mkdir(os.path.join(replaypath, "cdmemcpy"))
os.mkdir(os.path.join(replaypath, "cdmemcpy", "cdrom"))
os.mkdir(os.path.join(replaypath, "cd11"))
os.mkdir(os.path.join(replaypath, "cd11", "cdrom"))

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


os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmalloc", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmemset", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cdmemcpy", "cdrom"))
os.system("cd " + os.path.join(tutpath, "bin") + " && cp * " + os.path.join(replaypath, "cd11", "cdrom"))

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



guestcmdmalloc = "guest:cdmalloc || cd " + os.path.join(replaypath, "cdmalloc", "cdrom") + " && ./turn_on_taint && ./testmalloc"
guestcmdmemset = "guest:cdmemset || cd " + os.path.join(replaypath, "cdmemset", "cdrom") + " && ./turn_on_taint && ./testmemset"
guestcmdmemcpy = "guest:cdmemcpy || cd " + os.path.join(replaypath, "cdmemcpy", "cdrom") + " && ./turn_on_taint && ./testmemcpy"
guestcmd11 = "guest:cd11 || cd " + os.path.join(replaypath, "cd11", "cdrom") + " && ./turn_on_taint && ./test11"

try:
    record_debian(guestcmde, "cde", "i386")
except:
    print("ok")


try:
    record_debian(guestcmd4, "cdad", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdaf", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdau8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdau16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdau32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdau64", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdas8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdas16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdas32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdas64", "i386")
except:
    print("ok")



try:
    record_debian(guestcmd4, "cdsd", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdsf", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdsu8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdsu16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdsu32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdsu64", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdss8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdss16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdss32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdss64", "i386")
except:
    print("ok")



try:
    record_debian(guestcmd4, "cdmd", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdmf", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdmu8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdmu16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdmu32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdmu64", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdms8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdms16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdms32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdms64", "i386")
except:
    print("ok")


try:
    record_debian(guestcmd4, "cddd", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cddf", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cddu8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cddu16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cddu32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cddu64", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdds8", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdds16", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdds32", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd4, "cdds64", "i386")
except:
    print("ok")



try:
    record_debian(guestcmd8, "cdmalloc", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd9, "cdmemset", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd10, "cdmemcpy", "i386")
except:
    print("ok")
try:
    record_debian(guestcmd11, "cd11", "i386")
except:
    print("ok")

sys.exit(0)
