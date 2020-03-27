#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

// contains hypercall code
#include "taint.h"

int main(int argc, char **argv) {

    turn_on_taint();

    return 0;
}
