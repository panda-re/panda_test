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

// TEST 5 - label two vars, multiply and assign to third var
/*
int x;
int y;
int z;
Lx = set taint label on x
Ly = set taint label on y
x = 1
assert get taint label on x = Lx
y = 2
assert get taint label on y = Ly
z = x * y
assert get taint label on z = (Lx & Ly)
*/
#define x_LABEL 0xCCCCCCCC
#define y_LABEL 0xDDDDDDDD
int main(int argc, char **argv) {

    int x = 1;
    int y = 2;
    int z = 0;

    vm_label_buffer(&x, x_LABEL, sizeof(int));
    vm_label_buffer(&y, y_LABEL, sizeof(int));

    panda_assert_taint_label_range(&x, sizeof(int), x_LABEL);
    panda_assert_taint_label_range(&y, sizeof(int), y_LABEL);

    z = x * y;

    panda_assert_taint_label_range(&z, sizeof(int), x_LABEL);
    panda_assert_taint_label_range(&z, sizeof(int), y_LABEL);

    return 0;
}
