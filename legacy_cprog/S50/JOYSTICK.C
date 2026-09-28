/** --------------------------------------------------------
 ** Joystick Library for Dos. 'JTEST.c'
 ** Version: 1.1
 ** Last modified: June 15th, 1997
 ** (C) 1997 Simone Zanella Productions.
 ** E-mail: szanella@dsi.unive.it
 **         zanella@prometeo.it
 ** Web:    http://www.dsi.unive.it/~szanella/index.htm
 **         http://members.tripod.com/~szanella/index.htm
 ** --------------------------------------------------------
 ** This is freeware: use it as you like, but ALWAYS include
 ** the original author's name in the docs of your program.
 ** --------------------------------------------------------
 **/
#include <stdlib.h>
#include <dos.h>
#include <limits.h>
#include <conio.h>
#include <io.h>
#include <fcntl.h>
#include <sys\stat.h>
#include <stdio.h>

/* Bit maps for ReadJoystick */
#define JOY_UP    0x01
#define JOY_DN    0x02
#define JOY_LT    0x04
#define JOY_RT    0x08
#define JOY_AF    0x10
#define JOY_BF    0x20
#define JOY_CF    0x40
#define JOY_DF    0x80
#define JOY_EF    0x100
#define JOY_FF    0x200

/* Flags for mode (function InstallJoystick) */
#define JOY_2BUTTONS   0
#define JOY_4BUTTONS   1
#define JOY_6BUTTONS   2

/* Maps for values returned by InstallJoystick,
	flags for skipjoy parameter */
#define JOY_NONE       0
#define JOY_FIRST      1
#define JOY_SECOND     2
#define JOY_BOTH       3

/* Public functions to read joystick(s) */
unsigned char InstallJoystick(const unsigned char mode, const unsigned char skipjoy, const char * calibfile);
void ReadJoystick(unsigned int *first, unsigned int *second);

#define JOYPORT              0x201
/* Number of divisions, for determining thresholds */
#define SEGMENTS             2
/* Tolerance, to determine direction on 6-buttons joysticks */
#define JOY_TOL              100
 /* Constant for timed joy reading */
#define JOYCOUNTER           60000
/* Pseudo-functions */
#define GetBit(c, n)   ( c & ( 1 << (n) ) )

/* Static variables used for storing:
** - x and y coordinates;
** - threshold values;
** - status (ready/not ready);
** - mode (2, 4 or 6 buttons);
** - flags. 		*/
static int x[2], y[2], calib[2][4];
static unsigned char jready[2], joymode = JOY_2BUTTONS;
static unsigned int jstatus[2];

/* Maps for fire buttons (internal) */
static unsigned char fire1[2] = {16, 64};
static unsigned char fire2[2] = {32, 128};

/******************************************************/
/** Internal functions: should NOT be called by user **/
/******************************************************/
static unsigned char _readjport(void)
{
  /** Read joystick port, setting x and y coordinates for each joystick;
	the status of the 4 buttons is returned. */

  register long count;
  register unsigned char st, mask;

  mask = 0;
  if (jready[0]) mask |= 3;
  if (jready[1]) mask |= 12;
  count = x[0] = y[0] = x[1] = y[1] = 0;
  disable();
  /* Read port for JOYCOUNTER cycles */
  /* Don't count previous reading (VERY FAST machines) */
  do st = inportb(JOYPORT);
  while (st & mask);
  outportb(JOYPORT, 0xFF);
  do {
    st = inportb(JOYPORT);
    if (st & 1)  x[0]++;
    if (st & 2)  y[0]++;
    if (st & 4)  x[1]++;
    if (st & 8)  y[1]++;
    count++;
  } while ((st & mask) && count <= JOYCOUNTER);
  enable();
  return st;
}

static unsigned char _readjbutton(const unsigned char j)
{
  /** Read joystick, returning 0 if no fire button is pressed.**/
  register unsigned char st, mask, pressed;
  if (j)
    mask = 12;
  else
    mask = 3;
  outportb(JOYPORT, 0xFF);
  st = inportb(JOYPORT);
  pressed = (j) ? (!(st & 64) || !(st & 128)) : (!(st & 16) || !(st & 32));
  while (st & mask)
    st = inportb(JOYPORT);
  return pressed;
}

static unsigned char _readjpos(const unsigned char j)
{
  /** Wait for the user to press a joystick button,
    then read joystick port; return 0 if user aborted calibration. **/

  delay(1000);

  /* Wait for button pressed */
  while (!_readjbutton(j))
    if (kbhit())
      if (getch() == 0x1B)
        return 0;
  _readjport();
  /* Wait for button released */
  while (_readjbutton(j));

  return 1;
}

static unsigned int _manualdir(const unsigned char j)
{
  /** Direction check for manual calibration. **/
  register unsigned int jstat = 0;

  if (x[j] < calib[j][0])
    jstat |= JOY_LT; /* Left */
  else
    jstat |= (x[j] > calib[j][1]) ? JOY_RT : 0; /* Right or center */
  if (y[j] < calib[j][2])
    jstat |= JOY_UP; /* Up */
  else
    jstat |= (y[j] > calib[j][3]) ? JOY_DN : 0; /* Down or center */
  return jstat;
}

unsigned char _usercalib(const unsigned char j)
{
  /** Print out messages for performing manual calibration for joystick j;
  set calibration values and return 1 if successfull, 0 if user aborted. **/

  unsigned char i, l;
  int centx[2], centy[2], minx[2], maxx[2], miny[2], maxy[2];
  int ocentx, ocenty;

  char *msg[]={"Center stick and press a button (Esc abort)...",
               "Move stick to upper left and press a button (Esc abort)...",
               "Move stick to lower right and press a button (Esc abort)...",
               "While pressing button 5, press button 1 or 2 (Esc abort)...",
               "While pressing button 6, press button 1 or 2 (Esc abort)..."};

  printf("Calibration of joystick %d..\n", j + 1);
  for (i = 0; i < 3; i++) {
    printf(msg[i]);
    l = _readjpos(j);
    printf("\n");
    if (!l)
      return 0;
    /* Insert values for center, maximum, minimum variables */
    switch (i) {
      case 0:
        centx[j] = x[j];
        centy[j] = y[j];
        ocentx = x[1];
        ocenty = y[1];
        break;
      case 1:
        minx[j] = x[j];
        miny[j] = y[j];
        break;
      default:
        maxx[j] = x[j];
        maxy[j] = y[j];
        break;
    }
  }
  if (joymode == JOY_6BUTTONS) {
    unsigned int jstat;
    for (i = 0; i < 2; i++) {
      /* We must calibrate pseudo-directions corresponding
	to buttons 5 and 6 */
      printf(msg[3 + i]);
      delay(1000);
retry:
      /* Wait for button pressed */
      while (!_readjbutton(j))
        if (kbhit())
          if (getch() == 0x1B)
            return 0;
      _readjport();
      jstat = 0;
      if (x[1] < ocentx - JOY_TOL)
        jstat |= JOY_LT; /* Left */
      else
        jstat |= (x[1] > ocentx + JOY_TOL) ? JOY_RT : 0; /* Right or center */
      if (y[1] < ocenty - JOY_TOL)
        jstat |= JOY_UP; /* Up */
      else
        jstat |= (y[1] > ocenty + JOY_TOL) ? JOY_DN : 0; /* Down or center */
      /* Wait for button released */
      while (_readjbutton(j));

      if (jstat & (i ? (JOY_LT | JOY_RT) : (JOY_UP | JOY_DN)))
        if (i) /* Button 6: can be LEFT or RIGHT */
	  if (x[1] > ocentx) {
	    /* Button corresponds to RIGHT */
            calib[1][1] = ocentx + ((x[1] - ocentx) / SEGMENTS);
            calib[1][0] = INT_MIN;
          }
	  else {
	  /* Button corresponds to LEFT */
            calib[1][1] = INT_MAX;
            calib[1][0] = ocentx - ((ocentx - x[1]) / SEGMENTS);
          }
        else /* Button 5: can be UP or DOWN */
	  if (y[1] > ocenty) {
	    /* Button corresponds to DOWN */
            calib[1][3] = ocenty + ((y[1] - ocenty) / SEGMENTS);
            calib[1][2] = INT_MIN;
          }
	  else {
	    /* Button corresponds to UP */
            calib[1][3] = INT_MAX;
            calib[1][2] = ocenty - ((ocenty - y[1]) / SEGMENTS);
          }
      else
        goto retry;
      printf("\n");
    }
  }
  printf("\n");
  /* line BEFORE WHICH left is stuffed */
  calib[j][0] = centx[j] - ((centx[j] - minx[j]) / SEGMENTS);

  /* line AFTER WHICH right is stuffed */
  calib[j][1] = centx[j] + ((maxx[j] - centx[j]) / SEGMENTS);

  /* line BEFORE WHICH up is stuffed */
  calib[j][2] = centy[j] - ((centy[j] - miny[j]) / SEGMENTS);

  /* line AFTER WHICH down is stuffed */
  calib[j][3] = centy[j] + ((maxy[j] - centy[j]) / SEGMENTS);

  return 1;
}

static void _readjoy(void)
{
  /* Set flags for each joystick (directions and fire buttons) */
  register int  v;
  register unsigned char st, j;

  st = _readjport();
  for (j = 0; j < 2; j++)
    if (jready[j]) {
      jstatus[j] = 0;
      if (!(st & fire1[j]))
        jstatus[j] |= JOY_AF;
      if (!(st & fire2[j]))
        jstatus[j] |= JOY_BF;
      jstatus[j] |= _manualdir(j);
      if (joymode) { /* 4 buttons or 6 buttons */
        v = j ? 0 : 1;
	if (!(st & fire1[v]))
          jstatus[j] |= JOY_CF;
	if (!(st & fire2[v]))
          jstatus[j] |= JOY_DF;

	/** Buttons 5 and 6 are connected to directions on second joystick.
        ** Only one 6-button joystick can be connected, so we use jstatus[0]
	** instead of jstatus[j].   */

	if (joymode == JOY_6BUTTONS) {
          v = _manualdir(1);
          if (v & (JOY_UP | JOY_DN))
            jstatus[0] |= JOY_EF;
	  if (v & (JOY_LT | JOY_RT))
            jstatus[0] |= JOY_FF;
	  j = 2;
        }
      }
    }
}

static unsigned char _joyready(const unsigned char j)
{
  /** Probe joystick, returning 1 if it is present, 0 otherwise.
      Presence is determined in this way:
   - if position (x and y) and both fire buttons read through bios are 0,
     joystick is absent;
   - otherwise, it is present.
     If 'j' is 0, probes the first joystick; if 'j' is 1,
     probes the second.*/

  union REGS regs;
  register int x, y, fa, fb;

  /* Read position */
  regs.h.ah = 0x84;
  regs.x.dx = 1;
  int86(0x15, &regs, &regs);
  if (regs.x.cflag)
    return 0; /* Error: joystick not found */

  if (j) {
    x = regs.x.cx;
    y = regs.x.dx;
  }
  else {
    x = regs.x.ax;
    y = regs.x.bx;
  }

  /* Read fire buttons */
  regs.h.ah = 0x84;
  regs.x.dx = 0;
  int86(0x15, &regs, &regs);
  if (regs.x.cflag)
    return 0; /* Error: joystick not found */
  if (j) {
    fa = !GetBit(regs.x.ax, 6);
    fb = !GetBit(regs.x.ax, 7);
  }
  else {
    fa = !GetBit(regs.x.ax, 4);
    fb = !GetBit(regs.x.ax, 5);
  }
  if (x + y + fa + fb == 0)
    return 0;
  else
    return 1;
}

static void _savecalib(const char *filename, const unsigned char njoy)
{
  /*
  ** Store number of joysticks connected, joystick mode and
  ** calibration informations into filename (which is created
  ** or overwritten). No errors are reported; if filename is NULL,
  ** calibration is not saved.
  */

  if (filename != NULL) {
    register int i, l;
    int h;
    struct calibrecord {
      unsigned char njoy;
      unsigned char joymode;
      int calib[2][4];
    } cr;

    cr.njoy = njoy;
    cr.joymode = joymode;
    for (i = 0; i < 2; i++)
      for (l = 0; l < 4; l++)
        cr.calib[i][l] = calib[i][l];
    h = open(filename, O_WRONLY | O_BINARY | O_CREAT | O_TRUNC, S_IWRITE);
    if (h != -1) {
      write(h, (void *) &cr, sizeof(cr));
      close(h);
    }
  }
}

static unsigned char _checkcalib(const unsigned char j)
{
  /*
  ** Check if joystick j is centered, according to current calibration;
  ** returns JOY_FIRST or JOY_SECOND (according to j) if it needs to
  ** be re-calibrated, JOY_NONE otherwise.
  ** This routine does two checks, at one-second interval each:
  ** if both return joystick off-centered, the program assumes that
  ** calibration is needed.
  */

  int try = 0;
  unsigned int jstat;

retry:
  _readjport();
  jstat = _manualdir(j);
  if (jstat)
    if (try)
      return j + 1;
    else {
      delay(1000);
      goto retry;
    }
  return JOY_NONE;
}

static unsigned char _loadcalib(const char *filename, const unsigned char njoy)
{
  /*
  ** Load calibration and returns:
  **
  ** JOY_NONE       if mode and joy # are correct and joys appear centered
  ** JOY_FIRST      if joy #1 must be re-calibrated
  ** JOY_SECOND     if joy #2 must be re-calibrated
  ** JOY_BOTH       if both joys need to be re-calibrated
  */

  if (filename != NULL) {
    int h, i, l;
    unsigned char oldnjoy;
    struct calibrecord {
      unsigned char njoy;
      unsigned char joymode;
      int calib[2][4];
    } cr;

    h = open(filename, O_RDONLY | O_BINARY, S_IREAD);
    /* File not found: re-calibration */
    if (h == -1)
      return njoy;
    /* Wrong size: remove file and force re-calibration */
    if (filelength(h) != sizeof(cr)) {
      close(h);
      remove(filename);
      return njoy;
    }

    l = read(h, (void *) &cr, sizeof(cr)) != sizeof(cr);
    close(h);
    /* Error reading: re-calibration */
    if (l)
      return njoy;
    /* Mode incompatibility: re-calibration */
    if ((joymode == JOY_6BUTTONS && cr.joymode != JOY_6BUTTONS) ||
        (cr.joymode == JOY_6BUTTONS && joymode != JOY_6BUTTONS))
      return njoy;

    /* Different number of joysticks: re-calibration for only the new joystick */
    oldnjoy = njoy;
    for (i = 0; i < 2; i++)
      for (l = 0; l < 4; l++)
        calib[i][l] = cr.calib[i][l];

    if (oldnjoy != cr.njoy) {
      unsigned char t = 0;
      for (i = 1; i < 3; i++)
        if ((oldnjoy & i) && (cr.njoy & i))
          t |= _checkcalib(i - 1);
        else
          if (oldnjoy & i)
            t |= i;
      return t;
    }
    return JOY_NONE;
  }
  else
    return njoy;   /* NULL file specified: re-calibration */
}

/********************************************/
/** External functions: joystick interface **/
/********************************************/

unsigned char InstallJoystick(const unsigned char mode, const unsigned char skipjoy, const char *calibfile)
{
 /** This function checks and returns the number of installed joysticks.
  **
  ** 'mode' can be:
  **
  ** JOY_2BUTTONS   2-buttons joysticks (one or two)
  ** JOY_4BUTTONS   4-buttons joysticks (one or two)
  ** JOY_6BUTTONS   6-buttons joystick (only one)
  **
  ** 'skipjoy' can be:
  **
  ** JOY_NONE    all joysticks present are installed and calibrated
  ** JOY_FIRST   skip installation/calibration for first joystick
  ** JOY_SECOND  skip installation/calibration for second joystick
  **
  ** Most of the times, skipjoy will be JOY_NONE (all joysticks installed
  ** and calibrated) or JOY_SECOND (only first joystick is installed and
  ** calibrated, e.g. when your program uses just one joystick).
  **
  ** 'calibfile' is the name of the file from which calibration must be
  ** loaded (if exists) or to which it will be saved (if does NOT exist).
  ** If 'calibfile' is NULL, calibration won't be saved, i.e. the user will
  ** have to calibrate joystick(s) at each run.
  ** If 'mode' is JOY_2BUTTONS or JOY_4BUTTONS and mode determined from
  ** configuration file is JOY_6BUTTONS (or viceversa), calibration will be
  ** forced; the same will happen if number of joysticks connected is
  ** different or if the calibration appears incorrect.
  ** If calibration is aborted for one joystick, that joystick will be
  ** reported as not connected (it will be re-calibrated the next time you
  ** run the program).
  **
  ** Values returned
  ** JOY_NONE    if no joystick is installed
  ** JOY_FIRST   if only joystick 1 is installed
  ** JOY_SECOND  if only joystick 2 is installed
  ** JOY_BOTH    if both joysticks (or one 6-buttons joystick) are installed
  **
  ** Central values are set at current position. **/

  register unsigned char retval = 0, j;
  unsigned char j2calib;

  joymode = mode;

  /* Determine joysticks attached */
  for (j = 0; j < 2; j++)
    if ((jready[j] = _joyready(j)) != 0)
      retval += j + 1;

  /* Revert to 4-buttons mode if 6-buttons joystick not found */
  if (joymode == JOY_6BUTTONS && retval < JOY_BOTH)
    joymode = JOY_4BUTTONS;

  /* Prompt the user to calibrate joystick(s) */
  j2calib = _loadcalib(calibfile, retval);
  for (j = 0; j < 2; j++) {
    if ((skipjoy & (j + 1)) || (jready[j] &&
	(j2calib & (j + 1)) && !_usercalib(j))) {
      jready[j] = 0;
      retval -= j + 1;
    }
    /* No need to calibrate second (virtual) joystick when in 6-buttons mode */
    if (joymode == JOY_6BUTTONS)
      j = 2;
  }
  if (retval)
    _savecalib(calibfile, retval);
  return retval;
}

void ReadJoystick(unsigned int *first, unsigned int *second)
{
 /** Read both joysticks, returning into "first" and "second" an
  ** unsigned integer with the following flags set:
  **
  ** JOY_UP    Joystick moved up
  ** JOY_DN    Joystick moved down
  ** JOY_LT    Joystick moved to left
  ** JOY_RT    Joystick moved to right
  ** JOY_AF    Button 1 pressed
  ** JOY_BF    Button 2 pressed
  ** JOY_CF    Button 3 pressed (joymode = JOY_4BUTTONS or JOY_6BUTTONS)
  ** JOY_DF    Button 4 pressed (joymode = JOY_4BUTTONS or JOY_6BUTTONS)
  ** JOY_EF    Button 5 pressed (joymode = JOY_6BUTTONS)
  ** JOY_FF    Button 6 pressed (joymode = JOY_6BUTTONS)
  **
  ** If a NULL pointer is passed, no data is stored (useful if data
  ** for only one joystick are needed). */

  _readjoy();
  if (first)
    *first = jstatus[0];
  if (second)
    *second = jstatus[1];
}
/*--------------------- end lib ---------------------------*/
static int mode = JOY_2BUTTONS;
void printstatus(unsigned char jready, unsigned int j0, unsigned int j1)
{
  /* Show status for both joysticks */

  char l[13][26];
  unsigned char j, o, ln;
  unsigned int jflags;

  strcpy(l[0],  "     ³  ³          ³  ³  ");
  strcpy(l[1],  "   ÄÄÅÄÄÅÄ-      ÄÄÅÄÄÅÄ-");
  strcpy(l[2],  "     ³  ³          ³  ³  ");
  strcpy(l[3],  "   ÄÄÅÄÄÅÄÄ      ÄÄÅÄÄÅÄ-");
  strcpy(l[4],  "     ³  ³          ³  ³  ");
  strcpy(l[5],  "");
  strcpy(l[6],  "   A ³  ³        A ³  ³  ");
  strcpy(l[7],  "");
  strcpy(l[8],  "   B ³  ³        B ³  ³  ");
  strcpy(l[9],  "");
  strcpy(l[10], "   C ³  ³        C ³  ³  ");
  strcpy(l[11], "");
  strcpy(l[12], "   D ³  ³        D ³  ³  ");

  for (j = 0; j < 2; j++)
    if (jready & (j + 1)) {
      jflags = j ? j1 : j0;
      if (jflags & JOY_UP) {
        ln = 0;
        if (jflags & JOY_LT || jflags & JOY_RT)
          o = (jflags & JOY_LT) ? 3 : 9;
        else
          o = 6;
      }
      else
	if (jflags & JOY_DN) {
          ln = 4;
          if (jflags & JOY_LT || jflags & JOY_RT)
            o = (jflags & JOY_LT) ? 3 : 9;
          else
            o = 6;
        }
	else {
          ln = 2;
          if (jflags & JOY_LT || jflags & JOY_RT)
            o = (jflags & JOY_LT) ? 3 : 9;
          else
            o = 6;
        }
      l[ln][o + (j ? 14 : 0)] = 0xDB;
      l[ln][o + (j ? 15 : 1)] = 0xDB;
      if (jflags & JOY_AF) {
        l[6][(j ? 20 : 6)] = 0xDB;
        l[6][(j ? 21 : 7)] = 0xDB;
      }
      if (jflags & JOY_BF) {
        l[8][(j ? 20 : 6)] = 0xDB;
        l[8][(j ? 21 : 7)] = 0xDB;
      }
      if (mode > JOY_2BUTTONS) {

	if (jflags & JOY_CF) {
          l[10][(j ? 20 : 6)] = 0xDB;
          l[10][(j ? 21 : 7)] = 0xDB;
	}

	if (jflags & JOY_DF) {
          l[12][(j ? 20 : 6)] = 0xDB;
          l[12][(j ? 21 : 7)] = 0xDB;
        }

	if (mode == JOY_6BUTTONS) {
          int i;

          for (i = 0; i < 9; i++)
            strcpy(l[i] + 17, "        ");

          l[10][17] = 'E';
          l[12][17] = 'F';

	  if (jflags & JOY_EF) {
            l[10][20] = 0xDB;
            l[10][21] = 0xDB;
          }

	  if (jflags & JOY_FF) {
            l[12][20] = 0xDB;
            l[12][21] = 0xDB;
          }
	  goto end;
        }
      }
    }
end:
  for (j = 0; j < ((mode == JOY_2BUTTONS) ? 9 : 13); j++) {
    cputs(l[j]);
    cputs("\r\n");
  }
}

int main(int argc, char *argv[])
{
  int j, i;
  unsigned int status[2], oldstat[2];
  unsigned char sr;
  char * cp;

  clrscr();
  printf("JTEST - Joystick Test v1.1 / (C) 1997 Simone Zanella Productions\n\n");
  printf("Usage: JTEST [mode]\n");
  printf("Mode can be:   [0] = 2 buttons   1 = 4 buttons   2 = 6 buttons\n\n");

  /* Read mode (if specified) */
  if (argc > 1)
    mode = min(max(atoi(argv[1]), JOY_2BUTTONS), JOY_6BUTTONS);

  /* Build configuration file name (it will be located in JTEST.EXE directory) */
  cp = argv[0] + strlen(argv[0]) - 1;
  while (*cp != '.')
    cp--;
  strcpy(cp + 1, "JC");

  /* Initialize joystick(s) */
  sr = wherey();
  j = InstallJoystick(mode, JOY_NONE, argv[0]);
  gotoxy(1, sr);
  for (i = 0; i < 15; i++)
    delline();

  if (j) {
    printf("Joystick(s): %d. Mode: %d buttons\n",
           (j > 2) ? (mode == JOY_6BUTTONS ? 1 : 2) : 1, (mode + 1) * 2);

    printf("\r\nPress any key on the keyboard to exit..\n\n");
    oldstat[0] = oldstat[1] = -1;
    sr = wherey();

    /* Wait for a keypress */
    while (!kbhit()) {
      /* Read joystick(s) */
      ReadJoystick(&(status[0]), &(status[1]));
      if (status[0] != oldstat[0] || status[1] != oldstat[1]) {
        oldstat[0] = status[0];
        oldstat[1] = status[1];
        gotoxy(1, sr);
        /* Print status */
        printstatus(j, status[0], status[1]);
      }
    }
    /* Remove keypress from keyboard buffer */
    getch();
  }
  else
    cprintf("\nNo joysticks found.\n");
  return 0;
}
