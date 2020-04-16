#include "taint.h"

#define x_LABEL 0xCCCCCCCC
int main(int argc, char **argv) {

    int x = 1;

    panda_taint_label_buffer(&x, x_LABEL, sizeof(int));

    panda_taint_assert_label_range(&x, sizeof(int), x_LABEL);

    return 0;
}
