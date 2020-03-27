#ifndef __TAINT_H__
#define __TAINT_H__

#define TARGET_I386

/*#if !defined(TARGET_I386) && !defined(TARGET_ARM)
#error "Define your architecture (TARGET_I386 or TARGET_ARM) with -D"
#endif
*/
static const int LABEL_BUFFER = 7;
static const int LABEL_BUFFER_POS = 8;
static const int QUERY_BUFFER = 9;

//#define 

static inline void hypercall_query_reg(uint32_t reg_num, uint32_t off, long label) {
  int eax = 11;
  unsigned long ebx = reg_num;
  unsigned long ecx = off;
  unsigned long edx = 0;
  long edi = label;


  asm __volatile__
      ("mov  %0, %%eax \t\n\
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
  return;
}

static inline void hypercall_label_reg(uint32_t reg_num, uint32_t off, long label) {
  int eax = 10;
  unsigned long ebx = reg_num;
  unsigned long ecx = off;
  unsigned long edx = 0;
  long edi = label;


  asm __volatile__
      ("mov  %0, %%eax \t\n\
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
  return;
}

static inline void turn_on_taint() {
    int eax = 6;
    int ebx,ecx,edx,edi;
    edi = edx = ecx = ebx = eax;

  asm __volatile__
      ("mov  %0, %%eax \t\n\
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
  return;
}

//#ifdef TARGET_I386
static inline
void hypercall(void *buf, unsigned long len, long label, unsigned long off,
    int action) {
  int eax = action;
  void *ebx = buf;
  unsigned long ecx = len;
  unsigned long edx = off;
  long edi = label;
//  void *esi = pmli;

  asm __volatile__
      ("mov  %0, %%eax \t\n\
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
  return;
}

static inline
/*uint32_t*/void hypercall_for_query(void *buf, unsigned long off, long label) {
  int eax = QUERY_BUFFER;
  void *ebx = buf;
  unsigned long ecx = off;
//  void *edx = taint_label_storage;
  void *edx = 0;
  long edi = label;

//hypercall(buf, 1, 0, 0, QUERY_BUFFER);
//return 0;
//  *num_labels = 0;

//  printf("eax %08X\n", eax);

//  uint32_t rv = 0;

  asm __volatile__
      ("mov  %0, %%eax \t\n\
        mov  %1, %%ebx \t\n\
        mov  %2, %%ecx \t\n\
        mov  %3, %%edx \t\n\
	mov  %4, %%edi \t\n\
        cpuid \t\n\
      "
      :
      : "g" (eax), "g" (ebx), "g" (ecx), "g" (edx), "g" (edi)
       : "eax", "ebx", "ecx", "edx", "edi" 
      );

//  if(eax < 0 | eax > 16) {
//	  eax = 0;
//  }

//  return *num_labels;
}
//#endif // TARGET_I386


/* buf is the address of the buffer to be labeled
 *  * label is the label to be applied to the buffer
 *   * len is the length of the buffer to be labeled */
static inline
void vm_label_buffer(void *buf, int label, unsigned long len) {
    hypercall(buf, len, label, 0, LABEL_BUFFER);
}

static inline
void /*uint32_t*/ vm_query_buffer(void *buf, unsigned long off, long label) {
    hypercall_for_query(buf, off, label);
/*
    int num_labels;
   
//if(outbuf == 0) {

   hypercall_for_query(buf, off, 0, &num_labels);

    if (num_labels > 0) {
        uint32_t *label_buffer = (uint32_t *)malloc(sizeof(uint32_t) * num_labels);
	printf("label_buffer %08X\n", label_buffer);
	printf("outbufaddr %08X\n", outbufaddr);
	printf("*outbufaddr %08X\n", *((uint32_t *)outbufaddr));
        *((uint32_t *)outbufaddr) = &label_buffer[0];

	hypercall_for_query(buf, off, label_buffer, &num_labels);
    }
    else {
        *((uint32_t *)outbufaddr) = NULL;
    }

    return num_labels;*/
}
#endif
