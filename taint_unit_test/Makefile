CFLAGS = -m32 -O0
ASFLAGS = -felf32
LDFLAGS = -melf_i386
CC=gcc
AS=nasm
LD=ld
INCLUDES= -I../taint_include

SRC=src
CSRC=$(patsubst src/%,%,$(patsubst %.c,%,$(wildcard $(SRC)/*.c)))
ASMSRC=$(patsubst src/%,%,$(patsubst %.asm,%,$(wildcard $(SRC)/*.asm)))

all: dirs $(CSRC) $(ASMSRC)

dirs:
	mkdir -p bin
	mkdir -p obj

%:	src/%.c
		$(CC) $(CFLAGS) $(INCLUDES) -c $< -o obj/$@.o
		$(CC) $(CFLAGS) $(INCLUDES) obj/$@.o -o bin/$@

%:	src/%.asm
		$(AS) $(ASFLAGS) $< -o obj/$@.o
		$(LD) $(LDFLAGS) obj/$@.o -o bin/$@

.PHONY : clean
clean :
	-rm obj/* bin/*
	-rmdir obj/
	-rmdir bin/