f = open('ending.txt', 'r')
text = f.read()
calc=text[0]
for i in range(1,len(text)-1,1):
  c1 = ord(calc[i-1])
  c = ord(text[i])
  #c=((c1-32)+(o-32))%96+32
  o = c-32+96+32+32-c1
  if o > (96+32):
    o = c-32+32+32-c1
  calc += chr(o)

print calc[::-1]
