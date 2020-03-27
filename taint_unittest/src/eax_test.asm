; EXPECTED OUTPUT
; taint2: positional register label
; taint2: query labels on memory
; taint2: assert positive taint_contains(addr: BFC0E5BC, label: 12345678)
; taint2: query labels on memory
; taint2: assert negative taint_contains(addr: BFC0E5B4, label: 12345678)
; taint2: query labels on memory
; taint2: assert positive taint_contains(addr: BFC0E5BC, label: 12345678)

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
