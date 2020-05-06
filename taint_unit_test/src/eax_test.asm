%ifdef TARGET_I386
	global	_start
	section .text

_start:
; set taint on EAX (register 0)
	mov	eax, 10
	mov	ebx, 0
	mov	ecx, 0
	mov	edx, 0
	mov	edi, 0x12345678
	cpuid

; if taint system works correctly and EAX is tainted, we can check for this
; by pushing eax to stack, then testing the stack for taint label
; this time, it should be positive for taint
        push    eax
        mov     eax, 9
        mov     ebx, esp
        mov     ecx, 0
        mov     edx, 0
        mov     edi, 0x12345678
        cpuid
        pop     eax

; remove taint from the stack memory
	push	0
; test negative
	push	eax
        mov     eax, 9
	; testing stack-4 , the previous frame that we wiped with the push 0
        mov     ebx, esp
	sub	ebx, 4
        mov     ecx, 0
        mov     edx, 0
        mov     edi, 0x12345678
        cpuid
	pop	eax
	add	esp, 4

; repeat the test to see if "pop eax" preserves taint by pushing eax back to stack and testing it again
; stack should still test positive for taint which was transferred from eax if so
	push	eax
	mov	eax, 9
	mov	ebx, esp
	mov	ecx, 0
	mov	edx, 0
	mov	edi, 0x12345678
	cpuid
	pop	eax

; addition by constant, still tainted
	add	eax, 1
	push	eax
        mov     eax, 9
        mov     ebx, esp
        mov     ecx, 0
        mov     edx, 0
        mov     edi, 0x12345678
        cpuid
        pop     eax

; subtraction, still tainted
        sub     eax, 1
        push    eax
        mov     eax, 9
        mov     ebx, esp
        mov     ecx, 0
        mov     edx, 0
        mov     edi, 0x12345678
        cpuid
        pop     eax

; mult, still
	imul	eax, 1024
        push    edx
	push	eax

        mov     eax, 9
        mov     ebx, esp
	sub	ebx, 4
        mov     ecx, 0
        mov     edx, 0
        mov     edi, 0x12345678
        cpuid

	mov	eax, 9
	mov	ebx, esp
	mov	ecx, 0
	mov	edx, 0
	mov	edi, 0x12345678
	cpuid

	pop	eax
        pop     edx

; div, still
        div     eax
        push    edx
	push	eax

        mov     eax, 9
        mov     ebx, esp
        sub     ebx, 4
        mov     ecx, 0
        mov     edx, 0
        mov     edi, 0x12345678
        cpuid

        mov     eax, 9
        mov     ebx, esp
        mov     ecx, 0
        mov     edx, 0
        mov     edi, 0x12345678
        cpuid

	pop	eax
        pop     edx

	xor	ebx, ebx
	push	byte 1
	pop	eax
	int	80h

	section	.bss
test_word:	resw	1

%endif

%ifdef TARGET_X86_64
	global	_start
	section .text

_start:
; set taint on EAX (register 0)
	mov	rax, 10
	mov	rbx, 0
	mov	rcx, 0
	mov	rdx, 0
	mov	rdi, 0x12345678
	cpuid

; if taint system works correctly and EAX is tainted, we can check for this
; by pushing eax to stack, then testing the stack for taint label
; this time, it should be positive for taint
        push    rax
        mov     rax, 9
        mov     rbx, rsp
        mov     rcx, 0
        mov     rdx, 0
        mov     rdi, 0x12345678
        cpuid
        pop     rax

; remove taint from the stack memory
	push	0
; test negative
	push	rax
        mov     rax, 9
	; testing stack-4 , the previous frame that we wiped with the push 0
        mov     rbx, rsp
	sub	rbx, 4
        mov     rcx, 0
        mov     rdx, 0
        mov     rdi, 0x12345678
        cpuid
	pop	rax
	add	rsp, 4

; repeat the test to see if "pop eax" preserves taint by pushing eax back to stack and testing it again
; stack should still test positive for taint which was transferred from eax if so
	push	rax
	mov	rax, 9
	mov	rbx, rsp
	mov	rcx, 0
	mov	rdx, 0
	mov	rdi, 0x12345678
	cpuid
	pop	rax

; addition by constant, still tainted
	add	rax, 1
	push	rax
        mov     rax, 9
        mov     rbx, rsp
        mov     rcx, 0
        mov     rdx, 0
        mov     rdi, 0x12345678
        cpuid
        pop     rax

; subtraction, still tainted
        sub     rax, 1
        push    rax
        mov     rax, 9
        mov     rbx, rsp
        mov     rcx, 0
        mov     rdx, 0
        mov     rdi, 0x12345678
        cpuid
        pop     rax

; mult, still
	imul	rax, 1024
        push    rdx
	push	rax

        mov     rax, 9
        mov     rbx, rsp
	sub	rbx, 4
        mov     rcx, 0
        mov     rdx, 0
        mov     rdi, 0x12345678
        cpuid

	mov	rax, 9
	mov	rbx, rsp
	mov	rcx, 0
	mov	rdx, 0
	mov	rdi, 0x12345678
	cpuid

	pop	rax
        pop     rdx

; div, still
        div     rax
        push    rdx
	push	rax

        mov     rax, 9
        mov     rbx, rsp
        sub     rbx, 4
        mov     rcx, 0
        mov     rdx, 0
        mov     rdi, 0x12345678
        cpuid

        mov     rax, 9
        mov     rbx, rsp
        mov     rcx, 0
        mov     rdx, 0
        mov     rdi, 0x12345678
        cpuid

	pop	rax
        pop     rdx

	mov	rax, 60
	xor	rdi, rdi
	syscall

	section	.bss
test_word:	resw	1

%endif
