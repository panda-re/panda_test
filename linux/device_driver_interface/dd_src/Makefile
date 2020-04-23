obj-m += tt_ioctl_module.o

KROOT = /lib/modules/$(shell uname -r)/build

CFLAGS_USER="-O2 -Wall -std=gnu11 -pthread"
CFLAGS_KERN="-O2 -Wall"

all allofit: userprogs modules

modules modules_install clean::
	$(MAKE) -C $(KROOT) CFLAGS=$(CFLAGS_KERN) M=$(shell pwd) $@

userprogs:
	$(MAKE) CC="$(CC)" CFLAGS=$(CFLAGS_USER) tt_ioctl_userspace

clean::
	rm -rf  tt_ioctl_userspace Module.symvers modules.order
