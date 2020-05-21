#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <malloc.h>
#include <string.h>
#include <time.h>
#include <errno.h>
#include <assert.h>

#include "tt_ioctl_common.h"
#include "taint.h"

#define TT_IOW(type, nr, size) ((int)_IOC(_IOC_WRITE, (type), (nr), size))
#define TT_IOR(type, nr, size) ((int)_IOC(_IOC_READ, (type), (nr), size))
#define TT_IO(type, nr) ((int)_IO((type), (nr)))

uint8_t *buf = NULL;
uint8_t *buf_copy = NULL;
int buf_len = 0;
int fd = 0;
bool sig_triggered_copy_ok = false;

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
        puts("Userspace received kernel buffer: ");
        for (int i = 0; i < buf_len; ++i) {
            printf("0x%02x ", buf[i]);
        }
        puts("\n");
    }
}

void notify_write(int uncopied_byte_cnt, uint8_t* buf, int buf_len) {

    if(uncopied_byte_cnt) {
        fprintf(stderr, "Error writing to kernel buffer: %d uncopied bytes\n", uncopied_byte_cnt);
    } else {
        puts("Userspace transmitted buffer: ");
        for (int i = 0; i < buf_len; ++i) {
            printf("0x%02x ", buf[i]);
        }
        puts("\n");
    }
}

void copy_buf_handler(int sig) {

    sigset_t mask, prev_mask;
    int cmd;

    // Block other signals
    sigfillset(&mask);
    sigprocmask(SIG_BLOCK, &mask, &prev_mask);

    // Read persistant kernel buffer
    if ((sig == SIGIO) && (buf != NULL) && (buf_len > 0)) {
        cmd = TT_IOR(TT_IOC_TYPE, R_PERSIS, buf_len);
        if (!ioctl(fd, cmd, buf)) {
            sig_triggered_copy_ok = true;
        }
    }

    // Unblock other signals
    sigprocmask(SIG_SETMASK, &prev_mask, NULL);
}

int main(int argc, char *argv[]) {

    int uncopied_byte_cnt, status;
    int cmd;
    pid_t pid;
    char *dev_node_path = "/dev/taint_test_misc_device";

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
        fprintf(stderr, "Error opening device node: %s\n", strerror(errno));
        exit(EXIT_FAILURE);
    }

    buf = (uint8_t*)malloc(buf_len);
    buf_copy = (uint8_t*)malloc(buf_len);
    if ((!buf) || (!buf_copy)) {
        fprintf(stderr, "Error: failed to malloc %d bytes\n", buf_len);
        exit(EXIT_FAILURE);
    }

    if (signal(SIGIO, copy_buf_handler) == SIG_ERR) {
        fprintf(stderr, "Error registering handler: %s\n", strerror(errno));
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
    #ifdef TEST_TAINT
        panda_taint_label_buffer(buf, TAINTED_USER, buf_len);
    #endif
    cmd = TT_IOW(TT_IOC_TYPE, W_EPHEME, buf_len);
    uncopied_byte_cnt = ioctl(fd, cmd, buf);
    notify_write(uncopied_byte_cnt, buf, buf_len);

    // Write persistant kernel buffer
    #ifdef TEST_TAINT
        panda_taint_label_buffer(buf, TAINTED_USER, buf_len);
    #endif
    cmd = TT_IOW(TT_IOC_TYPE, W_PERSIS, buf_len);
    uncopied_byte_cnt = ioctl(fd, cmd, buf);
    notify_write(uncopied_byte_cnt, buf, buf_len);

    // Kernel Driver -> Process ----------------------------------------------------------------------------------------

    // Read ephemeral kernel buffer
    cmd = TT_IOR(TT_IOC_TYPE, R_EPHEME, buf_len);
    uncopied_byte_cnt = ioctl(fd, cmd, buf);
    notify_read(uncopied_byte_cnt, buf, buf_len);
    #ifdef TEST_TAINT
        panda_taint_assert_label_found_range(buf, TAINTED_KERN, buf_len);
    #endif

    // Read and verify persistant kernel buffer
    cmd = TT_IOR(TT_IOC_TYPE, R_PERSIS, buf_len);
    uncopied_byte_cnt = ioctl(fd, cmd, buf);
    notify_read(uncopied_byte_cnt, buf, buf_len);
    assert(!memcmp(buf, buf_copy, buf_len));
    #ifdef TEST_TAINT
        panda_taint_assert_label_found_range(buf, TAINTED_USER, buf_len);
        //panda_taint_assert_label_found_range(buf, TAINTED_KERN, buf_len);
    #endif

    // Process -> Kernel Driver -> Other Process -----------------------------------------------------------------------

    memset(buf, 0, buf_len);
    pid = fork();

    if (pid == -1) {

        fprintf(stderr, "Error forking child: %s\n", strerror(errno));
        exit(EXIT_FAILURE);

    // Child: wait for specific signal from parent
    } else if (pid == 0) {

        // Waiting on a global is inefficent and unnecessary for the purposes of this test
        // but allows us to test signal triggered actions, which may be useful for more involved tests later
        while (!sig_triggered_copy_ok) {
            sleep(1);
        }

        if (buf_copy && (!memcmp(buf, buf_copy, buf_len))) {
            #ifdef TEST_TAINT
                panda_taint_assert_label_found_range(buf, TAINTED_KERN, buf_len);
            #endif
            printf("Signal-triggered buffer copy to child process succeeded.\n");
            exit(EXIT_SUCCESS);
        } else {
            exit(EXIT_FAILURE);
        }

    // Parent: signal child to copy in buffer from kernelspace
    } else {

        // Set signal
        cmd = TT_IO(TT_IOC_TYPE, SET_SIGN);
        assert(!ioctl(fd, cmd, SIGIO));

        // Set target pid
        cmd = TT_IO(TT_IOC_TYPE, SET_PIDN);
        assert(!ioctl(fd, cmd, pid));

        // Send signal
        cmd = TT_IO(TT_IOC_TYPE, SEND_SIG);
        assert(!ioctl(fd, cmd));

        // Wait for successful termination
        waitpid(pid, &status, WUNTRACED);
        if (WIFEXITED(status)) {
            if (WEXITSTATUS(status) == 0) {
                printf("Test complete.\n");
            } else {
                fprintf(stderr, "Error: child exited with %d\n", WEXITSTATUS(status));
                exit(EXIT_FAILURE);
            }
        } else {
            fprintf(stderr, "Error: child didn't terminate normally.\n");
            exit(EXIT_FAILURE);
        }
    }

    close(fd);
    exit(EXIT_SUCCESS);
}
