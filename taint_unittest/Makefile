CFLAGS = -m32 -O0
ASFLAGS = -felf32
LDFLAGS = -melf_i386
CC=gcc
AS=nasm
LD=ld

CSRC=			\
		add_double \
		add_float \
		add_sint8 \
		add_sint16 \
		add_sint32 \
		add_sint64 \
		add_uint8 \
		add_uint16 \
		add_uint32 \
		add_uint64 \
		sub_double \
		sub_float \
		sub_sint8 \
		sub_sint16 \
		sub_sint32 \
		sub_sint64 \
		sub_uint8 \
		sub_uint16 \
		sub_uint32 \
		sub_uint64 \
		mul_double \
		mul_float \
		mul_sint8 \
		mul_sint16 \
		mul_sint32 \
		mul_sint64 \
		mul_uint8 \
		mul_uint16 \
		mul_uint32 \
		mul_uint64 \
		div_double \
		div_float \
		div_sint8 \
		div_sint16 \
		div_sint32 \
		div_sint64 \
		div_uint8 \
		div_uint16 \
		div_uint32 \
		div_uint64 \
		turn_on_taint	\
		test_label		\
		testmalloc		\
		testmemset		\
		testmemcpy	\
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
