/*
     GIF format save code
     Exact details can be obtained from CompuServe.
     3D Engine
*/
#include <stdlib.h>
#include <stdio.h>
#include <conio.h>
#include <mem.h>
#include <dos.h>

#define largest_code    4095
#define table_size      5003
typedef struct {
     signed char sig[6];
     unsigned short screenwidth;
     unsigned short screendepth;
     unsigned char  flags;
     unsigned char  background;
     unsigned char  aspect;
} GIFHEADER;

typedef struct {
     unsigned short left;
     unsigned short top;
     unsigned short width;
     unsigned short depth;
     unsigned char flags;
} IMAGEBLOCK;

static char code_buffer[259];
static unsigned char *ptr;
static long pixctr;
static long maxctr;
static short oldcode[table_size];
static short currentcode[table_size];
static unsigned char newcode[table_size];
static short code_size;
static short clear_code;
static short eof_code;
static short bit_offset;
static short byte_offset;
static short bits_left;
static short max_code;
static short free_code;

void init_table (short min_code_size)
{
     short i;

     code_size = min_code_size + 1;
     clear_code = (1 << min_code_size);
     eof_code  = clear_code + 1;
     free_code = clear_code + 2;
     max_code = (1 << code_size);
     for (i = 0; i < table_size; i++)
          currentcode[i] = 0;
}

void flush (FILE *fp, short n)
{
     fputc (n, fp);
     fwrite (code_buffer, 1, n, fp);
}

void write_code (FILE *fp, short code)
{
     unsigned long temp;

     byte_offset = bit_offset >> 3;
     bits_left = bit_offset & 7;

     if (byte_offset >= 254) {
          flush (fp, byte_offset);
          code_buffer[0] = code_buffer[byte_offset];
          bit_offset = bits_left;
          byte_offset = 0;
     }
     if (bits_left > 0) {
          temp = ((long) code << bits_left) | code_buffer[byte_offset];
          code_buffer[byte_offset] = temp;
          code_buffer[byte_offset + 1] = (temp >> 8);
          code_buffer[byte_offset + 2] = (temp >> 16);
     } else {
          code_buffer[byte_offset] = code;
          code_buffer[byte_offset + 1] = (code >> 8);
     }
     bit_offset += code_size;
}

short readpixel (void)
{
     unsigned char pxl;

     pixctr++;
     if (pixctr > maxctr)
          return 9999;
     pxl = *ptr;
     ptr++;
     return (pxl);
}

void compressimage (FILE *fp)
{
     short prefix_code;
     short suffix_char;
     short hx, d;

     /* write initial code size */
     fputc (8, fp);

     /* initialize the encoder */
     bit_offset = 0;
     init_table (8);
     write_code (fp, clear_code);
     if ((suffix_char = readpixel()) == 9999)
          return;

     /* initialize the prefix */
     prefix_code = suffix_char;

     /* get a character to compress */
     while ((suffix_char = readpixel()) != 9999) {
          /* derive an index into the code table */
          hx = (prefix_code ^ (suffix_char << 5)) % table_size;
          d = 1;
          for (;;) {
               /* see if the code is in the table */
               if (currentcode[hx] == 0) {
                    /* if not, put it there */
                    write_code (fp, prefix_code);
                    d = free_code;

                    /* find the next free code */
                    if (free_code <= largest_code) {
                         oldcode[hx] = prefix_code;
                         newcode[hx] = suffix_char;
                         currentcode[hx] = free_code;
                         free_code++;
                    }

                    /* expand the code size or scrap the table */
                    if (d == max_code) {
                         if (code_size < 12) {
                              code_size++;
                              max_code <<= 1;
                         }
                         else {
                              write_code (fp, clear_code);
                              init_table (8);
                        }
                    }
                    prefix_code = suffix_char;
                    break;
               }
	       if(oldcode[hx] == prefix_code && newcode[hx] == suffix_char) {
                    prefix_code = currentcode[hx];
                    break;
               }
               hx += d;
               d += 2;
               if (hx >= table_size)
                    hx -= table_size;
               }
          }

          /* write the prefix code */
          write_code (fp, prefix_code);

          /* and the end of file code */
          write_code (fp, eof_code);

          /* flush the buffer */
          if (bit_offset > 0)
               flush (fp, (bit_offset+7)/8);
          /* write a zero length block */
          flush (fp, 0);
}

void savegif (char *filename, unsigned char *image, char *palette)
{
     GIFHEADER gh;
     IMAGEBLOCK iblk;
     short b;
     FILE *fp;
     unsigned char pal[768];

     if ((fp = fopen (filename, "wb")) == NULL)
          return;
     ptr = image + 4;
     memset ((char *) &gh, 0, sizeof(GIFHEADER));
     memcpy (gh.sig, "GIF87a", 6);
     gh.screenwidth = ((image[1] & 0xff) << 8) + (image[0] & 0xff);
     gh.screendepth = ((image[3] & 0xff) << 8) + (image[2] & 0xff);
     gh.flags = 0xf7;
     fwrite((char *) &gh, 1, sizeof(GIFHEADER), fp);

     for (b = 0; b < 768; b++)
          pal[b] = palette[b] << 2;
     fwrite (pal, 1, 768, fp);
     memset ((char *) &iblk, 0, sizeof (IMAGEBLOCK));
     fputc(',', fp);
     iblk.left = 0;
     iblk.top  = 0;
     iblk.width = gh.screenwidth;
     iblk.depth = gh.screendepth;
     iblk.flags = 0x7;
     fwrite ((char *) &iblk, 1, sizeof (IMAGEBLOCK), fp);
     pixctr = 0;
     maxctr = iblk.width * iblk.depth;
     compressimage (fp);
     fputc (';', fp);
     fclose (fp);
}

void setpalette(unsigned char *pal)
{
     int i;
     unsigned char *ptr;
     ptr = pal;
     for(i = 0; i < 64; i++) {
          *ptr++ = i;
          *ptr++ = 0;
          *ptr++ = 0;
     }
     for(i = 0; i < 64; i++) {
          *ptr++ = 0;
          *ptr++ = i;
          *ptr++ = 0;
     }
     for(i = 0; i < 64; i++) {
          *ptr++ = 0;
          *ptr++ = 0;
          *ptr++ = i;
     }
     for(i = 0; i < 64; i++) {
          *ptr++ = i;
          *ptr++ = i;
          *ptr++ = i;
     }
     outp(0x3c8, 0);
     for(i = 0; i < 768; i++)
          outp(0x3c9, *pal++);
}

char *VGA = MK_FP(0xa000, 0);
char namepic[] = "pic0.gif";
void putpix(int x, int y, int color)
{
     *(VGA + y * 320 + x) = color;
}

void bar(int x0, int y0, int x1, int y1, int color)
{
     int i, j;

     for(j = y0; j < y1; j++)
          for(i = x0; i < x1; i++)
               *(VGA + j * 320 + i) = color;
}

void main(void)
{
     int i, j;
     char palette[768];
     unsigned char *image;

     image = malloc(320 * 200 + 4);
     ptr   = image;

     *ptr++ = 64;
     *ptr++ = 1;
     *ptr++ = 200;
     *ptr++ = 0;
     randomize();
     _AX = 0x13;
     geninterrupt(0x10);
     setpalette(palette);

     for(j = 0; j < 200; j++)
          for(i = 0; i < 320; i++)
               putpix(i, j, (i * j + i * i + j * j + i * i * 320));
     for(i = 0; i < 256; i++)
          bar(i + 32, 188, i + 33, 198, i);
     memcpy(image + 4, VGA, 320 * 200);
     savegif("pic.gif", image, palette);
     getch();
     memset(VGA, 0, 320 * 200);
     j = 0;
     for(i = 0; i < 2000; i++) {
          bar(random(320), random(200), random(320),
               random(200), random(256));
         if(j++ > 200) {
               j = 0;
               memcpy(image + 4, VGA, 320 * 200);
               savegif(namepic, image, palette);
               namepic[3] ++;
          }
     }
     _AX = 3;
     geninterrupt(0x10);
}