
/* program test VESA mode 640 x 480 x 256 x 2page
   program by 3D Engine Copyright 1996 */

#include "LIBVESA.C"
#define MAXBALL 20

int PAGE = 0;
int GX[MAXBALL], GY[MAXBALL];
int OGX[MAXBALL][2], OGY[MAXBALL][2];

int ADDX[MAXBALL], ADDY[MAXBALL];
int nBall[MAXBALL];
BYTE pal[768];
BYTE *Ball[4];
BYTE *Back[MAXBALL / 2][2];

BYTE GumBall[] = {  24, 24,
	0,  0,  0,  0,  0,  0,  0, 22, 25, 30, 36, 35,
   34, 30, 28, 25, 20,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0, 22, 35, 39, 45, 45, 44, 41,
   39, 37, 35, 32, 31, 25, 18,  0,  0,  0,  0,  0,
	0,  0,  0,  0, 28, 39, 44, 46, 46, 45, 44, 42,
   41, 39, 38, 36, 33, 28, 27, 18,  0,  0,  0,  0,
	0,  0,  0, 32, 42, 45, 48, 48, 46, 45, 44, 43,
   42, 40, 39, 38, 35, 32, 28, 25, 20,  0,  0,  0,
	0,  0, 28, 40, 45, 46, 48, 46, 46, 46, 45, 44,
   42, 41, 40, 39, 37, 34, 31, 27, 25, 18,  0,  0,
	0, 25, 36, 43, 46, 48, 46, 46, 46, 47, 46, 44,
   43, 41, 40, 40, 39, 36, 33, 29, 25, 23, 16,  0,
	0, 33, 41, 46, 48, 47, 46, 48, 53, 52, 47, 44,
   43, 42, 41, 40, 39, 36, 33, 29, 26, 23, 20,  0,
   22, 36, 46, 47, 47, 47, 46, 55, 57, 56, 48, 43,
   42, 42, 41, 41, 38, 36, 32, 29, 26, 24, 20, 16,
   25, 38, 46, 47, 47, 46, 46, 56, 59, 58, 49, 43,
   43, 42, 41, 40, 38, 36, 32, 29, 26, 25, 21, 16,
   30, 41, 44, 46, 45, 45, 47, 50, 53, 52, 47, 43,
   42, 41, 40, 39, 37, 35, 32, 29, 27, 25, 22, 17,
   33, 41, 45, 45, 44, 44, 44, 45, 48, 45, 43, 43,
   42, 41, 40, 38, 36, 34, 31, 29, 27, 25, 23, 18,
   33, 41, 45, 44, 43, 43, 42, 43, 43, 43, 43, 42,
   41, 40, 39, 37, 36, 33, 31, 29, 27, 25, 24, 19,
   30, 38, 42, 43, 41, 42, 41, 42, 41, 42, 43, 42,
   41, 40, 38, 37, 35, 33, 31, 29, 27, 25, 24, 18,
   26, 36, 41, 41, 41, 41, 40, 41, 41, 41, 42, 41,
   40, 39, 37, 36, 34, 32, 30, 28, 27, 26, 23, 18,
   23, 33, 39, 41, 40, 40, 40, 40, 41, 40, 40, 40,
   39, 37, 36, 34, 32, 30, 29, 27, 26, 25, 22, 17,
   18, 33, 36, 38, 39, 39, 39, 40, 39, 39, 38, 38,
   36, 35, 33, 32, 30, 29, 28, 27, 26, 24, 21, 15,
   16, 27, 35, 36, 38, 38, 38, 38, 38, 38, 36, 35,
   34, 33, 31, 31, 29, 29, 28, 27, 25, 23, 20, 13,
	0, 18, 30, 33, 35, 35, 36, 35, 35, 35, 34, 33,
   32, 31, 30, 29, 29, 29, 28, 27, 25, 23, 16,  0,
	0,  0, 24, 28, 31, 33, 33, 33, 32, 32, 31, 31,
   31, 30, 29, 29, 29, 29, 28, 26, 24, 18, 13,  0,
	0,  0, 16, 25, 28, 29, 30, 30, 30, 29, 29, 29,
   29, 29, 28, 29, 29, 28, 27, 24, 18, 13,  0,  0,
	0,  0,  0, 16, 24, 26, 28, 28, 28, 28, 27, 27,
   27, 28, 27, 27, 26, 26, 24, 18, 13,  0,  0,  0,
	0,  0,  0,  0, 15, 22, 24, 24, 25, 26, 26, 25,
   27, 26, 26, 25, 24, 21, 16, 13,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0, 15, 20, 22, 24, 23, 22,
   23, 23, 24, 20, 18, 14, 13,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0, 13, 14, 15, 16,
   15, 14, 14, 13, 12,  0,  0,  0,  0,  0,  0,  0
};
void Setpal(void)
{
	int i;
	BYTE *ptr;
	ptr = pal;
	for(i = 0; i < 64; i++) {
		*ptr++ = i;
		*ptr++ = 0;
        *ptr++ = 0;
	}
	for(i = 0; i < 64; i++)	{
		*ptr++ = 0;
		*ptr++ = i;
        *ptr++ = 0;
	}
	for(i = 0; i < 64; i++)	{
		*ptr++ = 0;
		*ptr++ = 0;
		*ptr++ = i;
	}
	for(i = 0; i < 64; i++)	{
		*ptr++ = i;
		*ptr++ = i;
		*ptr++ = i;
	}
	Setpalette(pal);
}

void Addcolor(BYTE *ptr,int color)
{
	int width,height,Length,i;
	width = *ptr++;
	height = *ptr++;
	Length = width * height;
	for(i=0;i<Length;i++,ptr++)
		if(*ptr != 0)
			*ptr += color;
}
void init(void)
{
	int i;

	for(i = 0; i < MAXBALL; i++) {
		nBall[i] = random(4);
		OGX[i][0] = GX[i] = 20 + random(550);
		OGX[i][1] = GX[i];
		OGY[i][0] = GY[i]= 20 + random(400);
		OGY[i][1] = GY[i];
		while((ADDX[i] = (random(4) - 2) * 2) == 0);
		while((ADDY[i] = (random(2) - 2) * 2) == 0);
	}
    while(kbhit()) getch();
}
void init1(void)
{
	int i;

	init();
	for(i = 0; i < MAXBALL / 2; i++) {
		Back[i][0] = Getmemimage(0, 0, 24, 24);
		Back[i][1] = Getmemimage(0, 0, 24, 24);
		Getimage(OGX[i][0], OGY[i][0], OGX[i][0] + 24,
				OGY[i][0] + 24, Back[i][0]);
		Getimage(OGX[i][1], OGY[i][1], OGX[i][1] + 24,
				OGY[i][1] + 24, Back[i][1]);
	}
}

void main(void)
{
	int i, j, k;
    int loop = 0;

	initvesa101();
	randomize();

	while(!kbhit()) {
		Bar(random(320), random(240),
			random(320) + 320, random(240) + 240, random(256));
		if(loop++ > 200) break;
	}
	Setpal();
	for(i = 0; i < 4; i++) {
		Ball[i] = Getmemimage(0, 0, 24, 24);
		memcpy(Ball[i], GumBall, 24 * 24 + 2);
		Addcolor(Ball[i], i * 64);
	}
	while(kbhit()) getch();
	loop = 0;
	SetActive(1);
	SetVisual(1);
	while(!kbhit()) {
		Putimage(random(620), random(460), Ball[random(4)]);
		if(loop++ > 15000) break;
	}
	loop = 0;
	init();
	SetActive(2);
	SetVisual(2);
	while(!kbhit()) {
		for(i = 0; i < MAXBALL; i++){
			GX[i] += ADDX[i];
			GY[i] += ADDY[i];
			if(GX[i] > 610 || GX[i] < 12) {
				ADDY[i] = (random(7) - 3) * 2;
				ADDX[i] = -ADDX[i];
			}
			if(GY[i] > 450 || GY[i] < 12) {
				ADDX[i] = (random(7) - 3) * 2 ;
				ADDY[i] = -ADDY[i];
			}
			if(GX[i] < 12) GX[i] = 12;
			if(GX[i] > 610) GX[i] = 610;
			if(GY[i] < 12) GY[i] = 12;
			if(GY[i] > 450) GY[i] = 450;
			OGX[i][PAGE] = GX[i];
			OGY[i][PAGE] = GY[i];
		}

		for(i = 0; i < MAXBALL; i++)
			Putimage(GX[i], GY[i], Ball[nBall[i]]);
		if(loop++ > 3000) break;
	}
	loop = 0;
	/* draw a screen two page */
	for(k = 0; k < 2; k++){
		SetActive(k);
		SetVisual(k);
		for(j = 0; j < 480; j++) {
			for(i=0;i<640;i++)
				putpix(i,j,(i*j+i*i+j*j+i*i*190) | 16);
		}
		for(i = 0; i < 12; i++)
			Rec(i, i, 639 - i, 479 - i, 40 + i * 18);
	}
	init1();
	while(!kbhit()) {
		SetVisual(PAGE);
		PAGE = 1 - PAGE;
		SetActive(PAGE);
		for(i = 0; i < MAXBALL / 2; i++){
			Putimage(OGX[i][PAGE], OGY[i][PAGE], Back[i][PAGE]);
			GX[i] += ADDX[i];
			GY[i] += ADDY[i];
			if(GX[i] > 605 || GX[i] < 12) {
				ADDY[i] = (random(4) - 2) * 4;
				ADDX[i] = -ADDX[i];
			}
			if(GY[i] > 445 || GY[i] < 12) {
				ADDX[i] = (random(4) - 2) * 4;
				ADDY[i] = -ADDY[i];
			}
			if(GX[i] < 12) GX[i] = 12;
			if(GX[i] > 605) GX[i] = 605;
			if(GY[i] < 12) GY[i] = 12;
			if(GY[i] > 445) GY[i] = 445;
			OGX[i][PAGE] = GX[i];
			OGY[i][PAGE] = GY[i];
		}
		for(i = 0; i < MAXBALL / 2; i++)
			Getimage(OGX[i][PAGE], OGY[i][PAGE],
				OGX[i][PAGE] + 24, OGY[i][PAGE] + 24, Back[i][PAGE]);
		for(i = 0; i < MAXBALL / 2; i++)
			Putimage(GX[i], GY[i], Ball[nBall[i]]);
		if(loop++ > 2000) break;
	}
	Textmode();
	for(i = 0; i < MAXBALL / 2; i++) {
		free(Back[i][0]);
		free(Back[i][1]);
	}
	for(i = 0; i < 4; i++)
		free(Ball[i]);
}