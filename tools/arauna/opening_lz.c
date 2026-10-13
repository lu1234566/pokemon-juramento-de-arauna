/* BIOS LZ77 encoder for authored cinematic frames; no emulator/test code. */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

static unsigned hash3(const uint8_t *p) {
    return ((unsigned)p[0]*251u + (unsigned)p[1]*31u + p[2]) & 65535u;
}

int AraunaOpeningCompress(const uint8_t *src, int size, uint8_t *dst, int minDistance) {
    int *head=malloc(65536*sizeof(int));
    int *prev=malloc(size*sizeof(int));
    if (!head || !prev) { free(head); free(prev); return -1; }
    for (int i=0;i<65536;i++) head[i]=-1;
    dst[0]=0x10; dst[1]=size; dst[2]=size>>8; dst[3]=size>>16;
    int pos=0, out=4;
    while (pos<size) {
        int flag=out++; dst[flag]=0;
        for (int bit=7;bit>=0 && pos<size;bit--) {
            int length=0, distance=0;
            if (pos+2<size) {
                int candidate=head[hash3(src+pos)], attempts=0;
                while (candidate>=0 && pos-candidate<=4096 && attempts++<128) {
                    if (pos-candidate>=minDistance) {
                        int n=0;
                        while (n<18 && pos+n<size && src[candidate+n]==src[pos+n]) n++;
                        if (n>length) { length=n; distance=pos-candidate; if (n==18) break; }
                    }
                    candidate=prev[candidate];
                }
            }
            int advance;
            if (length>=3) {
                dst[flag]|=1u<<bit;
                int displacement=distance-1;
                dst[out++]=((length-3)<<4)|(displacement>>8);
                dst[out++]=displacement;
                advance=length;
            } else { dst[out++]=src[pos]; advance=1; }
            for (int end=pos+advance;pos<end;pos++) {
                prev[pos]=-1;
                if (pos+2<size) { unsigned h=hash3(src+pos); prev[pos]=head[h]; head[h]=pos; }
            }
        }
    }
    while (out&3) dst[out++]=0;
    free(head); free(prev);
    return out;
}
