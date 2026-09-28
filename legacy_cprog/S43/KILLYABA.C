/* killyaba.c */
/* program by 3D Engine */
#include "mgraph.c"
/* the note defines */
#define C    0
#define Cs   1
#define Db   1
#define D    2
#define Ds   3
#define Eb   3
#define E    4
#define F    5
#define Fs   6
#define Gb   6
#define G    7
#define Gs   8
#define Ab   8
#define A    9
#define As  10
#define Bb  10
#define B   11

/* psuedo operations defines */
#define LOOP   12   /* repeat from begining    */
#define SO     13   /* switch octaves          */
#define R      14   /* rest (duration follows) */
#define END    15   /* end of the song         */

/* duration defines */
#define S    1
#define EI   2
#define Q    4
#define H    8
#define W   16
#define DW  32

/* the notes:frequency array */
unsigned int notes[6][12]={
  /* actually starts at octave #3 */
  {17145,17173,16209,15299,14441,13630,12865,12143,11462,10818,10211,9638},
  {9097,8586,8105,7650,7224,6816,6432,6071,5729,5409,5105,4819},
  {4548,4293,4052,3825,3610,3410,3216,3036,2867,2705,2554,2409},
  {2274,2147,2026,1912,1805,1702,1608,1518,1433,1352,1276,1205},
  {1137,1073,1013,956,903,852,804,759,716,676,638,602},
  {569,537,507,478,451,426,402,380,358,338,319,301}
  };
unsigned char songtable[]={ SO,2,G,W,R,EI,G,Q,R,EI,SO,3,C,DW,R,W,
   SO,2,G,W,R,EI,SO,3,C,Q,R,EI,E,DW,R,DW,
   SO,2,G,W,R,EI,SO,3,C,Q,R,EI,E,W,R,S,
   SO,2,G,W,R,EI,SO,3,C,Q,R,EI,E,W,R,S,
   SO,2,G,W,R,EI,SO,3,C,Q,R,EI,E,W,R,S,
   R,W,C,W,R,EI,E,Q,R,EI,G,W,
   R,W,E,W,R,EI,C,W,R,EI,SO,2,G,W,R,W,
   G,W,R,EI,G,Q,R,EI,SO,3,C,DW,R,DW,R,DW,
   LOOP };
/* globals for the song routines */
  char c_duration, c_octave;
  unsigned char *ptrsong;
  char sp_on,sp_off;

void interrupt (*oldvector)(void);
void interrupt song(void)
{
	unsigned char lsb,msb,c_note;
	if(c_duration)
		c_duration--;
	else{
		c_note = *ptrsong;
		switch(c_note) {
			case 12: ptrsong = songtable;
				 break;
			case 13: ptrsong++;
				 c_octave = *ptrsong++;
				 break;
			case 14: ptrsong++;
				 c_duration = *ptrsong++;
				 outp(97,sp_off); /* nosound */
				 break;
			case 15: break;
			default: ptrsong++;
				 c_duration = *ptrsong;
				 lsb=notes[c_octave][c_note]%256;
				 msb=notes[c_octave][c_note]/256;
				 /* sound on */
				 outp(67,182);
				 outp(66,lsb);
				 outp(66,msb);
				 outp(97,sp_on);
				 ptrsong++;
				 break;
		}
	}
}

void initsong(void)
{
/* set up */
  sp_off = inp(97);
  sp_on = sp_off|3;
  c_duration = 0;
  oldvector = getvect(0x1c);
  setvect(0x1c,song);
  /* it's playing */
}

void restoresong(void)
{
/* restores the old timer vector and speaker state */
  setvect(0x1c,oldvector);
  outp(97,sp_off);
}
BYTE Bitmap0[] = {   7,  8,
    0,  1,  3,  3,  3,  1,  0,
    1,  5,  7,  6,  6,  5,  1,
    3,  7,  6,  6,  6,  5,  3,
    4,  7,  6,  6,  6,  5,  4,
    4,  5,  6,  6,  6,  5,  4,
    4,  5,  6,  6,  6,  5,  4,
    4,  5,  6,  6,  6,  5,  4,
    4,  5,  6,  6,  6,  5,  4
   };
BYTE Bitmap1[] = {   7,  8,
    4,  5,  6,  6,  6,  5,  4,
    4,  7,  6,  6,  6,  5,  4,
    4,  7,  6,  6,  6,  5,  4,
    4,  7,  6,  6,  6,  5,  4,
    4,  5,  6,  6,  6,  5,  4,
    3,  5,  6,  6,  6,  5,  3,
    1,  5,  6,  6,  6,  5,  1,
    0,  1,  3,  3,  3,  1,  0
   };
BYTE Bitmap2[] = {   9,  6,
    0,  1,  3,  4,  4,  4,  4,  4,  4,
    1,  5,  5,  6,  7,  7,  5,  5,  5,
    3,  6,  7,  6,  6,  6,  6,  6,  6,
    3,  6,  6,  6,  6,  6,  6,  6,  6,
    1,  5,  5,  5,  5,  5,  5,  5,  5,
    0,  1,  3,  4,  4,  4,  4,  4,  4
   };
BYTE Bitmap3[] = {   9,  6,
    4,  4,  4,  4,  4,  4,  3,  1,  0,
    5,  7,  7,  6,  5,  5,  5,  5,  1,
    6,  7,  6,  6,  6,  6,  6,  6,  3,
    6,  6,  6,  6,  6,  6,  6,  6,  3,
    5,  5,  5,  5,  5,  5,  5,  5,  1,
    4,  4,  4,  4,  4,  4,  3,  1,  0
   };
BYTE Bitmap4[] = {   8,  6,
    0,  2,  5,  5,  5,  5,  2,  0,
    2,  5,  4,  5,  5,  4,  5,  2,
    5,  5,  1,  5,  5,  1,  5,  5,
    5,  5,  5,  5,  5,  5,  5,  5,
    2,  5,  5,  1,  1,  5,  5,  2,
    0,  2,  5,  4,  4,  5,  2,  0
   };
BYTE Bitmap5[] = {   8,  6,
    0,  2,  5,  5,  5,  5,  2,  0,
    2,  5,  4,  5,  5,  4,  5,  2,
    5,  5,  4,  5,  5,  4,  5,  5,
    5,  5,  5,  5,  5,  5,  5,  5,
    2,  5,  5,  4,  4,  5,  5,  2,
    0,  2,  5,  4,  4,  5,  2,  0
   };
BYTE *Ya[] = {Bitmap0,Bitmap1,Bitmap2,Bitmap3};
BYTE *YaBa[] = { Bitmap4,Bitmap5 };
BYTE color[] = {8, 0, 0,  0, 8, 0,  0, 0, 8,
	8, 8, 0, 8, 0, 8, 0, 8, 8,  8, 8, 8};
#define EASY   40
#define MIDDLE 20
#define HARD   10
#define MAPX 14
#define MAPY 24
#define LEVEL EASY		/* Change EASY, MIDDLE, HARD */
int NewCo0,NewCo1;
int YaX,YaY,PosYA=0;
int Color0,Color1,Delay=0;
int Line=10;
int Map[MAPX][MAPY+1];
int Type[MAPX][MAPY];
int SCORE = 0;
void setpalette(void)
{
	int i, j;
	outp(0x3c8,0);
	for(j=0;j<7;j++)
		for(i=0;i<8;i++){
			outp(0x3c9,color[j*3]*i);
			outp(0x3c9,color[j*3+1]*i);
			outp(0x3c9,color[j*3+2]*i);
		}
}
void PutSpriteColor(int x0, int y0, BYTE *ptr,int color)
{
	int i, j, x1, y1;
	x1 = x0 + *ptr++; y1 = y0 + *ptr++;
	for(j = y0; j < y1; j++)
		for(i = x0; i < x1; i++, ptr++)
			if(i >= 0 && i < 320 &&
				j >= 0 && j < 200 && *ptr )
			*(PageStart + LINE_Y[j]  + i ) = 8*color + *ptr ;
}

void InitGame(void)
{
	int i,j;

	for(j=0;j<MAPY+1;j++)
		for(i=0;i<MAPX;i++){
			Map[i][j] = Type[i][j] = 99;
			if(random(LEVEL)==0&& j > Line){
				Map[i][j] = random(7);
				Type[i][j] = 5;
			}
		}
	YaX = 7, YaY = 0;
	Color0 = random(7);
	Color1 = random(7);
	NewCo0 = random(7);
	NewCo1 = random(7);
}
void PutYa0(int c0,int c1)
{
	PutSpriteColor(YaX *9 +10,YaY*8+2,Ya[0],c0);
	PutSpriteColor(YaX *9 +10,YaY*8+10,Ya[1],c1);
}
void PutYa1(int c0,int c1)
{
	PutSpriteColor(YaX * 9 + 10 ,YaY * 8 +12,Ya[2],c0);
	PutSpriteColor(YaX * 9 + 19,YaY* 8 +12,Ya[3],c1);
}

void PutYa(void)
{
	if(PosYA == 0)
		PutYa0(Color0,Color1);
	if(PosYA == 1)
		PutYa1(Color1,Color0);
	if(PosYA == 2)
		PutYa0(Color1,Color0);
	if(PosYA == 3)
		PutYa1(Color0,Color1);
}
void PutYaBa(void)
{
	int i,j;
	for(j=0;j<MAPY;j++)
		for(i=0;i<MAPX;i++){
			if(Map[i][j]!=99)
				if(Type[i][j] == 5) {
					if(random(20)==0)
						PutSpriteColor(i*9+10+random(2),j*8+4,
							YaBa[random(2)],Map[i][j]);
					else
						PutSpriteColor(i*9+10,j*8+4,
							YaBa[random(2)],Map[i][j]);
				}
				else
					PutSpriteColor(i*9+10,j*8+4,
						Ya[Type[i][j]],Map[i][j]);
	}
}
void InitYa(void)
{
	int i;
	YaX = 7, YaY = PosYA = 0;
	Color0 = NewCo0;
	Color1 = NewCo1;
	NewCo0 = random(7);
	NewCo1 = random(7);
	for(i=0;i<40;i++)
	{
		sound(i*20+400); delay(15);
	}
	nosound();

}
void SetLine(void)
{
	if(PosYA==0){
		if(Map[YaX][YaY+2] != 99 || YaY > MAPY-3){
			Map[YaX][YaY] = Color0;
			Map[YaX][YaY+1] = Color1;
			Type[YaX][YaY] = 0;
			Type[YaX][YaY+1] = 1;
			InitYa();
		}
	}
	if(PosYA == 1){
		if(Map[YaX][YaY+1]!=99 ||Map[YaX+1][YaY+1] != 99 ||
			YaY > MAPY-2){
			Map[YaX][YaY] = Color1;
			Map[YaX+1][YaY] = Color0;
			Type[YaX][YaY] = 2;
			Type[YaX+1][YaY] = 3;
			InitYa();
		}
	}
	if(PosYA==2){
		if(Map[YaX][YaY+2]!= 99 || YaY > MAPY-3){
			Map[YaX][YaY] = Color1;
			Map[YaX][YaY+1] = Color0;
			Type[YaX][YaY] = 0;
			Type[YaX][YaY+1] = 1;
			InitYa();
		}
	}
	if(PosYA==3){
		if(Map[YaX][YaY+1]!= 99 ||Map[YaX+1][YaY+1]!=99 ||
			YaY > MAPY-2){
			Map[YaX][YaY] = Color0;
			Map[YaX+1][YaY] = Color1;
			Type[YaX][YaY] = 2;
			Type[YaX+1][YaY] = 3;
			InitYa();
		}
	}
}
int CheckLeft(void)
{
	if(PosYA == 0||PosYA == 2)
		if(Map[YaX-1][YaY+1]!=99 || Map[YaX-1][YaY+2]!=99)
			return(0);
	if(PosYA == 1||PosYA == 3)
		if(Map[YaX-1][YaY+1]!=99)
			return(0);
	return(1);
}
int CheckRight(void)
{
	if(PosYA == 0||PosYA == 2)
		if(Map[YaX+1][YaY+1]!=99 || Map[YaX+1][YaY+2]!=99)
			return(0);
	if(PosYA == 1 || PosYA == 3)
		if(Map[YaX+2][YaY+1]!=99)
			return(0);
	return(1);
}

void MoveDown(int i,int j)
{
	int k,TemT,TemM;
    TemT = Type[i][j-1];
	TemM = Map[i][j-1];
	Type[i][j-1] = Map[i][j-1]=99;
	for(k=j+1;k<MAPY;k++)
			if(Map[i][k]==99){
					Type[i][k-1] = Map[i][k-1]=99;
					Type[i][k] = TemT;
					Map[i][k] = TemM;
				}
				else break;
}
int CheckLevel(void)
{
	int i,j;
	for(j=0;j<MAPY;j++)
		for(i=0;i<MAPX;i++)
			if(Type[i][j] == 5)
				return 0;
	return(1);
}
void CheckMove(void)
{
	int i,j,k;
	for(j=0;j<MAPY;j++)
		for(i=0;i<MAPX;i++){
			if(Map[i][j]!= 99){
			if(Map[i][j] == Map[i][j+1] &&
			   Map[i][j] == Map[i][j+2] &&
			   Map[i][j] == Map[i][j+3] &&
			   Map[i][j] == Map[i][j+4]){

				   for(k =4;k>=0;k--){
					if(Type[i][j+k] == 2 && Type[i+1][j+k] == 3 &&
						Type[i+1][j+k+1] == 99 && j + k + 1 < MAPY)
							MoveDown(i+1,j+k+1);
					if(Type[i][j+k] == 3 && Type[i-1][j+k] == 2 &&
						Type[i-1][j+k+1] == 99)
							MoveDown(i-1,j+k+1);
					Type[i][j+k] =	Map[i][j+k] = 99;
				   }
					SCORE += 20;
					if( CheckLevel()) InitGame();
			   }
			   else
			   if(Map[i][j] == Map[i][j+1] &&
				   Map[i][j] == Map[i][j+2] &&
				   Map[i][j] == Map[i][j+3] ){
				for(k  = 3;k >= 0;k--){
					if(Type[i][j+k] == 2 && Type[i+1][j+k] == 3 &&
						Type[i+1][j+k+1] == 99 && j + k + 1 < MAPY)
							MoveDown(i+1,j+k+1);
					if(Type[i][j+k] == 3 && Type[i-1][j+k] == 2 &&
						Type[i-1][j+k+1] == 99)
							MoveDown(i-1,j+k+1);
					Type[i][j+k] = Map[i][j+k] = 99;

				}
				   if(Type[i][j-1] != 99)
						MoveDown(i,j);
                   SCORE +=10;
				for(i=0;i<40;i++){
					sound(i*20+200); delay(15);
				}
				nosound();
                if( CheckLevel()) InitGame();
				}
				
			}
		}

}

void main(void)
{
	int End = 1,i;
	randomize();
	InitKey();
	ptrsong = songtable;
	initsong();
	InitGame();
	InitMode13();
	setpalette();
	while(!KEY.Esc && End){
		memset(PageStart, 0, MemLength);
		if(KEY.Left && YaX > 0 && CheckLeft()) {
			KEY.Left = 0;
			YaX --;
		}
		if(KEY.Right&& CheckRight()){
			if((PosYA % 2) == 0 && YaX < MAPX - 1 ||
				(PosYA % 2) == 1 && YaX < MAPX - 2 ){
				KEY.Right = 0;
				YaX ++;
			}
		}
		if(KEY.Space) {
			KEY.Space = 0;
			if((PosYA %2) == 0 && YaX == MAPX-1)
				YaX --;
			if(++PosYA > 3) PosYA = 0;

		}
		if(KEY.Down) {
			Delay = 200;
		}
		if(Delay++>30)
		{
			Delay =0;
			YaY++;
			if(YaY>MAPY) {
				Color0 = random(7);
				Color1 = random(7);
				YaY=0;
			}

		}
		SetLine();
		CheckMove();
		PutYaBa();
		PutYa();
		PutSpriteColor(150 ,10,Ya[2],NewCo0);
		PutSpriteColor(159, 10,Ya[3],NewCo1);
		Rec(146,4,170,20,15);
		for(i=0;i<3;i++)
			Rec(3+i,i,141-i,199-i,31-i*2);
		PrintNum(146,30,SCORE);
		PutVGA();
		delay(50);
		for(i=0;i<MAPX;i++)
			if(Map[i][0]!=99) End=0;
	}
	CloseGraph();
	restoresong();
	SetOldKey();
	printf("GAME OVER\nYOUR SCORE = %d",SCORE);
}