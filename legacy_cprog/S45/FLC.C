/* program play flc */
/* flc.c by 3d Engine */
#include <stdio.h>
#include <stdlib.h>
#include <mem.h>
#include <time.h>
#include <dos.h>

#define TRUE 1
#define FALSE 0

typedef unsigned char Byte;
typedef signed char SByte;
typedef unsigned short int UWord;
typedef signed short int SWord;
typedef unsigned long int DWord;
typedef struct Animation Animation;
/* Data structure for animation */
struct Animation
{
   FILE *Handle;	/* File handle (for sources 0 and 1) */
   short Width;		/* Width of animation */
   short Height;	/* Height of animation */
   short Length;
   short NumFrames;	/* Number of frames in animation */
   short CurFrame;	/* Number of current frame */
   Byte *Frame;		/* Pointer to frame buffer or NULL */
   Byte *Palette;	/* Pointer to palette buffer or NULL */
};
Animation *animate;
unsigned char *frame;
unsigned char *FLC;
unsigned char palette[768];

Byte *allocimage(int w, int h)
{
	Byte *buf;
	buf = malloc(w * h + 4);
	buf[0] = w & 0xff;
	buf[1] = (w>>8)&0xff;
	buf[2] = h & 0xff;
	buf[3] = (h>>8) & 0xff;
	return(buf);
}
void Setpal(Byte *pal)
{
	int i;

	outp(0x3c8, 0);
	for(i = 0; i < 768; i++)
		outp(0x3c9, *pal++);
}
DWord GetDWord(FILE *handle)
{
	DWord result;

	result = (long)getc(handle);
	result |= (long)getc(handle) << 8;
	result |= (long)getc(handle) << 16;
	result |= (long)getc(handle) << 24;
	return(result);
}

void Chunk_Decode_COLOR(Animation *animation, Byte *chunk)
{
	int color = 0, num_packets;
	size_t offset = 8;
	int numcol, i;
	unsigned char *pal;

	num_packets=*(UWord *)(chunk + 6);
	while(num_packets-->0) {
		color += *(Byte *)(chunk + offset++);
		numcol = *(Byte *)(chunk + offset++);
		if(numcol == 0)
			numcol = 256;
		pal = (unsigned char *)animation->Palette + color * 3;
		while(numcol-->0) {
			for(i=0; i<3; i++)
				*pal++ = *(Byte *)(chunk + offset++);
		}
	}
	Setpal(animation->Palette);
}

void Chunk_Decode_LC(Animation *animation, Byte *chunk)
{
	Byte *line;
	int skip_lines, num_lines;
	size_t offset = 10;

	/* Skip unchanged lines */
	skip_lines = *(UWord *)(chunk + 6);
	line = animation->Frame + animation->Width * skip_lines;

	/* Decode changed lines */
	num_lines = *(UWord *)(chunk + 8);
	while(num_lines-->0) {
		int num_packets;
		size_t line_offset = 0;
		int size_count;

		/* Decode one packet at time */
		num_packets = *(Byte *)(chunk + offset++);
		while(num_packets-->0) {
		/* Skip unchanged bytes */
			line_offset += *(Byte *)(chunk + offset++);
			/* Decode changed bytes */
			size_count = *(SByte *)(chunk + offset++);
			if(size_count >= 0) {
			/* Copy data to the screen */
				while(size_count-->0)
					*(line+line_offset++) = *(chunk + offset++);
			}
			else {
				Byte color;
				/* Draw single color to the screen */

				color = *(chunk + offset++);
				while(size_count++ < 0)
					*(line + line_offset++) = color;
			}
		}
		/* Move to next line */
		line = line + animation->Width;
	}
}

void Chunk_Decode_BRUN(Animation *animation, Byte *chunk)
{
	Byte *line = animation->Frame;
	size_t offset = 6;
	int line_count;

	/* Decode picture line by line */
	for(line_count=0; line_count < animation->Height; line_count++) {
		size_t line_offset = 0;
		int num_packets;

		/* Go through all the packets */
		num_packets=*(Byte *)(chunk+offset++);
		while(num_packets-->0) {
			int size_count;

			/* Decode packet */
			size_count = *(SByte *)(chunk + offset++);
			if(size_count >= 0) {
				Byte color;
				/* Fill with single color */
				color = *(Byte *)(chunk + offset++);
				while(size_count-- > 0)
					*(line+line_offset++)=color;
			}
			else {
			/* Copy color data */
			while(size_count++ < 0)
				*(line + line_offset++) = *(Byte *)(chunk + offset++);
			}
		}
		/* Move to next line */
		line = line + animation->Width;
	}
}

void Chunk_Decode_DELTA(Animation *animation, Byte *chunk)
{
	UWord num_lines;
	size_t offset = 8;
	Byte *line = animation->Frame;

	/* Go through each line */
	num_lines = *(UWord *)(chunk + 6);
	while(num_lines > 0) {
		SWord num_packets;
		size_t line_offset = 0;

		/* Get number of packets */
		num_packets = *(SWord *)(chunk + offset);
		offset += 2;

		/* If negative skip that many lines otherwise decode packets */

		if(num_packets < 0)
			line += animation->Width * (-num_packets);
		else {
			while(num_packets-->0) {
				int size_count;

				/* Skip unchanged pixels */
				line_offset += *(Byte *)(chunk + offset++);

				/* Decode changed pixels */
				size_count = *(SByte *)(chunk + offset++);
				if(size_count >= 0) {
				/* Copy color data */

					while(size_count-->0) {
						*(UWord *)(line+line_offset) =
							*(UWord *)(chunk + offset);
						line_offset += 2;
						offset += 2;
					}
				}
				else {
					UWord color;
					/* Fill with one color */
					color = *(UWord *)(chunk + offset);
					offset += 2;
					while(size_count++ < 0) {
						*(UWord *)(line + line_offset) = color;
						line_offset += 2;
					}
				}
			}

			/* Move to next line */
			line += animation->Width;
			num_lines--;
		}
	}
}

void Chunk_Decode_256_COLOR(Animation *animation, Byte *chunk)
{
	size_t offset = 8;
	UWord num_packets;
	int color = 0;
	Byte *pal;

	num_packets = *(UWord *)(chunk + 6);
	while(num_packets-- > 0) {
		int num_colors;

		/* Skip unchanged colors */
		color += *(Byte *)(chunk + offset++);

		/* Decode changed colors */
		num_colors = *(Byte *)(chunk + offset++);
		if(num_colors == 0)
			num_colors = 256;
		pal = (unsigned char *)animation->Palette + color * 3;
		while(num_colors-- > 0) {
			int i;
			for(i = 0; i < 3; i++){
				*pal++ = *(Byte *)(chunk + offset++) >> 2;
				color++;
			}
		}
	}
	/* Call palette update function if present */
	Setpal(animation->Palette);
}

void Chunk_Decode(Animation *animation, Byte *chunk)
{
	UWord type;
	/* Get chunk type */
	type = *(UWord *)(chunk+4);
	/* Process chunk */
	switch(type) {
		case 11:    /* FLI_COLOR */
			Chunk_Decode_COLOR(animation, chunk);
			break;
		case 12:    /* FLI_LC */
			Chunk_Decode_LC(animation, chunk);
			break;
		case 13:    /* FLI_BLACK */
			memset(animation->Frame, 0, animation->Length);
			break;
		case 15:    /* FLI_BRUN */
			Chunk_Decode_BRUN(animation, chunk);
			break;
		case 16:    /* FLI_COPY */
			memcpy(animation->Frame, chunk + 6, animation->Length);
			break;
		case 7:     /* FLI_DELTA */
			Chunk_Decode_DELTA(animation, chunk);
			break;
		case 4:     /* FLI_256_COLOR */
			Chunk_Decode_256_COLOR(animation, chunk);
			break;
	}
}
Byte Frame_Decode(Animation *animation)
{
	Byte *frame;
	size_t chunk_length;
	int num_chunks;
	size_t offset;
	long frame_offset;
	size_t frame_length;
	UWord magic;

	/* Check if end of animation */
	if(animation->CurFrame >= animation->NumFrames) {
		animation->CurFrame = 0;
		fseek(animation->Handle, 128, SEEK_SET);
		return(FALSE);
	}
	/* Read frame length */
	frame_offset = ftell(animation->Handle);
	frame_length = GetDWord(animation->Handle);
	magic = (UWord) getc(animation->Handle);
	magic |= (UWord) getc(animation->Handle) << 8;
	fseek(animation->Handle, frame_offset, SEEK_SET);
	if(magic != 0xF1FA) {
		animation->CurFrame++;
		fseek(animation->Handle, frame_length, SEEK_CUR);
		return(TRUE);
	}

	/* Allocate memory for frame */
	if((frame = malloc(frame_length)) == NULL)
		return(FALSE);

	/* Read frame to memory */
	fread(frame, frame_length, 1, animation->Handle);
	animation->CurFrame++;

	num_chunks = *(UWord *)(frame + 6);
	offset = 16;
	while(num_chunks-- > 0) {
		/* Process one chunk */
		chunk_length = *(DWord *)(frame + offset);
		Chunk_Decode(animation, frame + offset);
		offset += chunk_length;
	}

	free(frame);
	return(TRUE);
}

Byte Frame_Seek(Animation *animation, int frame)
{
	/* Check if need to seek from the start */

	if(frame < animation->CurFrame) {
		animation->CurFrame = 0;
		fseek(animation->Handle, 128, SEEK_SET);

	}
	/* Seek forward */
	while(animation->CurFrame < frame) {
		if(Frame_Decode(animation) == FALSE)
			return(FALSE);

	}
	return(TRUE);
}

Byte DecodeHeader(Animation *animation, Byte *header)
{
	/* Read information from animation header */
	animation->NumFrames = *(UWord *)(header + 6);
	animation->Width = *(UWord *)(header + 8);
	animation->Height = *(UWord *)(header + 10);
	animation->Length = animation->Width * animation->Height;
	if(*(UWord *)(header + 12) != 8)
		return(FALSE);
	return(TRUE);
}

void PutBlock(int x,int y,Byte *ptr)
{
	int width, height, x0, x1, y1, addx, i;
	Byte *VGA = (Byte *)MK_FP(0xa000,0);

	width   = *ptr++;
	width  += (*ptr++ << 8);
	height  = *ptr++;
	height += (*ptr++ << 8);
	addx = (x < 0) ? abs(x) : 0;
	x1 = width + x - addx;
	x0 = (x1 > 319) ? x0 = width - (x1 - 319) : width;

	y1 = height + y;
	if(y1 > 199) y1 = 199;
	VGA += y * 320 + x + addx;
	if(addx) {
		ptr += addx;
		x0 = width - addx;
	}
	for(i = y; i < y1; i++) {
		if(i >= 0)
			memcpy(VGA, ptr, x0);
		VGA += 320;
		ptr  += width;
	}
}

Byte setflc(char *name)
{
	FILE *fp;
	Byte header[128];

	/* Allocate memory for new animation structure */
	animate = malloc(sizeof(Animation));
	/* Try to open file */
	if((fp=fopen(name, "rb")) == NULL) {
		free(animate);
		return(FALSE);
	}
	/* Decode animation header */
	fread(header, 128, 1, fp);
	if( DecodeHeader(animate,header) == FALSE ) {
		free(animate);
		fclose(fp);
		return(FALSE);
	}
	/* Initialize rest of the animation structure */
	FLC = allocimage(animate->Width, animate->Height);
	frame = FLC + 4;
	memset(frame, 0, animate->Width * animate->Height);
	animate->Frame = frame;
	animate->Palette = palette;
	animate->Handle = fp;
	animate->CurFrame = 0;
	return(TRUE);
}

void showflc(int x,int y)
{
	clock_t lasttime = clock(), nowtime;
	while(Frame_Decode(animate) != FALSE) {
		PutBlock(x, y, FLC);
		if(kbhit()) break;
		while((nowtime = clock()) == lasttime);
		lasttime = nowtime;
	}
}

void closeflc(void)
{
	fclose(animate->Handle);
	free(animate);
	free(FLC);
}

void main(void)
{
	_AX= 0x13;
	geninterrupt(0x10);
	setflc("car.flc");
	showflc(0,0);
	showflc(100,0);
	showflc(130,80);
	closeflc();
	_AX= 0x03;
	geninterrupt(0x10);

}