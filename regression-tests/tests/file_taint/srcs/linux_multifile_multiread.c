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

record read_record(const char *file1, const char *file2)
{
    record r;

    int fd1 = open(file1, O_RDONLY);
    int fd2 = open(file2, O_RDONLY);

    // interleave reads to really test the file handle resolution
    ssize_t res = read(fd1, &r.value1, sizeof(r.value1));
    assert(res != -1);

    res = read(fd2, &r.value3, sizeof(r.value3));
    assert(res != -1);

    res = read(fd1, &r.value2, sizeof(r.value2));
    assert(res != -1);

    close(fd1);
    close(fd2);

    return r;
}

int main(int argc, char **argv)
{
    if (argc < 2) {
        printf("usage: %s <file 1> <file 2>\n", argv[0]);
        return 0;
    }

    record r = read_record(argv[1], argv[2]);

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
