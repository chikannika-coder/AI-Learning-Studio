/* ---- Computer Time C Programmong ---- */
/* ----- WORM.C BY 3D ENGINE ----- */
#include <stdio.h>
#include <conio.h>
#include <stdlib.h>
#include <mem.h>
#include <dos.h>
#include <time.h>
typedef unsigned char BYTE;
char far *PageStart; char far *FirstAdr[4];
BYTE PAGE = 0;
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
     outport(0x3d4, 0x14);
}
#define SetActivePage(page)PageStart = FirstAdr[page]
void SetVisualPage(BYTE page)
{
     outport(0x3d4, (page << 14) | 0x0c);
     while   (inp(0x3da) & 8) ;/* -- VSync loop -- */
     while (!(inp(0x3da) & 8)) ;
}
void PutPixel(int x, int y, BYTE color)
{
     outport(0x3c4, (256 << (x & 3)) | 2);
     *(PageStart + (y << 6) + (y << 4) + (x >> 2)) = color;
}
void CopyPage(int pdest, int psource)
{
     register int i; char far *ptr0, far *ptr1;
     ptr0 = FirstAdr[pdest]; ptr1 = FirstAdr[psource];
     outport(0x3ce, 0x4105); outport(0x3c4, 0x0f02);
     for(i = 0; i < 16000; i++) *ptr0++ = *ptr1++;
     outport(0x3ce, 0x4005);
}
void PutSprite(int x0, int y0, BYTE *ptr)
{
     int i, j, k, x1, y1;
     x1 = x0 + *ptr++; y1 = y0 + *ptr++;
     for(j = y0; j < y1; j++)
          for(i = x0, k = (j << 4) + (j << 6); i < x1; i++, ptr++)
               if(*ptr && i >= 0 && i < 320 &&
                  j >= 0 && j < 200 ) {
                    outport(0x3c4, (256 << (i & 3)) | 2);
                    *(PageStart + k + (i >> 2)) = *ptr;
               }
}
#define FLIPPAGE()  { PAGE = 1 - PAGE; \
                    SetVisualPage(1 - PAGE); \
                    SetActivePage(PAGE); \
                    CopyPage(PAGE, 2); }
/* Keyboard new interrupt number 9 handler */
struct Keyboard { /* Keyboard input structure. */
    char RightArrow,LeftArrow,UpArrow,DownArrow,Space,Esc;
} KEY;
void interrupt (*OldKeyVec)(void);
void interrupt NewKeyInt(void)
{
     BYTE ch, ScanCode;
     ScanCode = inp(0x60); ch = inp(0x61);
     outp(0x61, (ch | 0x80)); outp(0x61, ch);
     outp(0x20, 0x20);
     if(ScanCode == 77)  KEY.RightArrow = 1;
     if(ScanCode == 205) KEY.RightArrow = 0;
     if(ScanCode == 72)  KEY.UpArrow    = 1;
     if(ScanCode == 200) KEY.UpArrow    = 0;
     if(ScanCode == 75)  KEY.LeftArrow  = 1;
     if(ScanCode == 203) KEY.LeftArrow  = 0;
     if(ScanCode == 80)  KEY.DownArrow  = 1;
     if(ScanCode == 208) KEY.DownArrow  = 0;
     if(ScanCode == 57)  KEY.Space      = 1;
     if(ScanCode == 185) KEY.Space      = 0;
     if(ScanCode == 1)   KEY.Esc        = 1;
}
#define NewIntkey() { OldKeyVec = getvect(9); \
                      setvect(9, NewKeyInt); }
/* *********** init data *********** */
int GX = 153, GY = 170, EgX, EgY, Life = 4;
int END = 0, Start = 0, Score = 0;
BYTE Pal[768];
#define MaxWorms 100
#define MaxLeng  30
int NumW = 10;      /* from 1 - 100     */
int LenW = 10;      /* form 1 - 30      */
int LenW_1;         /* equ ( LenW - 1 ) */
typedef struct {
     int x, y;
} point;
typedef struct {
     int addx, addy;
     point body[MaxLeng];
} WORM;
WORM *Worm;
int Addpoint[16][2] = {
   { 0, 2}, { 2, 0}, { 2,-2}, { 2, 2},
   { 0,-2}, {-2, 0}, {-2, 2}, {-2,-2},
   { 1, 2}, { 2, 1}, {-1, 2}, { 2,-1},
   { 1,-2}, {-2, 1}, {-1,-2}, {-2,-1} };
BYTE BWorm[] = {  6, 5,
    0,11, 4, 3, 1, 0,  11, 6, 8, 5, 2, 9,
   11, 7, 6, 3, 2, 1,   9, 3, 4, 2, 3, 9,
    0, 9, 1, 1, 9, 0  };
BYTE Egg[] = {  5, 6,
    0,23,25,22, 0,  23,27,26,25,21,
   26,31,30,26,23,  26,28,29,27,24,
   24,28,27,26,22,   0,22,22,22, 0  };
BYTE CRAP0[] = {  16, 10,
    0, 0, 9,12, 0, 0, 0, 0, 0, 0, 0, 0, 0,12, 9, 0,
    0, 0,11,14,12, 0, 0, 0, 0, 0, 0,12, 0,14,11, 0,
    0, 0,12,17,14, 0, 0,10, 0,10, 0,14,11,17,12, 0,
    0, 0, 0,11,16, 0, 0,20, 0,20, 0, 0,16,11, 9, 0,
    0, 0, 0, 0,12,14, 0,10,11,10, 0,13,10, 0, 0, 0,
    0,14,12, 0,12,14,19,19,17,15,14,10, 0,10,13, 0,
   10, 0, 0,13,15,19,13,18,18,12,15,14,10, 0, 0,10,
    0, 0,14, 0,13,16,14,13,12,14,14,13, 0,14, 0, 0,
    0,13, 0,13, 0,13,14,14,13,13,12, 0,12, 0,10, 0,
    0, 0, 0,10, 0, 0, 0, 0, 0, 0, 0, 0,11, 0, 0, 0  };
BYTE CRAP1[] = {  16, 10,
    0, 9,12, 0, 0, 0, 0, 0, 0, 0, 0, 0,12, 9, 0, 0,
    0,11,14, 0,12, 0, 0, 0, 0, 0, 0,12,14,11, 0, 0,
    0,12,17,11,14, 0, 9, 0, 9, 0, 0,14,17,12, 0, 0,
    0, 0,11,16,10, 0,19, 0,19, 0, 0,16,11, 0, 0, 0,
   10,13, 0, 0,14, 0, 0,10,11, 0, 0,11, 0, 0,14,12,
    0, 0,14, 0,12,14,19,19,17,15,14,10, 0,14, 0, 0,
   13, 0, 0,12,14,19,13,18,18,12,15,14,10, 0, 0,12,
    0,14,12, 0,13,16,14,13,12,14,14,12, 0,13,12, 0,
    0, 0, 0,13, 0,13,14,13,13,12,12, 0,12, 0, 0, 0,
    0, 0,10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,12, 0, 0  };
BYTE *CRAP[] = { CRAP0, CRAP1 };
BYTE Pal32[] = { /*  for set new color  */
   20, 4, 0,  28, 8, 0,  32,12, 0,  36,16, 0,
   40,20, 0,  44,24, 0,  48,30, 0,  62,48,20,
   12, 0, 0,  24, 0, 0,  24, 4, 0,  29, 0, 0,
   34, 0, 0,  40, 0, 0,  50, 0, 0,  55, 0, 0,
   63, 0, 0,  55,10, 0,  55,20, 0,  55,38, 0,
   13,13,13,  17,17,17,  21,21,21,  27,27,27,
   31,31,31,  36,36,36,  40,40,40,  44,44,44,
   48,48,48,  53,53,53,  59,59,59  };
void SetPal32Color(void)
{
     BYTE i, *ptr = Pal32;
     outp(0x3c8, 1);
     for(i = 1; i < 32; i++) {
          outp(0x3c9, *ptr++);
          outp(0x3c9, *ptr++);
          outp(0x3c9, *ptr++);
     }
}
void CirclePal(void)
{    /* Change Color 32 - 255 */
     int i;
     BYTE Tmp[3], *ptr;
     ptr = Pal + 96;
     memcpy(Tmp, ptr, 3);
     memcpy(ptr, ptr + 3, 672);
     memcpy(ptr + 669, Tmp, 3);
     outp(0x03c8, 32);
     for(i = 32; i < 256; i++) {
         outp(0x03c9, *ptr++);
          outp(0x03c9, *ptr++);
          outp(0x03c9, *ptr++);
     }
}
void Rectangle(int x0, int y0, int x1, int y1, BYTE color)
{
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
void ScreenSetup(void)
{
     int i, j;
     for (i = 32; i < 130; i++)
          Pal[i * 3] = i % 32;
     for (i = 70; i < 180; i++)
          Pal[i * 3 + 1] = i % 32;
     for (i = 170; i < 256; i++)
          Pal[i * 3 + 2] = i % 32;
     CirclePal(); SetActivePage(2);
     for (i = 0; i < 136; i++)
          Rectangle(i, i, 319 - i, 199 - i, i + 32);
     for(j = 0; j < 8; j++) {
          for(i = 0; i < 20; i++) {
               Rectangle(i + j * 42 + 2, i + 2,
                    22 - i + j * 42, 22 - i, i * 2 + 50);
               Rectangle(i + j * 41 + 2, i + 180,
                    30 - i + j * 41, 18 - i + 180, 200 - i * 3);
          }
     }
}
void GameWorm(void)
{
     int i, j, k;
     for (i = 0; i < MaxWorms; i++) {
          k = random(16);
          Worm[i].addx = Addpoint[k][0];
          Worm[i].addy = Addpoint[k][1];
          for(j = 0; j < LenW; j++) {
               Worm[i].body[j].x = 160;
               Worm[i].body[j].y = 100;
          }
     }
     EgX = random(300) + 10; EgY = random(180) + 10;
     while (!KEY.Esc && !END) {
          FLIPPAGE();
          if(KEY.UpArrow    && GY > 6)   GY -= 8;
          if(KEY.DownArrow  && GY < 180) GY += 8;
          if(KEY.LeftArrow  && GX > 4)   GX -= 8;
          if(KEY.RightArrow && GX < 300) GX += 8;
          if(GX + 8 >= EgX - 6 && GX + 8 < EgX + 8 &&
             GY + 5 >= EgY - 4 && GY + 5 < EgY + 10 ) {
               for (k = 1; k < 25; k++) {
                    sound(k *  200); delay(50);
               }
               nosound(); Score += 10;
               k = random(NumW);
               EgX = Worm[k].body[0].x;
               EgY = Worm[k].body[0].y;
               if(NumW < 100) NumW++;
          }
          for(i = 0; i < Life; i++) /* show Life */
               PutSprite(i * 17 + 2, 2, CRAP[random(2)]);
          PutSprite(EgX, EgY, Egg);
          for (i = 0; i < NumW; k = 0, i++) {
               if(Worm[i].body[0].x < 2 || Worm[i].body[0].x > 312 ) {
                    Worm[i].addx = -Worm[i].addx;
                    k = 1;
               }
               if(Worm[i].body[0].y < 2 || Worm[i].body[0].y > 192 ) {
                    Worm[i].addy = -Worm[i].addy;
               k = 1;
          }
          if (random(random(20) + 1) == 0 && k == 0) {
               k = random(16);
               Worm[i].addx = Addpoint[k][0];
               Worm[i].addy = Addpoint[k][1];
          }
          for(j = LenW_1; j > 0; j--) {
               Worm[i].body[j].x = Worm[i].body[j - 1].x;
               Worm[i].body[j].y = Worm[i].body[j - 1].y;
          }
          Worm[i].body[0].x += Worm[i].addx;
          Worm[i].body[0].y += Worm[i].addy;
     }
     for (i = 0; i < NumW; i++) {
          for(j = LenW_1; j >= 0; j--) {
               PutSprite(Worm[i].body[j].x,
               Worm[i].body[j].y, BWorm);
                    if( Worm[i].body[j].x > GX -  4 &&
                        Worm[i].body[j].x < GX + 16 &&
                        Worm[i].body[j].y > GY -  4 &&
                        Worm[i].body[j].y < GY + 10 &&
                        Start > 30 ) {
                         for (k = 0; k < 30; k++) {
                              sound(30 * random(200) + 800);
                              delay(20);
                         }
                         nosound(); Start = 0;
                         GX = 153; GY = 170;
                         if(Life-- == 0) END = 1;
                    }
               }
          }
          if(Start > 30) PutSprite(GX, GY, CRAP[random(2)]);
          else {
               Start++;
               if(PAGE) PutSprite(GX, GY, CRAP[random(2)]);
          }
          CirclePal();
     }
}
void main(int agc,char *agv[])
{
     if(agc > 1) NumW = atoi(agv[1]);
     if(agc > 2) LenW = atoi(agv[2]);
     if(NumW > MaxWorms) NumW = MaxWorms;
     if(LenW > MaxLeng)  LenW = MaxLeng;
     Worm = (WORM *) (malloc(sizeof(WORM) * MaxWorms));
     LenW_1 = LenW - 1;
     randomize(); delay(0);
     NewIntkey();
     SetModeX();
     ScreenSetup(); SetPal32Color();
     GameWorm();
     free(Worm);
     setvect(9, OldKeyVec);
     _AX = 3; geninterrupt(0x10);
     printf("...GAME OVER...\n");
     printf("Your Score = %d Point.\n",Score);
}