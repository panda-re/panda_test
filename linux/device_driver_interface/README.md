# Device Driver Interface

### About

Non-exhaustive test (specific subset) of the following whole-system taint transfers:

* Process -> Kernel Driver
* Kernel Driver -> Process
* (TODO) Process -> Kernel Driver -> Other Process (signal-triggered)

Exhaustive test for driver file abstractions (e.g. `/dev/device` and `/sys/device`(TODO)).

* Process -> Driver Inode
* Driver Inode -> Process

Tests are exercised by two components: a [userspace program](./tt_ioctl_userspace.c) and a [kernel module](./tt_ioctl_module.c) that supports [a list of commands](./tt_ioctl_cmds.h).

### Setup

TODO

### Running Test

TODO