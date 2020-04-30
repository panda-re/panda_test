CFLAGS = -m32 -O0
ASFLAGS = -felf32
LDFLAGS = -melf_i386
CC=gcc
AS=nasm
LD=ld
INCLUDES= -I../taint_include

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
		mod_sint8 \
		mod_sint16 \
		mod_sint32 \
		mod_sint64 \
		mod_uint8 \
		mod_uint16 \
		mod_uint32 \
		mod_uint64 \
		bwnot_sint8 \
		bwnot_sint16 \
		bwnot_sint32 \
		bwnot_sint64 \
		bwnot_uint8 \
		bwnot_uint16 \
		bwnot_uint32 \
		bwnot_uint64 \
		bwand_sint8 \
		bwand_sint16 \
		bwand_sint32 \
		bwand_sint64 \
		bwand_uint8 \
		bwand_uint16 \
		bwand_uint32 \
		bwand_uint64 \
		bwor_sint8 \
		bwor_sint16 \
		bwor_sint32 \
		bwor_sint64 \
		bwor_uint8 \
		bwor_uint16 \
		bwor_uint32 \
		bwor_uint64 \
		bwxor_sint8 \
		bwxor_sint16 \
		bwxor_sint32 \
	 	bwxor_sint64 \
		bwxor_uint8 \
		bwxor_uint16 \
		bwxor_uint32 \
		bwxor_uint64 \
		bwsl_sint8 \
		bwsl_sint16 \
		bwsl_sint32 \
		bwsl_sint64 \
		bwsl_uint8 \
		bwsl_uint16 \
		bwsl_uint32 \
		bwsl_uint64 \
		bwsr_sint8 \
		bwsr_sint16 \
		bwsr_sint32 \
		bwsr_sint64 \
		bwsr_uint8 \
		bwsr_uint16 \
		bwsr_uint32 \
		bwsr_uint64 \
		turn_on_taint	\
		label		\
		malloc		\
		memset		\
		memcpy	\
		test11

ASMSRC=			\
	eax_test

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
