#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

typedef struct {
    uint32_t value1;
    uint32_t value2;
    uint32_t value3;
} record;

record read_record(const char *file)
{
    record r;

    int fd = open(file, O_RDONLY);

    // read out of order to test pread
    ssize_t res = pread(fd, &r.value2, sizeof(r.value2), 4);
    assert(res != -1);

    res = pread(fd, &r.value1, sizeof(r.value1), 0);
    assert(res != -1);

    res = pread(fd, &r.value3, sizeof(r.value2), 8);
    assert(res != -1);

    close(fd);

    return r;
}

int main(int argc, char **argv)
{
    if (argc < 2) {
        printf("usage: %s <file>\n", argv[0]);
        return 0;
    }

    record r = read_record(argv[1]);

    if (r.value1 > 0x1234) {
        printf("branch 1\n");
    } else {
        printf("branch 2\n");
    }

    if (r.value2 > 0x2345) {
        printf("branch 3\n");
    } else {
        printf("branch 4\n");
    }

    if (r.value3 > 0x3456) {
        printf("branch 5\n");
    } else {
        printf("branch 6\n");
    }

    return 0;
}
