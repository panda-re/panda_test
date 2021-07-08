    org 0x100

section .text

_start:
    ; First we need to setup the serial port.
    mov ah, 0x00 ; int 0x14 initialization subfunction
    mov al, 0x00 ; zero out al, we're going to set our serial port values here

    ; Setup the serial port parameters.
    or  al, 0x0003 ; word length bits = 8
    or  al, 0x00A0 ; 2400 baud

    ; Call int 0x14
    int 0x14

    ; Open COM1
    mov ah, 0x3D
    mov al, 0x00
    mov dx,  com1
    int 0x21

    ; Read COM1
    mov bx, ax
    mov ah, 0x3F
    mov cx, 1
    mov dx, buffer
    int 0x21

    ; Close COM1
    mov ah, 0x3E
    int 0x21

    mov al, [buffer]
    cmp al, 100
    jbe .ldlte

.ldgt:
    mov dx, gt100msg
    jmp .show_result

.ldlte:
    mov dx, lte100msg

.show_result:
    mov ah, 0x09
    int 0x21

.end:
    mov al, 0x00
    mov ah, 0x31
    int 0x21

section .data

com1        db 'COM1',0;
gt100msg    db 'greater than 100',0x0D,0x0A,'$'
lte100msg   db 'less than or equal to 100',0x0D,0x0A,'$'

section .bss
buffer      resb 1
