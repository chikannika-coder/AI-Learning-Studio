/* program cutscene.c */
#ifdef __TINY__
#error CUTSCENE will not run in the tiny model.
#endif
#ifdef __SMALL__
#error CUTSCENE will not run in the small model.
#endif
#ifdef __MEDIUM__
#error CUTSCENE will not run in the medium model.
#endif

#include <stdlib.h>
#include <conio.h>
#include <stdio.h>
#include <dos.h>
#include <time.h>
#include <mem.h>
#include <alloc.h>
char far *MemVideo;
unsigned int LengthBuf = 320 * 200;
char far *MemBuf;
char far *FileBuf;		/* Will point to an I/O buffer    */
typedef unsigned int	WORD;
typedef unsigned char	BYTE;
typedef unsigned long	UWORD;
#define BUFSIZE  	8192	/* allocate for file reading.     */
#define FLI_COLOR	11      /* Types of FLI chunks            */
#define FLI_LC          12
#define FLI_BLACK       13
#define FLI_BRUN        15
#define FLI_COPY        16
typedef struct {		/* The structure of a .FLI header */
	UWORD size;
	WORD  magic;
	WORD  frames;
	WORD  width;
	WORD  height;
	WORD  bits;
	WORD  flags;
	WORD  speed;
	UWORD next;
	UWORD frit;
	BYTE expand[102];
} FLIHDR;
typedef struct {		/* The structure of a frame header  */
	UWORD size;
	WORD  magic;
	WORD  chunks;
	BYTE expand[8];
} FRAMEHDR;
void SetPal(char *ptr)
{
	int i;
	outp(0x3c8, 0);
	for(i = 0; i < 256; i++) {
		outp(0x3c9, *ptr++);
		outp(0x3c9, *ptr++);
		outp(0x3c9, *ptr++);
	}
}
unsigned int far *Clock = (unsigned int far *) 0x0046C;
void Timer(int clicks)
{
	unsigned int now;
	now = *Clock;
	while(abs(*Clock - now) < clicks);
}
void PlayFLI(char *file )
{
	FILE	*fp;
	FLIHDR	 hdr;
	FRAMEHDR frm;
	char far *PtrBuf;
	char 	 s, Pal[768];
	WORD	 type, cnt, change, fram, v ;
	WORD	 i, j, k;
	UWORD	 size, vc;
	/* Open file fli */
	if((fp = fopen(file, "rb" )) == 0) return;
	/* allocate a buffer for speed up  file I/O */
	FileBuf = (char *) malloc(BUFSIZE);
	setvbuf(fp, FileBuf, _IOFBF, BUFSIZE);
	/* Read header .fli = 128 byte */
	fread(&hdr, 128, 1, fp);
	for(fram = 0; fram <= hdr.frames; fram++) {
		/* Read in a frame header 16 byte */
		fread(&frm, 16, 1, fp);
		if(frm.size)
			for(i = 0; i < frm.chunks; i++) {
			fread(&size, 1, 4, fp);
			type = getw(fp);
			switch(type) {
			case FLI_LC :   vc = 0;
					j = getw(fp) * 320;
					change = getw(fp);
					for( i = 0; i < change; i++ ){
						PtrBuf = MemBuf + j;
						j += 320; vc++;
						k = getc(fp);
						while(k--) {
							vc += 2;
							PtrBuf += getc(fp);
							if((s = getc(fp)) > 0) {
								vc += s;
								while(s--)
									*PtrBuf++ =
									 getc(fp);
							}
							else {
								s = -s; vc++;
								v = getc(fp);
								while(s--)
									*PtrBuf++ = v;
							}
						}
					}
					if(vc & 1) getc(fp);
					break;
		       case FLI_BRUN  :	vc = 0;
					PtrBuf = MemBuf;
					for(i = 0; i < 200; i++) {
						j = getc(fp);
						while(j--) {
						   vc++;
						   if((s = getc( fp )) < 0) {
						      s = -s; vc += s;
						      while(s--)
							 *PtrBuf++ = getc(fp);
						   }
						   else {
							vc++; v = getc(fp);
							while(s--)
								*PtrBuf++ = v;
						   }
						}
					     }
					if(vc & 1) getc(fp);
					break;
		       case FLI_COLOR : vc = 2; j = 0;
					v = getw(fp);
					while(v--) {
						j += getc(fp) * 3;
						if((cnt = getc(fp)) == 0)
							cnt = 256;
						vc += cnt * 3 + 2;
						while(cnt--) {
						   Pal[j++] = getc(fp);
						   Pal[j++] = getc(fp);
						   Pal[j++] = getc(fp);
						}
					}
					SetPal(Pal);
					if(vc & 1) getc(fp);
					break;
		       case FLI_COPY  : fread(MemBuf, LengthBuf, 1, fp);
					break;
		       case FLI_BLACK : memset(MemBuf, 0, LengthBuf);
					break;
		       default        : goto end;
		    }
		}
		memcpy(MemVideo, MemBuf, LengthBuf);
		if(kbhit()) goto end;
                while   (inp(0x3da) & 8) ;
		while (!(inp(0x3da) & 8));
		Timer(1);
	}
end:	fclose(fp);
	free(FileBuf);
}
void main(int agc, char *agv[])
{
	if(agc<2) {
		printf ("type CUTSCENE <filename.fli>\n");
		exit(0);
	}
	_AX = 0x13;
	geninterrupt(0x10);
	MemVideo = MK_FP(0xa000, 0);
	MemBuf = malloc(LengthBuf);
	while(!kbhit())
		PlayFLI(agv[1]);
	/* Return to text mode */
	_AX = 3;
	geninterrupt(0x10);
}
