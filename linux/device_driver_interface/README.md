# Device Driver Interface

Non-exhaustive test (specific subset) of the following whole-system taint transfers:

* Process -> Kernel Driver
* Kernel Driver -> Process
* (TODO) Process -> Kernel Driver -> Other Process (signal-triggered)

Exhaustive test for process <-> driver inode (e.g. "/dev/device" and "/sys/device"(TODO)).

* Process -> Driver inode
* Driver inode -> Process

### Setup

TODO

### Running Test

TODO