import sys

def lsb(offset, isFlip, isLittle):
  with open("littleschoolbus.bmp", "rb") as img:
    bytes = bytearray(img.read())
  bytes=bytes[offset:]

  data=''
  bits=''
  for byte in bytes:
    if len(bits) < 8:
      bit = byte&1
      if bit == 0 and isFlip:
        bit = 1
      elif bit == 1 and isFlip:
        bit = 0
      if isLittle:
        bits = str(bit) + bits
      else:
        bits += str(bit)
    else:
      c = int(bits,2)
      if c >= 32 and c <= 126:
        data += chr(c)
      bits = ''

  return data


for i in range(0,8):
  for j in range(0,2):
    offset = lsb(i, False, j)
    flip = lsb(i, True, j)

    f = open(str(j)+'_offset_'+str(i), 'w')
    f.write(offset)
    f.close()

    f = open(str(j)+'_flip_'+str(i), 'w')
    f.write(flip)
    f.close()
