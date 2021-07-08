#include <stdint.h>
#include <stdio.h>
#include <windows.h>

void test_func(char *filename)
{
    HANDLE handle = CreateFile(filename, GENERIC_READ, FILE_SHARE_READ, 0,
                               OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (handle == INVALID_HANDLE_VALUE) {
        fprintf(stderr, "CreateFile(...) failed\n");
        exit(1);
    }

    uint32_t value;
    DWORD actually_read;
    if (!ReadFile(handle, &value, sizeof(value), &actually_read, NULL)) {
        fprintf(stderr, "ReadFile(...) failed\n");
        exit(2);
    }
    CloseHandle(handle);

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
