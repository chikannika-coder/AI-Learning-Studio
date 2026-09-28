/* program 'santa.c' */
/* By Mr. 3D Engine Dec '96 */

#include "mgraph.c"
#include "bitmap.c"

BYTE *Santa[16];
int SantaGx, SantaGy;
int SantaOGx, SantaOGy;
BYTE *SantaBack;
#define HMAX 20
int HamGx[HMAX], HamGy[HMAX];
int HamOGx[HMAX], HamOGy[HMAX];
BYTE *HamBack[HMAX], AddHam[HMAX];
BYTE *Hamberger, *Flor[3], *Fox, *Head;
int YOU = 3, SCORE = 0;
int MFox = HMAX / 4;

BYTE Palette[] = {
    44, 34, 24,  20, 30,  0,  30, 46,  0,  32, 30, 46,
    62, 54,  0,  12,  8,  0,  26, 16,  0,  42,  0,  0,
    40, 24, 16,  56, 32,  0,  56, 56, 56,  56,  0,  0,
     0, 10,  0,  22,  0,  4,  19, 19, 19,   0,  0,  0,
    12, 23,  7,  16, 31, 10,  21, 39, 13,  27, 46, 16,
    44, 57, 15,  56, 60, 56,  17, 17, 17,  39, 10,  0
};

void SetPal(void)
{
	int i;
	BYTE *ptr;
	ptr = Palette;
	outp(0x3c8, 1);
	for (i = 0; i < 24; i++) {
		outp(0x3c9, *ptr++);
		outp(0x3c9, *ptr++);
		outp(0x3c9, *ptr++);
	}
}
void PrintYou(void)
{
	int i;

	Bar(0, 0, (YOU + 1) * 22, 10, 0);
	for(i = 0; i < YOU; i++)
		PutImage(i * 22, 0, Head);
}
void InitBitmap(void)
{
	int i;

	Santa[0]  = UnpackBitmap(Bitmap0, 0);
	Santa[1]  = UnpackBitmap(Bitmap1, 0);
	Santa[2]  = UnpackBitmap(Bitmap2, 0);
	Santa[3]  = UnpackBitmap(Bitmap3, 0);
	Santa[4]  = UnpackBitmap(Bitmap4, 0);
	Santa[5]  = UnpackBitmap(Bitmap5, 0);
	Santa[6]  = UnpackBitmap(Bitmap6, 0);
	Hamberger = UnpackBitmap(Bitmap7, 0);
	Flor[0]   = UnpackBitmap(Bitmap8, 0);
	Flor[1]   = UnpackBitmap(Bitmap9, 0);
	Flor[2]   = UnpackBitmap(Bitmap8, 16);
	Fox	  = UnpackBitmap(Bitmap10, 16);
	for(i = 0; i < 7; i++)
		Santa[i + 7] = FlipBitmap(Santa[i]);
	Head = FlipBitmap(Santa[7]);
	*(Head + 1) = 10;
	PrintYou();
	SantaBack = malloc(486); /* 22*22+2 */
}
void GetBackSanta(void)
{
	GetImage(SantaGx, SantaGy,
		SantaGx + 22, SantaGy + 22, SantaBack);
}
void SetPosHam(int i)
{
	HamOGx[i] = HamGx[i] = random(300);
	HamOGy[i] = HamGy[i] = -random(100) * 2;
	AddHam[i] = random(2) + 1;
	if(i > MFox)
		AddHam[i] = random(4) + 2;
}
void GetBackHam(int i)
{
	GetImage(HamGx[i], HamGy[i],
		HamGx[i] + 18, HamGy[i] + 23, HamBack[i]);
}
void InitGame(void)
{
	int i;

	InitBitmap();
	SantaOGx = SantaGx = 32;
	SantaOGy = SantaGy = 162;
	GetBackSanta();
	for(i = 0; i < 100; i++)
		PutPixel(random(320), random(170), 11);
	for(i = 0; i < 20; i++)
		PutImage(i * 16, 184, Flor[random(3)]);
	for(i = 0; i < HMAX; i++) {
		HamBack[i] = malloc(416); /* 18 * 23 + 2) */
		SetPosHam(i);
		GetBackHam(i);
	}
}
void FreeEnd(void)
{
	int i;

	for(i = 0; i < 16; i++)
		free(Santa[i]);
	free(Hamberger);
	free(Flor[0]);
	free(Flor[1]);
	free(SantaBack);
	free(Head);
	for(i = 0; i < HMAX; i++)
		free(HamBack[i]);
}
int CheckGet(int pos)
{
	int i;

	for(i = 0; i < 22; i++) {
		if((SantaGx + i) > HamGx[pos] &&
			(SantaGx + i)  < (HamGx[pos] + 16) &&
			(SantaGy + 10) > HamGy[pos] &&
			(SantaGy + 10) < (HamGy[pos] + 16))
				return(1);
	}
	return(0);
}

void main(void)
{
	int i, Move = 0, oSkip = 0, Skip = 0, End = 1, s;
	randomize();
	InitKey();
	InitMode13();
	SetPal();
	InitGame();
	while(!KEY.Esc && End){
		PutImage(SantaOGx, SantaOGy, SantaBack);
		for(i = 0; i < HMAX; i++)
			PutImage(HamOGx[i], HamOGy[i], HamBack[i]);

		if(KEY.Right && SantaGx < 294 ) {
			SantaGx += 4;
			Move = 0;
			if(Skip++> 5) Skip = 0;
		}
		if(KEY.Left && SantaGx > 4 ) {
			SantaGx -= 4;
			Move = 7;
			if(Skip++ > 5) Skip = 0;
		}
		for(i = 0; i < HMAX; i++) {
			HamGy[i] += AddHam[i];
			if(HamGy[i] > 172) {
				if(i <= MFox) {
					for(s = 1; s < 40; s++) {
						sound(200 + s * random(30));
						delay(5);
					}
					nosound();
					SCORE -= 5;
					if(SCORE < 0) SCORE = 0;
					else
						PrintNum(300, 2, SCORE);

				}
				SetPosHam(i);
			}
			if(CheckGet(i))	{
				if(i > MFox){
					for(s = 1; s < 40; s++){
						sound(400 + s * random(30));
						delay(5);
					}
					nosound();
					YOU--;
					if(YOU <= 0) End = 0;
					else
						PrintYou();
				}
				else {
					for(s = 1; s < 30; s++){
						sound(800 + s * 10);
						delay(5);
					}
					nosound();
					SCORE += 10;
					PrintNum(300, 2, SCORE);
				}
				SetPosHam(i);
			}
			GetBackHam(i);
			HamOGx[i] = HamGx[i];
			HamOGy[i] = HamGy[i];
		}
		GetBackSanta();
		SantaOGx = SantaGx;
		SantaOGy = SantaGy;
		for(i = 0; i < HMAX; i++){

			if(i > MFox)
				PutSprite(HamGx[i], HamGy[i], Fox);
			else
				PutSprite(HamGx[i], HamGy[i], Hamberger);
		}
		if(oSkip != Skip)
			PutSprite(SantaGx, SantaGy, Santa[Move + Skip]);
		else {
			PutSprite(SantaGx, SantaGy, Santa[Move + 6]);
			Skip = 0;
		}
		oSkip = Skip;
		PutVGA();
		delay(80);
	}
	CloseGraph();
	FreeEnd();
	SetOldKey();
	printf("GAME OVER\nYou Score = %d\n", SCORE);
}