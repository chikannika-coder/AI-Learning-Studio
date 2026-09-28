/* FONT 4 COLOR PALETTE */
/* BY 3D Engine */

#include <stdio.h>
#include <conio.h>
#include <dos.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned char BYTE;
#define FMAX 180
#define NMAX 4
BYTE *SFONT[NMAX][FMAX];
BYTE SPACEFONT[NMAX], HIGHFONT[NMAX], FLEVEL2[NMAX];
BYTE ACTIVEFONT, OldWidthFont;
BYTE *Address = (BYTE *)MK_FP(0xa000, 0);
#define GrapMode() { _AX = 0x13; geninterrupt(0x10); }
#define TextMode() { _AX = 3; geninterrupt(0x10); }
#define C_RED	 0
#define C_GREEN  1
#define C_BLUE	 2
#define C_YELLOW 3
#define C_WHITE	 4

BYTE Pal[768];
struct bit_file {
	unsigned int b0 : 2;
	unsigned int b1 : 2;
	unsigned int b2 : 2;
	unsigned int b3 : 2;
};
union {
	struct bit_file Twobit;
	BYTE Onebyte;
}b;

void SetColorFont(int color, int no)
{
	int i;
	int CC[] = {1,0,0, 0,1,0, 0,0,1, 1,1,0, 1,1,1};
	BYTE *ptr;
	ptr = Pal + (no * 3 + 1) * 3;
	*ptr++ = CC[color * 3] * 28;
	*ptr++ = CC[color * 3 + 1] * 28;
	*ptr++ = CC[color * 3 + 2] * 28;
	*ptr++ = CC[color * 3] * 46;
	*ptr++ = CC[color * 3 + 1] * 46;
	*ptr++ = CC[color * 3 + 2] * 46;
	*ptr++ = CC[color * 3] * 63;
	*ptr++ = CC[color * 3 + 1] * 63;
	*ptr++ = CC[color * 3 + 2] * 63;
}

int setdot(BYTE n, int s)
{
	if(n != 0)
		n += s * 3;
	return(n);
}

void UnPakFont(char *name, int color, int no)
{
	int i, j, k, wi, hi;
	int addx, addy;
	BYTE *ptr, *ptr1;
	FILE *fp;

	fp = fopen(name, "rb");
	for(i = 0; i < 180; i++) {
		addx = fgetc(fp); addy = fgetc(fp);
		wi   = fgetc(fp); hi   = fgetc(fp);
		SFONT[no][i] = (BYTE *) malloc(wi * hi + 4);
		ptr = SFONT[no][i];
		*ptr++ = addx; *ptr++ = addy;
		*ptr++ = wi;   *ptr++ = hi;
		for(j = 0;j < hi; j++) {
			for(k = 0; k < (wi / 4); k++) {
				b.Onebyte = fgetc(fp);
				*ptr++ = setdot(b.Twobit.b0, no);
				*ptr++ = setdot(b.Twobit.b1, no);
				*ptr++ = setdot(b.Twobit.b2, no);
				*ptr++ = setdot(b.Twobit.b3, no);
			}
			k = wi % 4;
			if( k == 3) {
				b.Onebyte = fgetc(fp);
				*ptr++ = setdot(b.Twobit.b0, no);
				*ptr++ = setdot(b.Twobit.b1, no);
				*ptr++ = setdot(b.Twobit.b2, no);
			}
			if( k == 2) {
				b.Onebyte = fgetc(fp);
				*ptr++ = setdot(b.Twobit.b0, no);
				*ptr++ = setdot(b.Twobit.b1, no);
			}
			if( k == 1) {
				b.Onebyte = fgetc(fp);
				*ptr++ = setdot(b.Twobit.b0, no);
			}
		}
	}
	HIGHFONT[no] = fgetc(fp);
	FLEVEL2[no]  =  fgetc(fp);
	fclose(fp);
	SPACEFONT[no] = *(SFONT[no][12] + 2);
	SetColorFont(color, no);
}

void SetNoFont(int i)
{
	ACTIVEFONT = i;
}

void freefont(int no)
{
	int i;
	for(i = 0; i < 180; i++)
		free(SFONT[no][i]);
}

void PutChar(int x0, int y0, int no)
{
	int i, j, x1, y1;
	BYTE *ptr = SFONT[ACTIVEFONT][no];

	x0 += (char)*ptr++;
	y0 += (char)*ptr++;
	OldWidthFont = *ptr++;
	x1 = x0 + OldWidthFont;
	y1 = y0 + *ptr++;
	for(j = y0; j < y1; j++)
		for(i = x0; i < x1; i++, ptr++)
			if(*ptr && i >= 0 && i < 320 &&
				j >= 0 && j < 200 ) {
			*(Address + j * 320  + i) = *ptr;
		}
}

void PutText(int Gx, int Gy, char *str)
{
	BYTE ch, och = 0, ch1;
	while((ch = *str++) != 0 && Gx < 320) {
		if(ch < 33) Gx += SPACEFONT[ACTIVEFONT];
		else {
			if(ch > 32 && ch < 126) { /* English */
				PutChar(Gx, Gy, ch - 33);
				Gx += OldWidthFont + 1;
			}
			if(ch > 160 && ch < 209 || ch == 210 ) {
				if((och == 196  || och == 198) && ch == 210)/*ÄÒÆÒ*/
					PutChar(Gx, Gy, 159);
				else  /* ¡¢¤ ÎÐÒ*/
					PutChar(Gx, Gy, ch - 66);
				Gx += OldWidthFont + 1;
			}
			if(ch > 222 && ch < 231) { /* âãä */
				PutChar(Gx, Gy, ch - 70);
				Gx += OldWidthFont + 1 +
					(char) *SFONT[ACTIVEFONT][ch - 70];
			}
			if(ch > 239 && ch < 251) { /* num thai ðñòóôõö÷øù */
				PutChar(Gx, Gy, ch - 72);
				Gx += OldWidthFont + 1;
			}
			if(ch == 211) { /* Ó */
				PutChar(Gx, Gy, ch - 66);
                                PutChar(Gx, Gy, 144);
				Gx += OldWidthFont + 1;
			}
			if(ch >211 && ch <219 || ch ==209 ) /* ØÙ.*/
				PutChar(Gx, Gy, ch - 66);
			if(ch > 230 && ch < 237) { /* èéêëì */
				ch1 = *str;
				if(och == 209 || och > 211 && och < 216|| ch1==(BYTE)211)
					PutChar(Gx, Gy - FLEVEL2[ACTIVEFONT], ch - 70);
				else
					PutChar(Gx, Gy, ch - 70);
			}
		}
		och = ch;
	}

}

void SetPal(void)
{
	int i;

	outp(0x3c8, 0);
	for(i = 0; i < 768; i ++)
		outp(0x3c9, Pal[i]);
}
char text0[] = "·´ÊÍº¢éÍ¤ÇÒÁÀÒÉÒä·Â";
char text1[] = "áºº ñ ÃÙ»áººãªé ó à©´ÊÕ";
char text2[] = "¢éÍ¤ÇÒÁáÊ´§ä´é·Ñé§ÀÒÉÒä·Â";
char text3[] = "áÅÐ English ´éÇÂÅÐ ·èÒ¹¼ÙéªÁ";
char *Text[4] = { text0, text1, text2, text3};

#define NAME "FONT.FNT"
void main(void)
{
	int i, j = 0, k, y = 0;
	memset(Pal, 0, 768);
	UnPakFont(NAME, C_RED, 0);
	UnPakFont(NAME, C_YELLOW, 1);
	UnPakFont(NAME, C_BLUE, 2);
	UnPakFont(NAME, C_WHITE, 3);
        GrapMode();
	SetPal();
	for(i = 0; i < 7; i++) {
		SetNoFont(j);
		PutText(20, y, Text[j]);
		y += HIGHFONT[j];
		if(++j > 3) j =0;

	}
	getch();
	TextMode();
	for(i = 0; i < 4; i++)
		freefont(i);
}