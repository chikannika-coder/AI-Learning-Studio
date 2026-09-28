/* main TETRIS.C by SAWAT PONTREE */
/* type TCC TETRIS.C GRAPH.C [Enter] to compile */
#include "GRAPH.H"
struct Keyboard { /* Keyboard input structure.*/
    char RightArrow,LeftArrow,UpArrow,DownArrow,Space,Esc;
} KEY;
char far *PageStart;
char far *FirstAdr[4];
/* -------------- Main data & Code --------------- */
char Tris0[] = { -1,0,-1,1,0,1,1,1, 1,0,0,0,0,1,0,2,
		1,2,-1,1,0,1,1,1, -1,2,0,0,0,1,0,2 };
char Tris1[] = {  -1,0,0,0,0,1,0,2, 1,0,-1,1,0,1,1,1,
		 0,0,0,1,0,2,1,2, -1,1,0,1,1,1,-1,2 };
char Tris2[] = {  0,0,1,0,0,1,-1,1, 0,0,0,1,1,1,1,2,
		 0,0,1,0,0,1,-1,1, 0,0,0,1,1,1,1,2 };
char Tris3[] = {  0,0,1,0,1,1,2,1,  1,0,1,1,0,1,0,2,
		 0,0,1,0,1,1,2,1,  1,0,1,1,0,1,0,2 };
char Tris4[] = {  0,0,1,0,0,1,1,1,  0,0,1,0,0,1,1,1,
		 0,0,1,0,0,1,1,1,  0,0,1,0,0,1,1,1 };
char Tris5[] = { -1,0,0,0,1,0,0,1,  0,-1,0,0,0,1,-1,0,
		 -1,0,0,0,1,0,0,-1, 0,-1,0,0,0,1,1,0 };
char Tris6[] = { -1,0,0,0,1,0,2,0,  0,-1,0,0,0,1,0,2,
		 -1,0,0,0,1,0,2,0,  0,-1,0,0,0,1,0,2 };
char *TypeTris[]={ Tris0,Tris1,Tris2,Tris3,Tris4,Tris5,Tris6 };
BYTE L_Tris[] = { 17,8,17,17, 17,17,8,17, 17,8,17,8,
 8,8,8,8, 8,8,8,8, 17,17,17,8, 17,8,17,8 };
BYTE R_Tris[] = { 116,116,116,125, 125,116,116,116, 116,116,116,116,
 107,116,107,116, 116,116,116,116, 116,125,116,116, 107,125,107,125 };
BYTE BColor[] = { 10,20,41,51,69,80,99,110,129,140,161,185,200,215,230,245 };
BYTE No_Tris,NumTris = 0,OldNumTris;
BYTE ArrayTris[350],ColorTris = 6,NewColorTris,NewTris;
BYTE Num[]={  /* 0 - 9 */
 14,25,21,19,14, 8,12,8,8,8, 15,16,14,1,31, 15,16,14,16,15,
 12,10,9,31,8, 15,1,15,16,15, 14,1,15,17,14, 31,16,8,4,4,
 14,17,14,17,14, 14,17,30,16,14 };
int YourScore = 0;
int XTris,YTris,Ganx = 62,Gany = 10,DelayGY = 0,MAXDelay = 12;

void ClearBackTris(int page)
{
	int i,j;
	char far *ptr0, far *ptr1;
	ptr0 = FirstAdr[page] + 1;
	ptr1 = FirstAdr[3] + 1;
	outport(0x3ce,0x4105); outport(0x3c4,0xf02);
	for(j = 0;j < 195;j++)
	{
		for(i = 0;i < 33;i++) *ptr0++ = *ptr1++;
		ptr0 += 47; ptr1 += 47;
	}
	outport(0x3ce,0x4005);
}
void PrintNum(int x,int y,int n,BYTE color)
{
	int i,j,x1;
	BYTE *ptr;
	for(j = 0,ptr = Num + n * 5; j < 5; j++,y++,ptr++)
		for(i = 0,x1 = x;i < 5;i++,x1++)
			if((*ptr >> i) & 1) PutPixel(x1,y,color);
}
void PrintScore(void)
{
	int i = 0;
	char str[12];
	itoa(YourScore,str,10);
	while(str[i])
		PrintNum((i << 2) + (i << 1) + 150,45,str[i++] - '0',224);
}
void PutBlock(int x,int y,BYTE color)
{
	Bar(x + 2,y + 2,x + 7,y + 6,color - 1);
	Vline(x,x + 8,y,color + 3); Vline(x + 1,x + 7,y + 1,color + 1);
	Hline(x,y,y + 7,color + 3); Hline(x + 1,y + 1,y + 6,color + 1);
	Vline(x,x + 8,y + 7,color - 4); Vline(x + 1,x + 7,y + 6,color - 3);
	Hline(x + 8,y,y + 7,color - 5); Hline(x + 7,y + 1,y + 6,color - 3);
}
void PBlockTris(int x,int y,BYTE num,BYTE n,BYTE color)
{
	char *ptr,i;
	ptr = TypeTris[num] + (n << 3);
	for(i = 0;i < 4;i++)
	{
		PutBlock(x + *ptr * 9,y + (*(ptr + 1) << 3),BColor[color]);
		ptr+=2;
	}
}
void SetTris(BYTE num,BYTE color)
{
	int i;
	char *ptr;
	YTris--;
	ptr = TypeTris[num] + (NumTris << 3);
	for(i = 0;i < 4;i++)
	{
		ArrayTris[XTris + *ptr + (YTris + *(ptr + 1)) * 14] =
			BColor[color];
		ptr += 2;
	}
}
BYTE CheckTris(BYTE num)
{
	int i,Y;
	char *ptr;
	ptr = TypeTris[num] + (NumTris << 3);
	for(i = 0;i < 4;i++)
	{
		Y = YTris + *(ptr + 1);
		if(ArrayTris[Y * 14 + *ptr + XTris] != 0 || Y > 23)
			return(1);
		ptr+=2;
	}
	return(0);
}
BYTE *BKdata;  /* data picture */
void SetBackground(float k)
{
	int i,j;
	BYTE pl1,pl2,color,*ptr0;
	pl1 = 48+(sin(k / 30) * 47.0 + 256 * (int)(47 * cos(k / 40)));
	pl2 = 48+(sin(k / 14) * 47.0 + 256 * (int)(47 * sin(k / 32))) - pl1;
	ptr0 = BKdata + pl1;
	for(j = 0;j < 100;j++)
	{
		for(i = 0;i < 90;i++)
		{
			color = ((*ptr0++) + pl2);
			PutPixel(i + 142,j,color);
			PutPixel(320 - i,j,color);
			PutPixel(i + 142,199 - j,color);
			PutPixel(320 - i,199 - j,color);
		}
		ptr0 += 166;
	}
}
void InitBKdata(void)
{
	float x,y;
	BKdata = malloc(256 * 200);
	for (x = 0; x < 256; x++)
		for (y = 0; y < 200; y++)
			BKdata[y * 256 + x] = 6 * (sin(0.00284 * x * y) +
				cos(x / 20) + sin(y / 16));
}
void InitScreen(void)
{
	int i,color;
	SetActivePage(3);
	SetBackground(random(32767));
	color = BColor[random(16)];
	for(i = 0;i < 4;i++)
	{
		Rectangle(i,i,141 - i,200 - i,color + i);
		Rectangle(7 - i,7 - i,134 + i,193 + i,color + i);
	}
	Rectangle(144,0,193,34,232); Rectangle(147,2,191,32,232);
	Rectangle(145,0,192,33,233); Rectangle(146,1,192,33,233);
	Rectangle(145,40,193,54,248);
	Bar(8,7,134,194,0); Bar(146,41,193,54,0); Bar(147,2,191,32,0);
}
void CheckLine(BYTE Page)
{
	int i,j,check;
	BYTE *ptr,*ptr1,Line = 0;
	ptr = ArrayTris;
	for (i = 0; i < 10; i++){
		sound(10 * random(200) + 500); delay(8); }
	nosound();
	for(i = 0;i < 25;i++)
	{
		check = 0;
		ptr += 14;
		for(j = 0;j < 14;j++)
		{
			if(ArrayTris[i * 14 + j] == 0)
			{
				check = 1; break;
			}
		}
		if(check == 0)
		{
			Line++; YourScore++;
			SetActivePage(Page); SetVisualPage(Page);
			for(j = 0;j < 14;j++)
			{
				sound(40 * j + 900); delay(30); nosound();
				PutBlock(j * 9 + 8,(i << 3) + 2,
						BColor[ColorTris]);
			}
			ptr1 = ptr - 14;
			for(j = 0;j < i;j++)	/* move mem array */
			{
				memcpy(ptr1,ptr1 - 14,14);
				ptr1 -= 14;
			}
		}
	}
	if( Line )
	{
		InitScreen();
		for(i = 1;i < 25;i++)
		{
			for(j = 0;j < 14;j++)
				if(ArrayTris[i * 14 + j])
					PutBlock(j * 9 + 8,(i << 3) + 2,
						ArrayTris[i * 14 + j]);
		}
		CopyPage(0,3); CopyPage(1,3);
	}
	SetActivePage(Page); SetVisualPage(1 - Page);
}
void main(void)
{
	int i;
	BYTE Nt,Page = 0,G_Over = 0;
	printf("COMPUTER TIME Tetris Version 1.0\n");
	NewIntkey();
	randomize();
	delay(0);	/* clear function delay() */
	InitBKdata();
	memset(ArrayTris,0,350);
	SetModeX();
	SetNewPAL();
	No_Tris = random(7); NewTris = random(7);
	NewColorTris = random(16);
	InitScreen();
	PBlockTris(161,6,NewTris,0,NewColorTris);
	PrintScore();
	CopyPage(0,3); CopyPage(1,3);
	while(!(KEY.Esc || G_Over))
	{
		SetActivePage(Page); SetVisualPage(1 - Page);
		ClearBackTris(Page);
		if(KEY.UpArrow)
		{
			KEY.UpArrow = 0;
			OldNumTris = NumTris;
			if(++NumTris > 3) NumTris = 0;
			if(CheckTris(No_Tris)) NumTris = OldNumTris;
		}
		Nt = NumTris + (No_Tris << 2);
		if(KEY.LeftArrow && Ganx > L_Tris[Nt])
		{
			KEY.LeftArrow = 0;
			XTris-- ;
			if(!CheckTris(No_Tris)) Ganx -= 9;
		}
		if(KEY.RightArrow && Ganx < R_Tris[Nt] )
		{
			KEY.RightArrow = 0;
			XTris++;
			if(!CheckTris(No_Tris)) Ganx += 9;
		}
		if(KEY.Space || KEY.DownArrow)	DelayGY = MAXDelay;
		if(Ganx <= L_Tris[Nt])  Ganx = L_Tris[Nt];
		if(Ganx >= R_Tris[Nt])  Ganx = R_Tris[Nt];
		PBlockTris(Ganx,Gany,No_Tris,NumTris,ColorTris);
		if(++DelayGY > MAXDelay)  /* Set Speed */
		{
			DelayGY	= 0; Gany += 8;
		}
		XTris = (Ganx - 7) / 9; YTris = ((Gany - 10) >> 3) + 1;
		if(CheckTris(No_Tris))
		{
			KEY.DownArrow = 0;
			SetTris(No_Tris,ColorTris);
			SetActivePage(3);
			PBlockTris(Ganx,Gany - 8,No_Tris,NumTris,ColorTris);
                        CheckLine(Page);
			Ganx = 62; Gany = 10; NumTris = 0;
			No_Tris = NewTris; NewTris = random(7);
			ColorTris = NewColorTris;
			NewColorTris = random(16);
			Bar(146,41,193,54,0); Bar(147,2,191,32,0);
			PBlockTris(161,6,NewTris,0,NewColorTris);
			PrintScore();
			CopyPage(1 - Page,Page);
			for(i = 0;i < 14;i++)
				if(ArrayTris[i] != 0) G_Over = 1;
		}
		Page = 1 - Page;
	}
	TextMode();
	SetOldkey();
	printf("... GAME OVER ...\n");
	printf("... Your Score %d Line ...\n",YourScore);
}