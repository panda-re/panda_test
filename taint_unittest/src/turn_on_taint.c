// contains hypercall code
#include "taint.h"

// does what it says and does nothing else
int main(int argc, char **argv) {

    hypercall_enable_taint();

    return 0;
}
