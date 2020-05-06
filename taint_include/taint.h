#ifndef __TAINT_H__
#define __TAINT_H__

#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#if !defined(TARGET_I386) && !defined(TARGET_X86_64)
#error "Define your architecture (TARGET_I386 or TARGET_X86_64) with -D"
#endif

static const int ENABLE_TAINT = 6;
static const int LABEL_BUFFER = 7;
static const int LABEL_BUFFER_POS = 8;
static const int QUERY_BUFFER = 9;
static const int LABEL_REGISTER = 10;
static const int QUERY_REGISTER = 11;
static const int LOG = 12;

#if defined(TARGET_I386)
static inline
void hypercall(uint32_t eax, uint32_t ebx, uint32_t ecx, uint32_t edx, uint32_t edi) {
    asm __volatile__(
        "mov  %0, %%eax \t\n\
        mov  %1, %%ebx \t\n\
        mov  %2, %%ecx \t\n\
        mov  %3, %%edx \t\n\
        mov  %4, %%edi \t\n\
        cpuid \t\n\
        "
        : /* no output registers */
        : "g" (eax), "g" (ebx), "g" (ecx), "g" (edx), "g" (edi) /* input operands */
        : "eax", "ebx", "ecx", "edx", "edi" /* clobbered registers */
    );
}

#define HYPERCALL(a,b,c,d,e) hypercall((uint32_t)(a),(uint32_t)(b),(uint32_t)(c),(uint32_t)(d),(uint32_t)(e))
#endif

#if defined(TARGET_X86_64)
static inline
void hypercall(uint64_t rax, uint64_t rbx, uint64_t rcx, uint64_t rdx, uint64_t rdi) {
    asm __volatile__(
        "mov  %0, %%rax \t\n\
        mov  %1, %%rbx \t\n\
        mov  %2, %%rcx \t\n\
        mov  %3, %%rdx \t\n\
        mov  %4, %%rdi \t\n\
        cpuid \t\n\
        "
        : /* no output registers */
        : "g" (rax), "g" (rbx), "g" (rcx), "g" (rdx), "g" (rdi) /* input operands */
        : "rax", "rbx", "rcx", "rdx", "rdi" /* clobbered registers */
    );
}

#define HYPERCALL(a,b,c,d,e) hypercall((uint64_t)(a),(uint64_t)(b),(uint64_t)(c),(uint64_t)(d),(uint64_t)(e))
#endif

#if !defined(HYPERCALL)
#error "HYPERCALL wrapper macro not defined?"
#endif

static inline
void hypercall_log(char *c_str) {
    HYPERCALL(LOG, strlen(c_str)+1, (void *)c_str, 0, 0);
}

static inline
void hypercall_query_reg(uint32_t reg_num, uint32_t off, long label) {
    HYPERCALL(QUERY_REGISTER, reg_num, off, 0, label);
}

static inline
void hypercall_label_reg(uint32_t reg_num, uint32_t off, long label) {
    HYPERCALL(LABEL_REGISTER, reg_num, off, 0, label);
}

static inline
void hypercall_enable_taint() {
    HYPERCALL(ENABLE_TAINT, 0, 0, 0, 0);
}

static inline
void hypercall_label_buffer(void *buf, unsigned long len, long label) {
    HYPERCALL(LABEL_BUFFER, buf, len, 0, label);
}

static inline
void hypercall_query_buffer(void *buf, unsigned long off, long label, long positive) {
    HYPERCALL(QUERY_BUFFER, buf, off, positive, label);
}

/* buf is the address of the buffer to be labeled
 *  * label is the label to be applied to the buffer
 *   * len is the length of the buffer to be labeled */
static inline
void panda_taint_label_buffer(void *buf, int label, unsigned long len) {
    hypercall_label_buffer(buf, len, label);
}

static inline
void panda_taint_query_buffer(void *buf, unsigned long off, long label, long positive) {
    hypercall_query_buffer(buf, off, label, positive);
}

static inline
void panda_taint_assert_label_found(void *buf, uint32_t off, uint32_t expected_label) {
    panda_taint_query_buffer(buf, off, expected_label, 1);
}

static inline
void panda_taint_assert_label_not_found(void *buf, uint32_t off, uint32_t expected_label) {
    panda_taint_query_buffer(buf, off, expected_label, 0);
}

static inline
void panda_taint_assert_label_found_range(void *buf, size_t len, uint32_t expected_label) {
    int i;
    for(i=0;i<len;i++) {
        panda_taint_assert_label_found(buf, i, expected_label);
    }
}

static inline
void panda_taint_assert_label_not_found_range(void *buf, size_t len, uint32_t expected_label) {
    int i;
    for(i=0;i<len;i++) {
        panda_taint_assert_label_not_found(buf, i, expected_label);
    }
}

static inline
void panda_taint_log(char *c_str) {
    hypercall_log(c_str);
}

#endif // __TAINT_H__
