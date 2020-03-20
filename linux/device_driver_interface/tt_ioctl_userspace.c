#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <malloc.h>
#include <string.h>
#include <time.h>
#include <errno.h>

#include "tt_ioctl_cmds.h"

#define TT_IOW(type, nr, size) _IOC(_IOC_WRITE, (type), (nr), size)
#define TT_IOR(type, nr, size) _IOC(_IOC_READ, (type), (nr), size)

// CERT MSC30-C
int init_random() {

    struct timespec ts;

    if (timespec_get(&ts, TIME_UTC) == 0) {
        return 1;
    }

    srandom(ts.tv_nsec ^ ts.tv_sec);
    return 0;
}

int main(int argc, char *argv[]) {

    int fd, uncopied_byte_cnt, curr_err, buf_len;
    uint8_t *buffer;
    char *dev_node_path = "/dev/taint_test_misc_device";
    int cmd;

    // Init ------------------------------------------------------------------------------------------------------------

    if (argc >= 2) {
        dev_node_path = argv[1];
    } else {
        printf("Using default device node: %s\n", dev_node_path);
    }

    if (geteuid() != 0) {
        fprintf(stderr, "Error: must run as root to read/write \'%s\'!\n", dev_node_path);
        exit(EXIT_FAILURE);
    }

    if (argc >= 3) {
        buf_len = atoi(argv[2]);
    } else {
        buf_len = 25;
        printf("Using default buffer length: %d bytes\n", buf_len);
    }

    fd = open(dev_node_path, O_RDWR);
    if (!fd) {
        curr_err = errno;
        fprintf(stderr, "Error opening device node: %s\n", strerror(curr_err));
        exit(EXIT_FAILURE);
    }

    buffer = (uint8_t*)malloc(buf_len);
    if (!buffer) {
        fprintf(stderr, "Error: failed to malloc %d bytes\n", buf_len);
        exit(EXIT_FAILURE);
    }

    // Kernel Driver -> Process ----------------------------------------------------------------------------------------

    // RX: read kernel buffer
    cmd = (int)TT_IOR(TT_IOC_TYPE, R_EPHEME, buf_len);
    uncopied_byte_cnt = ioctl(fd, cmd, buffer);
    if(uncopied_byte_cnt) {
        fprintf(stderr, "Error reading from kernel buffer: %d uncopied bytes\n", uncopied_byte_cnt);
    } else {
        puts("\nUserspace received kernel buffer: ");
        for (int i = 0; i < buf_len; ++i) {
            printf("0x%02x ", buffer[i]);
        }
    }

    // Process -> Kernel Driver ----------------------------------------------------------------------------------------

    // Init buffer to write
    init_random();
    for (int i = 0; i < buf_len; ++i) {
        buffer[i] = random() % (UINT8_MAX - 1);
    }

    // TX: write kernel buffer
    cmd = (int)TT_IOW(TT_IOC_TYPE, W_EPHEME, buf_len);
    uncopied_byte_cnt = ioctl(fd, cmd, buffer);
    if(uncopied_byte_cnt) {
        fprintf(stderr, "Error writing to kernel buffer: %d uncopied bytes\n", uncopied_byte_cnt);
    } else {
        puts("\nUserspace transmitted buffer: ");
        for (int i = 0; i < buf_len; ++i) {
            printf("0x%02x ", buffer[i]);
        }
    }

    // Process -> Kernel Driver -> Other Process -----------------------------------------------------------------------

    // TODO (tnballo): add child fork and signal to trigger data copy here

    puts("\n");
    close(fd);
    exit(EXIT_SUCCESS);
}