/* program test vesa mode 24 bit color */
/* turbo c or borland c compile model large */
/* program by 3D Engine */
#include "vesa24.c"
BYTE *Spimage;
void savetga(char *name)
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
	FILE *fp;
	BYTE buf[3];
	int i,j;

	fp = fopen("fact.tga", "rb");
	fread(&taga, sizeof(struct TGA), 1, fp);
	fclose(fp);

	fp = fopen(name, "wb");
	fwrite(&taga, sizeof(struct TGA), 1, fp);
	for(j = 479;j >= 0; j--) {
		for(i = 0; i < 640; i++) {
			getpixelrgb(i, j, &buf[2], &buf[1], &buf[0]);
			fwrite(buf,3,1,fp);
		}
	}
	fclose(fp);
}
void main(void)
{
	IMAGE img, img1;
	BYTE *Spimage;
	int i;

	randomize();
	if(initvesa()) {
		Textmode();
		printf("Your vgacard not support.\n");
		exit(0);
	}
        LoadCUfont();
	ShowTGA(0, 0, "robot.tga");
	PutText3d(250,10,"Press Any key",255,200,255);
	getch();
	LoadGIF("jackson.gif", &img);
	LoadGIF("madona.gif", &img1);
	Putimage24(450, 10, &img);
	Putimage24(10, 315, &img1);
	PutText3d(450, 200, "JACKSON ราชาแห่งเพลง POP", 0, 255, 0);
	PutText3d(210, 450, "MADONA ซะอย่างขวัญใจขาโจ๋อยู่แล้ว", 0, 255, 255);
	Spimage = getimagergb(525, 15, 555, 50);
	for(i = 0; i < 10; i++)
		putimagergb(i * 40 + 20, 210, Spimage);
	while(kbhit()) getch();
	getch();
	while(!kbhit()) {
		Putimage24(random(600), random(400), &img);
		Putimage24(random(600), random(400), &img1);
		putimagergb(random(600), random(400), Spimage);
	}
	Textmode();
	freeimg24(&img);
	freeimg24(&img1);
	free(Spimage);
	free(CUfont);
}