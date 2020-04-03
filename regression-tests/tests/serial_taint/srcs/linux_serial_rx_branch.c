#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include <fcntl.h>
#include <termios.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    if (argc < 2) {
        fprintf(stderr, "usage: %s <Serial Device>\n", argv[0]);
        return 0;
    }

    int fd = open(argv[1], O_RDONLY | O_NOCTTY);
    assert(fd != -1);

    uint32_t value = 0;
    assert(read(fd, &value, sizeof(value)) != -1);

    if (value > 0x1234) {
        printf("greater than 0x1234\n");
    }

    return 0;
}
