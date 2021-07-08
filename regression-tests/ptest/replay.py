import atexit
import os
import subprocess
import uuid
import shutil
import tempfile

import ptest.testexec as testexec

class Replay:
    """
    A class to manage a replay.
    """
    def __init__(self, name, qemu, *plugins, **kwargs):
        self.name = testexec.resolve_replay(name)
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

    def cmdline(self):
        cmdline = self.qemu.cmdline() + ["-replay", self.name]
        if self.os:
            cmdline += ["-os", self.os]
        if self.plog:
            cmdline += ["-pandalog", self.plog]
        if not self.plugins:
            return cmdline
        for p in self.plugins:
            cmdline += p.cmdline()
        return cmdline

    def run(self):
        cmdline = self.cmdline()
        if testexec.verbose:
            print(" ".join(cmdline))
        cmdline[0] = os.path.join(testexec.build_directory, cmdline[0])
        retcode = subprocess.call(cmdline, stdout=self.stdout_file, stderr=self.stderr_file)
        return retcode

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
        return open(self.stderr_file.name, "r")

if __name__ == "__main__":
    from qemu import *
    net0 = NetBackend(NetBackend.BRIDGE, "net0", helper="/usr/local/bin/qemu-bridge-helper")
    rtl8139 = Device(Device.RTL8139, backend=net0)
    com1 = CharBackend(CharBackend.PIPE, "com1", path="/tmp/com1")
    pciser = Device(Device.PCI_SERIAL, backend=com1)
    replay = Replay("testrec", Qemu(Qemu.I386, 2048, net0, rtl8139, com1, pciser, vga=Qemu.CIRRUS))
    print(replay.cmdline())
