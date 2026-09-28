/* program showspi.c */
/* code by '3D Engine' */
#include <stdio.h>
#include <conio.h>
#include <dos.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned char BYTE;
BYTE Pal[768];
BYTE *BUFFER;
BYTE far *VGA = (BYTE far *)MK_FP(0xa000, 0);
void Setpal(BYTE *ptr)
{
	int i;


	outp(0x3c8, 0);
	for(i = 0; i < 256; i++){
		outp(0x3c9, (*ptr++ >> 2));
		outp(0x3c9, (*ptr++ >> 2));
		outp(0x3c9, (*ptr++ >> 2));
	}
}
void ShowPal(void)
{
	FILE *fp;
	fp = fopen("palette.pal", "rb");
	fread(Pal, 768, 1, fp);
	fclose(fp);
	Setpal(Pal);
}
void ShowCenterSpi(char *Name)
{
	FILE *fp;
	int wi, hi, w, h;
	int i;
	BYTE *ptr;

	fp  = fopen(Name,"rb");
	wi  =  fgetc(fp) & 0xff;
	wi += (fgetc(fp) & 0xff) << 8;
	hi  =  fgetc(fp) & 0xff;
	hi += (fgetc(fp) & 0xff) << 8;
	w = 160 - (hi>>1);
	h = 100 - (hi>>1);


	BUFFER = malloc(wi * hi);
	fread(BUFFER, wi * hi, 1, fp);
	fclose(fp);
	ptr = BUFFER;
	memset(VGA, 0, 320 * 200); 	/* clear screen */
	for (i = 0; i < hi; i++) {
		memcpy(VGA + (i + h) * 320 + w, ptr, wi);
		ptr += wi;
	}
	free(BUFFER);

}
void main(int agc,char *agv[])
{
	if(agc<1) {
		printf("Type 'showspi [name.spi]'\n");
		return;
	}
	_AX=0x13;
	geninterrupt(0x10);
	ShowPal();
	ShowCenterSpi(agv[1]);
	getch();
	_AX=3;
	geninterrupt(0x10);

}