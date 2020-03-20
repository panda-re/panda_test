#ifndef _TAINT_TEST_MDEV_H
#define _TAINT_TEST_MDEV_H

#include <linux/module.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/sched.h>
#include <linux/init.h>
#include <linux/slab.h>
#include <linux/device.h>
#include <linux/miscdevice.h>
#include <linux/oom.h>

#define TT_DEV_NAME "taint_test_misc_device"
static struct device *tt_dev;

static char *tt_dev_kbuf;
static size_t tt_dev_kbuf_size = (16 * PAGE_SIZE);

static const struct file_operations tt_dev_fops;

// Generic dev entry points --------------------------------------------------------------------------------------------

static inline int tt_dev_generic_open(struct inode *inode, struct file *file) {

    static int open_cnt;
    ++open_cnt;

    dev_info(tt_dev, "Opened device \'%s\' (major %d, minor %d). Open cnt = %d, ref cnt = %d\n",
        TT_DEV_NAME,
        imajor(inode),
        iminor(inode),
        (int)module_refcount(THIS_MODULE),
        open_cnt
    );

    return 0;
}

static inline int tt_dev_generic_release(struct inode *inode, struct file *file) {

    static int close_cnt;
    ++close_cnt;

    dev_info(tt_dev, "Closed device \'%s\' (major %d, minor %d). Close cnt = %d, ref cnt = %d\n",
        TT_DEV_NAME,
        imajor(inode),
        iminor(inode),
        (int)module_refcount(THIS_MODULE),
        close_cnt
    );

    return 0;
}

static inline ssize_t tt_dev_generic_read(struct file *file, char __user *buf, size_t lbuf, loff_t *ppos) {

    int num_bytes = simple_read_from_buffer(buf, lbuf, ppos, tt_dev_kbuf, tt_dev_kbuf_size);

    dev_info(tt_dev, "Read: %d bytes, offset %d\n",
         num_bytes,
         (int)*ppos
    );

    return num_bytes;
}

static inline ssize_t tt_dev_generic_write(struct file *file, const char __user *buf, size_t lbuf, loff_t *ppos) {

    int num_bytes = simple_write_to_buffer(tt_dev_kbuf, tt_dev_kbuf_size, ppos, buf, lbuf);

    dev_info(tt_dev, "Write: %d bytes, offset %d\n",
         num_bytes,
         (int)*ppos
    );

    return num_bytes;
}

// Misc device setup/teardown ------------------------------------------------------------------------------------------

static struct miscdevice tt_mdev = {
    .minor = MISC_DYNAMIC_MINOR,
    .name = TT_DEV_NAME,
    .fops = &tt_dev_fops,
};

static int __init tt_mdev_generic_init(void) {

    tt_dev_kbuf = kmalloc(tt_dev_kbuf_size, GFP_KERNEL);
    if (!tt_dev_kbuf) {
        pr_err("Failed to kmalloc %ld bytes\n", tt_dev_kbuf_size);
        return -ENOMEM;
    }

    if (misc_register(&tt_mdev)) {

        pr_err("Failed to register device \'%s\' (minor %d)\n",
            TT_DEV_NAME,
            tt_mdev.minor
        );

        kfree(tt_dev_kbuf);
        return -EBUSY;
    }

    tt_dev = tt_mdev.this_device;
    dev_info(tt_dev, "Successfully registered device \'%s\' (minor %d)\n",
        TT_DEV_NAME,
        tt_mdev.minor
    );

    return 0;
}

static void __exit tt_mdev_generic_exit(void) {

    dev_info(tt_dev, "Unregistering device \'%s\' (minor %d)\n",
        TT_DEV_NAME,
        tt_mdev.minor
    );

    misc_deregister(&tt_mdev);
    kfree(tt_dev_kbuf);
}

#endif //_TAINT_TEST_MDEV_H