/* graph.c ---- graphic mode X and keyboard routine ---- */
#include "GRAPH.H"
extern struct Keyboard { /* Keyboard input structure.*/
    char RightArrow,LeftArrow,UpArrow,DownArrow,Space,Esc;
} KEY;
extern char far *PageStart;
extern char far *FirstAdr[4];
void SetModeX(void)
{
	unsigned int i;
	_AX = 0x13; geninterrupt(0x10);
	PageStart = MK_FP(0xa000,0);
	outport(0x3c4, 0x604);
	outport(0x3c4, 0xf02);
	outport(0x3d4, 0xe317);
	for(i = 0;i < 0xffff;i++) *(PageStart + i) = 0;
	for(i = 0;i < 4;i++) FirstAdr[i] = MK_FP(0xa000 + (i << 10),0);
	outport(0x3d4, 0x14);
}
void SetVisualPage(BYTE page)
{
	outport(0x3d4, (page << 14) | 0xc);
	while (  inportb(0x3da) & 8) ;	/* Wait VSync loop */
	while (!(inportb(0x3da) & 8)) ;
}
void CopyPage(int pdest,int psource)
{
	int i;
	char far *ptr0, far *ptr1;
	ptr0 = FirstAdr[pdest];
	ptr1 = FirstAdr[psource];
	outport(0x3ce,0x4105); outport(0x3c4,0xf02);
	for(i = 0;i < 16000;i++) *ptr0++ = *ptr1++;
	outport(0x3ce,0x4005);
}
void PutPixel(int x, int y, BYTE color)
{
	outport(0x3c4, (256 << (x & 3)) | 2);
	*(PageStart + (y << 6) + (y << 4) + (x >> 2)) = color;
}
BYTE GetPixel(int x, int y)
{
	outp(0x3ce , 4); outp(0x3cf, x & 3);
	return *(PageStart + (y << 4) + (y << 6) + (x >> 2));
}
void Bar(int x0,int y0,int x1,int y1,BYTE color)
{
	int i,j;
	for(j = y0;j < y1;j++)
		for(i = x0;i < x1;i++)
			PutPixel(i,j,color);
}
void Vline(int x0,int x1,int y,BYTE color)
{
	int i;
	for(i = x0;i <= x1;i++) PutPixel(i,y,color);
}
void Hline(int x,int y0,int y1,BYTE color)
{
	int i;
	for(i = y0;i < y1;i++) PutPixel(x,i,color);
}
void Rectangle(int x0,int y0,int x1,int y1,BYTE color)
{
	Hline(x0,y0,y1,color); Hline(x1,y0,y1,color);
	Vline(x0,x1,y0,color); Vline(x0,x1,y1,color);
}
void SetNewPAL(void)
{
	int i,j,k;
	BYTE *ptr;
	BYTE NewColor[] = {    1,1,1, 7,7,7, 0,2,3, 0,2,4, 0,0,3,
			0,0,7, 3,0,4, 7,0,7, 4,0,2, 7,0,0, 2,0,0,
			0,3,1, 0,4,1, 0,7,0, 7,7,0, 7,3,0, 4,7,7 };
	outportb(0x3c8,0);
	for(j = 0,k = 1,ptr = NewColor;j < 17;j++,ptr += 3)
		for(i = 1;i < 16;i++,k++)
		{
			outportb(0x3c9, *ptr * i );
			outportb(0x3c9,*(ptr + 1) * i );
			outportb(0x3c9,*(ptr + 2) * i );
		}
}
/* Keyboard new interrupt number 9 handler */
#define RIGHT_ARROW_PRESSED	77
#define RIGHT_ARROW_RELEASED	205
#define UP_ARROW_PRESSED	72
#define UP_ARROW_RELEASED	200
#define LEFT_ARROW_PRESSED	75
#define LEFT_ARROW_RELEASED	203
#define DOWN_ARROW_PRESSED	80
#define DOWN_ARROW_RELEASED	208
#define SPACE_PRESSED		57
#define SPACE_RELEASED		185
#define ESC			1
/*** New Keyboard interrupt no 9 ***/
void interrupt (*OldKeyVec)(void);
void interrupt NewKeyInt(void)
{
	BYTE ch,ScanCode;
	ScanCode = inp(0x60); ch = inp(0x61);
	outp(0x61, (ch | 0x80)); outp(0x61, ch); outp(0x20, 0x20);
	if(ScanCode == RIGHT_ARROW_PRESSED)	KEY.RightArrow	= 1;
	if(ScanCode == RIGHT_ARROW_RELEASED)	KEY.RightArrow	= 0;
	if(ScanCode == UP_ARROW_PRESSED)	KEY.UpArrow	= 1;
	if(ScanCode == UP_ARROW_RELEASED)	KEY.UpArrow	= 0;
	if(ScanCode == LEFT_ARROW_PRESSED)	KEY.LeftArrow	= 1;
	if(ScanCode == LEFT_ARROW_RELEASED)	KEY.LeftArrow	= 0;
	if(ScanCode == DOWN_ARROW_PRESSED)	KEY.DownArrow	= 1;
	if(ScanCode == DOWN_ARROW_RELEASED)	KEY.DownArrow	= 0;
	if(ScanCode == SPACE_PRESSED)		KEY.Space	= 1;
	if(ScanCode == SPACE_RELEASED)		KEY.Space	= 0;
	if(ScanCode == ESC)			KEY.Esc		= 1;
}
void NewIntkey(void)
{
	memset(&KEY,0,sizeof(struct Keyboard));
	OldKeyVec = getvect(9); setvect(9,NewKeyInt);
}

void SetOldkey(void)
{
	setvect(9,OldKeyVec);
}