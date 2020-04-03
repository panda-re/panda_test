#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <windows.h>

int main(int argc, char **argv)
{
    if (argc < 3) {
        fprintf(stderr, "usage: %s <file 1 name> <file 2 name>\n", argv[0]);
        return 0;
    }

    char cmdline[2048] = {0};
    sprintf(cmdline, "win_singleproc_singlefile.exe %s\0", argv[1]);

    PROCESS_INFORMATION pi1 = {0};
    STARTUPINFO si1 = {0};
    if (!CreateProcess(NULL, cmdline, NULL, NULL, false, 0, NULL, NULL, &si1,
                       &pi1)) {
        fprintf(stderr, "could not start first process\n");
        return 1;
    }
    sprintf(cmdline, "win_singleproc_singlefile.exe %s\0", argv[2]);

    PROCESS_INFORMATION pi2 = {0};
    STARTUPINFO si2 = {0};
    if (!CreateProcess(NULL, cmdline, NULL, NULL, true, 0, NULL, NULL, &si2,
                       &pi2)) {
        fprintf(stderr, "could not start second process\n");
        return 2;
    }

    HANDLE handles[2] = {pi1.hProcess, pi2.hProcess};
    WaitForMultipleObjects(2, handles, true, INFINITE);

    return 0;
}
