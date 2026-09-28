/* program firework.c */
/* by 3d Engine sep '96 */
#include <stdio.h>
#include <math.h>
#include <conio.h>
#include <stdlib.h>
#include <dos.h>
#include "libvesa.c"

#define SIZE    150	/* size fire work */
#define MAXFIRE 1060	/* max pixel in one firework */
#define NUMFIRE 7	/* number of firework */
#define NUMBIG  50	/* number of big dot */

int tsin[2][360], tcos[2][360];
int X[NUMFIRE], Y[NUMFIRE], MAXY[NUMFIRE];
int GX[NUMFIRE][MAXFIRE], GY[NUMFIRE][MAXFIRE];
int DX[NUMFIRE][MAXFIRE], DY[NUMFIRE][MAXFIRE];
int GXTile[NUMFIRE], GYTile[NUMFIRE];
BYTE cout[NUMFIRE], CC[NUMFIRE], color[NUMFIRE];
BYTE TileU[NUMFIRE], SUBTile[NUMFIRE];
BYTE LTile[NUMFIRE];

BYTE Tile0[] = {   4,  8,
   58, 55, 47, 59,
   58, 45, 46, 54,
    0, 52, 46, 56,
    0, 55, 52, 58,
    0, 58, 52, 58,
    0, 60, 50, 60,
    0,  0, 55, 60,
    0,  0, 57,  0
   };
BYTE Tile1[] = {   5,  8,
   58, 55, 47, 59,  0,
   58, 45, 46, 54,  0,
    0, 52, 46, 56,  0,
    0, 55, 52, 58,  0,
    0,  0, 52, 58,  0,
    0,  0, 58, 53,  0,
    0,  0,  0, 55,  0,
    0,  0,  0,  0, 58
   };
BYTE Tile2[] = {   5,  8,
    0, 55, 47, 50, 60,
    0, 50, 46, 46, 57,
    0, 50, 46, 52,  0,
    0, 55, 46, 55,  0,
    0, 55, 52,  0,  0,
    0, 53,  0,  0,  0,
   58, 57,  0,  0,  0,
   58,  0,  0,  0,  0
   };
BYTE Boom0[] = {  11, 10,
    0,  0,  0,  0, 53,  0, 53,  0,  0,  0,  0,
    0,  0,  0, 44,164,164,  0,  0, 53,  0,  0,
    0,  0, 49,162,163,162,164,171,167, 53,  0,
   53, 49, 42,197,231,228,228,162,162, 44, 53,
   53,164,163,226,226,226,226,226,228,197,164,
    0,167,197,226,226,226,226,226,228,231,197,
   53, 49,163,228,226,226,226,228,228,197,167,
    0, 49,167,162,228,228,197,231,231,167, 53,
    0,  0,  0,163,197,195,163,164,171, 53,  0,
    0,  0,  0,  0, 53, 53,  0,  0,  0,  0,  0
   };
BYTE Boom1[] = {  17, 13,
    0,  0,  0,  0, 53, 42, 49,171,167,163,164,171,  0,  0,  0,  0,  0,
    0,  0,  0, 53, 42,163,195,195,195,231,231,162, 49,  0,  0,  0,  0,
    0,  0, 53,195,198,228,226,226,226,226,226,228,163,164,171, 53,  0,
    0,  0, 53,162,231,226,226,226,226,226,226,226,195,197,167, 42, 53,
    0, 53, 49,163,195,228,226,226,226,226,226,226,228,195,163,171, 53,
   53,167,163,162,197,228,226,226,226,226,226,226,228,231,162,167, 49,
  167,163,162,162,197,231,226,226,226,226,226,228,228,231,197,164, 44,
  167,162,162,162,197,231,226,226,226,226,228,231,231,195,197,163, 42,
    0, 53, 42,163,197,231,228,226,226,226,231,195,197,162,162,163,171,
    0,  0, 53,164,197,231,228,226,226,228,195,197,164,167,164,167, 42,
    0,  0,  0,171,163,195,231,226,226,231,195,197,171, 42, 42, 42, 49,
    0,  0,  0,  0, 53, 44,164,162,197,197,197,163, 42, 53,  0,  0,  0,
    0,  0,  0,  0,  0, 53,171,164,162,162,162,167, 53,  0,  0,  0,  0
   };
BYTE Boom2[] = {  16, 13,
    0,  0,  0,  0, 53,  0,  0,  0, 53,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0, 53, 42, 49, 53,  0,  0,  0,  0,  0,
    0,  0, 53, 44, 42,171,171,170,164,164,163,167, 42,  0,  0,  0,
    0,  0,  0, 53,171,164,167,171,171,171,167,163,167, 53,  0,  0,
    0,  0, 53, 53,164,163,171, 42, 42, 44, 44,197,162, 49, 53,  0,
    0, 53,171,163,162,162,162,197,231,195,164,162,163,171, 44, 53,
   53, 44,167,163,162,195,231,231,226,231,197,164,163,167, 42, 53,
   49, 44, 49,163,162,195,231,231,226,231,197,171, 42,167,171, 42,
   53, 49,167, 49,162,162,197,197,195,197,162,167,171, 42, 42, 42,
    0, 53,171,167,162,162,162,162,162,162,162,167,171, 49, 49, 49,
    0,  0,  0,  0, 53, 42,167,163,163,164,167, 49, 53, 53,  0,  0,
    0,  0,  0,  0,  0, 53, 49,171,167, 42, 49, 53,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0, 53, 49, 49, 53,  0,  0,  0,  0,  0,  0
   };
BYTE Boom3[] = {  12,  9,
    0,  0,  0,  0,  0,  0,  0, 53,  0,  0,  0,  0,
    0, 53, 53,  0,  0,  0, 53, 53, 49,  0,  0,  0,
    0, 53, 49, 53,  0,  0,  0, 53, 49, 53,  0,  0,
   53, 49,171, 44, 53,  0,  0,  0, 49,171, 49,  0,
   53, 44, 42, 49, 49,  0,  0, 53, 53,164,167, 53,
   53, 42,171, 44, 49, 53, 53, 49, 49,167,171, 53,
   49, 42,171,171, 44, 53, 49,171,167, 42, 44, 53,
   53, 49, 44, 44, 49, 53,171,171, 49,  0,  0,  0,
    0, 53, 53, 49, 53, 53, 49, 53,  0,  0,  0,  0
   };
BYTE Boom4[] = {  10,  8,
    0,  0,  0, 53,  0,  0,  0, 44,  0,  0,
    0,  0,  0,  0,  0,  0,  0, 53,  0,  0,
   49, 42,  0,  0,  0,  0,  0,  0, 53, 53,
   53, 42,  0,  0,  0,  0,  0,  0, 49, 42,
   53, 49,  0,  0,  0,  0,  0, 53, 44, 49,
   53, 42, 53, 53,  0,  0, 53, 53,  0,  0,
   53, 53, 53, 53,  0,  0, 53, 49,  0,  0,
    0, 53, 53,  0,  0,  0, 53, 53,  0,  0
   };

BYTE *BOOM[] = {Boom0, Boom1, Boom2, Boom3, Boom4};
BYTE *TILE[] = {Tile0, Tile1, Tile2, Tile1};
BYTE XBoom[] = {2, 1, 0, 3, 4};
BYTE YBoom[] = {3, 2, 0, 0, 1};

void PutPixel(int i, int j, int color)
{
	if(i < 640 && j < 480 && i >= 0 && j >= 0)
		putpix(i, j, color);
}

void BarClip(int x0, int y0, int x1, int y1, BYTE color)
{
	int i, j;

	for(j = y0; j < y1; j++)
		for(i = x0; i < x1; i++)
			PutPixel(i, j, color);

}
void  gensincos(void)
{
	int      i;

	for (i = 0; i < 360; i++) {
		tcos[0][i] = (int)(cos(M_PI * i / 180) * SIZE);
		tsin[0][i] = (int)(sin(M_PI * i / 180) * SIZE);
	}
        for (i = 0; i < 360; i++) {
		tcos[1][i] = (int)(tan(M_PI * i / 220) * SIZE);
		tsin[1][i] = (int)(sin(M_PI * i / 240) * SIZE);
	}
}

void Set1palette(int color, int red, int green, int blue)
{
	outp(0x3c8, color);	/* color number */
	outp(0x3c9, red);	/* red */
	outp(0x3c9, green);	/* green */
	outp(0x3c9, blue);	/* blue */
}

void setpal(void)
{
	int i;

	outp(0x3c8, 1);
	for(i = 32; i > 0; i--)	{
		outp(0x3c9, 0);
		outp(0x3c9, i * 2);
		outp(0x3c9, 0);
	}
	for(i = 32; i > 0; i--)	{
		outp(0x3c9, i * 2);
		outp(0x3c9, 0);
		outp(0x3c9, 0);
	}
	for(i = 32; i > 0; i--)	{
		outp(0x3c9, i * 2);
		outp(0x3c9, 0);
		outp(0x3c9, i * 2);
	}
	for(i = 32; i > 0; i--)	{
		outp(0x3c9, 0);
		outp(0x3c9, 0);
		outp(0x3c9, i * 2);
	}
	for(i = 32; i > 0; i--)	{
		outp(0x3c9, i * 2);
		outp(0x3c9, 0);
		outp(0x3c9, i);
	}
	for(i = 32; i > 0; i--)	{
		outp(0x3c9, i * 2);
		outp(0x3c9, i + 4);
		outp(0x3c9, 0);
	}
	for(i = 32; i > 0; i--)	{
		outp(0x3c9, i * 2);
		outp(0x3c9, i * 2);
		outp(0x3c9, 0);
	}
	for(i = 32; i > 0; i--)	{
		outp(0x3c9, i * 2);
		outp(0x3c9, i * 2);
		outp(0x3c9, i * 2);
	}
}

void putbigdot(int i, int j, int color)
{
	PutPixel(i, j, color);
	PutPixel(i + 1, j, color);
	PutPixel(i, j + 1, color);
	PutPixel(i + 1, j + 1, color);
}
void showfirepix(int Num)
{
	int i, tcolor, x, y;

	for(i = 0; i < MAXY[Num]; i++) {
		GX[Num][i] += DX[Num][i] + random(14) - 7;
		GY[Num][i] += DY[Num][i] + random(14) - 7;
		DY[Num][i] += 4;
		tcolor = (color[Num] << 5) + cout[Num] +
			 (abs(GY[Num][i] >> 8));
		x = GX[Num][i] >> 2 ;
		y = GY[Num][i] >> 2;
		if(i < NUMBIG)
			putbigdot(x, y, tcolor);
		else
			PutPixel(x, y, tcolor);
	}
}

BYTE inkey (void)
{
	_DL = 255;
	_AH = 6;
	geninterrupt(0x21);
	return(_AL);
}

void FireTileU(int j)
{
	int i, x;

	GYTile[j] -= SUBTile[j];
	if(GYTile[j] <= (GY[j][0] >> 2)){
		for(i = 0; i < 5; i++) {
			sound(i * 60);
			x = GXTile[j] - 8;
			Putimage(x + XBoom[i], GYTile[j] + YBoom[i], BOOM[i]);
/*			Set1palette(255, i, i, i + 3);*/
			delay(50);
			BarClip(x , GYTile[j], x + 18, GYTile[j] + 15, 0);
		}
		TileU[j] = 0;
/*		Set1palette(255, 1, 1, 2);*/
	}
	else {
		Putimage(GXTile[j], GYTile[j], TILE[LTile[j]]);
		if(LTile[j]++ > 2) LTile[j] = 0;
	}
	delay(10);
	nosound();
}

void init(int Num)
{
	int i, k, th, R;

	X[Num] = random(640) << 2;
	Y[Num] = random(400) << 2;
	MAXY[Num] = random(MAXFIRE >> 1) + (MAXFIRE >> 1);
        color[Num] = random(8);
	R = random(6);
	for(i = 0; i < MAXY[Num]; i++) {
		GX[Num][i] = X[Num] + random(15) - 5;
		GY[Num][i] = Y[Num] + random(15) - 5;
		k = random(20) + 1;
		th = random(360);
		if(R == 0)
		{
			DX[Num][i] = (tcos[1][th] / (random(k) + 1));
			DY[Num][i] = (tsin[0][th] / (random(k) + 1));
		}
		if (R == 2){
			DX[Num][i] = (tcos[0][th] / (random(k) + 1));
			DY[Num][i] = (tsin[1][th] / (random(k) + 1));
		}
		else {
			DX[Num][i] = (tcos[0][th] / (random(k) + 1));
			DY[Num][i] = (tsin[0][th] / (random(k) + 1));
		}
		DX[Num][i] += (random(25) - 14);
		DY[Num][i] += (random(25) - 14);

	}
	TileU[Num] = 1;
	SUBTile[Num] = random(8) + 8;
	GXTile[Num] = GX[Num][0] >> 2;
	GYTile[Num] = 480;
	LTile[Num] = 0;
}

void main(void)
{
	int i, j, x , y;

	gensincos();
	randomize();
	initvesa101();
	setpal();
	for(i = 0; i < NUMFIRE; i++){
		CC[i] = random(10) + 4;
		init(i);
	}
	do {
		for(j = 0; j < NUMFIRE; j++) {
			if(TileU[j] == 1)
				BarClip(GXTile[j], GYTile[j],
					GXTile[j] + 5, GYTile[j] + 8, 0);
			for(i = 0; i < MAXY[j]; i++) {
				x = GX[j][i] >> 2;
				y = GY[j][i] >> 2;
				if(i < NUMBIG)
					putbigdot(x, y, 0);
				else{
					if(j < 8)
						PutPixel(x, y, 0);
					else
						PutPixel(x, y, 255);
				}
			}
			if(TileU[j] == 1)
				FireTileU(j);
			else {
				if(cout[j]++ > CC[j]) {
					CC[j] = random(10) + 8;
					cout[j] = 0;
					init(j);
				}
				else
					showfirepix(j);
			}
		}
	}  while (inkey() != 27) ;
	_AX = 3;
	geninterrupt(0x10);
}
