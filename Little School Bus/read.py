import sys


HEADER_OFFSET = int(sys.argv[1])

with open("littleschoolbus.bmp", "rb") as img:
	bytes = bytearray(img.read())

bytes = bytes[HEADER_OFFSET:]

buffer = ""

bits = ""
for byte in bytes:
	if len(bits) < 8:
		bits += str(byte&1)
	elif bits is not "00000000":
		char = chr(int(bits, 2))
		if ord(char) > 64 and ord(char) < 123:
			buffer += char
		bits = ""

print(buffer)
