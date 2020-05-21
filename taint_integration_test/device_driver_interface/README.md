# Device Driver Interface

### About

Tests for the following whole-system taint transfers (TODO):

* Process -> Kernel (via `ioctl` or driver inode)
* Kernel -> Process (via `ioctl` or driver inode)
* Process -> Kernel -> Other Process (via signal-triggered `ioctl` or driver inode)

Tests are exercised by two components: a [userspace program](./tt_ioctl_userspace.c) and a [kernel module](./tt_ioctl_module.c) that supports [a list of commands](./tt_ioctl_cmds.h).
Driver inodes are `proc` filesystem paths (e.g. `/dev/device` and `/sys/device`).

### Setup

Install PyPANDA per [the documentation](https://github.com/panda-re/panda/blob/master/panda/python/docs/USAGE.md#installation).

Download Python dependencies:

```
pip install -r requirements.txt
```

### Running Test

```
python3 run_dd_test.py
```
