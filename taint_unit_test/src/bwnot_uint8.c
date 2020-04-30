#include "taint.h"
#define the_op ~
#define the_type uint8_t
#define x_LABEL 0xCCCCCCCC
int main(int argc, char **argv) {
    the_type x = (the_type)1;
    the_type z = (the_type)0;
    panda_taint_log("bwnot_uint8");
    panda_taint_label_buffer(&x, x_LABEL, sizeof(the_type));
    panda_taint_assert_label_found_range(&x, sizeof(the_type), x_LABEL);
    panda_taint_assert_label_not_found_range(&z, sizeof(the_type), x_LABEL);
    z = the_op(x);
    panda_taint_assert_label_found_range(&z, sizeof(the_type), x_LABEL);
    return 0;
}

