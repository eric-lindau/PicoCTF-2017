import sys

#printf base
base = [0x00007f376b95f160, 0x00007f712ed5a160, 0x00007f706fdac160]

with open("offset.txt") as f:
    index = 0
    for line in f:
        #print line
        table = line.split(".")
        for number in table:
            if "0x" not in number:
                continue
            num = int(number, 16)
            num -= base[index] - 0x4f160
            sys.stdout.write(hex(num)+'.')
        index += 1
        sys.stdout.write('\n')
