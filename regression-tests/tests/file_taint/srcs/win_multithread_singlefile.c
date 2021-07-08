#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include <windows.h>

static CRITICAL_SECTION cs;
static HANDLE handle;

DWORD WINAPI ProcessValue1(void *unused)
{
    EnterCriticalSection(&cs);
    uint32_t value = 0;
    DWORD actually_read = 0;
    assert(SetFilePointer(handle, 0, 0, FILE_BEGIN) !=
           INVALID_SET_FILE_POINTER);
    assert(ReadFile(handle, &value, sizeof(value), &actually_read, NULL));
    if (value > 0x1234) {
        printf("branch 1\n");
    } else {
        printf("branch 2\n");
    }
    LeaveCriticalSection(&cs);
    return 0;
}

DWORD WINAPI ProcessValue2(void *unused)
{
    EnterCriticalSection(&cs);
    uint32_t value = 0;
    DWORD actually_read = 0;
    assert(SetFilePointer(handle, 4, 0, FILE_BEGIN) !=
           INVALID_SET_FILE_POINTER);
    assert(ReadFile(handle, &value, sizeof(value), &actually_read, NULL));
    if (value > 0x2345) {
        printf("branch 3\n");
    } else {
        printf("branch 4\n");
    }
    LeaveCriticalSection(&cs);
    return 0;
}

DWORD WINAPI ProcessValue3(void *unused)
{
    EnterCriticalSection(&cs);
    uint32_t value = 0;
    DWORD actually_read = 0;
    assert(SetFilePointer(handle, 8, 0, FILE_BEGIN) !=
           INVALID_SET_FILE_POINTER);
    assert(ReadFile(handle, &value, sizeof(value), &actually_read, NULL));
    if (value > 0x3456) {
        printf("branch 5\n");
    } else {
        printf("branch 6\n");
    }
    LeaveCriticalSection(&cs);
    return 0;
}

int main(int argc, char **argv)
{
    if (argc < 2) {
        printf("usage: %s <file>\n", argv[0]);
        return 0;
    }
    handle = CreateFile(argv[1], GENERIC_READ, FILE_SHARE_READ, 0,
                        OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    InitializeCriticalSection(&cs);

    HANDLE threads[3];
    threads[0] = CreateThread(NULL, 0, ProcessValue1, NULL, 0, NULL);
    threads[1] = CreateThread(NULL, 0, ProcessValue2, NULL, 0, NULL);
    threads[2] = CreateThread(NULL, 0, ProcessValue3, NULL, 0, NULL);
    WaitForMultipleObjects(3, threads, TRUE, INFINITE);

    return 0;
}
