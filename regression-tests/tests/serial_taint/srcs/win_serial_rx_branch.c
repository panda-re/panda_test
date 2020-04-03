#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include <windows.h>

int main(int argc, char **argv)
{
    if (argc < 2) {
        printf("usage: %s <COM Port>\n", argv[0]);
        return 0;
    }

    // Copy COM port into a string that we can pass to CreateFile
    char path[256];
    sprintf(path, "\\\\.\\%s", argv[1]);

    // Open the Serial Port
    HANDLE com_handle =
        CreateFile(path, GENERIC_READ, 0, 0, OPEN_EXISTING, 0, NULL);
    assert(com_handle != INVALID_HANDLE_VALUE);

    // Read a uint32_t off the port
    uint32_t value = 0;
    DWORD actually_read = 0;
    assert(ReadFile(com_handle, &value, sizeof(value), &actually_read, NULL));

    // Close the port
    CloseHandle(com_handle);

    // Branch based on the value we read
    if (value > 0x1234) {
        printf("greater than 0x1234\n");
    }

    return 0;
}
