#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    if (argc < 2) {
        fprintf(stderr, "usage: %s <file 1> <file 2>\n", argv[0]);
        return 0;
    }

    const char *prog = "linux_singleproc_singlefile.elf";

    int pid1 = fork();
    if (pid1 == 0) {
        execl(prog, prog, argv[1], NULL);
        return 0;
    }

    int pid2 = fork();
    if (pid2 == 0) {
        execl(prog, prog, argv[2], NULL);
        return 0;
    }

    int status = 0;
    waitpid(pid1, &status, 0);
    waitpid(pid2, &status, 0);

    return 0;
}
