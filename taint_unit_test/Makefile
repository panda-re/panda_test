CFLAGS_I386 = -m32 -O0
CFLAGS_X64 = -O0

ASFLAGS_I386 = -felf32
ASFLAGS_X64 = -felf64

LDFLAGS_I386 = -melf_i386
LDFLAGS_X64 =

CC=gcc
AS=nasm
LD=ld

ifeq "$(TARGET)" "TARGET_I386"
CFLAGS=$(CFLAGS_I386)
ASFLAGS=$(ASFLAGS_I386)
LDFLAGS=$(LDFLAGS_I386)
endif

ifeq "$(TARGET)" "TARGET_X86_64"
CFLAGS=$(CFLAGS_X64)
ASFLAGS=$(ASFLAGS_X64)
LDFLAGS=$(LDFLAGS_X64)
endif

INCLUDES= -I../taint_include

SRC=src
CSRC=$(patsubst src/%,%,$(patsubst %.c,%,$(wildcard $(SRC)/*.c)))
ASMSRC=$(patsubst src/%,%,$(patsubst %.asm,%,$(wildcard $(SRC)/*.asm)))

all: dirs $(CSRC) $(ASMSRC)

dirs:
	mkdir -p bin
	mkdir -p obj

%:	src/%.c
		$(CC) -D$(TARGET) $(CFLAGS) $(INCLUDES) -c $< -o obj/$@.o
		$(CC) -D$(TARGET) $(CFLAGS) $(INCLUDES) obj/$@.o -o bin/$@

%:	src/%.asm
		$(AS) -D$(TARGET) $(ASFLAGS) $< -o obj/$@.o
		$(LD) $(LDFLAGS) obj/$@.o -o bin/$@

.PHONY : clean
clean :
	-rm obj/* bin/*
	-rmdir obj/
	-rmdir bin/
