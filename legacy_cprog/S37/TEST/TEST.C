//±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±
// File        : TEST.H
// Description : Vesa Bios Extention 2.0 test file
// Notes       : Brought to you by Vertigo. If you use this, or have
//               learned from this, send us an email and/or Greet us
//               In your demo =).
//
//±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±

#include <stdio.h>
#include <conio.h>
#include "VBE20.H"

char *memModel[]=
{
  "TEXT",
  "CGA",
  "HERCULES",
  "PLANAR",
  "PACKED",
  "MODEX",
  "RGB",
  "YUV"
};

void printModes(VBEINFO *vbeInfo);

//°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
// Main entry point
//°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
void main(void)
{
  VBEINFO *vbeInfo;

  // Detect the VBE bios

  if( (vbeInfo = vbeDetect()) == NULL )
  {
    printf("Can't find VESA bios extentions\n");
    exit(0);
  }

  // Print basic VBE info

  printf("\nVBE Version      : %d.%d\n"
	 "Oem              : %s\n"
	 "Total memory     : %gK\n",
	  vbeInfo->VbeVersion>>8,
	  vbeInfo->VbeVersion&0xFF,
	  vbeInfo->OemStringPtr,
	  ((float)vbeInfo->TotalMemory*64000.0f)/1024.0f);


  // Print extended VBE 2.0 info, if available

  if( vbeInfo->VbeVersion >= 0x200 )
  {

    printf("Oem software rev : %d.%d\n"
	   "Oem vendor name  : %s\n"
	   "Oem product name : %s\n"
	   "Oem product rev  : %s\n",
	    vbeInfo->OemSoftwareRev>>8,
	    vbeInfo->OemSoftwareRev&0xFF,
	    vbeInfo->OemVendorNamePtr,
	    vbeInfo->OemProductNamePtr,
	    vbeInfo->OemProductRevPtr);
  }

  // Check capabilities

  if( vbeInfo->Capabilities & VBE_CAPS_8BITDAC )
    printf("DAC can be 8bit\n");

  if( vbeInfo->Capabilities & VBE_CAPS_NONVGA )
    printf("Non-VGA compatible controller\n");

  if( vbeInfo->Capabilities & VBE_CAPS_BLANKRAMDAC )
    printf("Programmed DAC width blank bit\n");


  printf("\nPress any key for mode list\n");
  getch();

  printModes(vbeInfo);

}

//°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
// Print mode list
//
// In:
//   vbeInfo -> VBEINFO structure
//
// Out:
//   NONE
//
//°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
void printModes(VBEINFO *vbeInfo)
{
  VBEMODEINFO vbeModeInfo;
  unsigned short *vbeMode;

  vbeMode      = vbeInfo->VideoModePtr;
  while( *vbeMode != 0xFFFF )
  {
    if( vbeGetModeInfo(*vbeMode,&vbeModeInfo) )
    {
      printf("%xh : %4d x %-4d %2dbpp  ",
	     *vbeMode,
	     vbeModeInfo.XResolution,
	     vbeModeInfo.YResolution,
	     vbeModeInfo.BitsPerPixel);
    }
    // We only check overall mode attributes, and
    // ignore window A and B, since we're aiming
    // for LFB modes.

    if( vbeModeInfo.ModeAttributes & VBEMODE_CAPS_AVAILABLE )
      printf("AVL ");
    else
      printf("--- ");

    if( vbeModeInfo.ModeAttributes & VBEMODE_CAPS_TTYOUTPUT )
      printf("TTY ");
    else
      printf("--- ");

    if( vbeModeInfo.ModeAttributes & VBEMODE_CAPS_COLORMODE )
      printf("CLR ");
    else
      printf("--- ");

    if( vbeModeInfo.ModeAttributes & VBEMODE_CAPS_GRAPHMODE )
      printf("GRPH ");
    else
      printf("---- ");

    if( vbeModeInfo.ModeAttributes & VBEMODE_CAPS_NONVGA )
      printf("NONVGA ");
    else
      printf("VGA    ");

    if( vbeModeInfo.ModeAttributes & VBEMODE_CAPS_NONBANKED )
      printf("NONBANKED ");
    else
      printf("BANKED    ");

    if( vbeModeInfo.ModeAttributes & VBEMODE_CAPS_LINEAR )
      printf("LFB   ");
    else
      printf("NOLFB ");

    // Print memory model

    printf("(%s)\n",memModel[vbeModeInfo.MemoryModel]);

    vbeMode++;
  }
}
