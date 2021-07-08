#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include <windows.h>

int main(int argc, char **argv)
{
    if (argc < 2) {
        printf("usage: %s <file>\n", argv[0]);
        return 0;
    }

    HANDLE handle = CreateFile(argv[1], GENERIC_READ, FILE_SHARE_READ, NULL,
                               OPEN_EXISTING, FILE_FLAG_OVERLAPPED, NULL);
    assert(handle != INVALID_HANDLE_VALUE);

    uint32_t value = 0;
    DWORD actually_read = 0;
    OVERLAPPED overlapped_operation;
    overlapped_operation.hEvent = NULL;
    NTSTATUS status = ReadFile(handle, &value, sizeof(value), &actually_read,
                               &overlapped_operation);
    assert(overlapped_operation.Internal == STATUS_PENDING);
    CloseHandle(handle);

    return 0;
}
