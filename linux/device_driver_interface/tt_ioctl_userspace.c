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
#include <assert.h>

#include "tt_ioctl_cmds.h"

#define TT_IOW(type, nr, size) _IOC(_IOC_WRITE, (type), (nr), size)
#define TT_IOR(type, nr, size) _IOC(_IOC_READ, (type), (nr), size)

// CERT MSC30-C
int init_random() {

    struct timespec ts;

    if (timespec_get(&ts, TIME_UTC) == 0) {
        return -1;
    }

    srandom(ts.tv_nsec ^ ts.tv_sec);
    return 0;
}

void notify_read(int uncopied_byte_cnt, uint8_t* buf, int buf_len) {

    if(uncopied_byte_cnt) {
        fprintf(stderr, "Error reading from kernel buffer: %d uncopied bytes\n", uncopied_byte_cnt);
    } else {
        puts("\nUserspace received kernel buffer: ");
        for (int i = 0; i < buf_len; ++i) {
            printf("0x%02x ", buf[i]);
        }
    }
}

void notify_write(int uncopied_byte_cnt, uint8_t* buf, int buf_len) {

    if(uncopied_byte_cnt) {
        fprintf(stderr, "Error writing to kernel buffer: %d uncopied bytes\n", uncopied_byte_cnt);
    } else {
        puts("\nUserspace transmitted buffer: ");
        for (int i = 0; i < buf_len; ++i) {
            printf("0x%02x ", buf[i]);
        }
    }
}

int main(int argc, char *argv[]) {

    int fd, uncopied_byte_cnt, curr_err, buf_len;
    uint8_t *buf;
    uint8_t *buf_copy;
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

    buf = (uint8_t*)malloc(buf_len);
    buf_copy = (uint8_t*)malloc(buf_len);
    if ((!buf) || (!buf_copy)) {
        fprintf(stderr, "Error: failed to malloc %d bytes\n", buf_len);
        exit(EXIT_FAILURE);
    }

    // Process -> Kernel Driver ----------------------------------------------------------------------------------------

    if (init_random()) {
        fprintf(stderr, "Error: failed to initialize random stream\n");
        exit(EXIT_FAILURE);
    }

    // Init buffer to write and copy
    for (int i = 0; i < buf_len; ++i) {
        buf[i] = random() % (UINT8_MAX - 1);
    }
    memcpy(buf_copy, buf, buf_len);

    // Write ephemeral kernel buffer
    cmd = (int)TT_IOW(TT_IOC_TYPE, W_EPHEME, buf_len);
    uncopied_byte_cnt = ioctl(fd, cmd, buf);
    notify_write(uncopied_byte_cnt, buf, buf_len);

    // Write persistant kernel buffer
    cmd = (int)TT_IOW(TT_IOC_TYPE, W_PERSIS, buf_len);
    uncopied_byte_cnt = ioctl(fd, cmd, buf);
    notify_write(uncopied_byte_cnt, buf, buf_len);

    // Kernel Driver -> Process ----------------------------------------------------------------------------------------

    // Read ephemeral kernel buffer
    cmd = (int)TT_IOR(TT_IOC_TYPE, R_EPHEME, buf_len);
    uncopied_byte_cnt = ioctl(fd, cmd, buf);
    notify_read(uncopied_byte_cnt, buf, buf_len);

    // Read and verify persistant kernel buffer
    cmd = (int)TT_IOR(TT_IOC_TYPE, R_PERSIS, buf_len);
    uncopied_byte_cnt = ioctl(fd, cmd, buf);
    notify_read(uncopied_byte_cnt, buf, buf_len);
    assert(!memcmp(buf, buf_copy, buf_len));

    // Process -> Kernel Driver -> Other Process -----------------------------------------------------------------------

    // TODO (tnballo): add child fork and signal to trigger data copy here

    puts("\n");
    close(fd);
    exit(EXIT_SUCCESS);
}