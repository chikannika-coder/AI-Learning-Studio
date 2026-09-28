/* graph.h header file */
#include <stdio.h>
#include <conio.h>
#include <dos.h>
#include <mem.h>
#include <stdlib.h>
#include <time.h>
#include <alloc.h>
#include <math.h>
typedef unsigned char BYTE;
#define TextMode() { _AX = 3; geninterrupt(0x10); }
#define SetActivePage(page) PageStart = FirstAdr[page]
void SetModeX(void);
void SetVisualPage(BYTE page);
void CopyPage(int pdest,int psource);
void PutPixel(int x, int y, BYTE color);
BYTE GetPixel(int x, int y);
void Bar(int x0,int y0,int x1,int y1,BYTE color);
void Vline(int x0,int x1,int y,BYTE color);
void Hline(int x,int y0,int y1,BYTE color);
void Rectangle(int x0,int y0,int x1,int y1,BYTE color);
void SetNewPAL(void);
/* ---- keyboard ---- */
void interrupt NewKeyInt(void);
void NewIntkey(void);
void SetOldkey(void);
