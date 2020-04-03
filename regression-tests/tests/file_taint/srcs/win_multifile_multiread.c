#include <stdint.h>
#include <stdio.h>

#include <windows.h>

typedef struct {
    uint32_t value1;
    uint32_t value2;
    uint32_t value3;
} record;

record read_record(const char *file1, const char *file2)
{
    record r;

    HANDLE handle1 = CreateFile(file1, GENERIC_READ, FILE_SHARE_READ, 0,
                                OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    HANDLE handle2 = CreateFile(file2, GENERIC_READ, FILE_SHARE_READ, 0,
                                OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);

    // interleave reads to really test the file handle resolution
    DWORD actually_read = 0;
    if (!ReadFile(handle1, &r.value1, sizeof(r.value1), &actually_read, NULL)) {
        fprintf(stderr, "handle1, read 1: ReadFile(...) failed\n");
        return r;
    }
    if (!ReadFile(handle2, &r.value3, sizeof(r.value3), &actually_read, NULL)) {
        fprintf(stderr, "handle2, read 1: ReadFile(...) failed\n");
        return r;
    }
    if (!ReadFile(handle1, &r.value2, sizeof(r.value2), &actually_read, NULL)) {
        fprintf(stderr, "handle1, read 2: ReadFile(...) failed\n");
        return r;
    }

    CloseHandle(handle1);
    CloseHandle(handle2);

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
