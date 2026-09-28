/* --- Computer Time C Programing --- */
/* --- atom.c code by  3D Engine --- */
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
unsigned short page_offset[3];
#define TextMode() { _AX = 3; geninterrupt(0x10); }
unsigned short ModeX_360x240regs[] = {
   0x3d4,0x00,0x6b, 0x3d4,0x01,0x59, 0x3d4,0x02,0x5a,
   0x3d4,0x03,0x8e, 0x3d4,0x04,0x5e, 0x3d4,0x05,0x8a,
   0x3d4,0x06,0x0d, 0x3d4,0x07,0x3e, 0x3d4,0x08,0x00,
   0x3d4,0x09,0x41, 0x3d4,0x10,0xea, 0x3d4,0x11,0xac,
   0x3d4,0x12,0xdf, 0x3d4,0x13,0x2d, 0x3d4,0x14,0x00,
   0x3d4,0x15,0xe7, 0x3d4,0x16,0x06, 0x3d4,0x17,0xe3,
   0x3c4,0x01,0x01, 0x3c4,0x04,0x06, 0x3ce,0x05,0x40,
   0x3ce,0x06,0x05, 0x3c0,0x10,0x41, 0x3c0,0x13,0x00 };
void OutReg(unsigned short *R)
{
	unsigned short reg[3],i;
	for(i = 0;i < 24;i++) {
		reg[0] = *R++; reg[1] = *R++; reg[2] = *R++;
		if(reg[0] == 0x3c0) {
			inp(0x3da);
			outp(0x3c0, reg[1] | 0x20);
			outp(0x3c0, reg[2]);
		}
		else {
			outp(reg[0], reg[1]);
			outp(reg[0] + 1, reg[2]);
		}
	}
}
void SetModeX(void)
{
	unsigned int i;
	_AX = 0x13; geninterrupt(0x10);
	outp(0x3d4, 17);
	outp(0x3d5,(inp(0x3d5) & 127));
	outp(0x3c2,231);
	OutReg(ModeX_360x240regs);
	PageStart = MK_FP(0xa000,0);
	for(i = 0;i < 0xffff;i++) *(PageStart + i) = 0;
	for (i = 0; i < 3; i++) {
		page_offset[i] = (21600 * i);
		FirstAdr[i] = PageStart + page_offset[i];
	}
}
void PutPixel(int x, int y, BYTE color)
{
	if(x<0||x>359||y<0||y>239) return;
	outport(0x3c4, (256 << (x & 3)) | 2);
	*(PageStart + y*90 + (x >> 2)) = color;
}
#define SetActivePage(page)	PageStart = FirstAdr[page]
void SetVisualPage(unsigned int page)
{
	int P0,P1;
	P0 = (0x0C |  (page_offset[page] & 0xFF00));
	P1 = (0x0D | ((page_offset[page] & 0x00FF) << 8));
	outport(0x3D4, P0); outport(0x3d4, P1);
	while   (inportb(0x3da) & 8) ;	/* Wait VSync loop */
	while (!(inportb(0x3da) & 8)) ;
}
void CopyPage(int pdest,int psource)
{
	int i; char far *ptr0, far *ptr1;
	ptr0 = FirstAdr[pdest]; ptr1 = FirstAdr[psource];
	outport(0x3ce,0x4105); outport(0x3c4,0x0f02);
	for(i = 0;i < 21600;i++) *ptr0++ = *ptr1++;
	outport(0x3ce,0x4005);
}
BYTE pal32color[] = { /* palette data color 1 to 32 */
   63,52,52,  63,39,39,  63,26,26,  63,13,13,
   63, 0, 0,  59, 0, 0,  54, 0, 0,  50, 0, 0,
   46, 0, 0,  41, 0, 0,  37, 0, 0,  32, 0, 0,
   28, 0, 0,  24, 0, 0,  19, 0, 0,  13, 0, 0,
   63,63,60,  62,62,42,  62,62,28,  60,63, 0,
   60,60, 0,  59,56, 0,  59,52, 0,  59,48, 0,
   58,45, 0,  58,41, 0,  57,37, 0,  57,33, 0,
   51,27, 0,  45,20, 0,  39,13, 0,  33, 7, 0 };
void SetPal32Color(void)
{
	BYTE i,*ptr = pal32color;
	outp(0x3c8,1);
	for(i = 1;i < 34;i++) {
		outp(0x3c9,*ptr++);
		outp(0x3c9,*ptr++);
		outp(0x3c9,*ptr++);
	}
}
#define FLIPPAGE()    {	PAGE = 1 - PAGE;	\
			SetVisualPage(1 - PAGE);\
			SetActivePage(PAGE);	\
			CopyPage(PAGE,2); }
/* ------------- Data Bitmap BALL Image --------------- */
/* Lookup tables sin cos array */
double T_cos[360],T_sin[360];
typedef struct {	/* structure for one Ball */
	int x,y,z,Color;
} TypeBall;
#define MAXBALLS 17	/* 17 ball to 1 atom */
#define NUM_ATOM  20	/* you can change it */
TypeBall BALL[MAXBALLS],Temp[MAXBALLS];
int LBall[MAXBALLS];	/* for sort level */
int X_Angle = 0, Y_Angle = 0,Z_Angle = 0 ;
BYTE BallBitmap[] = {
   15, 15,
    0, 0, 0, 0, 0, 8, 7, 7, 7, 9, 0, 0, 0, 0, 0,
    0, 0, 0, 9, 7, 7, 6, 6, 7, 7, 7,10, 0, 0, 0,
    0, 0, 7, 6, 5, 5, 5, 6, 6, 6, 7, 8,10, 0, 0,
    0, 9, 6, 5, 2, 3, 5, 5, 6, 6, 6, 7, 8,12, 0,
    0, 7, 5, 2, 1, 2, 4, 5, 6, 6, 6, 7, 8,10, 0,
    9, 6, 5, 3, 2, 3, 4, 5, 6, 6, 6, 7, 8,10,13,
    8, 6, 5, 5, 4, 4, 5, 5, 6, 6, 6, 7, 9,10,14,
    8, 6, 6, 5, 5, 5, 5, 6, 6, 6, 6, 8, 9,11,15,
    8, 7, 6, 6, 6, 6, 6, 6, 6, 6, 7, 8,10,12,16,
    9, 7, 6, 6, 6, 6, 6, 6, 6, 7, 8, 9,11,13,16,
    0, 8, 7, 6, 6, 6, 6, 6, 7, 8, 9,10,12,14, 0,
    0,10, 8, 7, 7, 7, 7, 7, 7, 9,10,12,13,16, 0,
    0, 0,11, 8, 8, 8, 8, 8, 9,10,12,13,16, 0, 0,
    0, 0, 0,12,11,10,10,11,12,13,15,16, 0, 0, 0,
    0, 0, 0, 0, 0,13,13,14,15,16, 0, 0, 0, 0, 0  };
int postball[] = { /* x,y,z position */
    0,  0,  0,   -8,  8, -8 ,  -8, -8,  8,
    8, -8,  8,   -8,  8,  8,    8,  8,  8,
   -8, -8, -8,    8, -8, -8,    8,  8, -8,
  -14,-14, 14,   14,-14, 14,  -14, 14, 14,
   14, 14, 14,  -14,-14,-14,   14,-14,-14,
   14, 14,-14,  -14, 14,-14  };
void SetSinCosTables(void)
{
	int i;
	for(i = 0; i < 360; i++) {  /* 360 degree */
		T_cos[i] = (double)(cos((double)i *
			   M_PI / 180.0));
		T_sin[i] = (double)(sin((double)i *
			   M_PI / 180.0));
	}
}
void SetPostObj(void)
{
	int i;
	for(i = 0;i < MAXBALLS;i++) {
		BALL[i].x = postball[i * 3];
		BALL[i].y = postball[i * 3 + 1];
		BALL[i].z = postball[i * 3 + 2];
		BALL[i].Color = random(2);
		LBall[i] = i;
	}
}
void PutAtom(int x0,int y0,BYTE *ptr,int color)
{
	register int i,j,k,x1,y1;
	x1 = x0 + *ptr++; y1 = y0 + *ptr++;
	for(j = y0; j < y1; j++)
		for(i = x0,k = j * 90;i < x1;i++,ptr++)
			if(*ptr && i >= 0 && i< 360 &&
			   j >= 0 && j < 240 ) {
				outport(0x3c4, (256 << (i & 3)) | 2);
				*(PageStart + k + (i >> 2) ) =
				       *ptr + (color << 4);
			}
}
void RotateBall(int PosX,int PosY)
{
	register int i,j,dummy;
	disable();
	/* Rotations Atoms */
	for(i = 0;i < MAXBALLS;i++) {
		/*--- Rotate XYZ Axis ---*/
		Temp[i].x = (int)(BALL[i].x * T_cos[X_Angle] -
				BALL[i].z * T_sin[X_Angle]);
		Temp[i].z = (int)(BALL[i].x * T_sin[X_Angle] +
				BALL[i].z * T_cos[X_Angle]);
		Temp[i].y = (int)(BALL[i].y * T_cos[Y_Angle] +
				Temp[i].z * T_sin[Y_Angle]);
		Temp[i].z = (int)(-BALL[i].y * T_sin[Y_Angle] +
				Temp[i].z * T_cos[Y_Angle]) - 256;
		dummy = (int)(Temp[i].x * T_cos[Z_Angle] -
				Temp[i].y * T_sin[Z_Angle]);
		Temp[i].y = (int)(Temp[i].x * T_sin[Z_Angle] +
				Temp[i].y * T_cos[Z_Angle]);
		/* position x,y in 2D screen */
		Temp[i].x = (int)((dummy << 8) / Temp[i].z + PosX);
		Temp[i].y = (int)((Temp[i].y << 8) / Temp[i].z + PosY);
	}
	/* sort level atom to show */
	for(i = 0; i < MAXBALLS - 1;i++)
		for(j = i + 1; j < MAXBALLS; j++)
			if (Temp[LBall[j - 1]].z > Temp[LBall[j]].z) {
				dummy = LBall[j - 1];
				LBall[j - 1] = LBall[j];
				LBall[j] = dummy;
			}
	for(i = 0;i < MAXBALLS;i++)  /* putimage atom */
		PutAtom(Temp[LBall[i]].x,Temp[LBall[i]].y,
			BallBitmap,BALL[LBall[i]].Color);
	enable();
}
BYTE Inkey (void)
{       /* Easy key input no wait */
	_DL = 255; _AH = 6;
	geninterrupt(0x21);
	return(_AL);
}
void main(void)
{
	int GANX[NUM_ATOM],GANY[NUM_ATOM];
	int PX[NUM_ATOM],PY[NUM_ATOM];
	int i, ADDX = 8,ADDY = 8,ADDZ = 4;
	BYTE ch,PAGE = 0;
        randomize();
	SetModeX();
	SetPal32Color();
	SetSinCosTables();
	SetPostObj();
	for(i = 0;i < NUM_ATOM;i++) {
		GANX[i] = random(270) + 30;
		GANY[i] = random(170) + 30;
		PX[i] = random(6) - 3;
		PY[i] = random(6) - 3;
		if(! PX[i] && !PY[i])
			PX[i] = PY[i] = 2;
	}
	while((ch = Inkey()) != 27) {
		FLIPPAGE();
		if(ch == 'x' || ch == 'X') ADDX++;
		if(ch == 'y' || ch == 'Y') ADDY++;
		if(ch == 'z' || ch == 'Z') ADDZ++;
		if(ch == 32) /* spacebar change color atom */
			for(i = 0;i < MAXBALLS;i++)
				BALL[i].Color = random(2);
		if(ch == 'c'|| ch == 'C') /* clear */
			X_Angle = Y_Angle = Z_Angle =
			ADDX = ADDY = ADDZ = 0;
		if((X_Angle += ADDX) >= 360 ) X_Angle = 0;
		if((Y_Angle += ADDY) >= 360 ) Y_Angle = 0;
		if((Z_Angle += ADDZ) >= 360 ) Z_Angle = 0;
		for(i = 0;i < NUM_ATOM;i++) {
			RotateBall(GANX[i],GANY[i]);
			GANX[i] += PX[i]; GANY[i] += PY[i];
			if(GANX[i] <  30) PX[i] =  random(8) + 2;
			if(GANX[i] > 315) PX[i] =  random(8) - 6;
			if(GANY[i] <  30) PY[i] =  random(8) + 2;
			if(GANY[i] > 190) PY[i] =  random(8) - 6;
		}
		
	}
	TextMode();
}