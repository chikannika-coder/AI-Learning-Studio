/* program jupiter.c write by '3D Engine' */
#include <alloc.h>
#include "libgraph.c"

int Radius;	/* Radius of sphere	*/
int Diameter;	/* Diameter of sphere	*/
int Circum;	/* Circum of sphere	*/
int *Rah;	/* Rad at height	*/
BYTE *image;
int ImgWidth;	/* Width of image	*/
int ImgHeight;	/* Height of image	*/
int TRFV[320];		/* Vertical (scan line) transformations	*/
unsigned char *TRF;	/* Horizontal transformations	*/
unsigned char *TRFTMP;
#define SIZE 2		/* size of star */

BYTE Palette[768];
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

BYTE *LoadGIF(char *file)
{
	FILE *fp;
	int fc, oc, c, clear, ending;
	int code, newcodes, slot, top_slot;
	BYTE size, buf[13];
	BYTE *ptr, *buffer, *sp, *stack, *suffix;
	unsigned int *prefix;

	if((fp = fopen(file, "rb")) == NULL)
		return(NULL);
	fread(buf, 1, 13, fp);
	if(buf[0] != 'G' && buf[1] != 'I' && buf[2] != 'F') {
		fclose(fp); return(NULL);
	}
        fread(Palette, 768, 1, fp);
	for(c = 0; c < 768; c++) Palette[c] >>=  2;
	fread(buf, 1, 11, fp);
	ImgWidth  = (buf[6] << 8) + buf[5];
	ImgHeight = (buf[8] << 8) + buf[7];
	buffer = malloc(ImgWidth * ImgHeight);
	ptr    = buffer;
	size   = buf[10];
	if(size < 2 || 9 < size) {
		fclose(fp);
		return(NULL);
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
	free(stack);
	free(suffix);
	free(prefix);
	return(buffer);
}

unsigned char *LoadPCX(char *name)
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
	int i, j;
	BYTE *Membuf, *wptr;
	BYTE c, l;

	if((fp = fopen(name, "rb")) == NULL)
		return(NULL);
	fread(&Header, 16, 1, fp);
	/* Read and set the palette */
	fseek(fp, -768L, SEEK_END);
	fread(Palette, 768, 1, fp);
	for (i = 0; i < 768; i++)
		Palette[i] >>= 2;

	fseek(fp, 128, SEEK_SET);
	if(Header.version != 5) {
		fclose(fp);
		return(NULL);
	}
	ImgHeight = Header.vres;
	ImgWidth  = Header.hres;

	Membuf = (unsigned char *)malloc(ImgHeight * ImgWidth);
	wptr = Membuf;
	for (i = 0; i < ImgHeight; i++) {
		j = 0;
		while(j < ImgWidth) {
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
	return(Membuf);
}

/* set and put big text thai CU font file 'normal.fon' */
BYTE *CUfont;
void LoadCUfont(void)
{
     FILE *fp;

     CUfont = malloc(5120);
     fp = fopen("normal.fon", "rb");
     fread(CUfont, 5120, 1, fp);
     fclose(fp);
}
void PutChar(int x, int y, int num, int color)
{
	int i, k, x1 = x;
	BYTE *ptr = CUfont + num * 20;

	for(i = 0; i < 20; i++, ptr++, y++, x1 = x)
		for(k = 7; k >= 0; k--, x1++)
			if((*ptr >> k) & 1)
				PutPixel(x1, y, color);
}

void PutText(int Gx, int y, BYTE *str, int color)
{
     BYTE ch;

     while((ch = *str++) != 0 && Gx < 380) {
	  if(ch <= 32) Gx += 5;
          else {
               if(ch > 32 && ch < 209 || ch > 223 &&
		    ch < 231 || ch == 210 || ch > 239)
		    PutChar(Gx, y, ch , color);
               else
               if(ch > 215 && ch < 219) {
		    PutChar(Gx - 8, y, ch, color);
		    Gx -= 8;
               }
               else
               if(ch == 211) {
		    PutChar(Gx - 8, y, 237, color);
		    PutChar(Gx, y, 210, color);
               }
               else
	       if(ch == 209 || ch > 211 && ch < 216) {
		    PutChar(Gx - 8, y, ch, color);
		    Gx -= 8;
	       }
	       else
	       if(ch > 230 && ch < 237) {
                    if(*(str - 2) == 209 || *(str - 2) > 210 &&
			 *(str - 2) < 216 || *str == 211)
			 PutChar(Gx - 8, y, ch, color);
		    else
			 PutChar(Gx - 8, y + 4, ch, color);
		    Gx -= 8;
               }
	       Gx += 8;
          }
     }
}
void PutText3d(int x0, int y0, char *Text,int color)
{
	PutText(x0 + 1, y0 + 1, (BYTE *) Text, 0);
	PutText(x0, y0, (BYTE *) Text, color);

}
void Rec3d(int x0, int y0, int x1, int y1, int color )
{
	int i;

	for(i = 0; i < 3; i++)
		Rec(x0 + i, y0 + i, x1 - i + 1, y1 - i + 1, color - i);
}
void Background(void)
{
	int i;

	for(i = 1;i >= 0; i--){
		SetActivePage(i);
		Bar(213, 0, 359, 239, 5);
		Bar(0, 213, 211, 239, 4);
                Bar(230, 4, 340, 30, 1);
		Rec3d(213, 0, 359, 239, 30);
		Rec3d(0, 213, 211, 239,18);
		Rec3d(0, 0, 210, 210, 21);
		Rec3d(230, 4, 340, 30, 27);

		PutText3d(26, 215, "STAR TOUR VERSION 1.0", 15);
		PutText3d(248, 6, "´ÒÇ ¾ÄËÑÊº´Õ", 11);
		PutText3d(248, 30, "PROPERTIES", 15);
		PutText3d(218, 50, "Semimajor axis(AU)", 14);
		PutText3d(276, 65, "5.2", 11);
		PutText3d(218, 80, "Preriod(years)", 14);
		PutText3d(270, 95, "11.9", 11);
		PutText3d(219, 110, "Mass(Earth = 1)", 14);
		PutText3d(274, 125, "318", 11);
		PutText3d(218, 140, "Diameter(km)", 14);
		PutText3d(260, 155, "142,800", 11);
		PutText3d(218, 170, "Density(g/cm )", 14);
		PutText3d(274, 185, "1.3", 11);
		PutText3d(218, 200, "Rotation(hours)", 14);
		PutText3d(276, 215, "10", 11);
	}
}

void main(void)
{
	int i, j, Length;
	int rot, GanX, GanY;
	unsigned int offset, h_offset, line;
        BYTE *loc;
	double theta;
	float arc, fraction, dh;

	LoadCUfont();
	if((image = LoadGIF("jupiter.gif")) == NULL) {
		printf("File not found or type not match.\n");
		exit(0);
	}
	SetModeX();
	SetPalette(Palette);
	Circum   = ImgWidth;
	Diameter = (float) Circum / M_PI * SIZE ;
	Radius   = (float) (Circum) / (M_PI * 2.0) * SIZE;
	Length   = (int) Diameter;

	Rah = farmalloc(Length * sizeof(int) * SIZE);
	TRF = farmalloc(320 * 200+100);
	TRFTMP = farmalloc(320 * 200+100);
	for(j = 0; j < Length; j++) {
		Rah[j] = sqrt(Radius * Radius - (Radius - j) * (Radius - j));
		for(i = 0; i < Rah[j]; i++) {
			theta = asin((float) i / (float)Rah[j]);
			arc = (float) Circum / 1.5;
			fraction = theta / (M_PI);
			offset = fraction * arc;
			TRF[j * Length + i] = offset;
		}
		dh = (float) ImgHeight / (float) Diameter;
		line = (float) j * dh;
		TRFV[j] = ImgWidth * line;
	}
	GanX = Length / 2 + 5;
	GanY = 4;
	rot = ImgWidth;
	Background();
	while(!kbhit()) {
		FLIPPAGE();
		for(j = 0; j < Length ; j++) {
			loc = (BYTE *)(image + TRFV[j] + rot);
			for(i = 0; i < Rah[j]; i++) {
				h_offset = TRF[j * Length + i];
				PutPixel(GanX + i, GanY + j, *(loc + h_offset));
				PutPixel(GanX - i, GanY + j, *(loc - h_offset));
			}
		}
		rot -= 2;
		if(rot < 0) rot = ImgWidth;
	}
	TextMode();
	farfree(Rah);
	farfree(TRF);
	farfree(TRFTMP);
	free(image);
	free(CUfont);
}
