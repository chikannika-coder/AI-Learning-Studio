/* ---- C Programming ---- */
/* ----- winlogo.c ----- */
/* ---- Show Title Windows 95 ----*/
#include <stdio.h>
#include <conio.h>
#include <stdlib.h>
#include <string.h>
#include <dos.h>
typedef unsigned char BYTE;
char far *PageStart;
char far *FirstAdr[2];
unsigned short Page_Offset[2];
int LINE_Y[400], POT_X[320];
#define TextMode() { _AX = 3; geninterrupt(0x10); }
BYTE Pal[768];

void SetMode320x400(void)
{
     unsigned int i;
     _AX = 0x13; geninterrupt(0x10);
     outport(0x3c4, 0x604);
     outport(0x3c4, 0xf02);
     outport(0x3d4, 0xe317);
     outport(0x3d4, 0x4009);
     PageStart = FirstAdr[0] = MK_FP(0xa000, 0);
     FirstAdr[1] = PageStart + 32000;
     Page_Offset[0] = 0;
     Page_Offset[1] = 32000;
     for(i = 0; i < 0xffff; i++)
	  *(PageStart + i) = 0;
     for(i = 0; i < 400; i++)
	  LINE_Y[i] = i * 80;
     for(i = 0; i < 320; i++)
	  POT_X[i] = (256 << (i & 3)) | 2;
     outport(0x3d4, 0x14);
}

#define SetActivePage(page)  PageStart = FirstAdr[page]
void SetVisualPage(BYTE page)
{
     int P0,P1;
     P0 = (0x0c | (Page_Offset[page] & 0xff00));
     P1 = (0x0d | ((Page_Offset[page] & 0xff00) << 8));
     outport(0x3d4, P0);
     outport(0x3d4, P1);
     while  (inp(0x3da) & 8) ; /* VSync loop */
     while(!(inp(0x3da) & 8)) ;
}

void PutPixel(int x, int y, BYTE color)
{
     if(x < 0 || x > 319 || y < 0 || y > 399) return;
     outport(0x3c4, POT_X[x]);
     *(PageStart + LINE_Y[y]  + (x >> 2)) = color;
}

int GetPixel(int x,int y)
{
     outp(0x3ce, 4);
     outp(0x3cf, x & 3);
     return *(PageStart + LINE_Y[y] + (x >> 2));
}

void GetSprite(int x0, int y0, int x1, int y1, BYTE *ptr)
{
     int i, j;
     *ptr = x1 - x0;
     ptr++;
     *ptr = y1 - y0;
     ptr++;
     for(j = y0; j < y1; j++)
	  for(i = x0; i < x1; i++, ptr++)
	       *ptr = GetPixel(i, j);
}

void CopyPage(int pdest, int psource)
{
     register int i;
     char far *ptr0, far *ptr1;
     ptr0 = FirstAdr[pdest];
     ptr1 = FirstAdr[psource];
     outport(0x3ce, 0x4105);
     outport(0x3c4, 0x0f02);
     for(i = 0; i < 32000; i++)
	*ptr0++ = *ptr1++;
     outport(0x3ce, 0x4005);
}

void Bar(int x0, int y0, int x1, int y1, int color)
{
     int i, j;
     for(j = y0; j <= y1; j++)
	for(i = x0; i <= x1; i++)
	    PutPixel(i, j, color);
}

void PutSprite(int x0, int y0, BYTE *ptr)
{
     int i, j,  x1, y1;

     x1 = x0 + *ptr++; y1 = y0 + *ptr++;
     for(j = y0; j < y1; j++)
	  for(i = x0; i < x1; i++, ptr++)
	       if(*ptr && i >= 0 && i < 320 &&
     j >= 0 && j < 400 ) {
		    outport(0x3c4, POT_X[i]);
		    *(PageStart + LINE_Y[j]  + (i >> 2)) = *ptr;
	       }
}

void PutBlock(int x0, int y0, BYTE *ptr)
{
     int i, j,  x1, y1;

     x1 = x0 + *ptr++; y1 = y0 + *ptr++;
     for(j = y0; j < y1; j++)
	  for(i = x0; i < x1; i++, ptr++)
       if(i >= 0 && i < 320 &&
     j >= 0 && j < 400 ) {
		    outport(0x3c4, POT_X[i]);
		    *(PageStart + LINE_Y[j]  + (i >> 2)) = *ptr;
	       }
}

void PutScale(int x, int y, BYTE *bitmap, int sx, int sy)
{
     int height, width;
     int htemp, i, j, x1, y1;
     BYTE ch, *ptr;

     if(sx <= 0 || sy <= 0) return;
     x1 = x + sx; y1 = y + sy;
     ptr = bitmap;
     width = *ptr++; height = *ptr++;
     for ( j = y; j < y1; j++ ) {
     if(j > 399) return;
	  htemp = height * (j - y) / sy * width;
	  for ( i = x; i < x1; i++ ) {
	       ch  = *(ptr + ( width * (i - x) / sx) + htemp);
	       if(ch && i >= 0 && i < 320 && j >= 0) {
		    outport(0x3c4, POT_X[i]);
		    *(PageStart + LINE_Y[j]  + (i >> 2)) = ch;
	       }
	  }
     }
}
void Setpal(void)
{
     int i;
     outp(0x3c8, 0);
     for(i = 0; i < 768; i++)
	  outp(0x3c9, Pal[i]);
}

int LoadBMP(char *name)
{
     FILE *fp;
     int i, j;
     BYTE *ptr;
     unsigned int Length, Index, psi;
     BYTE palette[1024];
     BYTE *buf0, *buf1;

     Length = 320 * 200;
     fp = fopen(name,"rb");
     if(fp == NULL)
	  return 0;
     fseek(fp, 54, 0); /* seek header */
     fread(palette, 1024, 1, fp);
     /* set palette */
     ptr = Pal;
     for(psi = 0, i = 0; i <= 255; i++, psi += 4) {
	  *ptr++ = palette[psi + 2] >> 2;
	  *ptr++ = palette[psi + 1] >> 2;
	  *ptr++ = palette[psi] >> 2;
     }
     Setpal();
     buf0 = malloc(Length);
     buf1 = malloc(Length);
     fread(buf1, Length, 1, fp);
     fread(buf0, Length, 1, fp);
     fclose(fp);

     Index = Length;
     for(j = 0; j < 200; j++){
	  Index -= 320;
	  for(i = 0; i < 320; i++){
	       outport(0x3c4, POT_X[i]);
	       *(PageStart + LINE_Y[j]  + (i >> 2)) =
		    buf0[Index + i];
	  }
     }
     Index = Length;
     for(j = 200; j < 400; j++) {
	  Index -= 320;
	  for(i = 0; i < 320; i++) {
	       outport(0x3c4, POT_X[i]);
	       *(PageStart + LINE_Y[j]  + (i >> 2)) =
		    buf1[Index + i];
	  }
     }
     free(buf0);
    free(buf1);
     return 1;
}

void Rec(int x0, int y0, int x1, int y1, int color)
{
     int i;
     for(i=x0;i<=x1;i++){
	  PutPixel(i, y0, color);
	  PutPixel(i, y1, color);
     }
     for(i=y0;i<=y1;i++) {
	  PutPixel(x0, i, color);
	  PutPixel(x1, i, color);
     }
}

void interrupt(*oldTime)(void);
void interrupt LoopColor(void)
{
     /* Loop color 236 - 255 */
     BYTE color[3];
     int i;

     color[0] = Pal[708];
     color[1] = Pal[709];
     color[2] = Pal[710];
     memcpy(&Pal[708], &Pal[711], 60);
     Pal[765] = color[0];
     Pal[766] = color[1];
     Pal[767] = color[2];
     outp(0x3c8, 236);
     for(i = 0; i < 60; i++)
	  outp(0x3c9, Pal[i + 708]);
}

void InitLoopColor(void)
{
     oldTime = getvect(0x1c);
     setvect(0x1c, LoopColor);
}

void RestoreTime(void)
{
     setvect(0x1c, oldTime);
}

BYTE CBall[] = { 12, 20,
     0 , 0 , 0 , 0 , 4 , 5 , 5 , 4 , 0 , 0 , 0 , 0 ,
     0 , 0 , 0 , 5 , 10, 12, 11, 8 , 5 , 0 , 0 , 0 ,
     0 , 0 , 6 , 13, 13, 13, 13, 12, 8 , 5 , 0 , 0 ,
     0 , 4 , 13, 14, 14, 13, 12, 12, 12, 8 , 4 , 0 ,
     0 , 9 , 14, 17, 17, 14, 12, 11, 11, 10, 5 , 0 ,
     4 , 13, 17, 23, 22, 17, 12, 10, 10, 10, 7 , 3 ,
     5 , 14, 21, 27, 26, 20, 13, 10, 10, 10, 8 , 4 ,
     8 , 15, 24, 31, 29, 22, 13, 10, 9 , 9 , 8 , 6 ,
     10, 16, 23, 30, 28, 19, 12, 10, 9 , 9 , 8 , 6 ,
     11, 15, 20, 25, 24, 16, 11, 9 , 8 , 8 , 8 , 6 ,
     10, 15, 17, 19, 18, 14, 11, 9 , 8 , 7 , 7 , 6 ,
     9 , 14, 15, 16, 14, 12, 11, 9 , 8 , 7 , 7 , 6 ,
     7 , 13, 14, 13, 13, 12, 11, 10, 8 , 7 , 8 , 5 ,
     6 , 12, 13, 12, 12, 11, 11, 9 , 8 , 8 , 8 , 3 ,
     3 , 10, 12, 12, 11, 10, 10, 8 , 8 , 8 , 6 , 3 ,
     0 , 7 , 11, 11, 10, 9 , 8 , 8 , 8 , 8 , 5 , 0 ,
     0 , 4 , 10, 10, 10, 8 , 7 , 8 , 8 , 7 , 4 , 0 ,
     0 , 0 , 5 , 8 , 8 , 8 , 7 , 7 , 7 , 5 , 0 , 0 ,
     0 , 0 , 0 , 5 , 7 , 8 , 8 , 7 , 5 , 0 , 0 , 0 ,
     0 , 0 , 0 , 0 , 4 , 4 , 5 , 4 , 0 , 0 , 0 , 0 };

void SetPal1(void)
{
     int i;
     outp(0x3c8, 0);
     for(i = 0; i < 32; i++) {
	  outp(0x3c9, i * 2);
	  outp(0x3c9, i * 2);
	  outp(0x3c9, i * 2);
     }
     for(i = 0; i < 32; i++) {
	  outp(0x3c9, i * 2);
	  outp(0x3c9, 0);
	  outp(0x3c9, 0);
     }
     for(i = 0; i < 32; i++) {
	  outp(0x3c9, 0);
	  outp(0x3c9, i * 2);
	  outp(0x3c9, 0);
     }
     for(i = 0; i < 32; i++) {
	  outp(0x3c9, 0);
	  outp(0x3c9, 0);
	  outp(0x3c9, i * 2);
     }
     for(i = 0; i < 32; i++) {
	  outp(0x3c9, i * 2);
	  outp(0x3c9, i * 2);
	  outp(0x3c9, 0);
     }
     for(i = 0; i < 32; i++) {
	  outp(0x3c9, i * 2);
	  outp(0x3c9, 0);
	  outp(0x3c9, i * 2);
     }
     for(i = 0; i < 32; i++) {
	  outp(0x3c9, 0);
	  outp(0x3c9, i * 2);
	  outp(0x3c9, i * 2);
     }
}

void AddColor(BYTE *ptr, int color)
{
     int w, h, L , i;
     w = *ptr++;
     h = *ptr++;
     L = w * h;
     for(i = 0; i < L; i++)
	  if(*ptr++)
	       *ptr += color;
}

BYTE *BALL[7];

void Init(void)
{
     int i;
     for(i = 0; i < 7; i++) {
	  BALL[i] = malloc(12 * 20 + 2);
	  memcpy(BALL[i], CBall, 12 * 20 + 2);
	  AddColor(BALL[i], i * 32);
     }
}

void main(void)
{
     int i, j;

     BYTE *Image;
     SetMode320x400();
     SetVisualPage(1);
     if(!LoadBMP("LOGO.SYS")){
	  TextMode();
	  printf("File Not Found\n");
	  exit(0);
     }
     SetVisualPage(0);
     InitLoopColor();
     SetActivePage(1);
     CopyPage(1, 0);
     Bar(0, 0, 319, 389, 0);
     Init();

     for(j = 0; j < 17; j++)
	  for(i = 0; i < 24; i++)
	       PutSprite(i * 14, j * 23, BALL[random(7)]);
     getch();
     SetVisualPage(1);
     SetPal1();
     while(kbhit()) getch();
     while(!kbhit())
	  PutSprite(random(24) * 14, random(17) * 23, BALL[random(7)]);
     getch();
     while(kbhit()) getch();
     Setpal();
     SetVisualPage(0);
     getch();
     RestoreTime();
     TextMode();
     for(i = 0; i < 7; i++)
	  free(BALL[i]);
}
