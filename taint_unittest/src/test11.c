#include <string.h>
#include "taint.h"

#define a_LABEL 0x12345678
int main(int argc, char **argv) {

    uint8_t a=6;
    panda_taint_label_buffer(&a, a_LABEL, sizeof(uint8_t));

    uint8_t *buf = (uint8_t *)malloc(8);
    memset((void *)buf, a, 8);

    for(size_t i=0;i<8;i++) {
        panda_taint_assert_label_range(&buf[i], sizeof(uint8_t), a_LABEL);
    }

    return 0;
}
