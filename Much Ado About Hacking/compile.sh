gcc -O2 -Wall -Wno-unused -Imarlowe-1.0/spl/include -c MuchAdoAboutHacking.c
gcc -O2 -Wall -Wno-unused MuchAdoAboutHacking.o -Lmarlowe-1.0/spl/lib -lm -lspl -o MuchAdoAboutHacking
rm MuchAdoAboutHacking.o
