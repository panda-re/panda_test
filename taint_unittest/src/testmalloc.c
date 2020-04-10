#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

#include "taint.h"

void panda_assert_taint_label(void *buf, uint32_t off, uint32_t expected_label) {
	vm_query_buffer(buf, off, expected_label);
}

void panda_assert_taint_label_range(void *buf, size_t len, uint32_t expected_label) {
    int i;
    for(i=0;i<len;i++) {
        panda_assert_taint_label(buf, i, expected_label);
    }
}

// TEST 8 - malloc and label each byte in buffer
/**
char *buf;
buf = (void *)malloc(8);
memset((void *)buf, 0xff, 8);
Lbufi for i in [0,7] = set taint label on buf[i]
for i in [0,7] assert get taint label on buf[i] = Lbufi
*/
#define b0_LABEL 0xABCDEF00
#define b1_LABEL 0xABCDEF01
#define b2_LABEL 0xABCDEF02
#define b3_LABEL 0xABCDEF03
#define b4_LABEL 0xABCDEF04
#define b5_LABEL 0xABCDEF05
#define b6_LABEL 0xABCDEF06
#define b7_LABEL 0xABCDEF07
int main(int argc, char **argv) {

    char *buf = (char *)malloc(8);
    memset((void *)buf, 0xff, 8);

    vm_label_buffer(&buf[0], b0_LABEL, sizeof(char));
    vm_label_buffer(&buf[1], b1_LABEL, sizeof(char));
    vm_label_buffer(&buf[2], b2_LABEL, sizeof(char));
    vm_label_buffer(&buf[3], b3_LABEL, sizeof(char));
    vm_label_buffer(&buf[4], b4_LABEL, sizeof(char));
    vm_label_buffer(&buf[5], b5_LABEL, sizeof(char));
    vm_label_buffer(&buf[6], b6_LABEL, sizeof(char));
    vm_label_buffer(&buf[7], b7_LABEL, sizeof(char));

    panda_assert_taint_label_range(&buf[0], sizeof(char), b0_LABEL);
    panda_assert_taint_label_range(&buf[1], sizeof(char), b1_LABEL);
    panda_assert_taint_label_range(&buf[2], sizeof(char), b2_LABEL);
    panda_assert_taint_label_range(&buf[3], sizeof(char), b3_LABEL);
    panda_assert_taint_label_range(&buf[4], sizeof(char), b4_LABEL);
    panda_assert_taint_label_range(&buf[5], sizeof(char), b5_LABEL);
    panda_assert_taint_label_range(&buf[6], sizeof(char), b6_LABEL);
    panda_assert_taint_label_range(&buf[7], sizeof(char), b7_LABEL);

    return 0;
}
