import sys


HEADER_OFFSET = int(sys.argv[1])

with open("littleschoolbus.bmp", "rb") as img:
	bytes = bytearray(img.read())

bytes = bytes[HEADER_OFFSET:]
print(len(bytes))

buffer = ""

bits = ""
for byte in bytes:
	if len(bits) != 8:
		bits += str(byte&1)
	else:
		char = chr(int(bits, 2))
		if ord(char) > 32 and ord(char) < 127:
			buffer += char
		bits = ""

print(buffer)
