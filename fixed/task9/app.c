#include <stdio.h>
int main(int argc,char**argv)
{
    if(argc<2)
    {
        printf("need arg\n");
        return 1;
    }
    printf(argv[1]);
    return 0;
}
