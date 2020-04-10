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

#define the_op   /
#define the_type uint8_t
#define x_LABEL 0xCCCCCCCC
#define y_LABEL 0xDDDDDDDD
int main(int argc, char **argv) {

    the_type x = 1;
    the_type y = 2;
    the_type z = 0;

    vm_label_buffer(&x, x_LABEL, sizeof(the_type));
    vm_label_buffer(&y, y_LABEL, sizeof(the_type));

    panda_assert_taint_label_range(&x, sizeof(the_type), x_LABEL);
    panda_assert_taint_label_range(&y, sizeof(the_type), y_LABEL);

    z = x the_op y;

    panda_assert_taint_label_range(&z, sizeof(the_type), x_LABEL);
    panda_assert_taint_label_range(&z, sizeof(the_type), y_LABEL);

    return 0;
}
