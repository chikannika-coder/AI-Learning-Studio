#include <stdio.h>
#include <conio.h>
#include <dos.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <time.h>
typedef unsigned char BYTE;
BYTE *PageStart;
unsigned int MemLength;
unsigned int LINE_Y[200];

#define PutVGA() memcpy(MK_FP(0xa000,0),PageStart,MemLength);
void InitMode13(void)
{
	int i;

	_AX = 0x13;
	geninterrupt(0x10);
	for(i = 0; i < 200; i++)
		LINE_Y[i] = i * 320;
	MemLength = 320 * 200;
	PageStart = malloc(MemLength);
	memset(PageStart, 0, MemLength);
}
void CloseGraph(void)
{
	_AX = 3;
	geninterrupt(0x10);
	free(PageStart);
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
void PutImage(int x0, int y0, BYTE *ptr)
{
	int i, j, x1, y1;
	x1 = x0 + *ptr++; y1 = y0 + *ptr++;
	for(j = y0; j < y1; j++)
		for(i = x0; i < x1; i++, ptr++)
			if(i >= 0 && i < 320 &&
				j >= 0 && j < 200 )
			*(PageStart + LINE_Y[j]  + i ) = *ptr;
}
void PutSprite(int x0, int y0, BYTE *ptr)
{
	int i, j, x1, y1;
	x1 = x0 + *ptr++; y1 = y0 + *ptr++;
	for(j = y0; j < y1; j++)
		for(i = x0; i < x1; i++, ptr++)
			if(i >= 0 && i < 320 &&
				j >= 0 && j < 200 && *ptr )
			*(PageStart + LINE_Y[j]  + i ) = *ptr;
}
void GetImage(int x0, int y0,  int x1, int y1, BYTE *ptr)
{	/* get mem screen to mem image sprite */
	int i, j;
	*ptr++ = x1 - x0; *ptr++ = y1 - y0;
	for(j = y0; j < y1; j++)
		for(i = x0; i < x1; i++)
			*ptr++ = *(PageStart + LINE_Y[j] + i );
}
struct Keyboard { /* Keyboard input structure. */
    char Right, Left, Up, Down, Space, Esc;
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
#define InitKey() { OldKeyVec = getvect(9); \
		      setvect(9, NewKeyInt); }
#define SetOldKey() setvect(9, OldKeyVec)

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
		PNum(i * 6 + x, y, str[i] - '0', 10);
	} while(str[++i]);
}
void PackBitmap(BYTE *ptr1)
{
	static int k=0;
	int i, j ;
	BYTE memtmp[1024];
	BYTE width, height, *ptr;
	ptr = memtmp;
	width = *ptr1++; height = *ptr1++;
	*ptr++ = width >> 1; *ptr++ = height;
	for(j = 0;j < height; j++)
		for(i = 0; i < width; i += 2){
			*ptr++ = (*ptr1 << 4) | (*(ptr1+1));
			ptr1 += 2;
		}
	ptr = memtmp;
	width = *ptr++; height = *ptr++;
	printf("BYTE Bitmap%d[] = { %3d,%3d,\n", k++, width, height);
	for(j = 0; j < height; j++) {
		for(i = 0; i < width; i ++) {
			printf("%3d", *ptr++);
			if((i == width - 1) && (j == height - 1));
			else
				printf(",");
		}
		printf("\n");
	}
	printf(" };\n");
}
BYTE *UnpackBitmap(BYTE *ptr,int Add)
{
	int i, j;
	BYTE *BitImage;
	BYTE width, height, *ptr1;

	width = *ptr++;
	height = *ptr++;
	BitImage = malloc((width << 1) * height + 2);
	ptr1 = BitImage;
	*ptr1++ = width << 1 ;
	*ptr1++ = height;
	for(j = 0; j < height; j++){
		for(i = 0; i < width; i ++) {
			*ptr1 = ((*ptr >> 4) & 0x0f);
			*(ptr1 + 1) = (*ptr & 0x0f);
			if(*ptr1 > 0) *ptr1 += Add;
			if(*(ptr1 + 1) > 0) *(ptr1 + 1) += Add;
			ptr1 += 2; ptr++;
		}
	}
	return(BitImage);
}
BYTE *FlipBitmap(BYTE *ptr)
{
	int i, j;
	int width, height;
	BYTE *BitImage, *ptr1;
	width = *ptr++; height = *ptr++;
	BitImage = malloc(width * height + 2);
	ptr1 = BitImage;
	*ptr1++ = width; *ptr1++ = height;
	for(j = 0; j < height; j++)
		for(i = width - 1 ; i >= 0; i--)
			*(ptr1 + j * width + i)  = *ptr++;
	return(BitImage);
}