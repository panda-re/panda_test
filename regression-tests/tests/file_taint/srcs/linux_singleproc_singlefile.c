#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    if (argc < 2) {
        fprintf(stderr, "usage: %s <file name>\n", argv[0]);
        return 0;
    }

    int fd = open(argv[1], O_RDONLY);
    assert(fd != 0);

    uint32_t value;
    ssize_t res = read(fd, &value, sizeof(value));
    assert(res != -1);
    close(fd);

    if (value > 2147483647) {
        printf("branch 1\n");
    } else {
        printf("branch 2\n");
    }

    return 0;
}
