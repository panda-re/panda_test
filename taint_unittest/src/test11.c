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

// test 11 -- ?????
#define a_LABEL 0x12345678
int main(int argc, char **argv) {

    uint8_t a=6;
    vm_label_buffer(&a, a_LABEL, sizeof(uint8_t));

    uint8_t *buf = (uint8_t *)malloc(8);
    memset((void *)buf, a, 8);

    for(size_t i=0;i<8;i++) {
        panda_assert_taint_label_range(&buf[i], sizeof(uint8_t), a_LABEL);
    }

    return 0;
}
