/* --- Computer Time C Programming --- */
/* --- Blockout.c code by  3D Engine --- */
#include "libgraph.c"
char BlockArray[16][16];
BYTE *CleanArray[16][16];
int MouseX, MouseY, mousebutt = 0;
int BallX, BallY, AddX, AddY, NumBall = 5;
int oMouseX[2], oBallX[2], oBallY[2];
int StateBall, NumBlock, cclean;
int SCORE = 0;
BYTE Back0[] = { /* bitmap background 0 */
   16, 16,
  146,136,154,154,146,146,146,227,228,227,146,146,146,136,136,146,
  146,136,154,154,227,146,146,136,154,154,146,146,146,136,154,227,
  146,146,136,136,228,146,146,136,154,154,227,146,146,227,228,227,
  146,146,227,228,227,146,146,146,136,136,228,146,136,154,136,146,
  146,146,146,146,146,136,136,146,227,228,227,146,154,154,154,227,
  146,154,136,227,136,154,154,146,146,146,146,146,136,154,154,228,
  146,136,227,228,136,154,154,227,146,136,136,227,146,227,228,227,
  146,227,228,227,146,146,227,228,146,154,136,228,146,146,146,146,
  136,227,146,146,146,146,146,146,146,227,228,227,146,146,136,154,
  154,228,146,146,136,154,154,227,146,146,136,136,146,146,154,154,
  136,228,146,146,136,154,154,228,146,136,154,154,227,146,136,154,
  228,227,146,146,146,136,227,228,146,136,154,136,228,146,146,227,
  146,136,154,227,146,227,228,227,146,146,227,228,227,146,146,146,
  146,154,136,228,146,146,136,136,146,146,146,146,146,136,154,227,
  146,227,228,227,146,136,154,154,136,227,146,146,146,154,136,228,
  146,146,146,146,146,146,154,136,227,228,146,146,146,227,228,227 };
BYTE Back1[] = { /* bitmap background 1 */
   16, 16,
    8,  9, 26, 26, 10,  9,  8,  8,  8,  8,  9, 26, 10, 26,  9,  8,
    8,  8,  9,  9,  8,  8,  8,  8,  8,  8,  8,  9,  9,  9,  8,  8,
    8,  8,  8,  8,  8,  8, 10, 12, 12, 26, 10,  9,  8,  8,  8,  8,
    8,  8,  9,  9,  8,  9, 26, 12, 12, 26, 26, 10,  8,  9,  8,  8,
   26,  9,  8,  9,  8,  9, 26, 26, 10, 10,  9,  9,  8,  8, 10, 12,
   10,  9,  8,  8,  8,  8,  9, 10, 10,  9,  9,  8,  8,  9, 26, 26,
    9,  8,  8,  8,  8,  8,  8,  9,  9,  8,  8,  9,  8,  9, 26, 10,
    8,  8,  9, 26, 10,  9,  8,  9,  8,  8,  8,  8,  8,  8,  9,  9,
    8,  9, 26, 12, 26, 10,  9, 26,  9,  8,  9, 26, 10,  9,  8,  8,
    8,  9, 26, 10, 10,  9,  8,  9,  8,  8, 26, 12, 26, 10,  9,  8,
    8,  8,  9,  9,  8,  8,  8,  8,  8,  8,  9, 10, 26, 26,  9,  8,
   10,  9,  8,  8,  8,  8,  8,  8,  9,  9,  8,  9, 10,  9,  8,  9,
   26, 10,  8,  9,  8,  8,  8,  8,  8,  9,  8,  8,  8,  8,  8,  9,
    9,  8,  8,  8,  9,  9,  9,  8,  8,  8, 10, 12, 26, 10,  9,  8,
    8,  8, 10, 12, 12, 26, 10,  9,  8,  9, 26, 12, 12, 26, 10,  9,
    8,  9, 26, 12, 26, 10,  9,  8,  8,  9, 26, 26, 10,  9,  9,  9
    };
BYTE Back2[] = { /* bitmap background 2 */
   16, 16,
  154,136,228,228,228,227,136,154,154,136,228,228,227,136,136,136,
  154,154,227,228,229,228,227,136,154,136,228,229,228,228,227,154,
  136,154,136,228,229,229,228,154,154,154,227,228,228,227,154,154,
  228,228,154,136,154,154,154,154,154,136,154,154,154,154,154,136,
  228,136,154,154,154,154,154,136,136,136,136,227,227,136,154,136,
  154,136,227,227,136,154,136,227,227,136,228,228,228,228,136,154,
  154,227,229,228,228,227,227,228,228,227,229,251,229,227,136,154,
  154,228,251,250,229,228,228,229,228,227,251,251,250,227,154,154,
  154,228,251,251,250,228,227,228,227,136,228,229,228,154,136,136,
  136,227,228,228,227,136,227,228,228,228,136,136,136,227,228,227,
  227,136,154,136,136,227,228,250,229,228,227,227,228,228,229,228,
  228,136,227,228,228,228,229,251,250,229,228,228,228,229,251,228,
  227,228,228,229,229,250,251,251,251,250,229,229,229,228,229,227,
  228,229,250,251,251,251,252,252,252,252,251,251,251,250,229,228,
  250,251,251,250,250,251,154,154,154,154,251,250,250,251,251,250,
  251,250,251,154,154,154,154,154,154,154,154,154,154,251,250,251
  };
BYTE Back3[] = { /* bitmap background 3 */
   16, 16,
  154,146,146,228,251,146,154,136,146,227,250,228,228,251,227,136,
  154,146,146,228,251,227,136,136,146,228,229,227,227,250,228,146,
  136,146,146,227,251,228,146,136,227,229,228,146,146,228,229,227,
  136,146,146,146,229,229,227,146,228,229,227,136,136,227,251,228,
  136,146,146,146,228,251,228,228,229,228,146,154,136,146,251,228,
  146,146,146,146,227,229,229,228,228,227,136,154,146,146,251,228,
  146,146,146,161,228,228,229,250,228,146,136,154,146,227,251,228,
  146,146,161,228,229,228,228,229,250,228,146,136,146,228,229,227,
  146,161,228,229,228,146,146,228,229,250,227,146,227,229,228,146,
  228,229,229,228,146,136,136,146,228,251,228,227,228,229,227,227,
  229,228,227,146,136,154,136,146,227,250,228,228,229,228,227,228,
  228,146,136,154,136,146,227,228,228,229,229,228,227,146,228,229,
  146,136,136,146,146,228,229,229,228,228,250,227,146,227,229,228,
  136,154,146,146,228,229,228,227,146,227,251,228,146,228,229,227,
  154,136,146,146,229,228,146,136,136,146,251,228,227,250,228,146,
  154,146,146,227,251,227,136,136,146,146,251,228,228,251,227,136
  };
BYTE *BACKGROUND[] = { Back0, Back1, Back2, Back3 }; /* 4 type */
BYTE SmallBall[] = { /* bitmap show num ball */
    8,  6,
    0, 11, 11, 12, 12, 11, 10,  0,
   11, 13, 14, 15, 16, 13, 13, 11,
   12, 14, 18, 23, 19, 11,  9, 13,
   12, 14, 17, 16, 11,  8,  9, 12,
   11, 12, 11,  8,  7,  9, 12, 11,
    0, 11, 12, 13, 12, 13, 11,  0
};
BYTE Ball[] = { /* bitmap silver ball */
   15, 13,
    0,  0,  0,  0, 10, 11, 11, 11, 11, 11, 10,  0,  0,  0,  0,
    0,  0, 10, 12, 13, 14, 13, 13, 13, 14, 14, 12, 10,  0,  0,
    0, 11, 12, 14, 14, 15, 16, 16, 14, 13, 12, 13, 12, 10,  0,
   10, 12, 14, 16, 18, 20, 21, 21, 18, 14, 11, 11, 13, 12,  0,
   12, 14, 15, 18, 21, 21, 21, 19, 15, 11,  8,  9, 11, 14, 11,
   12, 14, 16, 19, 20, 19, 18, 15, 11,  9,  8,  8, 11, 15, 12,
   13, 14, 15, 17, 18, 16, 14, 11,  9,  8,  8,  9, 11, 15, 13,
   12, 14, 14, 14, 13, 11,  9,  8,  7,  7,  8, 10, 13, 15, 13,
   12, 12, 12, 11,  9,  8,  7,  7,  8,  9, 10, 12, 14, 14, 12,
   10, 12, 12,  9,  9,  8,  9,  9, 10, 12, 13, 15, 15, 13, 10,
    0, 11, 12, 12, 11, 11, 11, 12, 13, 14, 15, 15, 14, 11,  0,
    0,  0, 11, 12, 13, 13, 13, 14, 15, 14, 14, 12, 10,  0,  0,
    0,  0,  0, 10, 10, 11, 11, 12, 12, 11, 11,  0,  0,  0,  0
};
BYTE Sakabure[] = { /* bitmap mouse picture for hit ball */
   38,  4,
    0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0,
    4, 4, 6, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 6, 4, 4,
    0, 0, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0,
    0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0
};
void PrintScore(int color)
{    /* print score at top left page 0 & page 1 */
     char str[10], i = 0;
     itoa(SCORE, str, 10);
     SetActivePage(1 - PAGE);
     CopyBlock(310, 1, 359, 6);
     while(str[i])
          PrintNum(i * 6 + 310, 1, str[i++] - '0', color);
     SetActivePage(PAGE);
     CopyBlock(310, 1, 359, 6);
     i = 0;
     while(str[i])
          PrintNum(i * 6 + 310, 1, str[i++] - '0', color);
}
void SetPalColor(void)
{    /* set new color palette */
     static BYTE NewColor[] = {  7,7,7, 0,2,3, 0,2,4, 0,0,3, 0,0,7,
       3,0,4, 7,0,7, 4,0,2, 7,0,0, 2,0,0, 0,3,1, 0,4,1, 0,7,0,
       7,7,0, 7,3,0, 4,7,7 };
     static BYTE Palette[] = {  62,62,41, 59,56, 0, 59,48, 0, 58,41, 0,
       45,19, 0, 32, 7, 0,  2, 2, 2,  6, 6, 6, 11,11,11, 15,15,15,
       19,19,19, 24,24,24, 28,28,28, 31,31,31, 35,35,35, 40,40,40,
       43,43,43, 46,46,46, 51,51,51, 54,54,54, 63,63,63 };
     int i, j;
     BYTE *ptr;
     outp(0x3c8, 15);
     for(j = 0, ptr = NewColor; j < 16; j++, ptr += 3)
          for(i = 1; i < 16; i++) {
               outp(0x3c9,  *ptr * i );
               outp(0x3c9, *(ptr + 1) * i );
               outp(0x3c9, *(ptr + 2) * i );
          }
     ptr = Palette;
     outp(0x3c8, 1);
     for(i = 1;i < 22; i++) {
          outp(0x3c9, *ptr++);
          outp(0x3c9, *ptr++);
          outp(0x3c9, *ptr++);
     }
}
void PutBlock(int x, int y, BYTE c)
{    /* show block 3d rectangle */
     static BYTE BColor[] = { 14, 19, 38, 52, 70, 81, 100, 111,
          130, 141, 162, 186, 201, 216, 231, 246 };
     BYTE color = BColor[c - 1] ;
     Bar(x + 2, y + 2, x + 19, y + 6, color - 1);
     Vline(x, x + 20, y, color + 2);
     Vline(x + 1, x+19, y + 1, color);
     Hline(x, y, y + 7, color + 2);
     Hline(x + 1, y + 1, y + 6, color);
     Vline(x, x + 20, y + 7, color - 5);
     Vline(x + 1, x + 19, y + 6, color - 4);
     Hline(x + 20, y, y + 7, color - 6);
     Hline(x + 19, y + 1, y + 6, color - 4);
     PutPixel(x, y, color);
     PutPixel(x, y + 6, color);
     PutPixel(x + 1, y + 6, color - 3);
     PutPixel(x + 19, y, color - 2);
     PutPixel(x + 20, y + 7, color - 6);
}
void PutArrayBlocks(void)
{    /* put array block 3d */
     int i, j;
     NumBlock = 0;
     for(j = 0; j < 16; j++)
          for(i = 0; i < 16; i++) {
               GetSprite(i * 21 + 12, j * 8 + 12,
                    i * 21 + 33, j * 8 + 20, CleanArray[j][i]);
               if(BlockArray[j][i]) {
                    PutBlock(i * 21 + 12 , j * 8 + 12,
                         BlockArray[j][i]);
                    NumBlock ++;
               }
          }
}
void PrintNumBall(void)
{    /* show total num ball */
     int i;
     CopyBlock(10, 1, 150, 7); /* clear numball background */
     for(i = 0; i < NumBall; i++)
          PutSprite(i * 9 + 10, 1, SmallBall);
}
void MoveBall(void)
{    /* move ball & check */
     static int i, j;
     int k;
     CopyBlock(oBallX[PAGE], oBallY[PAGE],   /* clear ball */
          oBallX[PAGE] + 15, oBallY[PAGE] + 13);
     BallX += AddX;
     BallY += AddY;
     if(BallX <   8) AddX =  random(3) + 3; /* ball to right */
     if(BallX > 340) AddX =  random(3) - 4; /* ball to left */
     if(BallY <  10) AddY =  random(3) + 3; /* ball upper */
     if(BallY > 260) {   /* not hit  (ball under) */
          BallX = MouseX + 12;
          BallY = 221;
          StateBall = 0;
          for(k = 0; k < 8; k++) {
               sound(50 * k + 900);
               TimeDelay(2);
          }
          nosound();
          NumBall--;
          SetActivePage(1 - PAGE);
          PrintNumBall();
          SetActivePage(PAGE);
          PrintNumBall();
          return;
     }
     if(cclean == 1) {   /* clear block loop 2 */
          cclean = 0;
          PutSprite(i * 21 + 12, j * 8 + 12,
          CleanArray[j][i]);
     }
     if(StateBall == 1 && BallY > 221 && BallY < 226 &&  /* hit */
         BallX > (MouseX - 12) && BallX < (MouseX + 38)) {
          sound(20 * random(200) + 900);
          TimeDelay(1);
          nosound();
          AddY =  random(2) - 3;
          BallY = 221;
     }
     if(BallY > 12 && BallY < 139 && BallX > 12) {
          i = (BallX - 12) / 21;
          j = (BallY - 12) / 8;
          if(BlockArray[j][i]) {
               BlockArray[j][i] = 0;
               cclean = 1;
               sound(10 * random(200) + 500);
               TimeDelay(1);
               nosound();
               SetActivePage(2);   /* clear block loop 1 */
               PutSprite(i * 21 + 12, j * 8 + 12,
               CleanArray[j][i]);
               SetActivePage(PAGE);
               PutSprite(i * 21 + 12, j * 8 + 12,
               CleanArray[j][i]);
               NumBlock--;
               SCORE += 10;
               PrintScore(2);
               AddY = (BallY > oBallY[PAGE]) ?
                    random(3) - 3 : random(2) + 2;
          }
     }
     if(!StateBall) {
          BallX = MouseX + 12;
          BallY = 221;
     }
     PutSprite(BallX, BallY, Ball);
     oBallX[PAGE] = BallX;
     oBallY[PAGE] = BallY;
}
void InitScreen(void)
{    /* init screen & init position ball & block */
     int i, j, k;
     if(!PAGE) FLIPPAGE();
     BallX = oBallX[0] = oBallX[1] = 160;
     BallY = oBallY[0] = oBallY[1] = 221;
     AddX = 2; AddY = -2;
     cclean = 0; StateBall = 0;
     for(j = 0; j < 16; j++)
          for(i = 0; i < 16; i++)
               BlockArray[j][i] = random(4) ? random(16) + 1 : 0;
     SetActivePage(1);
     k = random(4);
     for(j = 0; j < 15; j++)
          for(i = 0; i < 22; i++)
               PutSprite(i * 16, j * 16, BACKGROUND[k]);
     for(i = 0 ; i < 4; i++) {
          Rec(i, i, 359 - i, 248 - i, i * 2 + 96);
          Rec(7 - i, 7 - i, 352 + i, 240 + i, i * 2 + 96);
     }
     CopyPage(2, 1);
     SetActivePage(1);
     PutArrayBlocks();
     CopyPage(2, 1);
     PrintNumBall();
     CopyPage(0, 1);
     PrintScore(2);
     SetActivePage(0);
     GetMouseInfo(&MouseX, &MouseY, &mousebutt);
}
void main(void)
{
     int i, j;
     randomize();
     SetModeX();
     SetPalColor();
     if(!InitMouse()) {
          TextMode();
          printf("mouse not found.\n");
          exit(0);
     }
     MoveMouse(160, 235);
     for(j = 0; j < 16; j++)  /* init memory for clear block */
          for(i = 0; i < 16; i++)
               CleanArray[j][i] = malloc(170);
     InitScreen();
     oMouseX[PAGE] = MouseX;
     while(!kbhit() && mousebutt != 2) {
          FLIPPAGE();
          GetMouseInfo(&MouseX, &MouseY, &mousebutt);
          if(mousebutt == 1 && !StateBall) {
               StateBall = 1;
               AddY =  random(3) - 3;
          }
          CopyBlock(oMouseX[PAGE], 234, oMouseX[PAGE] + 38, 238);
          MoveBall();
          if(NumBall < 1)  break; /* end to game over */
          if(NumBlock < 1) InitScreen();
          PutSprite(MouseX, 234, Sakabure);
	  oMouseX[PAGE] = MouseX;
	  delay(40);
     }
     CloseMouse();
     for(j = 0; j < 16; j++)  /* clear mem array */
          for(i = 0; i < 16; i++)
               free(CleanArray[j][i]);
     TextMode();
     printf("-- < GAME OVER > --\n");
     printf ("< Your score = %d >", SCORE);
}