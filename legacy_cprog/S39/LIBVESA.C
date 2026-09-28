/* Graphic lib vesa 640 x 480 x 256 x 2 page
   program by 3D Engine */
#include <stdio.h>
#include <conio.h>
#include <dos.h>
#include <stdlib.h>
#include <time.h>
#include <mem.h>
typedef unsigned char BYTE;
/* header from asm code */
int initvesa101 (void); /* set VESA mode */
void putpix(int x,int y,unsigned char color);
int  getpix(int x,int y);
void SetVisual(int p);
void SetActive(int p);
#define Textmode()  _AX = 3; geninterrupt(0x10);
void Clearpage(int page)
{
	int i,j;
	SetActive(page);
	for(j = 0; j < 480; j++)
		for(i = 0; i < 640; i++)
			putpix(i,j,0);
}
void Putimage(int x0, int y0, BYTE *img)
{
	int i, j, k, x1, y1, Width, Height;
	BYTE *ptr;

	ptr = img;
	Width  = *ptr++;
	Height = *ptr++;
	x1 = x0 + Width;
	y1 = y0 + Height;
	for(j = y0; j < y1; j++)
		for(i = x0; i < x1; i++) {
			k = *ptr++;
			if(i < 640 && j < 480 && i >= 0 && j >= 0&& k!=0)
				putpix(i, j, k);
		}
}
BYTE *Getmemimage(int x0,int y0,int x1,int y1)
{
	return(malloc((x1-x0)*(y1-y0)+2));
}
void Getimage(int x0, int y0,int x1, int y1, BYTE *img)
{
	int i, j ;
	BYTE *ptr;

	ptr = img;
	*ptr++ = x1 - x0;
	*ptr++ = y1 - y0;
	for(j = y0; j < y1; j++)
	{
		if(j>=480) break;
		for(i = x0; i < x1; i++) {
			if(i < 640 && i >= 0 && j >= 0)
				*ptr = getpix(i, j);
			ptr++;
		}
	}
}
void Setpalette(BYTE *ptr)
{
	int i;
	outp(0x3c8,0);
	for(i=0;i<768;i++)
		outp(0x3c9,*ptr++);
}
void Rec(int x0, int y0, int x1, int y1, BYTE color)
{
	int i;
	for(i = x0; i <= x1; i++) {
		putpix(i, y0, color);
		putpix(i, y1, color);
	}
	for(i = y0; i < y1; i++) {
		putpix(x0, i, color);
		putpix(x1, i, color);
	}
}
void Bar(int x0, int y0, int x1, int y1, BYTE color)
{
	int i, j;
	for(j = y0; j < y1; j++)
		for(i = x0; i < x1; i++)
			putpix(i, j, color);

}