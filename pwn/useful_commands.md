

- to disable ASLR: (=2 to bring it back on)
```bash
sudo sysctl -w kernel.randomize_va_space=0
```

- to check symbols (symbol table):
```bash
readelf -s
```

- to check GOT (global offset table)
```bash
objdump -d -j .got.plt
```

- Ret2LibC specific:
```bash
# to get the base of libc address and its path (if ASLR is off)
ldd ./exec_name 
# to get 'system' and '/bin/sh' addresses 
readelf -s /path/to/libc | grep system
strings -a -t x /path/to/libc | grep '/bin/sh'
```

