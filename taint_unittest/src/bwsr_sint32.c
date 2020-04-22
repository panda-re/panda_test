#include "taint.h"
#define the_op >>
#define the_type int32_t
#define x_LABEL 0xCCCCCCCC
#define y_LABEL 0xDDDDDDDD
int main(int argc, char **argv) {
    the_type x = (the_type)1;
    the_type y = (the_type)2;
    the_type z = (the_type)0;
    panda_taint_label_buffer(&x, x_LABEL, sizeof(the_type));
    panda_taint_label_buffer(&y, y_LABEL, sizeof(the_type));
    panda_taint_assert_label_found_range(&x, sizeof(the_type), x_LABEL);
    panda_taint_assert_label_found_range(&y, sizeof(the_type), y_LABEL);
    panda_taint_assert_label_not_found_range(&z, sizeof(the_type), x_LABEL);
    panda_taint_assert_label_not_found_range(&z, sizeof(the_type), y_LABEL);
    z = x the_op y;
    panda_taint_assert_label_found_range(&z, sizeof(the_type), x_LABEL);
    panda_taint_assert_label_found_range(&z, sizeof(the_type), y_LABEL);
    return 0;
}

