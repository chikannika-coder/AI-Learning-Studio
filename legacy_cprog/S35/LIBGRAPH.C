/* --- Computer Time C Programming --- */
/* --- libgraph.c code by  3D Engine --- */
#include <stdio.h>
#include <conio.h>
#include <dos.h>
#include <mem.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>
typedef unsigned char BYTE;
char far *PageStart;
char far *FirstAdr[3];
unsigned int LINE_Y[240];
unsigned int POT_X[360];
unsigned short page_offset[3];
int PAGE = 0;
#define TextMode() {_AX = 3; geninterrupt(0x10);}
unsigned short ModeX_360x240regs[] = {
   0x3d4,0x00,0x6b, 0x3d4,0x01,0x59, 0x3d4,0x02,0x5a,
   0x3d4,0x03,0x8e, 0x3d4,0x04,0x5e, 0x3d4,0x05,0x8a,
   0x3d4,0x06,0x0d, 0x3d4,0x07,0x3e, 0x3d4,0x08,0x00,
   0x3d4,0x09,0x41, 0x3d4,0x10,0xea, 0x3d4,0x11,0xac,
   0x3d4,0x12,0xdf, 0x3d4,0x13,0x2d, 0x3d4,0x14,0x00,
   0x3d4,0x15,0xe7, 0x3d4,0x16,0x06, 0x3d4,0x17,0xe3,
   0x3c4,0x01,0x01, 0x3c4,0x04,0x06, 0x3ce,0x05,0x40,
   0x3ce,0x06,0x05 };
void OutReg(void)
{	/* set vga register mode X */
	unsigned short i, j, *Reg = ModeX_360x240regs;
	for(i = 0; i < 22; i++) {
		j = *Reg++;
		outp(j, *Reg++);
		outp(j + 1, *Reg++);
	}
}
void SetModeX(void)
{	/* set mode X 360x240x256 3 page */
	unsigned int i;
	_AX = 0x13;
	geninterrupt(0x10);
	outp(0x3d4, 17);
	outp(0x3d5, (inp(0x3d5) & 127));
	outp(0x3c2, 231);
	OutReg();
	outp(0x3c0, 0x30);
	outp(0x3c0, 0x41);
	outp(0x3c0, 0x33);
	outp(0x3c0, 0);
	PageStart = MK_FP(0xa000, 0);
	for(i = 0; i < 0xffff; i++)
		*(PageStart + i) = 0;
	for (i = 0; i < 3; i++) {
		page_offset[i] = (21600 * i);
		FirstAdr[i] = PageStart + page_offset[i];
	}
	for(i = 0; i < 240; i++)
		LINE_Y[i] = i * 90;
	for(i = 0; i < 360; i++)
		POT_X[i] = (256 << (i & 3)) | 2;
}
void PutPixel(int x, int y, BYTE color)
{	/* put pixel */
	if(x < 0 || x > 359 || y < 0 || y > 239) return;
	outport(0x3c4, POT_X[x]);
	*(PageStart + LINE_Y[y] + (x >> 2)) = color;
}
BYTE GetPixel(int x, int y)
{	/* get pixel */
     outportb(0x3ce, 4);
     outportb(0x3cf, x & 3);
     return *(PageStart + LINE_Y[y] + (x >> 2));
}
#define SetActivePage(page)	PageStart = FirstAdr[page]
void SetVisualPage(unsigned int page)
{	/* show page */
	int P0, P1;
	P0 = (0x0C |  (page_offset[page] & 0xFF00));
	P1 = (0x0D | ((page_offset[page] & 0x00FF) << 8));
	outport(0x3D4, P0); outport(0x3d4, P1);
	while   (inp(0x3da) & 8) ;	/* Wait VSync loop */
	while (!(inp(0x3da) & 8)) ;
}
void Vline(int x0, int x1, int y, BYTE color)
{	/* vertical line */
	int i;
	for(i = x0; i <= x1; i++)
		PutPixel(i, y, color);
}
void Hline(int x, int y0, int y1, BYTE color)
{	/* horizontal line */
	int i;
	for(i = y0; i < y1; i++)
		PutPixel(x, i, color);
}
void Bar(int x0, int y0, int x1, int y1, int color)
{	/* color bar */
     int i, j;
     for(j = y0; j < y1; j++)
	     for(i = x0; i < x1; i++)
		     PutPixel(i, j, color);
}
void Rec(int x0, int y0, int x1, int y1, int color)
{	/* rectangle */
	int i;
	for(i = y0; i <= y1; i++) {
		PutPixel(x0, i, color);
		PutPixel(x1, i, color);
	}
	for(i = x0; i <= x1; i++) {
		PutPixel(i, y0, color);
		PutPixel(i, y1, color);
	}
}
void CopyPage(int pdest, int psource)
{	/* copy page psource to pdest */
	int i; char far *ptr0, far *ptr1;
	ptr0 = FirstAdr[pdest]; ptr1 = FirstAdr[psource];
	outport(0x3ce, 0x4105); outport(0x3c4, 0x0f02);
	for(i = 0;i < 21600; i++)
		*ptr0++ = *ptr1++;
	outport(0x3ce, 0x4005);
}
void CopyBlock(int x0,int y0,int x1,int y1)
{	/* copy block mem from page 2 to activepage */
	int i, j;
	char far *ptr0, far *ptr1;
	x0 >>= 2; x1 >>= 2;
	if(x0 > 90 || x1 < 0 || y1 < 0 ) return;
	if(x0 < 0)   x0 = 0;	/* check clip x0 */
	if(y0 < 0)   y0 = 0;
	if(x1 > 90)  x1 = 90;
	if(y1 > 240) y1 = 240;
	outport(0x3ce, 0x4105); outport(0x3c4, 0x0f02);
	for(j = y0; j < y1; j++) {
		ptr0 = PageStart + LINE_Y[j];
		ptr1 = FirstAdr[2] + LINE_Y[j];
		for(i = x0; i <= x1; i++)
			*(ptr0 + i) = *(ptr1 + i);
	}
	outport(0x3ce, 0x4005);
}
void PutSprite(int x0, int y0, BYTE *ptr)
{	/* put mem image sprite to activepage */
	int i, j, x1, y1;
	x1 = x0 + *ptr++; y1 = y0 + *ptr++;
	for(j = y0; j < y1; j++)
		for(i = x0; i < x1; i++, ptr++)
			if(*ptr && i >= 0 && i < 360 &&
				j >= 0 && j < 240 ) {
			outport(0x3c4, POT_X[i]);
			*(PageStart + LINE_Y[j]  + (i >> 2)) = *ptr;
		}
}
void GetSprite(int x0, int y0,  int x1, int y1,BYTE *ptr)
{	/* get mem screen to mem image sprite */
	int i, j;
	*ptr = x1 - x0;
	ptr++;
	*ptr = y1 - y0;
	ptr++;
	for(j = y0; j < y1; j++)
		for(i = x0; i < x1; i++, ptr++)
			*ptr = GetPixel(i, j);
}
#define FLIPPAGE()    {	SetVisualPage(PAGE);	\
			PAGE = 1- PAGE; 	\
			SetActivePage(PAGE); }
/* mouse function */
/*************************************************
 Initialize the mouse.
 Returns 1 if the mouse exists, 0 if it doesn't.
**************************************************/
int InitMouse(void)
{	/* set and check mouse */
	union REGS r;
	r.x.ax = 0;
	int86( 0x33, &r, &r );
	if( r.x.ax ) {	/* get mouse driver */
		r.x.ax = 7;	/* setmouse gan x */
		r.x.cx = 7;	/* left */
		r.x.dx = 316;	/* right */
		int86(0x33,&r,&r);
		r.x.ax=8;	/* set mouse gan y */
		r.x.cx = 0;	/* up */
		r.x.dx=237;	/* down */
		int86(0x33,&r,&r);
		r.x.ax = 0x1c;	/* hide mouse */
		r.x.bx = 1;
		int86( 0x33, &r, &r );
		return 1;
	}
	return 0;
}
/*********************************************
 Returns the mouse status. gan x gan y
 and its button status is returned in 'b'.
**********************************************/
void GetMouseInfo( int* x, int* y, int* b )
{
	union REGS r;
	r.x.ax = 3;
	int86( 0x33, &r, &r );
	*b = r.x.bx;
	*x = r.x.cx;
	*y = r.x.dx;
}
void CloseMouse(void)
{	/* clear mouse */
	union REGS r;
	r.x.ax = 0;
	int86( 0x33, &r, &r );
}
void MoveMouse(int x, int y)
{	/* set mouse position */
	union REGS r;
	r.x.dx = y;
	r.x.cx = x;
	r.x.ax = 4;
	int86( 0x33, &r, &r );
}
unsigned int far *Clock = (unsigned int far *) 0x046C;
void TimeDelay(unsigned int t)
{	/* time delay */
	unsigned int now;
	now = *Clock;
	while(abs(*Clock - now) < t);
}
BYTE Num[] = { /* 0 - 9 */
	14,25,21,19,14, 8,12,8,8,8, 15,16,14,1,31, 15,16,14,16,15,
	12,10,9,31,8, 15,1,15,16,15, 14,1,15,17,14, 31,16,8,4,4,
	14,17,14,17,14, 14,17,30,16,14	};
void PrintNum(int x, int y, int n, int color)
{	/* print Number at x, y position */
	int i, j, x1;
	BYTE *ptr;
	for(j = 0,ptr = Num + n * 5; j < 5; j++, y++, ptr++)
		for(i = 0, x1 = x; i < 5; i++, x1++)
			if((*ptr >> i) & 1) PutPixel(x1, y, color);
}