#include <stdio.h>

int main()
{
    int addr= 0x0804852b; //Function Adress
    //addr-= (0x8048621 + 0x5); //Call Adress + 0x5
    addr <<= 4;
    //addr >>= 4;
    printf("Hex: 0x%x\n", addr);
    printf("Decimal: %d\n", addr);

    return 0;
}


