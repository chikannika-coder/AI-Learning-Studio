#include <stdio.h>
#include <conio.h>
#include <dos.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

/* -- load GIF routine -- */
#define BYTE unsigned char
#define BUFSIZE 8192
#define MAX_CODES 4096
int curr_size, navail_bytes, nbits_left;
BYTE GifPal[768];
BYTE *VGA = (BYTE *)MK_FP(0xa000,0);



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
BYTE *LoadGif(char *file)
{
	FILE *fp;
	int fc, oc, c, clear, ending,i;
	int code, newcodes, slot, top_slot;
	int w0, w1, h0, h1;
	BYTE size, buf[13];
	BYTE *img;
	BYTE *ptr, *sp, *stack, *suffix;
	char *FileBuf;
	unsigned int *prefix;
	int width,height;

	if((fp = fopen(file, "rb")) == NULL)
		return(NULL);
	FileBuf = (char *)malloc(BUFSIZE);
	setvbuf(fp, FileBuf, _IOFBF, BUFSIZE);
	fread(buf, 1, 13, fp);
	if(buf[0] != 'G' && buf[1] != 'I' && buf[2] != 'F') {
		fclose(fp); return(NULL);
	}
	fread(GifPal, 768, 1, fp);
	for(i = 0; i < 768; i++)
		GifPal[i] >>= 2;
	fread(buf, 5, 1, fp);
	w0 = getc(fp);
	w1 = getc(fp);
	width  = (w1 << 8) + w0;
	h0 = getc(fp);
	h1 = getc(fp);
	height = (h1 << 8) + h0;
	getc(fp);
	size = getc(fp);
	img = malloc(width * height + 4);
	ptr = img;
	*ptr++ = w0;
	*ptr++ = w1;
	*ptr++ = h0;
	*ptr++ = h1;
	if(size < 2 || 9 < size) {
		fclose(fp);
		return(NULL);
	}
	stack  = (BYTE *)malloc(MAX_CODES + 1);
	suffix = (BYTE *)malloc(MAX_CODES + 1);
	prefix = (unsigned int *)malloc(sizeof(int) * (MAX_CODES + 1));
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
	return (img);
}
void SetPalGif(void)
{
	int i;

	outp(0x3c8,0);
	for(i=0;i<768;i++)
		outp(0x3c9,GifPal[i]);
}
void PutBlock(int x, int y, BYTE *ptr)
{
	int width, height, x0, x1, y1, addx, i;
	BYTE *VGA1 = VGA;

	width   = *ptr++;
	width  += (*ptr++ << 8);
	height  = *ptr++;
	height += (*ptr++ << 8);
	addx = (x < 0) ? abs(x) : 0;
	x1 = width + x - addx;
	x0 = (x1 > 319) ? x0 = width - (x1 - 319) : width;

	y1 = height + y;
	if(y1 > 199) y1 = 199;
	VGA1 += y * 320 + x + addx;
	if(addx) {
		ptr += addx;
		x0 = width - addx;
	}
	for(i = y; i < y1; i++) {
		if(i >= 0)
			memcpy(VGA1, ptr, x0);
		VGA1 += 320;
		ptr  += width;
	}
}
BYTE *GetBlock(int x0, int y0, int x1, int y1, BYTE *ptr)
{
	BYTE *img,*ptr1;
	int width, height, w, h, i, j;

        width = *ptr++;
	width += (*ptr++ << 8);
	height = *ptr++;
	height += (*ptr++ << 8);
	w = x1 - x0;
	h = y1 - y0;
	img = malloc(w * h + 4);
	ptr1 = img;
	*ptr1++ = w & 0xff;
	*ptr1++ = (w >> 8) & 0xff;
	*ptr1++ = h & 0xff;
	*ptr1++ = (h >> 8) & 0xff;
	for(j = y0; j < y1; j++)
		for(i = x0; i < x1; i++)
			*ptr1++ = *(ptr + j * width +i);
	return(img);
}
void SinkUp(char *name)
{
	int i,j;
	BYTE *img,*img1;
	img = LoadGif(name);
	SetPalGif();
	for(i=0;i<200;i++){
		img1 = GetBlock(0,i,320,i+1,img);
		for(j=i;j<200;j++)
			PutBlock(0,j,img1);
		free(img1);
	}
	free(img);
}
void ScrollUp(char *name)
{
	int i;
	BYTE *img;
	img = LoadGif(name);
	SetPalGif();
	for(i = 199; i >= 0; i--)
		PutBlock(0,i,img);
	free(img);
}
void ClearScrollUp(char *name)
{
	int i;
	BYTE *img;
	img = LoadGif(name);
	SetPalGif();
	for(i = 0; i >= -199; i--){
		PutBlock(0,i,img);
		memset(VGA+(i+199)*320,0,320);
	}
	free(img);
}
void ScrollDown(char *name)
{
	int i;
	BYTE *img;
	img = LoadGif(name);
	SetPalGif();
	for(i = -200; i < 0; i++)
		PutBlock(0,i,img);
	free(img);
}
void ClearScrollDown(char *name)
{
	int i;
	BYTE *img;
	img = LoadGif(name);
	SetPalGif();

	for(i = 0; i < 200; i++){
		PutBlock(0,i,img);
		memset(VGA+i*320,0,320);
	}
	free(img);
}
void ScrollLeft(char *name)
{
	int i;
	BYTE *img;
	img = LoadGif(name);
	SetPalGif();
	for(i = -320; i <= 0 ; i++)
		PutBlock(i,0,img);
	free(img);
}
void ClearScrollLeft(char *name)
{
	int i,j;
	BYTE *img;
	img = LoadGif(name);
	SetPalGif();

	for(i = 0; i < 320; i++){
		PutBlock(i,0,img);
		for(j=0;j<200;j++){
			* (VGA + j * 320 + i - 1) = 0;
		}
	}
	free(img);
}
void ScrollRight(char *name)
{
	int i;
	BYTE *img;
	img = LoadGif(name);
	SetPalGif();
	for(i = 319; i >= 0 ; i--)
		PutBlock(i,0,img);
	free(img);
}
void ClearScrollRight(char *name)
{
	int i,j;
	BYTE *img;
	img = LoadGif(name);
	SetPalGif();

	for(i = 0; i >= - 320; i--){
		PutBlock(i,0,img);
		for(j=0;j<200;j++){
			* (VGA + j * 320 + i + 320) = 0;
		}
	}
	free(img);
}
#define InitGraph()  { _AX = 0x13; geninterrupt(0x10); }
#define CloseGraph() { _AX = 0x3; geninterrupt(0x10); }
void DelayKey(int Delay)
{
	int i,j;

	for(j = 0; j < Delay; j++) {
		for(i = 0; i < 40; i++)
			if(kbhit()) break;
		if(kbhit()){
			if(getch()==27) {
				CloseGraph()
				exit(0);
			}
			break;
		}
	}
}
void main(void)
{
	InitGraph();

	ScrollUp("BIGLAKE.GIF");
	DelayKey(120);
	ClearScrollUp("BIGLAKE.GIF");
	ScrollDown("BIGLAKE.GIF");
	DelayKey(120);
	ClearScrollDown("BIGLAKE.GIF");
	ScrollLeft("BIGLAKE.GIF");
	DelayKey(120);
	ClearScrollLeft("BIGLAKE.GIF");
	ScrollRight("BIGLAKE.GIF");
	DelayKey(120);
	ClearScrollRight("BIGLAKE.GIF");
	SinkUp("BIGLAKE.GIF");
	DelayKey(120);
	ClearScrollUp("BIGLAKE.GIF");
	CloseGraph();
}