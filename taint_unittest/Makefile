CFLAGS = -m32 -O0
ASFLAGS = -felf32
LDFLAGS = -melf_i386
CC=gcc
AS=nasm
LD=ld

CSRC=			\
		turn_on_taint	\
		test4		\
		test5		\
		test6		\
		test7		\
		test8		\
		test9		\
		test10	\
		test11

ASMSRC=			\
	eax_test

all:	$(CSRC) $(ASMSRC)

%:	src/%.c
		$(CC) $(CFLAGS) -c $< -o obj/$@.o
		$(CC) $(CFLAGS) obj/$@.o -o bin/$@
%:	src/%.asm
		$(AS) $(ASFLAGS) $< -o obj/$@.o
		$(LD) $(LDFLAGS) obj/$@.o -o bin/$@

.PHONY : clean
clean :
	-rm obj/*.o bin/*
	-rmdir obj/
	-rmdir bin/
