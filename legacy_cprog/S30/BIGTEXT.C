/* ---- Computer Time C Programming ---- */
/* ------- BIGTEXT.C BY 3D Engine ------ */
#include <stdio.h>
#include <conio.h>
#include <stdlib.h>
#include <string.h>
#include <dos.h>
typedef unsigned char BYTE;
char far *PageStart;
char far *FirstAdr[4];
BYTE PAGE = 0;
int LINE_Y[200], POT_X[320];
#define TextMode() { _AX = 3; geninterrupt(0x10); }
void SetModeX(void)
{
     unsigned int i;
     _AX = 0x13; geninterrupt(0x10);
     outport(0x3c4, 0x604);
     outport(0x3c4, 0xf02);
     outport(0x3d4, 0xe317);
     PageStart = MK_FP(0xa000, 0);
     for(i = 0; i < 0xffff; i++) *(PageStart + i) = 0;
     for(i = 0; i < 4; i++) FirstAdr[i] = MK_FP(0xa000 + (i << 10), 0);
     for(i = 0; i < 200; i++) LINE_Y[i] = i * 80;
     for(i = 0; i < 320; i++) POT_X[i] = (256 << (i & 3)) | 2;
     outport(0x3d4, 0x14);
}
#define SetActivePage(page)  PageStart = FirstAdr[page]
void SetVisualPage(BYTE page)
{
     outport(0x3d4, (page << 14) | 0x0c);
     while  (inp(0x3da) & 8) ; /* VSync loop */
     while(!(inp(0x3da) & 8)) ;
}
void PutPixel(int x, int y, BYTE color)
{
     if(x < 0 || x > 319 || y < 0 || y > 199) return;
     outport(0x3c4, POT_X[x]);
     *(PageStart + LINE_Y[y]  + (x >> 2)) = color;
}
void CopyPage(int pdest, int psource)
{
     register int i;
     char far *ptr0, far *ptr1;
     ptr0 = FirstAdr[pdest]; ptr1 = FirstAdr[psource];
     outport(0x3ce, 0x4105); outport(0x3c4, 0x0f02);
     for(i = 0; i < 16000; i++) *ptr0++ = *ptr1++;
     outport(0x3ce, 0x4005);
}
void Bar(int x0, int y0, int x1, int y1, int color)
{
     int i,j;
     for(j = y0; j < y1; j++)
          for(i = x0; i < x1; i++)
               PutPixel(i, j, color);
}
void PutSprite(int x0, int y0, BYTE *ptr)
{
     int i, j,  x1, y1;
     x1 = x0 + *ptr++; y1 = y0 + *ptr++;
     for(j = y0; j < y1; j++)
          for(i = x0; i < x1; i++, ptr++)
               if(*ptr && i >= 0 && i < 320 &&
                     j >= 0 && j < 200 ) {
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
          if(j > 199) return;
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
#define FLIPPAGE()  { PAGE = 1 - PAGE;  \
               SetVisualPage(1 - PAGE); \
               SetActivePage(PAGE);     \
               CopyPage(PAGE, 2); }
/* --------------------------------------- */
typedef long Fixedpoint;
#define FIXED_TO_INT(a)   (int)((a) >> 16)
#define INT_TO_FIXED(a)   ((Fixedpoint)(a) << 16)
#define FixedDiv(a, b)    (Fixedpoint)(a / ((b + 0x8000) >> 16))
typedef struct {
     Fixedpoint x, y, z, Speed;
} POINT;
typedef struct {
     int x, y;
} POINT_2D;
Fixedpoint  CheckZ;
#define MAX_STARS 150
POINT stars[MAX_STARS];
void MakePoint(int x, int y, int z, POINT *p)
{
     p->x = INT_TO_FIXED(x);
     p->y = INT_TO_FIXED(y);
     p->z = INT_TO_FIXED(z);
}
void ThreeD2TwoD(POINT *threeD, POINT_2D *twoD)
{
     twoD->x = (int)((FixedDiv(threeD->x, -threeD->z) << 8) >> 16);
     twoD->y = (int)((FixedDiv(threeD->y, -threeD->z) << 8) >> 16);
}
void InitStars(void)
{
     int i;
     /* set color stars */
     outp(0x3c8, 16);
     for(i = 1; i < 64; i++) {
          outp(0x3c9, i);
          outp(0x3c9, i);
          outp(0x3c9, i);
     }
     /* set first position stars */
     for (i = 0; i < MAX_STARS; i++) {
          MakePoint(random(20) - 10, random(20) - 10,
               random(50) - 60, &stars[i]);
          stars[i].Speed = INT_TO_FIXED(random(2) + 1);
     }
     CheckZ = INT_TO_FIXED(-4);
}
void AnimateStars(void)
{
     POINT_2D p;
     int i;
     /* move the stars forward, replacing as necessary */
     for (i = 0; i < MAX_STARS; i++) {
          stars[i].z += stars[i].Speed;
          ThreeD2TwoD(&stars[i], &p);
          if (p.x < -160 || p.x > 160 || p.y < -100 || p.y > 100 ||
               stars[i].z > CheckZ) {
               MakePoint(random(20) - 10, random(20) - 10,
                    random(10) - 65, &stars[i]);
               ThreeD2TwoD(&stars[i], &p);
          }
          PutPixel(p.x + 160, p.y + 100, FIXED_TO_INT(stars[i].z) + 81);
     }
}
/* set and put big text thai CU font file 'normal.p24' */
BYTE *CUfont, *Text;
#define SCALE 4
#define STEP  8
BYTE memfonttemp[434] = { 18, 24 };
void LoadCUfont(void)
{
     FILE *fp;
     CUfont = malloc(12096);
     fp = fopen("normal.p24", "rb");
     fread(CUfont, 12096, 1, fp);
     fclose(fp);
}
void PutChar(int x,int y, int num, int color)
{
     int i, j, k, y1;
     BYTE *ptr = CUfont + num * 54;
     for(j = 0; j < 18; j++, x++)
          for(i = 0, y1 = y; i < 3; i++, ptr++)
               for(k = 7; k >= 0; k--, y1++)
                    if((*ptr >> k) & 1)
                         PutPixel(x, y1, color);
}
void PutBigChar(int x, int y, int num, int color, int scale)
{
     int i, k, x1, y1;
     BYTE *ptr = CUfont + num * 54;
     if(x + 18 * scale < 0) return;
     for(x1 = 2; x1 < 20; x1++)
          for(i = 0, y1 = 0; i < 3; i++, ptr++)
               for(k = 7; k >= 0; k--, y1++)
                    *(memfonttemp + y1 * 18 + x1) =
                         ((*ptr >> k) & 1) ? color : 0;
     PutScale(x, y, memfonttemp, 18 * scale, 24 * scale);
}
void PutBigText(int Gx, int y, BYTE *str, int color, int scale)
{
     BYTE ch;
     while((ch = *str++) != 0 && Gx < 380) {
          if(ch < 32) Gx += 18 * scale;
          else {
               if(ch > 32 && ch < 209 || ch > 223 &&
                    ch < 231 || ch == 210 || ch > 239)
                    PutBigChar(Gx, y, ch - 32, color, scale);
               else
               if(ch > 215 && ch < 219) {
                    PutBigChar(Gx - 16 * scale, y + 20 * scale,
                         ch - 32, color, scale);
                    Gx -= scale * 16;
               }
               else
               if(ch == 211) {
                    PutBigChar(Gx - 18 * scale, y - 20 * scale, ch - 32,
                         color, scale);
                    PutBigChar(Gx, y, 178, color, scale);
               }
               else
               if(ch == 209 || ch > 211 && ch < 216) {
                    PutBigChar(Gx - 16 * scale, y - 20 * scale, ch - 32,
                         color, scale);
                    Gx -= scale * 16;
               }
               else
               if(ch > 230 && ch < 237) {
                    if(*str == 211)
                         PutBigChar(Gx - 10 * scale, y - 25 * scale, ch - 32,
                              color, scale);
                    else
                    if(*(str - 2) == 209 || *(str - 2) > 210 &&
                         *(str - 2) < 216 )
                         PutBigChar(Gx - 16 * scale, y - 29 * scale, ch - 32,
                              color, scale);
                    else
                         PutBigChar(Gx - 16 * scale, y - 20 * scale, ch - 32,
                              color, scale);
                    Gx -= scale * 16;
               }
               Gx += scale * 16;
          }
     }
}
int ReadText(void)
{
     FILE *fp;
     unsigned int length;
     fp = fopen("TEXT.TXT", "rb");
     fseek(fp, 0, SEEK_END);
     length = (unsigned int) ftell(fp);
     fseek(fp, 0, SEEK_SET);
     Text = malloc(length);
     fread(Text, length, 1, fp);
     fclose(fp);
     *(Text + length) = 0;
     return(length);
}
void main(void)
{
     int i, length, ch, len, gx = 320;
     LoadCUfont();
     len = ReadText();
     length = (160 * SCALE) - (len * 18 * SCALE );
     if (length >0 ) length = -32767;
     for(i=0 ; i < len; i++) { /* check string thai length */
          ch = Text[i];
          if(ch > 211 && ch < 219 || ch == 209 ||
               ch > 230 && ch < 237 )
               length += 18 * SCALE;
     }
     SetModeX();
     InitStars();
     while(!kbhit()) {
          FLIPPAGE();
          AnimateStars();
          PutBigText(gx, 50, Text, 14, SCALE);
          if(gx < length ) gx = 320;
          gx -= STEP;
     }
     TextMode();
}