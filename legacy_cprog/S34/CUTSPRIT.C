
/* --- Computer Time C Programming --- */
/* --- CUTSPRIT.C code by  3D Engine --- */
#include <stdio.h>
#include <conio.h>
#include <dos.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
typedef unsigned char BYTE;
char far *PageStart = (char far *) MK_FP(0xa000, 0);
unsigned int LINE_Y[200];
#define TextMode() {_AX = 3; geninterrupt(0x10);}
void InitGmode(void)
{
	int i;
	_AX = 0x13;
	geninterrupt(0x10);
	for(i = 0;i < 200; i++)
		LINE_Y[i] = i * 320;
}
void PutPixel(int x, int y, BYTE color)
{	/* put pixel */
	if(x < 0 || x > 319 || y < 0 || y > 199) return;
	*(PageStart + LINE_Y[y] + x ) = color;
}
BYTE GetPixel(int x, int y)
{	/* get pixel */
     return *(PageStart + LINE_Y[y] + x );
}
void Bar(int x0, int y0, int x1, int y1, int color)
{	/* color bar */
     int i, j;
     for(j = y0; j < y1; j++)
	     for(i = x0; i < x1; i++)
		     PutPixel(i, j, color);
}
void Rec(int x0, int y0, int x1, int y1, int color)
{	/* rectangle */
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
void Putimgmem(BYTE *ptr0,BYTE *ptr1)
{	/* put mem image sprite */
	int i, j, x1, y1;

	*ptr1++ = x1 = *ptr0++;
	*ptr1++ = y1 = *ptr0++;
	for(j = 0; j < y1; j++)
		for(i = 0; i < x1; i++, ptr0++, ptr1++){
			if(*ptr0 && i >= 0 && i < 320 &&
				j >= 0 && j < 200 ) {
				*ptr1 = *ptr0;
			}
		}
}
void PutImg(int x0, int y0, BYTE *ptr)
{
	int i, j, x1, y1;
	x1 = x0 + *ptr++; y1 = y0 + *ptr++;
	for(j = y0; j < y1; j++)
		for(i = x0; i < x1; i++, ptr++)
			if(i >= 0 && i < 320 &&
				j >= 0 && j < 200 )
			*(PageStart + LINE_Y[j]  + i ) = *ptr;
}
void GetImg(int x0, int y0,  int x1, int y1, BYTE *ptr)
{	/* get mem screen to mem image sprite */
	int i, j;
	*ptr++ = x1 - x0; *ptr++ = y1 - y0;
	for(j = y0; j < y1; j++)
		for(i = x0; i < x1; i++)
			*ptr++ = GetPixel(i, j);
}

BYTE Inkey (void)
{       /* Easy key input no wait */
	_DL = 255;
	_AH = 6;
	geninterrupt(0x21);
	return(_AL);
}

/* new mouse function */
/*************************************************
 Initialize the mouse.
 Returns 1 if the mouse exists, 0 if it doesn't.
**************************************************/
#define SIZEMX 11
#define SIZEMY 14
#define MEMSIZE 156
int MouseX, MouseY, oMouseX, oMouseY;
int mousebutt, StMouse = 2;
BYTE MouseT[MEMSIZE], MouseT1[MEMSIZE];
BYTE Cursor[] = {	/* bitmap cursor */
   11, 14,
  255,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
  255,255,  0,  0,  0,  0,  0,  0,  0,  0,  0,
  255,255,255,  0,  0,  0,  0,  0,  0,  0,  0,
  255,255,255,255,  0,  0,  0,  0,  0,  0,  0,
  255,255,255,255,255,  0,  0,  0,  0,  0,  0,
  255,255,255,255,255,255,  0,  0,  0,  0,  0,
  255,255,255,255,255,255,255,  0,  0,  0,  0,
  255,255,255,255,255,255,255,255,  0,  0,  0,
  255,255,255,255,255,255,255,255,255,  0,  0,
  255,255,255,255,255,255,255,255,255,255,  0,
  255,255,255,255,255,255,255,255,255,255,255,
  255,255,255,  0,  0,  0,  0,  0,  0,  0,  0,
  255,255,  0,  0,  0,  0,  0,  0,  0,  0,  0,
  255,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
};

int IniMouse(void)
{	/* set and check mouse */
	union REGS r;
	r.x.ax = 0;
	int86( 0x33, &r, &r );
	if( r.x.ax ) {	/* get mouse driver */
		r.x.ax = 7;	/* setmouse gan x */
		r.x.cx = 0;	/* left */
		r.x.dx = 1276;	/* right */
		int86(0x33,&r,&r);
		r.x.ax = 8;	/* set mouse gan y */
		r.x.cx = 0;	/* up */
		r.x.dx = 796;	/* down */
		int86(0x33,&r,&r);
		r.x.ax = 0x1c;	/* hide mouse */
		r.x.bx = 1;
		int86( 0x33, &r, &r );
		return 1;
	}
	return 0;
}

/*********************************************
 Returns the mouse status. gan x gan y
 and its button status is returned in 'b'.
**********************************************/
void GetMouseInfo( int *x, int *y, int *b )
{
	union REGS r;
	if(StMouse == -1) return;
	r.x.ax = 3;
	int86( 0x33, &r, &r );
	*b = r.x.bx;
	*x = r.x.cx >> 2;
	*y = r.x.dx >> 2;
}

void CloseMouse(void)
{	/* clear mouse */
	union REGS r;
	r.x.ax = 0;
	int86( 0x33, &r, &r );
}

void MoveMouse(int x, int y)
{	/* set mouse position */
	union REGS r;
	if(StMouse == -1) return;
	r.x.dx = y << 2;
	r.x.cx = x << 2;
	r.x.ax = 4;
	int86( 0x33, &r, &r );
}

void PutMouse(void)
{
	if(StMouse  < 1) return;
        GetMouseInfo(&MouseX, &MouseY, &mousebutt);
	if(MouseX != oMouseX || MouseY != oMouseY || StMouse == 2){
		PutImg(oMouseX, oMouseY, MouseT1);
		GetImg(MouseX, MouseY, MouseX + SIZEMX,
			MouseY + SIZEMY, MouseT);
		memcpy(MouseT1, MouseT, MEMSIZE);
		Putimgmem(Cursor, MouseT);
		PutImg(MouseX, MouseY, MouseT);
		oMouseX = MouseX;
		oMouseY = MouseY;
                StMouse = 1;
		while   (inp(0x3da) & 8) ;
		while (!(inp(0x3da) & 8)) ;
	}
}

void HideMouse(void)
{
	if(StMouse == -1) return;
	StMouse = 0;
	PutImg(oMouseX, oMouseY, MouseT1);
}

void ShowMouse(void)
{
	if(StMouse == -1) return;
	StMouse = 2;
	GetImg(oMouseX, oMouseY, oMouseX + SIZEMX,
		oMouseY + SIZEMY, MouseT);
	memcpy(MouseT1, MouseT, MEMSIZE);
}

void InitMouse(void)
{
	if(!IniMouse()) {
		StMouse = -1;
		return;
	}
	MoveMouse(0, 0);
	oMouseX = MouseX = 0;
	oMouseY = MouseY = 0;
	GetImg(oMouseX, oMouseY, oMouseX + SIZEMX,
		oMouseY + SIZEMY, MouseT);
	memcpy(MouseT1, MouseT, MEMSIZE);
	PutMouse();
}

BYTE Palette[768];
BYTE *Image;
BYTE *Back[2];
char namefile[] = "IMAGE00.C";
int Numi = 0, Post = 0;

void SetPalette(BYTE *Pal)
{
	int i;
	BYTE *ptr;
	ptr = Pal;
	outp(0x3c8, 0);
	for (i = 0; i < 256; i++) {
		outp(0x3c9, *ptr++);
		outp(0x3c9, *ptr++);
		outp(0x3c9, *ptr++);
	}
}

int ShowPCX(char *name)
{
	FILE *fp;
	typedef struct {
		char manufacturer;
		char version;
		char encoding;
		char BitsPerPixel;
		int x1;
		int y1;
		int x2;
		int y2;
		int hres;
		int vres;
	/* -------  not user ---------*/
	/*	char palette[48];
		char reserved;
		char colour_planes;
		int BytesPerLine;
		int PaletteType;
		char filler[58]; */
	} PCXHEADER;
	PCXHEADER Header;
	int WWidth, WHeight, i, j;
	BYTE *Membuf, *wptr;
	char far *ptr;
	BYTE c, l;

	if((fp = fopen(name, "rb")) == NULL)
		return(0);
	fread(&Header, 16, 1, fp);
	/* Read and set the palette */
	fseek(fp, -768L, SEEK_END);
	fread(Palette, 768, 1, fp);
	for (i = 0; i < 768; i++)
		Palette[i] >>= 2;
	SetPalette(Palette);
	fseek(fp, 128, SEEK_SET);
	WHeight = Header.vres;
	WWidth  = Header.hres;
	Membuf = malloc(WHeight * WWidth);
        wptr = Membuf;
	for (i = 0; i < WHeight; i++) {
		j = 0;
		while(j < WWidth) {
			if((c = fgetc(fp)) > 191) {
				l = c - 192;
				c = fgetc(fp);
				memset(wptr, c, l);
				wptr += l;
				j += l;
			}
			else {
				*wptr++ = c;
				j++;
			}
		}
	}
	fclose(fp);
	ptr = PageStart;
	wptr = Membuf;
	for(i = 0; i < WHeight; i++) {
		memcpy(ptr, wptr, WWidth);
		ptr += 320;
		wptr += WWidth;
	}
	free(Membuf);
	return(1);
}

void PNum(int x, int y, int n, int color)
{	/* print Number at x, y position */
	static BYTE Num[] = { /* 0 - 9 */
	14,25,21,19,14, 8,12,8,8,8, 15,16,14,1,31, 15,16,14,16,15,
	12,10,9,31,8, 15,1,15,16,15, 14,1,15,17,14, 31,16,8,4,4,
	14,17,14,17,14, 14,17,30,16,14	};
	int i, j, x1;
	BYTE *ptr;
	for(j = 0, ptr = Num + n * 5; j < 5; j++, y++, ptr++)
		for(i = 0, x1 = x; i < 5; i++, x1++)
			if((*ptr >> i) & 1) PutPixel(x1, y, color);
}

void PrintNum(int x, int y, int SCORE)
{
	char str[10];
	int i = 0;

	itoa(SCORE, str, 10);
	Bar(x, y, x + 18, y + 8, 0);
	do {
		PNum(i * 6 + x, y, str[i] - '0', 255);
	} while(str[++i]);
}

void BlockCut(void)
{
	int FGx, FGy, oGx, oGy;

	oGx = FGx = MouseX;
	oGy = FGy = MouseY;
	HideMouse();
	GetImg(FGx, FGy, FGx + 1, FGy + 1, Image);
	ShowMouse();
	while(mousebutt != 0){
		HideMouse();
		PutImg(FGx, FGy, Image);
		if(mousebutt > 1) {
			ShowMouse();
			return;
		}
		GetImg(FGx, FGy, oGx, oGy, Image);
		Rec(FGx, FGy, oGx - 1, oGy - 1, 255);
                PrintNum(130, 194, Image[0]);
		PrintNum(160, 194, Image[1]);
		PrintNum(270, 194, oGx);
		PrintNum(300, 194, oGy);
		ShowMouse();
		oGx = MouseX;
		oGy = MouseY;
		if(oGx <= FGx)
			oGx  = FGx + 1;
		if(oGy <= FGy)
			oGy  = FGy + 1;
		if((oGx - FGx) > 255)
			oGx = 255;
		PutMouse();
		delay(100);
	}
	HideMouse();
	PutImg(FGx, FGy, Image);
	if(FGx > 160) {
		PutImg(1, 1, Image);
		Rec(0, 0, 1 + Image[0], Image[1] + 1, 255);
		Post = 0;
	}
	else {
		PutImg(161, 1, Image);
		Rec(160, 0, 161 + Image[0], Image[1] + 1, 255);
		Post = 1;
	}
	ShowMouse();
}

void SaveFile(void)
{
	FILE *fp;
	BYTE *ptr;
        BYTE red, green, blue;
	int i, j, width, height;

	sound(1000);
	fp  = fopen(namefile, "wt");
	ptr = Image;
	width  = *ptr++;
	height = *ptr++;
	fprintf(fp, "BYTE Bitmap%d[] = { %3d,%3d,\n  ",
			Numi, width, height);
	for(j = 0; j < height; j++) {
		for(i = 0; i < width; i ++) {
			fprintf(fp, "%3d", *ptr++);
			if((i == width - 1) && (j == height - 1));
			else
				fprintf(fp, ",");
		}
		fprintf(fp, "\n  ");
	}
	fprintf(fp," };\n\n");
	ptr = Palette;
	fprintf(fp, "BYTE Palette[] = {\n  ");
	for(j = 0; j < 64; j++) {
		for(i = 0; i < 4; i++){
			red   = *ptr++;
			green = *ptr++;
			blue  = *ptr++;
			fprintf(fp, " %3d,%3d,%3d",
				red, green, blue);
			if((i == 3) && (j == 63));
			else
				fprintf(fp, ",");
		}
        	fprintf(fp,"\n  ");
	}
	fprintf(fp, " };\n");
	fclose(fp);
	nosound();
	if(namefile[6] == '9' && namefile[5] == '9')
		return;
	if(++namefile[6] > '9' && namefile[5] < '9') {
		namefile[5]++;
		namefile[6] = '0';
	}
	Numi++;
}

void main(int agc, char *agv[])
{
	BYTE ch, i = 0;

	if(agc == 1) {
		printf("type CUTSPRIT [Filename.pcx] to run\n");
		exit(0);
	}
	InitGmode();
	if(!ShowPCX(agv[1])){
		TextMode();
		printf("File %s not found.\n", agv[1]);
		exit(0);
	}
	Image   = malloc(256 * 200 + 2);
	Back[0] = malloc(160 * 200 + 2);
	Back[1] = malloc(160 * 200 + 2);
	GetImg(0, 0, 160, 200, Back[0]);
	GetImg(160, 0, 320, 200, Back[1]);
	InitMouse();
	while((ch = toupper(Inkey())) !=27 ) {
		if(mousebutt == 1 ) {
			if(i++ > 0) {
				HideMouse();
				if(Post == 0)
					PutImg(0, 0, Back[0]);
				else
					PutImg(160, 0, Back[1]);
				ShowMouse();

			}
			BlockCut();
			mousebutt = 0;
		}
		if(mousebutt == 2 || ch == 32 ) {
			HideMouse();
                        PutImg(0, 0, Back[0]);
			PutImg(160, 0, Back[1]);
			ShowMouse();

		}
		if(ch == 'S' || ch == 13)
			SaveFile();
		PutMouse();
		PrintNum(0, 194, MouseX);
		PrintNum(30, 194, MouseY);
	}
	free(Image);
	free(Back[0]);
	free(Back[1]);
	CloseMouse();
	TextMode();
}
