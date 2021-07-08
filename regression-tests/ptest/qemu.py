import atexit
import os
import subprocess
import socket
import tempfile
import time
import uuid

import pexpect.fdpexpect

import ptest.testexec as testexec

class NetBackend:
    """
    A class to handle the netdev option in QEMU.
    """
    BRIDGE = "bridge"
    USER = "user"

    def __init__(self, ndtype, identifier, **kwargs):
        self.ndtype = ndtype
        self.identifier = identifier
        self.extra = {}
        for key, val in kwargs.items():
            self.extra[key] = val

    def frontend_arg(self):
        return "netdev=%s" % (self.identifier)

    def cmdline(self):
        cmdline = "-netdev %s,id=%s" % (self.ndtype, self.identifier)
        if not self.extra:
            return cmdline.split()
        cmdline += ","
        args = []
        for key in self.extra:
            value = self.extra[key]
            if type(value) == str:
                value = "%s" % (value)
            args.append("%s=%s" % (key, value))
        cmdline += ",".join(args)
        return cmdline.split()
 
class CharBackend:
    """
    A class to handle the chardev option in QEMU.
    """
    PIPE = "pipe"
    SOCKET = "socket"

    def __init__(self, cdtype, identifier, **kwargs):
        self.cdtype = cdtype
        self.identifier = identifier
        self.extra = {}
        for key, val in kwargs.items():
            self.extra[key] = val

    def frontend_arg(self):
        return "chardev=%s" % (self.identifier)

    def cmdline(self):
        cmdline = "-chardev %s,id=%s" % (self.cdtype, self.identifier)
        if not self.extra:
            return cmdline.split()
        cmdline += ","
        args = []
        for key in self.extra:
            value = self.extra[key]
            if type(value) == str:
                value = "%s" % (value)
            args.append("%s=%s" % (key, value))
        cmdline += ",".join(args)
        return cmdline.split()

class Drive:
    """
    A class to handle drives in QEMU
    """
    IDE = "ide"
    SCSI = "scsi"

    def __init__(self, backing_file, identifier, interface=None):
        self.backing_file = backing_file
        self.identifier = identifier
        self.interface = interface

    def frontend_arg(self):
        return "drive=%s" % (self.identifier)

    def cmdline(self):
        cmdline = "-drive if=%s,file=%s,id=%s" % (str(self.interface).lower(), self.backing_file, self.identifier)
        return cmdline.split()
 
class Device:
    """
    A class to handle the device option in QEMU.
    """
    E1000 = "e1000"
    RTL8139 = "rtl8139"
    NE2K_PCI = "ne2k_pci"
    NE2K_ISA = "ne2k_isa"
    ISA_SERIAL = "isa-serial"
    PCI_SERIAL = "pci-serial"
    SCSI_DISK = "scsi-disk"
    USB_TABLET = "usb-tablet"
    IDE_HD = "ide-hd"

    def __init__(self, device, backend=None, **kwargs):
        self.device = device
        self.backend = backend
        self.extra = {}
        for key, val in kwargs.items():
            self.extra[key] = val

    def cmdline(self):
        cmdline = "-device %s" % (self.device)
        if self.backend:
            cmdline += ",%s" % (self.backend.frontend_arg())
        if not self.extra:
            return cmdline.split()
        return cmdline.split()

class Qemu:
    """
    A class to handle manipulation of the QEMU command-line options.
    Note this is for QEMU options only, PANDA options are handled by another
    class.
    """
    I386 = "i386"
    X86_64 = "x86_64"
    ARM = "arm"
    PPC = "ppc"

    CIRRUS = "cirrus"

    DISPLAY_SDL = "sdl"
    DISPLAY_NONE = "none"

    def __init__(self, arch, ram, *extra, **kwargs):
        self.arch = arch
        self.ram = ram
        self.vga = None
        self.machine = None
        self.cpu = None
        
        # this is for non-keyword options, such as "-llvm"
        self.options = None

        for name, value in kwargs.items():
            if name == "vga":
                self.vga = value
            elif name == "machine":
                self.machine = value
            elif name == "cpu":
                self.cpu = value
            elif name == "options":
                self.options = value
        self.extra = list(extra)

    def boot_async(self, loadvm=None, display=DISPLAY_SDL, monitor=False):
        cmdline = self.cmdline(monitor=monitor)

        if loadvm:
            cmdline.append("-loadvm")
            cmdline.append(loadvm)

        cmdline.append("-display")
        cmdline.append(display)

        cmdline[0] = os.path.join(testexec.build_directory, cmdline[0])

        p = subprocess.Popen(cmdline)
        def shutdown_panda():
            p.terminate()
            p.wait()
        atexit.register(shutdown_panda)
        return p

    def cmdline(self, monitor=False):
        cmdline = ["%s-softmmu/panda-system-%s" % (self.arch, self.arch), "-m", str(self.ram)]
        if True == testexec.get_build_is_bindir():
            cmdline = ["panda-system-%s" % (self.arch), "-m", str(self.ram)]
        if self.vga:
            cmdline += ["-vga", self.vga]
        if self.machine:
            cmdline += ["-machine", self.machine]
        if self.cpu:
            cmdline += ["-cpu", self.cpu]
        if self.options:
            cmdline += self.options.split()
        for arg in self.extra:
            cmdline += arg.cmdline()
            
        if monitor:
            self.monitor_path = os.path.join(tempfile.gettempdir(),
                str(uuid.uuid4()))
            cmdline.append("-monitor")
            cmdline.append("unix:" + self.monitor_path + ",server,nowait")
            
        return cmdline

    def monitor(self):
        retries = 10
        while retries > 0:
            retries -= 1
            try:
                self._mon_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self._mon_sock.connect(self.monitor_path)
                return pexpect.fdpexpect.fdspawn(self._mon_sock)
            except Exception as e:
                if retries == 0:
                    raise e
                print("waiting for qemu monitor...")
                time.sleep(1)

if __name__ == "__main__":
    netdev = NetBackend(NetBackend.BRIDGE, "net0", helper="/usr/local/bin/qemu-bridge-helper")
    print(netdev.cmdline())
    netdev = NetBackend(NetBackend.USER, "net1")
    print(netdev.cmdline())

    chardev = CharBackend(CharBackend.PIPE, "com1", path="/tmp/com1")
    print(chardev.cmdline())
    chardev = CharBackend(CharBackend.SOCKET, "com2", path="/tmp/com2.socket")
    print(chardev.cmdline())

    e1000 = Device(Device.E1000, backend=netdev)
    print(e1000.cmdline())
    pciser = Device(Device.PCI_SERIAL, backend=chardev)
    print(pciser.cmdline())

    qemu = Qemu(Qemu.I386, 1024, netdev, e1000, chardev, pciser)
    print(qemu.cmdline())
