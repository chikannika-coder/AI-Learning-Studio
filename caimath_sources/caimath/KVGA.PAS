{






                     }
Unit Kvga;
Interface
Uses Crt,Graph,Dos;
Type
         NameHeap                  =    ^HeapSt;
         HeapSt                    =    string[14];
         FontSize                  =    Array[1..20] Of Byte;
         FontType                  =    Array[0..255] Of FontSize;
         String120                 =    String[120];
         String30                  =    String[30];

Const    Bit : Array[0..7] Of Byte =    (1,2,4,8,16,32,64,128);

Var
         Font                      :    FontType;
         FiFont                    :    File Of FontType;
         Col,Row,XMouse,
         YMouse,MaxColumn       :    integer;
         Ch,Funckey                :    Char;
         SolidSquare               :    Array[1..6] of PointType;
         UpShade                   :    Array[1..6] of PointType;
         DownShade                 :    Array[1..6] of PointType;
         No                        :    Byte;
         Fname                     :    Array[1..250] of NameHeap;
         DownMode                  :    Boolean;
         Regs                      :    Registers;


Procedure  Soundon(note,tone,Delaytime : integer);
Procedure  OpenGraph;
Procedure  Readchar;
Procedure  LoadFont(Finame : String30);
Procedure  PutChar(x1,y1,x,y : Integer; Ind : Byte);
Procedure  Writexy(x,y : integer; Message : String120);
Procedure  WritexyPixel(x,y : integer; Message : String120);
Procedure  Bbar(x1,y1,x2,y2 : word; patt,color : byte);
Procedure  Block3d(x1,y1:integer; Key : string; Mode:byte);
Procedure  Board3d(x1,y1,x2,y2: Integer;DownMode,Color:Byte;Size : Integer);
Procedure  Clsgr(X1,Y1,X2,Y2 : Integer);

IMPLEMENTATION

Procedure Clsgr(X1,Y1,X2,Y2 : Integer);
Var OldFill : FillSettingsType;
Begin
  GetFillSettings(OldFill);
  SetFillStyle(0,OldFill.Color);
  Bar (X1,Y1,X2,Y2);
  SetFillStyle(OldFill.Pattern,OldFill.Color);
End;

Procedure Soundon(note, tone, Delaytime : integer);
Begin
        Sound( note * tone div 3 );
        delay(Delaytime);
        nosound;
End;

Procedure Egavgadriver;external;{$L Vgadrv.obj}

Procedure Opengraph;
var GraphDriver,GraphMode,Graphck,Grfont   :    integer;
begin
     Detectgraph(Graphdriver,Graphmode);
     GraphDriver:=detect;
     case  Graphdriver of
         7: begin
            Clrscr;
            writeln('This Program Support VGA Monitor Only'#10);
            halt;
            end;
        else
            Graphmode:=1;
        end;
            Graphck:=RegisterBgiDriver(@EgaVgaDriver);
            initgraph(Graphdriver,Graphmode,'c:\lang\tp7\egavga.bgi');
End;

Procedure Readchar;
begin
     repeat
        regs.AH:=$1;  intr($16,regs);
     until KeyPressed;
        Regs.AH:=$0;  intr($16,regs);
        ch:=char(regs.AX); Funckey:=#0;
        if ch=#0 then Funckey:=chr(regs.AH);
end;

Procedure  LoadFont(Finame : String30);
Var  i,j,k : byte;
     ch : char;
begin
            Assign(Fifont,Finame);
            {$I-} reset(fifont); {$I+}
            If IOresult <> 0 then
            begin
               Closegraph;
               textcolor(15);write('Font ');
               textcolor(14);gotoxy(6,1);write('Support ');
               textcolor(11);gotoxy(14,1);write('Not ');
               textcolor(12);gotoxy(18,1);write('Found.');
               normvideo;
               halt(0);
            end;
            reset(fifont);
            Read(Fifont,Font);
            close(fifont);
end;

Procedure  PutChar(x1,y1,x,y : Integer; Ind : Byte);
var  Bfont  :  Byte;
     Color  :  Word;
     Pixel  :  Word;
     i,j    :  Integer;
         begin
            For j := 1 To 20 Do
            begin
               Bfont := Font[Ind,j];
               (*Bfont := (Font[Ind,j]) Or (Font[Ind,j] Shl 1);  // Bold//*)
               For i := 7 Downto 0 Do
               begin
                  If Bit[i] and Bfont <> $0 Then
                  begin
                     Color := GetColor;
                     PutPixel((x*8)+(7-i),(y*x1)+j-y1,Color);
                  end
                  else
                  begin
{                     Pixel := GetPixel((x*8)+(7-i),y+j);
                     PutPixel((x*8)+(7-i),y+j,Pixel);         }
                  end;
               end;
            end;
         end;


Procedure  Writexy(x,y : integer; Message : String120);
var  len,ind : Byte;
Begin
            Row  := y;  Col := x;
            For len := 1 to Length(Message) Do
            begin
               Ind := Ord(Message[len]);
               case ind  of
                 209,212..219,231..238 : begin
                                            dec(col);
                                         end;
               end; { case ind of }
               PutChar(19,15,col,row,ind);
               inc(col);
            end;
         end;

Procedure  WritexyPixel(x,y : integer; Message : String120);
var  len,ind : Byte;
Begin
            Row  := y;  Col := x;
            For len := 1 to Length(Message) Do
            begin
               Ind := Ord(Message[len]);
               case ind  of
                 209,212..219,231..238 : begin
                                            dec(col);
                                         end;
               end; { case ind of }
               PutChar(1,0,col,row,ind);
               inc(col);
            end;
         end;



Procedure Bbar(x1,y1,x2,y2:word; patt,color:byte);
begin
     SetFillStyle(Patt,color);
     bar(x1,y1,x2,y2);
end;

Procedure Block3d(x1,y1:integer; Key:string; Mode:byte);
var xx,yy,x2,y2 : word;  cc,c1,c2:byte;
begin
     SetTextstyle(0,0,1);
     xx:=x1; yy:=y1; x2:=x1+length(Key)*8+5;  Y2:=Y1+14;
     SolidSquare[1].x:=x1; SolidSquare[1].y:=y1;
     SolidSquare[2].x:=x2; SolidSquare[2].y:=y1;
     SolidSquare[3].x:=x2; SolidSquare[3].y:=y2;
     SolidSquare[4].x:=x1; SolidSquare[4].y:=y2;
     cc:=getcolor;
     setcolor(0); rectangle(x1-1,y1-1,x2+1,y2);
     rectangle(x1-2,y1-2,x2+2,y2+1); setcolor(cc);
     c1:=15; c2:=8;
     if DownMode then
        begin
             c1:=8; c2:=15;
        end;
     if Mode=0 then
        begin
          Upshade[1].x:=x1;         Upshade[1].y:=y1;
          Upshade[2].x:=x2;         Upshade[2].y:=y1;
          Upshade[3].x:=x2-2;       Upshade[3].y:=y1+2;
          Upshade[4].x:=x1+2;       Upshade[4].y:=y1+2;
          Upshade[5].x:=x1+2;       Upshade[5].y:=y2-2;
          Upshade[6].x:=x1;         Upshade[6].y:=y2;
          DownShade[1].x:=x1;       DownShade[1].y:=y2;
          DownShade[2].x:=x1+2;     DownShade[2].y:=y2-2;
          DownShade[3].x:=x2-2;     DownShade[3].y:=y2-2;
          DownShade[4].x:=x2-2;     DownShade[4].y:=y1+2;
          DownShade[5].x:=x2;       DownShade[5].y:=y1;
          DownShade[6].x:=x2;       DownShade[6].y:=y2;
          SetFillstyle(1,7);        FillPoly(4,SolidSquare);
          SetFillStyle(1,c1);       FillPoly(6,Upshade);
          SetFillStyle(1,c2);       FillPoly(6,Downshade);
          Setcolor(0);              OutTextXY(xx+4,yy+3,key);
        end
        else
         begin
            SetFillStyle(1,7);     FillPoly(4,SolidSquare);
            Setcolor(0);           OutTextxy(xx+4,yy+3,key);
         end;
           DownMode:=False;
end;

PROCEDURE Board3d(x1,y1,x2,y2:integer; Downmode,Color : Byte;Size : Integer);
var  xx,yy : word;  c1,c2 : byte;
begin
      xx:=x1;
      SolidSquare[1].x:=x1;      SolidSquare[1].y:=y1;
      SolidSquare[2].x:=x2;      SolidSquare[2].y:=y1;
      SolidSquare[3].x:=x2;      SolidSquare[3].y:=y2;
      SolidSquare[4].x:=x1;      SolidSquare[4].y:=y2;
      Setcolor(0);
      rectangle(x1-1,y1-1,x2+1,y2);
      rectangle(x1-2,y1-2,x2+2,y2+1);
      Upshade[1].x:=x1;         Upshade[1].y:=y1;
      Upshade[2].x:=x2;         Upshade[2].y:=y1;
      Upshade[3].x:=x2-Size;       Upshade[3].y:=y1+Size;
      Upshade[4].x:=x1+Size;       Upshade[4].y:=y1+Size;
      Upshade[5].x:=x1+Size;       Upshade[5].y:=y2-Size;
      Upshade[6].x:=x1;         Upshade[6].y:=y2;
      DownShade[1].x:=x1;       DownShade[1].y:=y2;
      DownShade[2].x:=x1+Size;     DownShade[2].y:=y2-Size;
      DownShade[3].x:=x2-Size;     DownShade[3].y:=y2-Size;
      DownShade[4].x:=x2-Size;     DownShade[4].y:=y1+Size;
      DownShade[5].x:=x2;       DownShade[5].y:=y1;
      DownShade[6].x:=x2;       DownShade[6].y:=y2;
        c1:=15; c2:=8;
      if DownMode = 1 then
        begin
             c1:=8; c2:=15;
        end;
            SetFillstyle(1,Color);        FillPoly(4,SolidSquare);
            SetFillStyle(1,c1);       FillPoly(6,Upshade);
            SetFillStyle(1,c2);       FillPoly(6,Downshade);
            DownMode:=0;
end;
END.
