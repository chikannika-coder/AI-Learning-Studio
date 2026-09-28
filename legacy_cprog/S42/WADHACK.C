/*  Program 'wadhack.c'*/
/* Code by '3D Engine' */
#include <conio.h>
#include <stdio.h>
#include <dos.h>
#include <stdlib.h>
#include <string.h>
#include <alloc.h>
#define MAXDIR 3500
typedef unsigned char BYTE;
typedef unsigned int  WORD;
typedef unsigned long ULONG;
BYTE Pal[768];
BYTE *BUFFER;
BYTE *buf;
int NumWad = 0;
int WWidth,WHigh;
BYTE *CUfont;
BYTE far *VGA = (BYTE far *) MK_FP(0xa000, 0);

typedef struct {
	char wadtag[4];		/* wad identification tag */
	ULONG waddirlen;	/* number of entries in directory */
	ULONG waddiraddr;	/* byte file offset of directory */
} WadHeader;

/* wad directory entry structure */
typedef struct {
	ULONG resptr;		/* byte file offset of resource */
	ULONG reslen;		/* byte length of resource */
	char  name[8];		/* name of resource */
} WadDirEntry;

/* wad directory entry structure */
struct {
	ULONG Addr;		/* byte file offset of resource */
	ULONG Len;		/* byte length of resource */
	char name[9];		/* name of resource */
	BYTE  Flag;
} Wadpos[MAXDIR];

/* structure picture */
typedef struct {
	short pwid;
	short phgt;
	short pxoff;
	short pyoff;
        ULONG postlen;
	ULONG *coloffs;
	BYTE  *posts;
} PicData;

void putpix(int x, int y, BYTE color)
{
	if(x < 0 || y < 0 || x > 319 || y > 199) return;
	*(VGA + y * 320 + x) = color;
}

/* set and put text thai need file 'normal.fon' form CW */
void LoadCUfont(void)
{
     FILE *fp;

     CUfont = malloc(5120);
     fp = fopen("normal.fon", "rb");
     fread(CUfont, 5120, 1, fp);
     fclose(fp);
}

void PutChar(int x, int y, int num, BYTE color)
{
	int i, k, x1 = x;
	BYTE *ptr = CUfont + num * 20;

	for(i = 0; i < 20; i++, ptr++, y++, x1 = x)
		for(k = 7; k >= 0; k--, x1++)
			if((*ptr >> k) & 1)
				putpix(x1, y, color);
}

void PutText(int Gx, int y, BYTE *str, BYTE color)
{
     BYTE ch;

     while((ch = *str++) != 0) {
	  if(ch <= 32)
		Gx += 5;
          else {
               if(ch > 32 && ch < 209 || ch > 223 &&
		    ch < 231 || ch == 210 || ch > 239)
		    PutChar(Gx, y, ch, color);
               else
	       if(ch > 215 && ch < 219) {
		    Gx -= 8;
		    PutChar(Gx, y, ch, color);
               }
               else
               if(ch == 211) {
		    PutChar(Gx - 8, y, 237, color);
		    PutChar(Gx, y, 210, color);
               }
               else
	       if(ch == 209 || ch > 211 && ch < 216) {
		    Gx -= 8;
		    PutChar(Gx, y, ch, color);
	       }
	       else
	       if(ch > 230 && ch < 237) {
		    Gx -=8;
                    if(*(str - 2) == 209 || *(str - 2) > 210 &&
			 *(str - 2) < 216 || *str == 211)
			 PutChar(Gx, y, ch, color);
		    else
			 PutChar(Gx, y + 4, ch, color);
	       }
	       Gx += 8;
          }
     }
}

/* Directory locations for start/end tags */
void AddpDir(WadDirEntry *wde, int Type)
{
	if(NumWad >= MAXDIR) return;
	Wadpos[NumWad].Addr = wde->resptr;
	Wadpos[NumWad].Len  =  wde->reslen;
	Wadpos[NumWad].Flag = Type;
	memcpy(Wadpos[NumWad].name, wde->name, 8);
	Wadpos[NumWad].name[8] = 0;
	NumWad++;
}

/* Read the directory from a wad file */
int ReadWadDir(char *name)
{
        WadHeader phdr;
	WadDirEntry wde;
	ULONG i;
	int SSprite = 0;
	int SWall = 0;
	int SFlor = 0;
	char Nametemp[9];
	FILE *fp;

	Nametemp[8] = NumWad = 0;
	fp = fopen(name, "rb");
	if(fp == NULL) return(0);
	fread(&phdr, 12, 1, fp);
	fseek(fp,phdr.waddiraddr, SEEK_SET);
	for (i = 0; i < phdr.waddirlen; i++) {
		fread(&wde, 16, 1, fp);
		memcpy(Nametemp,wde.name, 8);
		printf("%4ld %-10s %6ld\n", i, Nametemp, wde.reslen);
		if(strcmp(wde.name, "PLAYPAL") == 0) /* Palette */
			AddpDir(&wde, 1);
		if(strcmp(wde.name, "S_START") == 0)
			SSprite = 1;
		if(strcmp(wde.name, "S_END") == 0)
			SSprite = 0;
		if(SSprite == 1 && wde.reslen != 0)  /* Sprite */
			AddpDir(&wde, 2);
		if(strcmp(wde.name, "P_START") == 0)
			SWall = 1;
		if(strcmp(wde.name, "P_END") == 0)
			SWall = 0;
		if(SWall == 1 && wde.reslen != 0) /* Wall Texture */
			AddpDir(&wde, 2);
		if(strcmp(wde.name,"F_START") == 0)
			SFlor = 1;
		if(strcmp(wde.name, "F_END") == 0)
			SFlor = 0;
		if(SFlor == 1 && wde.reslen != 0) /* Flor Texture */
			AddpDir(&wde, 3);
	}
	fclose(fp);
	return(1);
}

void Setpal(BYTE *ptr)
{
	int i;

	outp(0x3c8, 0);
	for(i = 0; i < 256; i++){
		outp(0x3c9, (*ptr++ >> 2));
		outp(0x3c9, (*ptr++ >> 2));
		outp(0x3c9, (*ptr++ >> 2));
	}
}

void ConvertImg(PicData *p, WORD logw)
{
	int i, j;
	ULONG rown, npix;
	WORD postlen;
	BYTE *ptr;

	ptr = BUFFER;
	postlen = 0;
	for (i = 0; i < p->pwid; i++)
	{
		postlen = (WORD) p->coloffs[i] - (p->pwid << 2) - 8;
		rown = (ULONG) p->posts[postlen++];
		while (rown != 255) {
			npix = p->posts[postlen];
			postlen += 2;
			for (j = 0; j < npix; j++)
				ptr[(WORD) (logw * (rown + j) + i) ]
					= p->posts[postlen++];
			postlen++;
			rown = p->posts[postlen++];
		}
	}
}

void ShowSprite(int width, int high)	/* show at center crt */
{
	BYTE *ptr;
	int i, w, h;
	ptr = BUFFER;

	w = 160 - (width >> 1);		/* center x */
	h = 100 - (high  >> 1);		/* center y */
	memset(VGA, 15, 320 * 200); 	/* clear screen */
	for (i = 0; i < high; i++) {
		memcpy(VGA + (i + h) * 320 + w, ptr, width);
		ptr += width;
	}
}

short getshort(BYTE *buf, int i)
{
	return((buf[i] & 0xff) + ((buf[i + 1] & 0xff) << 8));
}

/* Extract a Graphic or Sprite */
void OutputPic(FILE *fp, int idx)
{
	ULONG n;
	ULONG o;
	PicData pic;

	o = Wadpos[idx].Addr;
	n = Wadpos[idx].Len;
	if(n > (320 * 200) || n <= 0) return;
	buf = malloc((unsigned int) n);
	fseek(fp,o,SEEK_SET);
	fread(buf,(WORD) n, 1, fp);
	pic.pwid  = getshort(buf, 0);
	pic.phgt  = getshort(buf, 2);
	pic.pxoff = getshort(buf, 4);
	pic.pyoff = getshort(buf, 6);
	pic.coloffs = (ULONG *) (((short *)buf) + 4);
	pic.posts = (BYTE *) (buf + (WORD) pic.coloffs[0]);
	memset(BUFFER, 0, pic.pwid * pic.phgt);
	ConvertImg(&pic, pic.pwid);
	ShowSprite(pic.pwid, pic.phgt);
	WWidth = pic.pwid;
	WHigh  = pic.phgt;
	free(buf);
}


void SaveSprite(int i)
{
	FILE *fp;
	char NAME[14];

	sound(2000);
	strcpy(NAME, Wadpos[i].name);
	strcat(NAME, ".SPI");
	fp = fopen(NAME,"wb");
	fputc(WWidth&0xff,fp);
	fputc((WWidth>>8)&0xff,fp);
	fputc(WHigh & 0xff, fp);
	fputc((WHigh >> 8) & 0xff, fp);
	fwrite(BUFFER, WWidth *WHigh, 1, fp);
	fclose(fp);
	delay(200);
	nosound();
}

void SavePalette(void)
{
	FILE *fp;

	fp = fopen("PALETTE.PAL", "wb");
	fwrite(Pal, 768, 1, fp);
	fclose(fp);
}

void main(int agc, char *agv[])
{
	int i, RFile;
	char str[8];
	BYTE ch;
	FILE *fp;
	printf("%d",sizeof(WadDirEntry));
	if(agc < 2) {
		printf("type 'WADHACK [file.wad]' To run\n");
		exit(0);
	}
	RFile = ReadWadDir(agv[1]);
	if(RFile != 0){
		LoadCUfont();
		BUFFER = malloc(320 * 200);
		_AX = 0x13;
		geninterrupt(0x10);
		fp = fopen(agv[1], "rb");
		for(i = 0; i < NumWad; i++){
			if(Wadpos[i].Flag == 1)	{
				fseek(fp, Wadpos[i].Addr, SEEK_SET);
				fread(Pal, 768, 1, fp);
				Setpal(Pal);
			}
			else {
				if(Wadpos[i].Flag == 2)
					OutputPic(fp, i);
				if(Wadpos[i].Flag == 3)	{
					fseek(fp, Wadpos[i].Addr, SEEK_SET);
					fread(BUFFER, 4096, 1, fp);
					ShowSprite(64,64);
				}
				itoa(i, str, 10);
				PutText(100, 180, (BYTE *)str, 225);
				PutText(140, 180, (BYTE *)Wadpos[i].name, 200);
				ch = getch();
				if(ch == 27)	/*  Esc */
					break;
				if(ch == 8 && i > 0)
					i -= 2; /* back sprite */
				if(ch == 's')  /*save sprite*/
					SaveSprite(i--);
				if(ch == 'p') {/* save palette */
					SavePalette();
					i--;
				}
			}
		}
		fclose(fp);
		free(BUFFER);
		free(CUfont);
		_AX = 3;
		geninterrupt(0x10);
		printf("Num picture = %d\n", i);
	}
	else
		printf("File %s not found\n", agv[1]);
	exit(0);
}
