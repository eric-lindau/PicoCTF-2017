#!/usr/bin/python

import os
import random

def GetOutput(command):
    lastline = os.popen(command).readlines()
    result = lastline[0].rstrip()
    return result

output = GetOutput("nc shell2017.picoctf.com 19789")[29:]

flag = ""
random.seed("random")
for c in output:
  if c.islower():
    #rotate number around alphabet a random amount
    flag += chr((ord(c)-ord('a')+26-random.randrange(0,26))%26 + ord('a'))
  elif c.isupper():
    flag += chr((ord(c)-ord('A')+26-random.randrange(0,26))%26 + ord('A'))
  elif c.isdigit():
    flag += chr((ord(c)-ord('0')+10-random.randrange(0,10))%10 + ord('0'))
  else:
    flag += c

print flag
