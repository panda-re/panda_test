_: clean all

all: win_serialtaint_rx_branch.exe dos_serialtaint_rx_branch.com linux_serialtaint_rx_branch.elf

win_serialtaint_rx_branch.exe:
	@echo win_serial_rx_branch.exe...
	@i686-w64-mingw32-gcc win_serial_rx_branch.c -o win_serial_rx_branch.exe

dos_serialtaint_rx_branch.com:
	@echo dos_serial_rx_branch.com...
	@nasm -fbin dos_serial_rx_branch.asm -o serialr.com

linux_serialtaint_rx_branch.elf:
	@echo linux_serial_rx_branch.elf...
	@gcc -m32 linux_serial_rx_branch.c -o linux_serial_rx_branch.elf

clean:
	@rm -f *.com *.exe *.elf
