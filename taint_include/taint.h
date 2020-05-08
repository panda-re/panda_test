#ifndef __TAINT_H__
#define __TAINT_H__

#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#if !defined(TARGET_I386) && !defined(TARGET_X86_64) && !defined(TARGET_ARM)
#error "Define your architecture (TARGET_I386, TARGET_X86_64 or TARGET_ARM) with -D"
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
void hypercall(uint32_t eax, uint32_t ebx, uint32_t ecx, uint32_t edx, uint32_t edi, uint32_t esi) {
    asm __volatile__(
        "mov  %0, %%eax \t\n\
        mov  %1, %%ebx \t\n\
        mov  %2, %%ecx \t\n\
        mov  %3, %%edx \t\n\
        mov  %4, %%edi \t\n\
        mov  %5, %%esi \t\n\
        cpuid \t\n\
        "
        : /* no output registers */
        : "g" (eax), "g" (ebx), "g" (ecx), "g" (edx), "g" (edi), "g" (esi) /* input operands */
        : "eax", "ebx", "ecx", "edx", "edi", "esi" /* clobbered registers */
    );
}

#define HYPERCALL(a,b,c,d,e,f) hypercall((uint32_t)(a),(uint32_t)(b),(uint32_t)(c),(uint32_t)(d),(uint32_t)(e),(uint32_t)(f))
#endif

#if defined(TARGET_X86_64)
static inline
void hypercall(uint64_t rax, uint64_t rbx, uint64_t rcx, uint64_t rdx, uint64_t rdi, uint64_t rsi) {
    asm __volatile__(
        "mov  %0, %%rax \t\n\
        mov  %1, %%rbx \t\n\
        mov  %2, %%rcx \t\n\
        mov  %3, %%rdx \t\n\
        mov  %4, %%rdi \t\n\
        mov  %5, %%rsi \t\n\
        cpuid \t\n\
        "
        : /* no output registers */
        : "g" (rax), "g" (rbx), "g" (rcx), "g" (rdx), "g" (rdi), "g" (rsi) /* input operands */
        : "rax", "rbx", "rcx", "rdx", "rdi", "rsi" /* clobbered registers */
    );
}

#define HYPERCALL(a,b,c,d,e,f) hypercall((uint64_t)(a),(uint64_t)(b),(uint64_t)(c),(uint64_t)(d),(uint64_t)(e),(uint64_t)(f))
#endif

#if defined(TARGET_ARM)
// how many bits? just going to put "int" there
// I don't have an arm toolchain so I was only able to verify that
// this builds with godbolt.org Compiler Explorer
// but not run it to test with the arm-softmmu taint2 plugin
static inline
void hypercall(int r0, int r1, int r2, int r3, int r4, int r5) {
    asm __volatile__(
        "mov  %%r0, %0 \t\n\
        mov  %%r1, %1 \t\n\
        mov  %%r2, %2 \t\n\
        mov  %%r3, %3 \t\n\
        mov  %%r4, %4 \t\n\
        mov  %%r5, %5 \t\n\
        mcr  p7, 0, %%r0, %%c0, %%c0, 0\t\n\
        "
        : /* no output registers */
        : "g" (r0), "g" (r1), "g" (r2), "g" (r3), "g" (r4), "g" (r5) /* input operands */
        : "r0", "r1", "r2", "r3", "r4", "r5" /* clobbered registers */
    );

}

#define HYPERCALL(a,b,c,d,e,f) hypercall((int)(a),(int)(b),(int)(c),(int)(d),(int)(e),(int)(f))
#endif

#if !defined(HYPERCALL)
#error "HYPERCALL wrapper macro not defined?"
#endif

static inline
void hypercall_log(char *c_str) {
    HYPERCALL(LOG, strlen(c_str)+1, (void *)c_str, 0, 0, 0);
}

static inline
void hypercall_query_reg(uint32_t reg_num, uint32_t reg_off, long label, long positive) {
    HYPERCALL(QUERY_REGISTER, reg_num, reg_off, positive, label, 0);
}

static inline
void hypercall_label_reg(uint32_t reg_num, uint32_t reg_off, long label) {
    HYPERCALL(LABEL_REGISTER, reg_num, reg_off, 0, label, 0);
}

static inline
void hypercall_enable_taint() {
    HYPERCALL(ENABLE_TAINT, 0, 0, 0, 0, 0);
}

static inline
void hypercall_label_buffer(void *buf, unsigned long len, long label) {
    HYPERCALL(LABEL_BUFFER, buf, len, 0, label, 0);
}

static inline
void hypercall_query_buffer(void *buf, uint32_t off, long label, long positive) {
    HYPERCALL(QUERY_BUFFER, buf, off, positive, label, 0);
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
