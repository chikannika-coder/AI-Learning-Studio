/* Graphic lib truecolor 24 bits per pixel
   or 16,777,216 million color pallette
   program by 3D Engine */
#include <stdio.h>
#include <conio.h>
#include <dos.h>
#include <stdlib.h>
#include <time.h>
#include <mem.h>
typedef unsigned char BYTE;
typedef struct {
	int width;
	int height;
	BYTE pal[768];
	BYTE *IMG;
} IMAGE;
#define BUFSIZE  8192	/* allocate for file reading. */
char far *vgamem = MK_FP(0xa000, 0); /* pointre to vga memory */
char far *ptrscreen;
int adrx[640], adry[480], banky[480];
BYTE *CUfont;

/* header from asm code */
int initvesa24 (void); /* set VESA mode */
void setbank(int i);   /* set bank mem vesa */
#define Textmode()  _AX = 3; geninterrupt(0x10);
#define Setbank1()  setbank(banky[y]); \
		    ptrscreen = vgamem + adrx[x] + adry[y];
int initvesa(void)
{
	int i;

	for(i = 0; i < 640; i++)
		adrx[i] = i * 3; /* one pixel equ 3 byte */
	for(i = 0; i < 480; i++){
		banky[i] = (i >> 5);
		adry[i]  = (i % 32) << 11;
/*		adry[i]  = i*3*640;	*/

	}
	return(initvesa24());
}
void putpixelrgb(int x, int y, BYTE r, BYTE g, BYTE b)
{ /* put color red green blue */
	Setbank1();
	*ptrscreen++ = b;
	*ptrscreen++ = g;
	*ptrscreen   = r;
}
void getpixelrgb(int x, int y, BYTE *r, BYTE *g, BYTE *b)
{ /* get color red green blue */
        Setbank1();
	*b = *ptrscreen++;
	*g = *ptrscreen++;
	*r = *ptrscreen;
}
/* -- load GIF routine -- */
#define MAX_CODES 4096
int curr_size, navail_bytes, nbits_left;
int get_next_code(FILE *fp)
{
	static unsigned int code_mask[] = {
		0, 1, 3, 7, 0x0f,
		0x01f, 0x03f, 0x07f, 0x0ff,
		0x01ff, 0x03ff, 0x07ff, 0x0fff };
	static BYTE b1, byte_buff[257], *pbytes;
	unsigned long ret;

	if(!nbits_left) {
		if(navail_bytes <= 0) {
			pbytes = byte_buff;
			if((navail_bytes = getc(fp)) != 0)
				fread(byte_buff, 1, navail_bytes, fp);
		}
		b1 = *pbytes++;
		nbits_left = 8;
		navail_bytes--;
	}
	ret = b1 >> (8 - nbits_left);
	while(curr_size > nbits_left) {
		if(navail_bytes <= 0) {
			pbytes = byte_buff;
			if((navail_bytes = getc( fp )) != 0)
				fread(byte_buff, 1, navail_bytes, fp);
		}
		b1 = *pbytes++;
		ret |= b1 << nbits_left;
		nbits_left += 8;
		navail_bytes--;
	}
	nbits_left -= curr_size;
	return((int) ret & code_mask[curr_size]);
}
void LoadGIF(char *file, IMAGE *img)
{
	FILE *fp;
	int fc, oc, c, clear, ending;
	int code, newcodes, slot, top_slot;
	BYTE size, buf[13];
	BYTE *ptr, *sp, *stack, *suffix;
	char *FileBuf;
	unsigned int *prefix;

	if((fp = fopen(file, "rb")) == NULL)
		return;
	FileBuf = malloc(BUFSIZE);
	setvbuf(fp, FileBuf, _IOFBF, BUFSIZE);
	fread(buf, 1, 13, fp);
	if(buf[0] != 'G' && buf[1] != 'I' && buf[2] != 'F') {
		fclose(fp); return;
	}
	fread(img->pal, 768, 1, fp);
	fread(buf, 5, 1, fp);
	img->width  = getw(fp);
	img->height = getw(fp);
	getc(fp);
	size = getc(fp);
	img->IMG = malloc(img->width * img->height);
	ptr    = img->IMG;
	if(size < 2 || 9 < size) {
		fclose(fp);
		return;
	}
	stack  = malloc(MAX_CODES + 1);
	suffix = malloc(MAX_CODES + 1);
	prefix = malloc(sizeof(int) * (MAX_CODES + 1));
	sp = stack;
	curr_size = size + 1;
	top_slot  = 1 << curr_size;
	clear  = 1 << size;
	ending = clear + 1;
	slot   = newcodes = ending + 1;
	navail_bytes = nbits_left = oc = fc = 0;
	while((c = get_next_code(fp)) != ending) {
		if(c == clear) {
			curr_size = size + 1;
			slot = newcodes;
			top_slot = 1 << curr_size;
			while((c = get_next_code(fp)) == clear);
			if(c == ending) break;
			if(c >= slot) c = 0;
			*ptr++ = oc = fc = c;
		}
		else {
			if((code = c) >= slot) {
				code = oc;
				*sp++ = fc;
			}
			while(code >= newcodes) {
				*sp++ = *(suffix + code);
				code  = *(prefix + code);
			}
			*sp++ = code;
			if(slot < top_slot) {
				*(suffix + slot) = fc = code;
				*(prefix + slot++) = oc;
				oc = c;
			}
			if(slot >= top_slot && curr_size < 12) {
				top_slot <<= 1;
				curr_size++;
			}
			while(sp > stack)
				*ptr++ = *(--sp);
		}
	}
	fclose(fp);
	free(stack); free(suffix);
	free(prefix); free(FileBuf);
}
void Putimage24(int x0, int y0, IMAGE *img)
{
	int i, j, k, x1, y1, Width, Height;
	BYTE *ptr;

	Width  = img->width;
	Height = img->height;
	ptr    = img->IMG;
	x1 = x0 + Width;
	y1 = y0 + Height;
	for(j = y0; j < y1; j++)
		for(i = x0; i < x1; i++) {
			k = *ptr++;
			if(i < 640 && j < 480 && i >= 0 && j >= 0&& k!=0)
				putpixelrgb(i, j,
					img->pal[k * 3],
					img->pal[k * 3 + 1],
					img->pal[k * 3 + 2]);
		}
}
void Putimageclip24(int x0, int y0, IMAGE *img, int add)
{
	int i, j, k, x1, y1, Width, Height;
	BYTE *ptr;

	Width  = img -> width;
	Height = img -> height;
	ptr  = img -> IMG;
	x1 = x0 + Width;
	y1 = y0 + Height;
	for(j = y0; j < y1; j++)
		for(i = x0; i < x1; i++) {
			k = *ptr++;
			if(i < 640 && j < 480 && i >= 0 && j >= 0 && k > 0)
				putpixelrgb(i, j,
					img->pal[k * 3] + add,
					img->pal[k * 3 + 1] + add,
					img->pal[k * 3 + 2] + add);
		}
}
void freeimg24(IMAGE *img)
{
	free(img->IMG);
}
BYTE *getimagergb(int x, int y0,int x1,int y1)
{
	int y, Width, Height;
	BYTE *img,*ptr;

	Width  = x1 - x;
	Height = y1 - y0;
	img = malloc(Width * 3 * Height + 2);
	ptr  = img;
	*ptr++ = Width;
	*ptr++ = Height;
	Width *= 3;
	for(y = y0; y < y1; y++)
	{
        	Setbank1();
		memcpy(ptr, ptrscreen, Width);
		ptr += Width;
	}
	return(img);
}
void putimagergb(int x0, int y0, BYTE *img)
{
	int i, j, x1, y1, r, g, b;
	int Width, Height;
	BYTE *ptr;

	ptr = img;
	Width  = *ptr++;
	Height = *ptr++;
	x1 = x0 + Width;
	y1 = y0 + Height;
	for(j = y0; j < y1; j++)
		for(i = x0; i < x1; i++) {
                	b = *ptr++;
			g = *ptr++;
			r = *ptr++;
			if(i < 640 && j < 480 && i >= 0 && j >= 0)
				putpixelrgb(i, j, r, g, b);
		}

}
void ShowBMP(int x, int y0, char *name)
{
	/* BMP 24 bit picture file header structure  */
	struct BMP {
		char id[2];		/* BM */
		long filesize;
		int  reserved[2];
		long headersize;
		long infoSize;
		long sizex;
		long sizey;
		int  biPlanes;
		int  bits;
		long biCompression;
		long biSizeImage;
		long biXPelsPerMeter;
		long biYPelsPerMeter;
		long biClrUsed;
		long biClrImportant;
	} bmp;
	BYTE *buf;
	int y, y1, length;
	FILE *fp;
	char *FileBuf;

	fp = fopen(name,"rb");
        FileBuf = (char *) malloc(BUFSIZE);
	setvbuf(fp, FileBuf, _IOFBF, BUFSIZE);
	fread(&bmp, sizeof(struct BMP), 1, fp);
	y1 = (int)(y0 + bmp.sizey - 1);
	length = (int)(bmp.sizex * 3);
	buf = malloc(length);
	for(y = y1; y >= y0; y--) {
		fread(buf, length, 1, fp);
                Setbank1();
		memcpy(ptrscreen, buf, length);
	}
	fclose(fp);
	free(buf);
	free(FileBuf);
}
void ShowTGA(int x, int y0, char *name)
{
	/* TARGA picture file header structure  */
	struct TGA {
		char textSize;
		char mapType;
		char dataType;
		int  mapOrig;
		int  mapLength;
		char CMapBits;
		int  XOffset;
		int  YOffset;
		int  x;
		int  y;
		char dataBits;
		char imType;
	} taga;
	BYTE *buf;
	int y, y1, length;
	FILE *fp;
	char *FileBuf;

	fp = fopen(name, "rb");
        FileBuf = (char *) malloc(BUFSIZE);
	setvbuf(fp, FileBuf, _IOFBF, BUFSIZE);
	fread(&taga, sizeof(struct TGA), 1, fp);
	y1 = y0 + taga.y - 1;
	length = taga.x * 3;
	buf = malloc(length);
	for(y = y1; y >= y0; y--) {
		fread(buf, length, 1, fp);
                Setbank1();
		memcpy(ptrscreen, buf, length);
	}
	fclose(fp);
	free(buf);
        free(FileBuf);
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
void PutChar(int x, int y, int num, int r, int g, int b)
{
	int i, k, x1 = x;
	BYTE *ptr = CUfont + num * 20;

	for(i = 0; i < 20; i++, ptr++, y++, x1 = x)
		for(k = 7; k >= 0; k--, x1++)
			if((*ptr >> k) & 1)
				putpixelrgb(x1, y, r, g, b);
}
void PutText(int Gx, int y, BYTE *str, int r, int g, int b)
{
     BYTE ch;

     while((ch = *str++) != 0) {
	  if(ch <= 32) Gx += 5;
          else {
               if(ch > 32 && ch < 209 || ch > 223 &&
		    ch < 231 || ch == 210 || ch > 239)
		    PutChar(Gx, y, ch , r, g, b);
               else
	       if(ch > 215 && ch < 219) {
		    Gx -= 8;
		    PutChar(Gx, y, ch, r, g, b);
               }
               else
               if(ch == 211) {
		    PutChar(Gx - 8, y, 237, r, g, b);
		    PutChar(Gx, y, 210, r, g, b);
               }
               else
	       if(ch == 209 || ch > 211 && ch < 216) {
		    Gx -= 8;
		    PutChar(Gx, y, ch, r, g, b);
	       }
	       else
	       if(ch > 230 && ch < 237) {
		    Gx -=8;
                    if(*(str - 2) == 209 || *(str - 2) > 210 &&
			 *(str - 2) < 216 || *str == 211)
			 PutChar(Gx, y, ch, r, g, b);
		    else
			 PutChar(Gx, y + 4, ch, r, g, b);
	       }
	       Gx += 8;
          }
     }
}
void PutText3d(int x0, int y0, char *Text, int r, int g, int b)
{
	PutText(x0 + 1, y0 + 1, (BYTE *) Text, 0, 0, 0);
	PutText(x0, y0, (BYTE *) Text, r, g, b);
}
/* end of librabies */