#include <linux/module.h>
#include <stdint.h>

#include "tt_mdev.h"

#define TT_IOC_TYPE 't'
#define XOR_CONST 0x13
#define DEF_CONST 0xFF

static inline long tt_dev_unlocked_ioctl(struct file *fp, unsigned int cmd, unsigned long arg) {

	int uncopied_byte_cnt, direction, buf_len;
	uint8_t *buffer;
	void __user *io_argp = (void __user *)arg;

	// Verify cmd
	if (_IOC_TYPE(cmd) != TT_IOC_TYPE) {
		dev_err(tt_dev, " invalid cmd (0x%x), type error\n", cmd);
		return -EINVAL;
	}

	// kmalloc buffer of requested buf_len
	buf_len = _IOC_SIZE(cmd);
	buffer = kmalloc((size_t)buf_len, GFP_KERNEL);
	if (!buffer) {
		dev_err(tt_dev, " failed to kmalloc %d bytes\n", buf_len);
		return -ENOMEM;
	}

	// Init buffer with default constant
	memset(buffer, DEF_CONST, buf_len);

	// TODO (tnballo): Start backing the dynamic temp buf with tt_dev_kbuf for "last written" persistance
	// Right now, ioctl read is static and decoupled from /dev/taint_test_misc_device read/write

	// Handle request
	direction = _IOC_DIR(cmd);
	switch (direction) {

		// Process -> Kernel Driver ------------------------------------------------------------------------------------

		// Transparent write to buf
		case _IOC_WRITE:

			dev_info(tt_dev," writing %d bytes from userspace to device \'%s\'\n",
				buf_len,
				TT_DEV_NAME
			);

			uncopied_byte_cnt = copy_from_user(buffer, io_argp, buf_len);
			dev_info(tt_dev, " copy_from_user() failure count: %d\n", uncopied_byte_cnt);
			break;

		// Kernel Driver -> Process ------------------------------------------------------------------------------------

		// Returns current buff contents XORed with const
		case _IOC_READ:

			dev_info(tt_dev," reading %d bytes from device \'%s\' to userspace\n",
				buf_len,
				TT_DEV_NAME
			);

			for (int i = 0; i < buf_len; ++i) {
				buffer[i] = buffer[i] ^ XOR_CONST;
			}

			uncopied_byte_cnt = copy_to_user(io_argp, buffer, buf_len);
			dev_info(tt_dev, " copy_to_user() failure count: %d\n", uncopied_byte_cnt);
			break;

		// Process -> Kernel Driver -> Other Process -------------------------------------------------------------------

		// TODO (tnballo): add signalling here to test Process -> Kernel Driver -> Other Process with indirection, switch on cmd

		// Error
		default:
			dev_err(tt_dev, " invalid cmd (0x%x), direction error\n", cmd);
			return -EINVAL;
	}

	// Log buffer
	dev_info(tt_dev, " buffer: ");
	for (int i = 0; i < buf_len; ++i) {
		dev_info(tt_dev, "0x%02x ", buffer[i]);
	}
	dev_info(tt_dev, "\n");

	kfree(buffer);
	return uncopied_byte_cnt;
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
MODULE_DESCRIPTION("PANDA test for ioctl plugin and process->kernel/kernel->process/process->kernel->process taint");
MODULE_LICENSE("GPL v2");