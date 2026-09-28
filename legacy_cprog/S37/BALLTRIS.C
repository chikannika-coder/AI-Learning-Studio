/* game balltris.c 24 bit color */
/* program by 3D Engine */
#include "vesa24.c"
/* Keyboard new interrupt number 9 handler */
struct Keyboard { /* Keyboard input structure. */
	char Right, Left, Up, Down, Space,Esc;
} KEY;
void interrupt (*OldKeyVec)(void);
void interrupt NewKeyInt(void)
{
     BYTE ch, ScanCode;
     ScanCode = inp(0x60); ch = inp(0x61);
     outp(0x61, (ch | 0x80)); outp(0x61, ch);
     outp(0x20, 0x20);
     if(ScanCode == 77)  KEY.Right = 1;
     if(ScanCode == 205) KEY.Right = 0;
     if(ScanCode == 72)  KEY.Up    = 1;
     if(ScanCode == 200) KEY.Up    = 0;
     if(ScanCode == 75)  KEY.Left  = 1;
     if(ScanCode == 203) KEY.Left  = 0;
     if(ScanCode == 80)  KEY.Down  = 1;
     if(ScanCode == 208) KEY.Down  = 0;
     if(ScanCode == 57)  KEY.Space = 1;
     if(ScanCode == 185) KEY.Space = 0;
     if(ScanCode == 1)   KEY.Esc   = 1;
}
#define NewIntkey() { OldKeyVec = getvect(9); \
		      setvect(9, NewKeyInt); }
#define SetOldkey() setvect(9, OldKeyVec)

BYTE GumBall[] = {  24, 24,
    0,  0,  0,  0,  0,  0,  0, 22, 25, 30, 36, 35, 34, 30, 28, 25, 20,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0, 22, 35, 39, 45, 45, 44, 41, 39, 37, 35, 32, 31, 25, 18,  0,  0,  0,  0,  0,
    0,  0,  0,  0, 28, 39, 44, 46, 46, 45, 44, 42, 41, 39, 38, 36, 33, 28, 27, 18,  0,  0,  0,  0,
    0,  0,  0, 32, 42, 45, 48, 48, 46, 45, 44, 43, 42, 40, 39, 38, 35, 32, 28, 25, 20,  0,  0,  0,
    0,  0, 28, 40, 45, 46, 48, 46, 46, 46, 45, 44, 42, 41, 40, 39, 37, 34, 31, 27, 25, 18,  0,  0,
    0, 25, 36, 43, 46, 48, 46, 46, 46, 47, 46, 44, 43, 41, 40, 40, 39, 36, 33, 29, 25, 23, 16,  0,
    0, 33, 41, 46, 48, 47, 46, 48, 53, 52, 47, 44, 43, 42, 41, 40, 39, 36, 33, 29, 26, 23, 20,  0,
   22, 36, 46, 47, 47, 47, 46, 55, 57, 56, 48, 43, 42, 42, 41, 41, 38, 36, 32, 29, 26, 24, 20, 16,
   25, 38, 46, 47, 47, 46, 46, 56, 59, 58, 49, 43, 43, 42, 41, 40, 38, 36, 32, 29, 26, 25, 21, 16,
   30, 41, 44, 46, 45, 45, 47, 50, 53, 52, 47, 43, 42, 41, 40, 39, 37, 35, 32, 29, 27, 25, 22, 17,
   33, 41, 45, 45, 44, 44, 44, 45, 48, 45, 43, 43, 42, 41, 40, 38, 36, 34, 31, 29, 27, 25, 23, 18,
   33, 41, 45, 44, 43, 43, 42, 43, 43, 43, 43, 42, 41, 40, 39, 37, 36, 33, 31, 29, 27, 25, 24, 19,
   30, 38, 42, 43, 41, 42, 41, 42, 41, 42, 43, 42, 41, 40, 38, 37, 35, 33, 31, 29, 27, 25, 24, 18,
   26, 36, 41, 41, 41, 41, 40, 41, 41, 41, 42, 41, 40, 39, 37, 36, 34, 32, 30, 28, 27, 26, 23, 18,
   23, 33, 39, 41, 40, 40, 40, 40, 41, 40, 40, 40, 39, 37, 36, 34, 32, 30, 29, 27, 26, 25, 22, 17,
   18, 33, 36, 38, 39, 39, 39, 40, 39, 39, 38, 38, 36, 35, 33, 32, 30, 29, 28, 27, 26, 24, 21, 15,
   16, 27, 35, 36, 38, 38, 38, 38, 38, 38, 36, 35, 34, 33, 31, 31, 29, 29, 28, 27, 25, 23, 20, 13,
    0, 18, 30, 33, 35, 35, 36, 35, 35, 35, 34, 33, 32, 31, 30, 29, 29, 29, 28, 27, 25, 23, 16,  0,
    0,  0, 24, 28, 31, 33, 33, 33, 32, 32, 31, 31, 31, 30, 29, 29, 29, 29, 28, 26, 24, 18, 13,  0,
    0,  0, 16, 25, 28, 29, 30, 30, 30, 29, 29, 29, 29, 29, 28, 29, 29, 28, 27, 24, 18, 13,  0,  0,
    0,  0,  0, 16, 24, 26, 28, 28, 28, 28, 27, 27, 27, 28, 27, 27, 26, 26, 24, 18, 13,  0,  0,  0,
    0,  0,  0,  0, 15, 22, 24, 24, 25, 26, 26, 25, 27, 26, 26, 25, 24, 21, 16, 13,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0, 15, 20, 22, 24, 23, 22, 23, 23, 24, 20, 18, 14, 13,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0, 13, 14, 15, 16, 15, 14, 14, 13, 12,  0,  0,  0,  0,  0,  0,  0
   };

IMAGE img[12];
BYTE Apal[] = { /* value ball color num = 0 - 4 */
	4,0,0, 0,4,0, 0,0,4, 4,4,0, 3,1,4, 4,1,3,
	4,4,4,  0,4,3, 4,2,0, 2,2,1,  0,2,0, 1,2,3
};
#define MAXDELAY 300
BYTE *Back[10][19];
int nBaray[3], Baray[3];
int Gx, Gy, oGx, oGy;
int Delay = MAXDELAY;
int MAP[10][19];
int SCORE = 0;
int Level = 3;
void setballcolor(IMAGE *img, int r, int g, int b)
{
	int i;
	img->width = img->height = 24;
	img->IMG = GumBall + 2;
	for(i = 0; i < 192; i += 3) {	/* 64*3 */
		img->pal[i]   = (i / 3) * r;
		img->pal[i + 1] = (i / 3) * g;
		img->pal[i + 2] = (i / 3) * b;
	}
}
void RecRGB(int x0, int y0, int x1, int y1, int r, int g, int b)
{
	int i;
	for(i = x0; i <= x1; i++) {
		putpixelrgb(i, y0, r, g, b);
		putpixelrgb(i, y1, r, g, b);
	}
	for(i = y0; i < y1; i++) {
		putpixelrgb(x0, i, r, g, b);
		putpixelrgb(x1, i, r, g, b);
	}
}
void BarRGB(int x0, int y0, int x1, int y1, int r, int g, int b)
{
	int i, j;
	for(j = y0; j < y1; j++)
		for(i = x0; i < x1; i++)
			putpixelrgb(i, j, r, g, b);

}
void initball(void)
{
	int i, j;
	BYTE r, g, b;
	BYTE *ptr = Apal;
	for(i = 0; i < 12; i++) {
		r = *ptr++;
		g = *ptr++;
		b = *ptr++;
		setballcolor(&img[i], r, g, b);
	}
	for(i = 0; i < 10; i++)
		RecRGB(i, i, 262 - i, 479 - i, i * 20 + 75, 0, i*10);
	for(i = 0; i < 5; i++)
		RecRGB(i + 264, i, 299 - i, 85 - i, 0, 0, i * 20 + 80);

	for(j = 10; j < 470; j++)
		for(i = 10; i < 253; i++){
			getpixelrgb(i, j, &r, &g, &b);
			putpixelrgb(i, j, r/3, g/3, b/3);
		}
	for(j = 0; j < 10; j++)
		for(i = 0; i < 19; i++){
			MAP[j][i] = 255;
			Back[j][i] = getimagergb(j * 24 + 12,i * 24 + 13,
				j * 24 + 36, i * 24 + 37);
		}
	for(i = 0; i < 3; i++)
		nBaray[i] = random(Level);
	Gx = oGx = 5;
	Gy = oGy = 0;
}

void getballary(void)
{
	int i;
	static Line = 0;
    if(++Line > 10){
		Line = 0;
		for(i = 0; i < 3; i++)
			Baray[i] = nBaray[i];
		nBaray[0] = nBaray[1] = nBaray[2] = random(Level);
	}
	else
	for(i = 0; i < 3; i++){
		Baray[i] = nBaray[i];
		nBaray[i] = random(Level);
	}
	for(i = 0; i < 3; i++)
		Putimage24(270, i * 24 + 7, &img[nBaray[i]]);
}
void Clearblock(void)
{
	int i;

	for(i = 0; i < 3; i++)
		putimagergb(oGx * 24 + 12, (oGy + i) * 24 + 13,
			Back[oGx][oGy + i]);
}
int CheckGx(int j)
{
	int i;
	for(i = 0; i < 3; i++) {
		if(MAP[j][i + Gy] != 255)
			return(0);
	}
	return(1);
}
int CheckGy(void)
{
	int i;
	for(i = 0; i < 3; i++) {
		if(MAP[Gx][Gy + i] != 255)
			return(1);
	}
	return(0);
}
void puthline(int i, int j)
{
	if(MAP[i][j] == 255)
		putimagergb(i * 24 + 12, j * 24 + 13,
			Back[i][j]);
	else
		Putimage24(i * 24 + 12,	j * 24 + 13, &img[MAP[i][j]]);
}

void bubble(int i, int j)
{
	int k;
	if(i > 9 || j > 19) return;
	for(k = j; k > 1 ; k--)
		MAP[i][k] = MAP[i][k - 1];
	for(k = 0; k < 10; k++)
		MAP[k][0] = 255;
	for(k = 0; k < 19; k++){
		if(MAP[i][k] == 255)
			putimagergb(i * 24 + 12, k * 24 + 13,
				Back[i][k]);
		else
			Putimage24(i * 24 + 12,	k * 24 + 13, &img[MAP[i][k]]);
	}
	for(i = 1; i < 40; i++){
		sound(1500 * i);
		delay(20);
	}
	nosound();
	SCORE ++;
}
int checkline(int i, int j)
{
	int ch;

	ch = MAP[i][j];
	if(j < 15 && ch == MAP[i][j + 1] && ch == MAP[i][j + 2] &&
		ch == MAP[i][j + 3] && ch == MAP[i][j + 4])
		return(3);	/* 5 line horizontal */
	if(j < 16 && ch == MAP[i][j + 1] && ch == MAP[i][j + 2] &&
		ch == MAP[i][j + 3] )
		return(2);	/* 4 line horizontal */
	if(j < 17 && ch == MAP[i][j + 1] && ch == MAP[i][j + 2] && j < 18 )
		return(1);

	if(i < 6 && ch == MAP[i + 1][j] && ch == MAP[i + 2][j] &&
		ch == MAP[i + 3][j] && ch == MAP[i + 4][j])
		return(6); /* 5 line vertical */
	if(i < 7 && ch == MAP[i + 1][j] && ch == MAP[i + 2][j] &&
		ch == MAP[i + 3][j])
		return(5); /* 4 line vertical */
	if(i < 8 && ch == MAP[i + 1][j] && ch == MAP[i + 2][j])
		return(4); /* 3 line verticle */

	if(i < 6 && j < 15 && ch == MAP[i + 1][j + 1] &&
		ch == MAP[i + 2][j + 2] && ch == MAP[i + 3][j + 3] &&
		ch == MAP[i + 4][j + 4])
		return(9);
	if(i < 7 && j < 16 && ch == MAP[i + 1][j + 1] &&
		ch == MAP[i + 2][j + 2] && ch == MAP[i + 3][j + 3])
		return(8);
	if(i < 8 && j < 17 && ch == MAP[i + 1][j + 1] &&
		ch == MAP[i + 2][j + 2])
		return(7);

	if(i > 3 && j < 15 && ch == MAP[i - 1][j + 1] &&
		ch == MAP[i - 2][j + 2] && ch == MAP[i - 3][j + 3] &&
		ch == MAP[i - 4][j + 4])
		return(12);
	if(i > 2 && j < 16 && ch == MAP[i - 1][j + 1] &&
		ch == MAP[i - 2][j + 2] && ch == MAP[i - 3][j + 3])
		return(11);
	if(i > 1 && j < 17 && ch == MAP[i - 1][j + 1] &&
		ch == MAP[i - 2][j + 2])
		return(10);
	else
		return(0);
}
void checkdown(void)
{
	int i, j, k, ch;
	for(j = 0; j < 19; j++) {
		for(i = 0; i < 10; i++){
			if(MAP[i][j] != 255){
				ch = checkline(i, j);
				if(ch > 0 && ch < 4)
					for(k = 0; k < ch + 2; k++)
						bubble(i, j + k);
				if(ch > 3 && ch < 7)
					for(k = 0; k < ch - 1; k++)
						bubble(i + k, j);
				if(ch > 6 && ch < 10)
					for(k = 0; k < ch - 4; k++)
						bubble(i + k, j + k);
				if(ch > 9 && ch < 13)
					for(k = 0; k < ch - 7; k++)
						bubble(i - k, j + k);
			}
		}
	}
}

void main(void)
{
	int i, j;

	randomize();
	do {
		clrscr();
		printf("<--- BALLTRIS --->\n");
		printf("input level color (3 - 12 color)\n< -- key '0' - '9' -- > : ");
		Level = getch() - '0';
	} while(Level < 0 || Level > 9);
	printf("%d",Level);
	Level += 3;
	initvesa();
	ShowTGA(0,0,"BALLTRIS.TGA");
	initball();
	NewIntkey();
	getballary();
	while(!KEY.Esc) {
		if(KEY.Right && Gx < 9 && CheckGx(Gx + 1)){
			Gx++;
			KEY.Right = 0;
		}
		if(KEY.Left && Gx > 0 && CheckGx(Gx - 1)){
			Gx--;
			KEY.Left = 0;
		}
		if(KEY.Up){	/* change color ball */
			i = Baray[0];
			Baray[0] = Baray[1];
			Baray[1] = Baray[2];
			Baray[2] = i;
			for(i = 0; i < 3; i++)
				Putimage24(Gx * 24 + 12,(Gy + i) * 24 + 13,
					&img[Baray[i]]);
			KEY.Up = 0;
		}
		if(KEY.Down && Gy < 16){
			Delay = 0;
			Gy++;
		}
		if(Gy > 16 || CheckGy()){
			for(i = 0; i < 3; i++) {
				MAP[Gx][Gy + i - 1] = Baray[i];
			}
			Gy = oGy = 0;
			Gx = oGx = 5;
			getballary();

			for(i = 0; i < 10; i++){
				if(MAP[i][0] != 255){
					KEY.Esc = 1;
					for(j = 0; j < 3; j++)
						Putimage24(Gx * 24 + 12,(Gy + j) * 24 + 13,
							&img[Baray[j]]);
					break;
				}
			}
		}
		if(Gx != oGx || Gy != oGy){
			Clearblock();
			for(i = 0;i < 3; i++)
				Putimage24(Gx * 24 + 12, (Gy + i) * 24 + 13,
					&img[Baray[i]]);
			oGx = Gx;
			oGy = Gy;
			while   (inp(0x3da) & 8);
			while (!(inp(0x3da) & 8));
		}
		if(Delay-- < 0) {
			Delay = MAXDELAY;
			Gy ++;
		}
		checkdown();
		delay(8);
	}
	SetOldkey();
	Textmode();
	gotoxy(30, 10);
	printf("--- GAME OVER ---");
	gotoxy(24, 12);
	printf("YOUR SCORE = %8d0   POINT\n",SCORE);
}