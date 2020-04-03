#include <stdint.h>
#include <stdio.h>
#include <windows.h>

int main(int argc, char **argv)
{
    if (argc < 2) {
        fprintf(stderr, "usage: %s <file name>\n", argv[0]);
        return 0;
    }

    HANDLE handle = CreateFile(argv[1], GENERIC_READ, FILE_SHARE_READ, 0,
                               OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (handle == INVALID_HANDLE_VALUE) {
        fprintf(stderr, "CreateFile(...) failed\n");
        return 1;
    }

    uint32_t value;
    DWORD actually_read;
    if (!ReadFile(handle, &value, sizeof(value), &actually_read, NULL)) {
        fprintf(stderr, "ReadFile(...) failed\n");
        return 2;
    }
    CloseHandle(handle);

    if (value > 2147483647) {
        printf("branch 1\n");
    } else {
        printf("branch 2\n");
    }

    return 0;
}
