#ifndef _TAINT_TEST_COMMON_H
#define _TAINT_TEST_COMMON_H

#define TT_IOC_TYPE 't'

/*
 * IOCTL commands
 */

#define R_EPHEME 0  // Read from ephemeral buffer (freed before ioctl() return)
#define W_EPHEME 1  // Write to ephemeral buffer (freed before ioctl() return)
#define R_PERSIS 2  // Read from persistant buffer (freed only on module unload)
#define W_PERSIS 3  // Write to persistant buffer (freed only on module unload)
#define SET_SIGN 4  // Set signal number for kernel to send
#define SET_PIDN 5  // Set PID for kernel to send signal to
#define SEND_SIG 6  // Send specified signal to specified PID

/*
 * Taint labels
 */

#define TEST_TAINT

#define TAINTED_USER 0xABCDEF00
#define TAINTED_KERN 0xABCDEF01

#endif //_TAINT_TEST_COMMON_H