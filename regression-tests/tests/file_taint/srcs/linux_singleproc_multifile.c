#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

void test_func(char *filename)
{
    int fd = open(filename, O_RDONLY);
    assert(fd != 0);

    uint32_t value;
    ssize_t res = read(fd, &value, sizeof(value));
    assert(res != -1);

    if (value > 2147483647) {
        printf("branch 1\n");
    } else {
        printf("branch 2\n");
    }
}

int main(int argc, char **argv)
{
    if (argc < 3) {
        fprintf(stderr, "usage: %s <file 1 name> <file 2 name>\n", argv[0]);
        return 0;
    }

    test_func(argv[1]);
    test_func(argv[2]);

    return 0;
}
