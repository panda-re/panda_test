obj-m += tt_ioctl_module.o

INCLUDES= -I../../../taint_include
KROOT = /lib/modules/$(shell uname -r)/build
TARGET=TARGET_X86_64

CFLAGS_USER="-O2 -Wall -std=gnu11 -pthread -D $(TARGET) $(INCLUDES)"
CFLAGS_KERN="-O2 -Wall -D $(TARGET) $(INCLUDES)"

all allofit: userprogs modules

modules modules_install clean::
	$(MAKE) -C $(KROOT) CFLAGS=$(CFLAGS_KERN) M=$(shell pwd) $@

userprogs:
	$(MAKE) CC="$(CC)" CFLAGS=$(CFLAGS_USER) tt_ioctl_userspace

clean::
	rm -rf  tt_ioctl_userspace Module.symvers modules.order
