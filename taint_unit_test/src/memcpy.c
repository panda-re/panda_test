#include <string.h>
#include "taint.h"

// malloc two buffers and label each byte in first buffer, memcpy to second buffer
/**

char *buf;
buf = (void *)malloc(8);
memset((void *)buf, 0xff, 8);
buf2 = (void *)malloc(8);
Lbufi for i in [0,7] = set taint label on buf[i]
for i in [0,7] assert get taint label on buf[i] = Lbufi
memcpy((void *)buf2, (void *)buf, 8)
for i in [0,7] assert get taint label on buf2[i] = Lbufi
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

    uint8_t *buf = (uint8_t *)malloc(8*sizeof(uint8_t));

    panda_taint_log("memcpy");

    memset((void *)buf, 0xff, 8*sizeof(uint8_t));

    panda_taint_label_buffer(&buf[0], b0_LABEL, sizeof(uint8_t));
    panda_taint_label_buffer(&buf[1], b1_LABEL, sizeof(uint8_t));
    panda_taint_label_buffer(&buf[2], b2_LABEL, sizeof(uint8_t));
    panda_taint_label_buffer(&buf[3], b3_LABEL, sizeof(uint8_t));
    panda_taint_label_buffer(&buf[4], b4_LABEL, sizeof(uint8_t));
    panda_taint_label_buffer(&buf[5], b5_LABEL, sizeof(uint8_t));
    panda_taint_label_buffer(&buf[6], b6_LABEL, sizeof(uint8_t));
    panda_taint_label_buffer(&buf[7], b7_LABEL, sizeof(uint8_t));

    panda_taint_assert_label_found_range(&buf[0], sizeof(uint8_t), b0_LABEL);
    panda_taint_assert_label_found_range(&buf[1], sizeof(uint8_t), b1_LABEL);
    panda_taint_assert_label_found_range(&buf[2], sizeof(uint8_t), b2_LABEL);
    panda_taint_assert_label_found_range(&buf[3], sizeof(uint8_t), b3_LABEL);
    panda_taint_assert_label_found_range(&buf[4], sizeof(uint8_t), b4_LABEL);
    panda_taint_assert_label_found_range(&buf[5], sizeof(uint8_t), b5_LABEL);
    panda_taint_assert_label_found_range(&buf[6], sizeof(uint8_t), b6_LABEL);
    panda_taint_assert_label_found_range(&buf[7], sizeof(uint8_t), b7_LABEL);

    uint8_t *buf2 = (uint8_t *)malloc(8*sizeof(uint8_t));
    memcpy((void *)buf2, (void *)buf, 8);

    panda_taint_assert_label_found_range(&buf2[0], sizeof(uint8_t), b0_LABEL);
    panda_taint_assert_label_found_range(&buf2[1], sizeof(uint8_t), b1_LABEL);
    panda_taint_assert_label_found_range(&buf2[2], sizeof(uint8_t), b2_LABEL);
    panda_taint_assert_label_found_range(&buf2[3], sizeof(uint8_t), b3_LABEL);
    panda_taint_assert_label_found_range(&buf2[4], sizeof(uint8_t), b4_LABEL);
    panda_taint_assert_label_found_range(&buf2[5], sizeof(uint8_t), b5_LABEL);
    panda_taint_assert_label_found_range(&buf2[6], sizeof(uint8_t), b6_LABEL);
    panda_taint_assert_label_found_range(&buf2[7], sizeof(uint8_t), b7_LABEL);

    return 0;
}
