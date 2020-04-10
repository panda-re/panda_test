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

#define x_LABEL 0xCCCCCCCC
int main(int argc, char **argv) {

    int x = 1;

    vm_label_buffer(&x, x_LABEL, sizeof(int));

    panda_assert_taint_label_range(&x, sizeof(int), x_LABEL);

    return 0;
}
