{*******************************
******************************}
 Unit kfade;
 InterFace

 Uses Crt;

 Const
   PelAddrRgR  = $3C7;
   PelAddrRgW  = $3C8;
   PelDataReg  = $3C9;

 Type
   Rgb = Record
           R, G, B : Byte;
         End;

 Var I : Integer; Ch : Char; Col : Array[0..63] Of Rgb;


 Procedure GetCol(C : BYTE; VAR R, G, B : BYTE);
 Procedure SetCol(C, R, G, B : BYTE);
 Procedure SetInten(b : BYTE);
 Procedure InitRgb;
 Procedure FadeIn(Del : Word);
 Procedure FadeOut(Del : Word);

 Implementation

 Procedure GetCol(C : BYTE; VAR R, G, B : BYTE);
 Begin
   Port[PelAddrRgR] := C;
   R := Port[PelDataReg];
   G := Port[PelDataReg];
   B := Port[PelDataReg];
 End;

 Procedure SetCol(C, R, G, B : BYTE);
 Begin
   Port[PelAddrRgW] := C;
   Port[PelDataReg] := R;
   Port[PelDataReg] := G;
   Port[PelDataReg] := B;
 End;

 Procedure SetInten(b : BYTE);
 Var I          : Integer;
     fr, fg, fb : Byte;
 Begin
   For i := 0 To 63 Do
   Begin
      fr := col[i].r*b DIV 63;
      fg := col[i].g*b DIV 63;
      fb := col[i].b*b DIV 63;
      SetCol(i, fr, fg, fb);
   End;
 End;

 Procedure InitRgb;
 Begin
   For i := 0 To 63 Do
     GetCol(i, col[i].r, col[i].g, col[i].b);
 End;

 Procedure FadeIn(Del : Word);
 Begin
   For I := 63 DownTo 0 Do
   Begin
     SetInten(I);
     Delay(Del);
   End;
 End;

 Procedure FadeOut(Del : Word);
 Begin
   For I := 0 To 63 Do
   Begin
     SetInten(I);
     Delay(Del);
   End;
 End;
End.