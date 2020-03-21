#include <linux/module.h>

#include "tt_mdev.h"
#include "tt_ioctl_cmds.h"

#define XOR_CONST 0x13
#define DEF_CONST 0xFF

static int sig_pid = -1;
static struct task_struct *sig_task = NULL;
static int sig_to_send = SIGKILL;

static int read_buf(void __user *io_argp, char* buf, int buf_len) {

    int uncopied_byte_cnt = 0;

    dev_info(tt_dev,"Reading %d bytes from device \'%s\' to userspace\n",
        buf_len,
        TT_DEV_NAME
    );

    uncopied_byte_cnt = copy_to_user(io_argp, buf, buf_len);
    if (uncopied_byte_cnt) {
        dev_err(tt_dev, "copy_to_user() failed byte cnt: %d\n", uncopied_byte_cnt);
    }

    return uncopied_byte_cnt;
}

static int write_buf(void __user *io_argp, char* buf, int buf_len) {

    int uncopied_byte_cnt = 0;

    dev_info(tt_dev,"Writing %d bytes from userspace to device\'%s\'\n",
        buf_len,
        TT_DEV_NAME
    );

    uncopied_byte_cnt = copy_from_user(buf, io_argp, buf_len);
    if (uncopied_byte_cnt) {
        dev_err(tt_dev, "copy_from_user() failed byte cnt: %d\n", uncopied_byte_cnt);
    }

    return uncopied_byte_cnt;
}

static inline long tt_dev_unlocked_ioctl(struct file *fp, unsigned int cmd, unsigned long arg) {

    int direction, buf_len, i;
    void __user *io_argp = (void __user *)arg;
    int ret_val = 0;
    char *buf = NULL;

    if (_IOC_TYPE(cmd) != TT_IOC_TYPE) {
        dev_err(tt_dev, "Invalid cmd (0x%x), type error\n", cmd);
        return -EINVAL;
    }

    buf_len = _IOC_SIZE(cmd);
    if (buf_len > TT_KBUF_MAX) {
        dev_err(tt_dev, "Exceeded buffer size limit: %lu bytes\n", TT_KBUF_MAX);
        return -EINVAL;
    }

    if ((_IOC_NR(cmd) == R_EPHEME) || (_IOC_NR(cmd) == W_EPHEME)) {

        buf = kmalloc((size_t)buf_len, GFP_KERNEL);
        if (!buf) {
            dev_err(tt_dev, "Failed to kmalloc %d bytes\n", buf_len);
            return -ENOMEM;
        }

        memset(buf, DEF_CONST, buf_len);
    }

    direction = _IOC_DIR(cmd);
    switch (direction) {

        // Process -> Kernel Driver ------------------------------------------------------------------------------------

        case _IOC_WRITE:

            switch(_IOC_NR(cmd)) {

                // Ephemeral write
                case W_EPHEME:
                    ret_val = write_buf(io_argp, buf, buf_len);
                    kfree(buf);
                    break;

                // Persistant write
                case W_PERSIS:
                    ret_val = write_buf(io_argp, tt_dev_kbuf, buf_len);
                    break;

                default:
                    dev_err(tt_dev, "Invalid cmd (0x%x): bad write type\n", cmd);
                    return -EINVAL;
            }
            break;

        // Kernel Driver -> Process ------------------------------------------------------------------------------------

        case _IOC_READ:

            switch(_IOC_NR(cmd)) {

                // Ephemeral read
                case R_EPHEME:

                    // Current buff contents XORed with an arbitray constant
                    // TODO (tnballo): taint label test for 2 labels
                    for (i = 0; i < buf_len; ++i) {
                        buf[i] = buf[i] ^ XOR_CONST;
                    }

                    ret_val = read_buf(io_argp, buf, buf_len);
                    kfree(buf);
                    break;

                // Persistant read
                case R_PERSIS:
                    ret_val = read_buf(io_argp, tt_dev_kbuf, buf_len);
                    break;

                default:
                    dev_err(tt_dev, "Invalid cmd (0x%x): bad read type\n", cmd);
                    return -EINVAL;
            }
            break;

        // Process -> Kernel Driver -> Other Process -------------------------------------------------------------------

        case _IOC_NONE:

            switch(_IOC_NR(cmd)) {

                // Set signal to send
                case SET_SIGN:
                    sig_to_send = (int)arg;
                    dev_info(tt_dev, "Set signal to send: %d\n", sig_to_send);
                    break;

                // Set PID to send signal to
                case SET_PIDN:
                    sig_pid = (int)arg;
                    dev_info(tt_dev, "Set pid to send signals to: %d\n", sig_pid);
                    sig_task = pid_task(find_vpid(sig_pid), PIDTYPE_PID);
                    break;

                // Send configured signal to configured PID
                case SEND_SIG:

                    if (sig_pid == -1) {
                        dev_warn(tt_dev, "No signal set, using default: %d\n", sig_to_send);
                    }

                    if (!sig_task) {
                        sig_task = current;
                        sig_pid = (int)current->pid;
                        dev_warn(tt_dev, "No pid set, using current: %d\n", sig_pid);
                    }

                    ret_val = send_sig(sig_to_send, sig_task, 0);
                    dev_info(tt_dev, "Sent signal %d to pid %d, returned %d\n",
                        sig_to_send,
                        sig_pid,
                        ret_val
                    );
                    break;

                default:
                    dev_err(tt_dev, "Invalid cmd (0x%x): bad direction-less type\n", cmd);
                    return -EINVAL;
            }
            break;

        default:
            dev_err(tt_dev, "Invalid cmd (0x%x): bad direction\n", cmd);
            return -EINVAL;
    }

    return ret_val;
}

// Module init ---------------------------------------------------------------------------------------------------------

static const struct file_operations tt_dev_fops = {
    .owner = THIS_MODULE,
    .unlocked_ioctl = tt_dev_unlocked_ioctl,
    .open = tt_dev_generic_open,
    .release = tt_dev_generic_release,
    .read = tt_dev_generic_read,
    .write = tt_dev_generic_write
};

module_init(tt_mdev_generic_init);
module_exit(tt_mdev_generic_exit);

MODULE_AUTHOR("Tiemoko Ballo");
MODULE_DESCRIPTION("PANDA test for taint tracking across device driver interfaces");
MODULE_LICENSE("GPL v2");