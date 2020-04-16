#include "taint.h"

#define the_op ~
#define the_type int16_t
#define x_LABEL 0xCCCCCCCC
int main(int argc, char **argv) {

    the_type x = 1;
    the_type z = 0;

    panda_taint_label_buffer(&x, x_LABEL, sizeof(the_type));

    panda_taint_assert_label_range(&x, sizeof(the_type), x_LABEL);

    z = the_op(x);

    panda_taint_assert_label_range(&z, sizeof(the_type), x_LABEL);

    return 0;
}
