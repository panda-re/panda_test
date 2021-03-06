#!/bin/sh
set -ex

cd $(dirname $0)

./turn_on_taint
./add_double
./add_float
./add_sint16
./add_sint32
./add_sint64
./add_sint8
./add_uint16
./add_uint32
./add_uint64
./add_uint8
./bwand_sint16
./bwand_sint32
./bwand_sint64
./bwand_sint8
./bwand_uint16
./bwand_uint32
./bwand_uint64
./bwand_uint8
./bwnot_sint16
./bwnot_sint32
./bwnot_sint64
./bwnot_sint8
./bwnot_uint16
./bwnot_uint32
./bwnot_uint64
./bwnot_uint8
./bwor_sint16
./bwor_sint32
./bwor_sint64
./bwor_sint8
./bwor_uint16
./bwor_uint32
./bwor_uint64
./bwor_uint8
./bwsl_sint16
./bwsl_sint32
./bwsl_sint64
./bwsl_sint8
./bwsl_uint16
./bwsl_uint32
./bwsl_uint64
./bwsl_uint8
./bwsr_sint16
./bwsr_sint32
./bwsr_sint64
./bwsr_sint8
./bwsr_uint16
./bwsr_uint32
./bwsr_uint64
./bwsr_uint8
./bwxor_sint16
./bwxor_sint32
./bwxor_sint64
./bwxor_sint8
./bwxor_uint16
./bwxor_uint32
./bwxor_uint64
./bwxor_uint8
./div_double
./div_float
./div_sint16
./div_sint32
./div_sint8
./div_uint16
./div_uint32
./div_uint8
./label
./malloc
./memcpy
./memset
./mod_sint16
./mod_sint32
./mod_sint8
./mod_uint16
./mod_uint32
./mod_uint8
./mul_double
./mul_float
./mul_sint16
./mul_sint32
./mul_sint64
./mul_sint8
./mul_uint16
./mul_uint32
./mul_uint64
./mul_uint8
./sub_double
./sub_float
./sub_sint16
./sub_sint32
./sub_sint64
./sub_sint8
./sub_uint16
./sub_uint32
./sub_uint64
./sub_uint8

#disabled due to failures that havent been worked through yet

# these two are due to 32-bit x86 gcc calling a function to do division and mod in software
# with all kinds of special / corner cases in the resulting taint based on input values
#./mod_sint64
#./mod_uint64
#./div_sint64
#./div_uint64

# these are just not up to date
#./eax_test
#./test11
