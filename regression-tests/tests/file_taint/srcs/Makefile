# Note Windows tests assume you've got MinGW installed.

all: win_singleproc_singlefile.exe win_singleproc_multifile.exe win_multiproc_singlefile.exe win_multiproc_multifile.exe win_positional.exe win_multifile_multiread.exe win_multithread_singlefile.exe win_async.exe linux_singleproc_singlefile.elf linux_singleproc_multifile.elf linux_multiproc_singlefile.elf linux_multiproc_multifile.elf linux_positional.elf linux_multifile_multiread.elf linux_multithread_singlefile.elf linux_pread.elf linux_badread.elf


win_singleproc_singlefile.exe:
	@echo win_singleproc_singlefile.exe...
	@i686-w64-mingw32-gcc win_singleproc_singlefile.c -o win_singleproc_singlefile.exe

win_singleproc_multifile.exe:
	@echo win_singleproc_multifile.exe...
	@i686-w64-mingw32-gcc win_singleproc_multifile.c -o win_singleproc_multifile.exe

win_multiproc_singlefile.exe:
	@echo win_multiproc_singlefile.exe...
	@i686-w64-mingw32-gcc -g win_multiproc_singlefile.c -o win_multiproc_singlefile.exe

win_multiproc_multifile.exe:
	@echo win_multiproc_multifile.exe...
	@i686-w64-mingw32-gcc -g win_multiproc_multifile.c -o win_multiproc_multifile.exe

win_positional.exe:
	@echo win_positional.exe
	@i686-w64-mingw32-gcc win_positional.c -o win_positional.exe

win_multifile_multiread.exe:
	@echo win_multifile_multiread.exe
	@i686-w64-mingw32-gcc win_multifile_multiread.c -o win_multifile_multiread.exe

win_multithread_singlefile.exe:
	@echo win_multithread_singlefile.exe
	@i686-w64-mingw32-gcc win_multithread_singlefile.c -o win_multithread_singlefile.exe

win_async.exe:
	@echo win_async.exe
	@i686-w64-mingw32-gcc win_async.c -o win_async.exe

linux_singleproc_singlefile.elf:
	@echo linux_singleproc_singlefile.elf
	@gcc -m32 linux_singleproc_singlefile.c -o linux_singleproc_singlefile.elf

linux_singleproc_multifile.elf:
	@echo linux_singleproc_multifile.elf
	@gcc -m32 linux_singleproc_multifile.c -o linux_singleproc_multifile.elf

linux_multiproc_singlefile.elf:
	@echo linux_multiproc_singlefile.elf...
	@gcc -m32 linux_multiproc_singlefile.c -o linux_multiproc_singlefile.elf

linux_multiproc_multifile.elf:
	@echo linux_multiproc_multifile.elf...
	@gcc -m32 linux_multiproc_multifile.c -o linux_multiproc_multifile.elf

linux_positional.elf:
	@echo linux_positional.elf...
	@gcc -m32 linux_positional.c -o linux_positional.elf

linux_multifile_multiread.elf:
	@echo linux_multifile_multiread.elf...
	@gcc -m32 linux_multifile_multiread.c -o linux_multifile_multiread.elf

linux_multithread_singlefile.elf:
	@echo linux_multithread_singlefile.elf...
	@gcc -m32 linux_multithread_singlefile.c -o linux_multithread_singlefile.elf -pthread

linux_pread.elf:
	@echo linux_pread.elf...
	@gcc -m32 linux_pread.c -o linux_pread.elf

linux_badread.elf:
	@echo linux_badread.elf...
	@gcc -m32 linux_badread.c -o linux_badread.elf
	
clean:
	rm -f *.exe *.elf
