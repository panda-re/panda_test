import atexit
import os
import subprocess
import uuid
import shutil
import socket
import tempfile
import time

import pexpect.fdpexpect

import ptest.testexec as testexec

class RunLive:
    """
    A class to manage a live PANDA run.  The disk image should be provided to
    the Qemu instance passed in, via a Drive instance.  When ready to start the
    guest, call run with monitor=True if access to the Qemu monitor is desired.
    Then the monitor method can be called to fetch the instance of the monitor,
    which is an instance of the fdspawn class from the pexpect utilities.
    """
    def __init__(self, qemu, *plugins, **kwargs):
        self.qemu = qemu
        self.os = None
        self.plog = None
        for k, v in kwargs.items():
            if k == "os":
                self.os = v
            elif k == "plog":
                self.plog = v
        self.plugins = list(plugins)

        stdout_path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        stderr_path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        self.stdout_file = open(stdout_path, "w")
        self.stderr_file = open(stderr_path, "w")

        def delete_files():
            self.stdout_file.close()
            self.stderr_file.close()
            os.remove(self.stdout_file.name)
            os.remove(self.stderr_file.name)
        atexit.register(delete_files)

    def cmdline(self, monitor=False):
        cmdline = self.qemu.cmdline(monitor=monitor)
        
        if self.os:
            cmdline += ["-os", self.os]
        if self.plog:
            cmdline += ["-pandalog", self.plog]
        if not self.plugins:
            return cmdline
        for p in self.plugins:
            cmdline += p.cmdline()
        return cmdline

    def run(self, monitor=False):
        cmdline = self.cmdline(monitor=monitor)
        
        if testexec.verbose:
            print(" ".join(cmdline))
            
        cmdline[0] = os.path.join(testexec.build_directory, cmdline[0])
        spo = subprocess.Popen(cmdline, stdout=self.stdout_file,
            stderr=self.stderr_file)
        def shutdown_panda():
            spo.terminate()
            spo.wait()
        atexit.register(shutdown_panda)
        return spo
        
    def monitor(self):
        return self.qemu.monitor()
                
    def dump_console(self, stdout=True, stderr=False):
        """
        Prints stdout and/or stderr to the console. By default, only stdout is
        printed.
        """
        if (stdout):
            print("STDOUT:")
            print(open(self.stdout_file.name, "r").read())
        if (stderr):
            print("STDERR:")
            print(open(self.stderr_file.name, "r").read())

    def copy_stderr(self, destination):
        """
        Copies the stderr file to the specified destination.
        """
        shutil.copyfile(self.stderr_file.name, destination)

    def copy_stdout(self, destination):
        """
        Copies the stdout file to the specified destination.
        """
        shutil.copyfile(self.stdout_file.name, destination)

    def stdout(self):
        """
        Returns a file handle to the temporary stdout log file.
        """
        return open(self.stdout_file.name, "r")

    def stderr(self):
        """
        Returns a file handle to the temporary stderr log file.
        """
        return open(self.stdout_file.name, "r")
