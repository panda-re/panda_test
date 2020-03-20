# Device Driver Interface

Non-exhaustive test (specific subset) of the following whole-system taint transfers:

* Process -> Kernel Driver
* Kernel Driver -> Process
* (TODO) Process -> Kernel Driver -> Other Process (signal-triggered)

Exhaustive test for driver file abstractions (e.g. `/dev/device` and `/sys/device`(TODO)).

* Process -> Driver Inode
* Driver Inode -> Process

### Setup

TODO

### Running Test

TODO