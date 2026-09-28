/* program bomber.c code by 3D Engine */
#include <string.h>
#include "libgraph.c"
/* Keyboard new interrupt number 9 handler */
struct Keyboard { /* Keyboard input structure. */
    char RightArrow, LeftArrow, UpArrow, DownArrow, Space, Esc;
} KEY;
void interrupt (*OldKeyVec)(void);
void interrupt NewKeyInt(void)
{
     BYTE ch, ScanCode;
     ScanCode = inp(0x60); ch = inp(0x61);
     outp(0x61, (ch | 0x80)); outp(0x61, ch); outp(0x20, 0x20);
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
#define NewIntkey() { OldKeyVec = getvect(9); setvect(9, NewKeyInt); }
#define SetOldkey() setvect(9, OldKeyVec)
BYTE Bitmap0[] = {  7, 15,
   0,  0, 17, 34, 33, 32,  0,   0,  1,135,215,120, 33,  0,
   0, 39,221,221,221,120, 16,   0, 39, 42,187,171, 40, 16,
   0, 40,177,187, 27,184, 16,   0, 24, 43,187,187, 40, 16,
   0,  2,141,221,215,130,  0,   0, 39, 51, 51, 51, 39, 32,
   1,120, 69, 85, 84, 72,129,   1, 33, 51,200, 35, 49, 33,
   1,225, 69, 85, 86,130,226,   0, 17,120, 17, 39,129, 17,
   0,  1,255, 17, 47,241,  0,   1, 17, 34, 17, 18, 17, 16,
   0, 17, 17, 17, 17, 17,  0 };
BYTE Bitmap1[] = {  7, 15,
   0,  1, 34, 34, 17,  0,  0,   0, 24,119,221,215, 17,  0,
   1,141,221,221,221,143, 16,   1,219,171,186,178,113,  0,
   1,219, 27,177,184,209,  0,   1,139,187,187,178,113,  0,
   0, 23,221,221,119, 18, 16,   1, 34, 35, 51, 51, 39,113,
  24, 47,147, 85, 84, 40,146,  24,130, 34,200, 51, 25,242,
  17, 34, 69, 84, 68, 48, 16,   0, 24,120, 18,119, 16,  0,
   0, 17, 34, 18,136, 33,  0,   1, 17, 17, 18,255, 33, 16,
   0, 17, 17, 17, 17, 17,  0 };
BYTE Bitmap2[] = {  7, 15,
   2,  0, 17, 34, 34, 16,  0,  31,145,135,125,120,129,  0,
   1, 23,221,221,215,120, 16,   0, 39,221,114,186,186, 16,
   0, 24,221,139,177,186, 32,   0, 18,221,130,187,186, 16,
   0,  1, 23, 34, 40,136, 16,   0,  1, 49,135, 35, 49,  0,
   0,  1, 52,119, 36, 81,  0,   0,  1, 49, 41, 34,140,  0,
   0,  1, 49,159, 36, 48,  0,   0,  0, 24,119,114, 16,  0,
   0, 17, 17,159,249, 17, 16,   1, 17, 17, 18, 33, 17, 16,
   0, 17, 17, 17, 17, 17,  0 };
BYTE Bitmap3[] = {  7, 15,
   2,  1, 18, 34, 18,  0,  0,  31, 40,119,221,120, 32,  0,
  17,135,215,119,120,129,  0,   1,125,114,187,171,161,  0,
   1,141,139,187, 27, 18,  0,   1,135,130,187,187,161,  0,
   0, 24,120, 34,136, 33,  0,   0, 33, 49, 39, 41,242,  0,
   2,130, 83, 40,215,145,  0,   2,145, 51, 49, 33, 32,  0,
   2, 18, 69, 84, 69,130, 16,   0, 40,215, 35, 40,114,145,
   1,146,114, 17, 17,153, 33,   1, 31,145, 17, 17, 17, 16,
   0, 17, 17, 17, 17, 17,  0 };
BYTE Bitmap4[] = {  7, 15,
   1,  0, 17, 34, 17,  0,  0,  25, 17,119,221,120, 32,  0,
   1, 40,221,221,215,130,  0,   0, 23,221,221, 43,170,  0,
   0, 23,221,216,187, 26,  0,   0, 40,125,216, 43,170,  0,
   0, 18,136,135,136,145, 16,   0,  1, 35,136, 49, 18,241,
   0, 25, 39,137, 85, 50,129,   0, 25,146, 51, 49, 17, 16,
   0,  2, 36, 69,102, 49,  0,   0, 25, 34, 34,119,130, 16,
   0, 25, 40, 33, 40,159, 32,   1, 17, 17, 17, 17, 34, 16,
   0, 17, 17, 17, 17, 17,  0 };
BYTE Bitmap5[] = {    7, 15,
   0,  0, 17, 18, 33, 16,  0,   0,  2,135, 47,146,129,  0,
   0, 23,221,210, 39,120, 16,   0, 29,221,221,221,119, 16,
   0, 29,221,221,221,119, 16,   0, 23,221,221,221,120, 16,
   0,  8,119,119,119,130,  0,   0, 39, 51, 51, 51, 23, 32,
   1,114, 69, 85, 86, 72,113,  24,129, 35, 51, 51, 18,130,
  25,242, 69, 85, 85, 66,242,   1, 18,120, 33, 39,129, 17,
   0, 18,249, 33, 47,145, 16,   1, 17, 34, 17, 18, 33, 17,
   0, 17, 17, 17, 17, 17, 16 };
BYTE Bitmap6[] = {  7, 15,
   0,  1, 34, 33, 17,  0,  0,   0, 24,125,210,249, 16,  0,
   2,125,221,221,136, 33,  0,   2,221,221,221,221,129,  0,
   2,221,221,221,221,129,  0,   2,221,221,221,215,129,  0,
   2, 23,119,119,120, 33,  0,  18,131, 51, 51, 50,120, 33,
  40,132, 85, 86, 67,136,145,  40, 51, 51, 51, 51, 25,241,
  18, 36, 85, 84,104, 16, 16,   1,141,113, 39,215, 16,  0,
   1, 40,129, 18,130, 16,  0,  17,159,145, 17, 17, 17,  0,
   1, 17, 17, 17, 17, 16,  0 };
BYTE Bitmap7[] = {  6, 11,
 139,188,222,254,220,184, 188,204,222,254,204,187,
 204,206,239,255,221,204, 220,221,239,255,238,220,
 255,255,255,255,255,221, 255,255,255,255,255,255,
 221,255,255,255,255,238, 205,237,239,255,223,204,
 204,220,239,255,253, 92, 187,205,239,254,221,203,
 139,204,223,254,204,184 };
BYTE Bitmap8[] = {  6, 11,
   0,  0, 24,152,144,  0,   0,  0,155,203,168,  0,
   0,  9,188,236,184,  0,   0, 26,205,238,201, 16,
   8,154,205,253,202, 16,   0,155,206,254,187,144,
   0,156,205,254,203,137,   1,155,206,253,203,144,
   1,155,222,254,203,128,   0,140,206,253,203,144,
   1,155,207,255,203,153 };
BYTE Bitmap9[] = {  6, 11,
  25,188,223,236,185,128,   8,188,223,220,185, 16,
  25,188,255,236,201, 16,  25,188,223,236,184,128,
   8,187,223,236,184, 16,  24,172,223,220,184,129,
   1,155,222,220,168,  0,   1,155,206,236,145,  0,
   0,139,205,205,144,  0,   0,136,187,171,144,  0,
   0, 16,152, 25, 16,  0 };
BYTE Bitmap10[] = {  6, 11,
   0,  1, 16,  1, 25,137,   0,129,153,153,153,153,
 129,154,188,188,203,169, 154,188,204,204,204,204,
  25,204,204,221,255,223, 170,204,221,255,255,255,
 154,188,206,237,220,236,  25,188,204,204,204,199,
 153,153,187,188,188,185,   0, 17,153,137,153,153,
   0,  0,  1,  0,  1,145 };
BYTE Bitmap11[] = {  6, 11,
   0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  3, 16,
   0,  1, 17, 34, 66,  0,   1, 17, 18,243, 48,  0,
  17, 51, 19, 67, 33,  0,  20,255, 17, 34, 17, 16,
  47,242, 17, 17, 17, 16,  36, 33, 17, 17, 17, 16,
  17, 17, 17, 17, 17, 16,   1, 17, 17, 17, 17,  0,
   0, 17, 17, 17, 16,  0 };
BYTE Bitmap12[] = {  6, 11,
   0,  1, 17, 18,  4, 58,   1, 17, 17, 52, 50,250,
  17, 68, 35, 68, 47, 32,  19,255, 50, 68, 49, 19,
  31,243, 17, 35, 50, 18,  31, 49, 17, 18, 17, 17,
  19, 33, 17, 17, 17, 17,  17, 17, 17, 17, 17, 17,
  17, 17, 17, 17, 17, 16,   1, 17, 17, 17, 17,  0,
   0,  1, 17, 17, 18,  0 };
BYTE Bitmap13[] = {  7, 13,
   0,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0,  0,  0,
   0,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0,  0,  0,
   1, 17,  0,  0,  0, 17, 16,  19,204, 17, 17, 17,204, 17,
  28, 19,200,136,124, 19,193,  19,204, 58,187,163,204, 17,
  18, 53,170,187,168, 50, 19,  24,138, 17, 17, 17,168,113,
   2, 51,170,187,170, 51, 16,   0, 17, 19, 51, 49, 17,  0,
   0,  1, 17, 17, 17, 16,  0 };
BYTE Bitmap14[] = {   7, 13,
   0,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0,  0,  0,
   1, 17,  0,  0,  0, 17,  0,  19,195, 17, 17, 17,195, 16,
  28, 28, 56,136, 44, 28, 48,  19,195,171,187,162,195, 16,
  50, 58,177, 17,186, 51, 16,  24,171, 31,207, 59,168, 48,
  24,171, 31,239, 27,168, 16,  18, 91,177, 17,171, 82, 16,
  18, 51,170,170,170, 51, 16,   1, 17, 19, 51, 49, 17,  0,
   0,  1, 17, 17, 17,  0,  0 };
BYTE Bitmap15[] = {  7, 13,
   1,193,  3, 51,  1,193,  0,  28, 28, 56,136, 44, 28, 16,
  28, 28, 74,170,108, 60, 16,   1,194,165, 21,162,193,  0,
  18,138,177,193,171,130, 16,   3,139,177,239,171,131,  0,
  18,139,177,239,171,130, 16,   3,139,177,209,171,131,  0,
  18, 91,177,193,171, 82, 16,  24,154,165, 21,170,162, 16,
  18, 51,170,170,163, 50, 16,   1, 17, 19, 51, 17, 17,  0,
   0, 17, 17, 17, 17, 16,  0 };
BYTE Bitmap16[] = {   6, 12,
  85, 85, 85, 85, 85, 85,  84, 85, 85, 85, 85, 84,
  85, 84, 85, 85, 84, 85,  85, 85, 85, 85, 85, 85,
  85, 85, 85, 85, 85, 85,  85, 85, 84, 85, 85, 69,
  85, 85, 85, 85, 85, 85,  84, 85, 85, 85, 85, 85,
  85, 85, 85, 85, 84, 85,  85, 85, 69, 85, 85, 85,
  85, 69, 85, 69, 85, 69,  85, 85, 85, 84, 85, 85 };
BYTE Bitmap17[] = {   6, 12,
 153,170,169,170,170,153, 170,153,156,153,156,217,
 153,153,156,153,156,220, 154,204,204,204,204,216,
 169,156,153,156,156,220, 170,204,204,204,204,220,
 154,153,156,153,156,221, 154,153,156,153,156,220,
 169,204,220,204,204,220, 156,221,221,221,205,221,
 156,205,204,204,220,205,  84, 34, 50, 50, 35, 34 };
BYTE Bitmap18[] = {  6, 12,
 255,255,255,255,255,240, 254,119,119,119,119,246,
 254,126,238,238,238,246, 254,126,255,255,255,246,
 254,126,255,255,255,246, 255,255,255,255,255,246,
 254,238,238,238,238,230, 119,119,119,119,119,118,
 118,102,102,102,102,230, 118,119,119,119,119,118,
 119,119,119,119,119,118,  66, 50, 50, 50, 35, 34 };
BYTE Bitmap19[] = {  15,  6,  /* Score */
  15,255,243, 15, 15, 15,  0,240,243,  0,240,243,  0,240,  0,
 241, 17, 31, 19,241, 31, 16,241, 15, 16,241, 15, 16,241,  0,
 161,168, 10, 16, 17, 10, 16,161, 10, 16,161, 10, 16,161,  0,
 170, 26, 26, 26, 10, 10, 16,161, 10,170,170, 10,170,170,  0,
 145, 17, 25, 24,145, 24,145,137, 25, 17,153, 25, 17,153, 16,
  17,  0,  1, 16, 17,  1, 17, 17, 17, 16,  1, 17, 16,  1, 16
 };
BYTE palette[]={
   6, 6, 6, 17,17,17,  0,20,28,  0,20,52,  0,44,59,
  27,52,60, 48,48,48, 36,36,36, 36,12,28, 35,20, 0,
  58,29, 0, 43,18,20, 60,60,60, 60,28,60, 60, 0,44,
  12,12,12,  6, 6, 6,  0,20, 0, 12,28, 0,  0,38, 0,
  20,20,20, 28,28,28, 36,20,20, 44,20, 0, 56,28, 0,
  63, 0, 0, 28,12, 0, 24, 0, 0, 44,44,44, 52,52,52,
   3, 3, 3, 28,12,12, 33,20,20, 28,28,28, 44,28,12,
  36,28, 0, 36,12, 0, 52,20, 0, 60,36, 0, 52,44,12,
  63,63, 0, 63,63,63, 60,44, 0, 63, 0, 0, 34, 0, 0,
   6, 6, 6, 12,12,12, 25,25,25, 40,40,40, 60,44,28,
  57,33,20, 40,28, 0, 28,12, 0, 44, 0, 0, 63, 0, 0,
  60,20, 0, 60,48, 0, 60,60,20, 60,60,40, 63,63,63
  };
BYTE *BitImage[30];
void SetPal(void)
{
     int i;
     BYTE *ptr = palette;
     outp(0x3c8, 1);
     for(i = 0; i < 75; i++) {
          outp(0x3c9, *ptr++); 
          outp(0x3c9, *ptr++); 
          outp(0x3c9, *ptr++);
     }
}
void PackBitmap(BYTE *ptr1)
{
     static int k;
     int i, j ;
     BYTE memtmp[1024];
     BYTE width, height, *ptr;
     ptr = memtmp;
     width = *ptr1++; height = *ptr1++;
     *ptr++ = width >> 1; *ptr++ = height;
     for(j = 0;j < height; j++)
          for(i = 0; i < width; i += 2, ptr1 += 2){
               *ptr++ = (*ptr1 << 4) | (*(ptr1+1));
          }
     ptr = memtmp;
     width = *ptr++; height = *ptr++;
     printf("BYTE Bitmap%d[] = { %3d,%3d,\n", k++, width, height);
     for(j = 0; j < height; j++) {
          for(i = 0; i < width; i ++) {
               printf("%3d", *ptr++);
               if((i == width - 1) && (j == height - 1));
               else printf(",");
          }
          printf(" ");
          if((j & 1) == 1) printf("\n");
     }
     printf(" };\n");
}
void UnpackBitmap(BYTE *ptr, int num, int Add)
{
     int i, j;
     BYTE width, height, *ptr1;
     width = *ptr++;
     height = *ptr++;
     BitImage[num] = malloc((width << 1) * height + 2);
     ptr1 = BitImage[num];
     *ptr1++ = width << 1 ;
     *ptr1++ = height;
     for(j = 0; j < height; j++){
          for(i = 0; i < width; i ++, ptr1 += 2, ptr++) {
               *ptr1 = ((*ptr >> 4) & 0x0f);
               *(ptr1 + 1) = (*ptr & 0x0f);
               if(*ptr1 > 0) *ptr1 += Add;
               if(*(ptr1 + 1) > 0) *(ptr1 + 1) += Add;
          }
     }
}
void FlipBitmap(int num0, int num1)
{
     int i, j;
     int width, height;
     BYTE *ptr, *ptr1;
     ptr = BitImage[num0];
     width = *ptr++; height = *ptr++;
     BitImage[num1] = malloc(width * height + 2);
     ptr1 = BitImage[num1];
     *ptr1++ = width; *ptr1++ = height;
     for(j = 0; j < height; j++)
          for(i = width - 1 ; i >= 0; i--)
               *(ptr1 + j * width + i)  = *ptr++;
}
#define MAXGOST  50
#define MAXBOOM  9
char Map[25][19], Skip[49];
int MAXGOST1 = 10, MAXBOOM1 = 2; /* set first gost & boom */
int GX, GY, GUX, GUY, BCh[MAXBOOM][4], Level = 1;
int oGanx[2], oGany[2], MxFire = 2, BoomMan = 5;
int Gxgost[MAXGOST], Gygost[MAXGOST], Cgost[MAXGOST];
int ArGostx[MAXGOST], ArGosty[MAXGOST], HaveGost[MAXGOST];
int oGxgost[MAXGOST][2], oGygost[MAXGOST][2];
int CheckGost[MAXGOST], Gran[MAXGOST];
int Gloop[] = {23, 24, 25, 24, 23};
int addmove[4][2] = { 0,-2,  -2,0, 0,2, 2,0 };
int cmove[4][2] = { 0,-1, -1,0, 0,1, 1,0 };
int NBoom[MAXBOOM], GxBoom[MAXBOOM], GyBoom[MAXBOOM];
int TimeBoom[MAXBOOM], TimeBoom1[MAXBOOM];
int TimeMan, End = 0, SCORE = 100, NGost = 0, Gmove = 0;
void PrintScore(void)
{
     char str[10];
     int i, j;
     itoa(SCORE, str, 10);
     SetActivePage(2);
     Bar(315, 17, 355, 28, 9);
     i = 0; j = 346 - 6 * strlen(str);
     do {
          PrintNum(i * 6 + j + 1, 21, str[i] - '0', 0);
          PrintNum(i * 6 + j, 20, str[i] - '0', 5);
     } while(str[++i]);
     PrintNum(i * 6 + j + 1, 21, 0, 0);
     PrintNum(i * 6 + j, 20, 0 , 5);
     SetActivePage(1 - PAGE);
     CopyBlock(314, 16, 355, 28);
     SetActivePage(PAGE);
     CopyBlock(315, 17, 355, 28);
}
void PrintBoomMan(void)
{
     SetActivePage(2);
     Bar(337, 221, 351, 233, 24);
     PrintNum(342, 225, BoomMan, 0);
     PrintNum(341, 224, BoomMan, 13);
     SetActivePage(1 - PAGE);
     CopyBlock(337, 221, 351, 233);
     SetActivePage(PAGE);
     CopyBlock(337, 221, 351, 233);
     if(--BoomMan < 0) End = 1;
}
int Checkblock(int x, int y)
{
     int i, j;
     i = (x - 5) / 12; j = (y - 3) / 12;
     if(Map[i][j]) return(0);
     else return(1);
}
void MoveSkipX(void)
{
     if(Skip[GUX] == 1) {
          GX -= 6; GUX --;
     }
     if(Skip[GUX] == 3) {
          GX += 6; GUX ++;
     }
}
void MoveSkipY(void)
{
     if(Skip[GUY] == 1) {
          GY -= 6; GUY --;
     }
     if(Skip[GUY] == 3) {
          GY += 6; GUY ++;
     }
}
int CMapBlock(int i)
{
     if( Map[ArGostx[i] + cmove[Gran[i]][0]]
            [ArGosty[i] + cmove[Gran[i]][1]] > 0) return(1);
     else return(0);
}
void MoveGost(void)
{
     int i, j, k, Addx, Addy;
     for(i = 0; i < MAXGOST1; i++) {/* clear */
          if(HaveGost[i] > 0){
               CopyBlock(oGxgost[i][PAGE], oGygost[i][PAGE],
                    oGxgost[i][PAGE] + 16, oGygost[i][PAGE] + 13);
               if(HaveGost[i] == 2) HaveGost[i] = 0;
          }
     }
     for(i = 0; i < MAXGOST1; i++) {
          if(HaveGost[i]) {
               Addx = Gxgost[i] + addmove[Gran[i]][0];
               Addy = Gygost[i] + addmove[Gran[i]][1];
               if(Addx < 4 || Addx > 294 || Addy < 3 || Addy > 220 ||
                 (CMapBlock(i) && CheckGost[i] == 0) ||
                 (!random(5) && CheckGost[i] == 0)) {
                    j = 0;
                    do {
                         Gran[i] = random(4);
                         if(j++ > 16) break;
                    } while(CMapBlock(i));
                    CheckGost[i] = 0;
               }
               else {
                    if(++CheckGost[i] > 5) {
                         CheckGost[i] = 0;
                         ArGostx[i] += cmove[Gran[i]][0];
                         ArGosty[i] += cmove[Gran[i]][1];
                    }
                    Gxgost[i] = Addx; Gygost[i] = Addy;
                    if(((Gxgost[i] + 5) / 12 == (GX - 5) / 12) &&
                       ((Gygost[i] + 4) / 12 == (GY - 3) / 12) &&
                       TimeMan == 0) {
                         PrintBoomMan();
                         TimeMan = 30;
                         for(k = 0; k < 8; k++) {
                              sound(150 * k + 1500); delay(30);
                         } 
                         nosound();
                    }
               }
               oGxgost[i][PAGE] = Gxgost[i];
               oGygost[i][PAGE] = Gygost[i];
          }
     }
}
void posGost(int i)
{
     int x, y;
     do {
          x = random(25); y = random(19);
     } while(Map[x][y] != 0 || ( x == 0 && y == 0));
     ArGostx[i] = x; ArGosty[i] = y; CheckGost[i] = 0;
     oGxgost[i][0] = oGxgost[i][1] = Gxgost[i] = x * 12 + 5;
     oGygost[i][0] = oGygost[i][1] = Gygost[i] = y * 12 + 4;
     Gran[i] = random(4); HaveGost[i] = 1;
}
void Background(void)
{
     int i, j;
     for(i = 0; i < 48; i += 4)
          for(j = 0; j < 4; j++)
               Skip[i + j] = j;
     Skip[48] = 0;
     SetActivePage(2);
     for(i = 0 ; i < 2; i++) {
          Rec(i + 1, i + 1, 310 - i, 238 - i, 3 + i);
          Rec(4 - i, 4 - i, 307 + i, 235 + i, 3 + i);
     }
     for(j = 0; j < 19; j++)
          for(i = 0; i < 25; i++)
               Map[i][j] = (!random(5)) ? 1 : 0;
     for(j = 1; j < 18; j += 2)
          for(i = 1; i < 25; i += 2)
               Map[i][j] = 2;
     Map[0][0] = Map[1][0] = Map[0][1] = 0;
     for(j = 0; j < 19; j++)
          for(i = 0; i < 25; i++)
               PutSprite(i * 12 + 6, j * 12 + 6,
     BitImage[Map[i][j]+26]);
     Bar(312, 1, 359, 240, 48);
     PutSprite(318, 220, BitImage[0]);
     PutSprite(320, 202, BitImage[22]);
     PutSprite(321, 7, BitImage[29]);
     Rec(337, 201, 352, 214, 0);
     Bar(336, 200, 351, 213, 18);
     Rec(336, 200, 351, 213, 19);
     PrintNum(342,205, MAXBOOM1, 0);
     PrintNum(341, 204, MAXBOOM1, 15);
     Rec(337, 221, 352, 234, 0);
     Rec(336, 220, 351, 233, 11);
     Rec(315,  17, 356,  29, 0);
     Rec(314,  16, 355,  28, 10);
     CopyPage(0, 2); CopyPage(1, 2);
     PrintBoomMan(); PrintScore();
     SetActivePage(PAGE);
     for(i = 0 ; i < MAXGOST1; i++) {
          posGost(i); Cgost[i] = 1;
     }
     for(i = 0; i < MAXBOOM1; i++)
          NBoom[i] = 0;
     oGanx[0] = oGanx[1] = GX = 5;
     oGany[0] = oGany[1] = GY = 3;
     GUX = GUY = 0; TimeMan = 30;
}
void SetBoom(void)
{
     int i;
     for(i = 0; i < MAXBOOM1; i++){
          if(NBoom[i] == 0 && Map[(GX - 5) / 12][(GY - 3) / 12] != 4) {
               TimeBoom[i] = 25; TimeBoom1[i] = 2;
               Map[(GX - 5) / 12][(GY - 3) / 12] = 4;
               GxBoom[i] = GX + 1; GyBoom[i] = GY + 4;
               NBoom[i] = 1; break;
          }
     }
}
void ClearBlock(int i, int j)
{
     int k;
     if(i >= 0 && i < 25 && j >= 0 && j < 19 ) {
          if(Map[i][j] == 1) {
               Map[i][j] = 0;
               for(k = 2; k >= 0; k--){
                    SetActivePage(k);
                    PutSprite(i * 12 + 6, j * 12 + 6,
                             BitImage[Map[i][j] + 26]);
               }
               SCORE += 1; PrintScore();
               SetActivePage(PAGE);
          }
     }
}
void ClearBoom(void)
{
     int i, j, x, y;
     for(i = 0; i < MAXBOOM1; i++){
          x = (GxBoom[i] - 4) / 12; y = (GyBoom[i] + 1) / 12;
          if(NBoom[i] > 0) {
               CopyBlock(GxBoom[i] - MxFire * 12, GyBoom[i],
               GxBoom[i] + MxFire * 12 + 12, GyBoom[i] + 11);
               CopyBlock(GxBoom[i], GyBoom[i] - MxFire * 12,
               GxBoom[i] + 12, GyBoom[i] + MxFire * 12 + 11);
          }
          else {
               ClearBlock(x, y - BCh[i][0]); 
               ClearBlock(x, y + BCh[i][1]);
               ClearBlock(x - BCh[i][2], y); 
               ClearBlock(x + BCh[i][3], y);
          }
          if(End == -1) { /* New Level */
               End = NGost = 0; BoomMan++;
               if(MAXGOST1 < MAXGOST) MAXGOST1++;
               j = Level % 3;
               if(j == 0 && BoomMan < 9) BoomMan++;
               if(j == 1 && MxFire < 10) MxFire++;
               if(j == 2 && MAXBOOM1 < MAXBOOM) MAXBOOM1++;
               Level++;
               Background(); return;
          }
     }
}
void CheckKill(int i, int j, int k)
{
     int x, y;
     x = (GX - 5) / 12; y = (GY - 3) / 12;
     if(TimeMan == 0 &&(i == x && j == y ||
       (x == (GxBoom[k] - 4) / 12 && y == (GyBoom[k] + 1) / 12))) {
          PrintBoomMan(); TimeMan = 30;
          for(k = 0; k < 8; k++) {
               sound(150 * k + 1500); delay(30);
          }
          nosound();
     }
     if(Map[i][j] == 4) {
          for(k = 0; k < MAXBOOM1; k++) {
               if(i == (GxBoom[k] - 4) / 12 &&
                  j == (GyBoom[k] + 1) / 12 ){
                    TimeBoom[k] = 2; break;
               }
          }
     }
     for(k = 0; k < MAXGOST1; k++) {
          if(HaveGost[k] == 1) {
               if(i == (Gxgost[k] + 5) / 12 &&
                  j == (Gygost[k] + 4) / 12) {
                    sound(1000); delay(200);
                    HaveGost[k] = 2;
                    SCORE += 10; PrintScore();
                    if(++NGost >= MAXGOST1)
                         End = -1;
                    nosound();
               }
          }
     }
}
void PutFire(int i)
{
     int j = 0, k, x, y;
     x = (GxBoom[i] - 4) / 12; y = (GyBoom[i] + 1) / 12;
     for( k = 0; k < 4; k++) BCh[i][k] = 0;
     while(Map[x][y - j] == 0 && (GyBoom[i] - j * 12) > 3 && j < MxFire) {
          CheckKill(x, y - j - 1, i);
          for(k = 0; k < 10; k += 4)
               PutSprite(GxBoom[i], GyBoom[i] - j * 12 - k, BitImage[17]);
          j++;
     }
     if(Map[x][y - j] > 0 )
          CopyBlock(x * 12 + 6, ((y - j) * 12) + 6,
                    x * 12 + 18, ((y - j) * 12) + 18);
     BCh[i][0] = j; j = 0;
     while(Map[x][y + j] == 0 && (GyBoom[i] + j * 12) < 219 && j < MxFire) {
          CheckKill(x, y + j + 1, i);
          for(k = 2; k < 10; k += 4)
               PutSprite(GxBoom[i], GyBoom[i] + j * 12 + k, BitImage[18]);
          j ++;
     }
     if(Map[x][y + j] > 0)
          CopyBlock(x * 12 + 6, ((y + j) * 12)+6,
                    x * 12 + 18, ((y + j) * 12) + 18);
     BCh[i][1] = j; j = 0;
     while(Map[x - j][y] == 0 && (GxBoom[i] - j * 12) > 5 && j < MxFire) {
          CheckKill(x - j - 1, y, i);
          for(k = 2; k < 10; k += 4)
               PutSprite(GxBoom[i] - j * 12 - k, GyBoom[i], BitImage[19]);
          j ++;
     }
     if(Map[x - j][y] > 0 )
          CopyBlock((x - j) * 12 + 6, y  * 12 + 6,
                    (x - j) * 12 + 12, y * 12 + 18);
     BCh[i][2] = j; j = 0;
     while(Map[x + j][y] == 0 && (GxBoom[i] + j * 12) < 293 && j < MxFire) {
          CheckKill(x + j + 1, y, i);
          for(k = 2; k < 10; k += 4)
               PutSprite(GxBoom[i] + j * 12 + k , GyBoom[i], BitImage[20]);
          j ++;
     }
     if(Map[x+j][y] > 0 )
          CopyBlock((x + j) * 12 + 10, y  * 12 + 6,
                    (x + j) * 12 + 18, y * 12 + 18);
     BCh[i][3] = j;
     PutSprite(GxBoom[i], GyBoom[i], BitImage[16] );
}
void ShowBoom(void)
{
     int i, j;
     for(i = 0; i < MAXBOOM1; i++){
          if(NBoom[i] == 3) NBoom[i] = 0;
          if(NBoom[i] == 2) NBoom[i] = 3;
          if(NBoom[i] == 1) {
               if(--TimeBoom[i] <= 0) {
                    Map[(GxBoom[i] - 4) / 12][(GyBoom[i] + 1) / 12] = 0;
                    if(--TimeBoom1[i] < 0) {
                         NBoom[i] = 2; TimeBoom1[i] = 0;
                    }
                    for(j = 1; j < 8; j++) {
                         sound(700 + j * 40); delay(10);
                    }
                    PutFire(i); nosound();
               }
               else /* show boom */
                    PutSprite(GxBoom[i], GyBoom[i],
                              BitImage[random(2) + 21]);
          }
     }
}
void main(void)
{
     int i, move = 0, img = 0, checkkey = 0;
     UnpackBitmap(Bitmap0 ,  0,  0); UnpackBitmap(Bitmap1 ,  1,  0);
     UnpackBitmap(Bitmap0 ,  2,  0); UnpackBitmap(Bitmap2 ,  4,  0);
     UnpackBitmap(Bitmap2 ,  6,  0); UnpackBitmap(Bitmap3 ,  5,  0);
     UnpackBitmap(Bitmap4 ,  7,  0); UnpackBitmap(Bitmap5 , 12,  0);
     UnpackBitmap(Bitmap5 , 14,  0); UnpackBitmap(Bitmap6 , 13,  0);
     UnpackBitmap(Bitmap7 , 16, 45); UnpackBitmap(Bitmap8 , 17, 45);
     UnpackBitmap(Bitmap9 , 18, 45); UnpackBitmap(Bitmap10, 19, 45);
     UnpackBitmap(Bitmap11, 21, 45); UnpackBitmap(Bitmap12, 22, 45);
     UnpackBitmap(Bitmap13, 23, 30); UnpackBitmap(Bitmap14, 24, 30);
     UnpackBitmap(Bitmap15, 25, 30); UnpackBitmap(Bitmap16, 26, 15);
     UnpackBitmap(Bitmap17, 27, 15); UnpackBitmap(Bitmap18, 28, 15);
     UnpackBitmap(Bitmap19, 29, 45);
     FlipBitmap(19, 20); FlipBitmap(13, 15); FlipBitmap(1, 3);
     for(i = 4; i < 8; i++) /* boomberman move left */
          FlipBitmap(i, i + 4);
     randomize();
     SetModeX();
     SetPal();
     Background();
     NewIntkey();
     while (!KEY.Esc && End <= 0) {
          FLIPPAGE();
          ClearBoom();
          CopyBlock(oGanx[PAGE], oGany[PAGE],
                    oGanx[PAGE] + 16, oGany[PAGE] + 15);
          MoveGost();
          checkkey = 0;
          if(KEY.Space) {
               MoveSkipX(); MoveSkipY();
               SetBoom();
               KEY.Space = 0;
          }
          if(KEY.DownArrow  && GY < 219){
               if(Checkblock(GX, GY + 12)) {
                    GY += 6; GUY++; img = 0; checkkey = 1;
               }
               MoveSkipX();
          }
          if(KEY.RightArrow && GX < 293) {
               if(Checkblock(GX + 12, GY)) {
                    GX += 6; GUX++; img = 4; checkkey = 1;
               }
               MoveSkipY();
          }
          if(KEY.LeftArrow  && GX > 5) {
               if(Checkblock(GX - 6, GY)) {
                    GX -= 6; GUX --; img = 8; checkkey = 1;
               }
               MoveSkipY();
          }
          if(KEY.UpArrow && GY > 3) {
               if(Checkblock(GX, GY - 6)) {
                    GY -= 6; GUY --; img = 12; checkkey = 1;
               }
               MoveSkipX();
          }
          if(checkkey) { /* check animate move */
               if(++move > 3) move = 0;
          } 
          else move = 0;
          ShowBoom();
          for(i = 0; i < MAXGOST1; i++){
               if(HaveGost[i] == 1)
                    PutSprite(Gxgost[i], Gygost[i], 
                              BitImage[Gloop[Gmove]]);
          }
          if(TimeMan % 2 || TimeMan == 0)
               PutSprite(GX, GY, BitImage[img + move]);
          if(++Gmove > 4) Gmove = 0;
          oGanx[PAGE] = GX; oGany[PAGE] = GY;
          if(--TimeMan < 0) TimeMan = 0;
          delay(250);
     }
     for(i = 0; i < 30; i++) free(BitImage[i]);
     SetOldkey(); TextMode();
     printf("-- < GAME OVER > --\n< Your Scores = %d0 >\n", SCORE);
}