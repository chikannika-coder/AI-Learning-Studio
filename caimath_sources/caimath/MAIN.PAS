{$M 16384,0,327680}
Program CAI_Mathematic_Conic_Section;
Uses graph,crt,dos,kfade,kvga,yjjsvga;
Var
   real_delay,real_delay2 : real;
   ch{,ikey}              : char;
   valout,x,y,err         : integer;
   exit                   : boolean;
   serr                   : string;
{+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++}

Procedure YJJdelay(ms : word);
var Xdelay : word;
begin
     Xdelay := round((real_delay2*ms)/5000);
     delay(Xdelay);
end;

Procedure Draw_Quadant(xorigin,yorigin,colorquadant,length : integer);
var ci   : integer;
    Quit : boolean;
begin
     quit := false;
     ci   := 0;
     repeat
           setcolor(colorquadant);
           line(xorigin-ci,yorigin,xorigin+ci,yorigin);
           line(xorigin,yorigin-ci,xorigin,yorigin+ci);
           inc(ci);
           yjjdelay(10);
     until ci = length;
end;

Procedure Draw_Quadant_hk(horigin,korigin,colorquadant : integer);
var ci   : integer;
    Quit : boolean;
begin
     quit := false;
     ci   := 0;
     setcolor(colorquadant);
     repeat
            line(45,265-korigin,45+ci,265-korigin);
            line(horigin+230,80,horigin+230,80+ci);
            inc(ci);
            yjjdelay(10);
      until ci = 370;
 end;

Procedure SlideMenu(cc : integer);
var pyi : integer;
begin
     for pyi := 622 downto 469 do
     begin
          setcolor(cc);line(pyi,65,pyi,468);
          setcolor(0); line(pyi+5,65,pyi+5,468);
          yjjdelay(10);
     end;
end;

{$I help.pas}
{$I start.pas}
{$I preview.pas}
(*{$I paray.pas}
{$I parax.pas}
{$I circle.pas}
{$I ellipsex.pas}
{$I ellipsey.pas}
{$I compare.pas} Executed *)

{++++++++++++++++++++++++++++Menu-Program+++++++++++++++++++++++++++++++++++}
Procedure MenuProgramborder;
begin
     yjjborder(1,1,640,59,17,28);
     yjjborder(1,60,640,480,17,28);
     setfillstyle(4,20); bar(18,78,622,410);
     setfillstyle(1,0);  bar(320,90,580,353);
     settextstyle(2,0,7); setcolor(51); outtextxy(146,22,'C.A.I.');
                          setcolor(10); outtextxy(215,22,'Mathematic');
                          setcolor(94); outtextxy(339,22,'Conic Section');
     yjjborder(15,415,625,425,20,28);
                            setcolor(51); writexypixel(4,430,chr(135));
                                          writexypixel(6,434,'ขึ้น');
                            setcolor(47); writexypixel(10,435,chr(136));
                                          writexypixel(12,434,'ลง');
                            setcolor(100);writexypixel(16,434,'เลือกเมนู');
                            setcolor(57); writexypixel(60,434,'Enter เพื่อเข้าสู่เมนู');

end;

{***************************<sim_preview>***********************************}
Procedure Sim_preview;
begin
     yjjboard(45,85,185,117,17,21,21);
     setcolor(100); settextstyle(1,0,3);
     outtextxy(73,97,'Preview');
end;
{***************************<sim_Para_Y>***********************************}
Procedure Sim_Para_Y;
begin
     yjjboard(45,125,185,158,17,21,21);
     setcolor(100); settextstyle(1,0,3);
     outtextxy(73,137,'Parabola-Y');
End;
{***************************<Sim_Para_X>***********************************}
Procedure Sim_Para_X;
begin
     yjjboard(45,165,185,198,17,21,21);
     setcolor(100); settextstyle(1,0,3);
     outtextxy(73,177,'Parabola-X');
end;
{***************************<Sim_Circle>***********************************}
Procedure Sim_Circle;
begin
     yjjboard(45,205,185,238,17,21,21);
     setcolor(100); settextstyle(1,0,3);
     outtextxy(73,217,'Circle');
End;
{***************************<Sim_Ellipse_X>******************************}
Procedure Sim_Ellipse_X;

begin
     yjjboard(45,245,185,278,17,21,21);
     setcolor(100); settextstyle(1,0,3);
     outtextxy(73,257,'Ellipse-X');
End;
{***************************<Sim_Ellipse_Y>********************************}
Procedure Sim_Ellipse_Y;
begin
     yjjboard(45,285,185,318,17,21,21);
     setcolor(100); settextstyle(1,0,3);
     outtextxy(73,297,'Ellipse-Y');
End;

{***************************<Sim_Compare>************************************}
Procedure Sim_compare;
begin
     yjjboard(45,325,185,358,17,21,21);
     setcolor(100); settextstyle(1,0,3);
     outtextxy(73,337,'Compare');
End;

{***************************<Sim_Quit>**************************************}
Procedure Sim_Quit;
begin
     yjjboard(45,365,185,398,17,21,21);
     setcolor(100); settextstyle(1,0,3);
     outtextxy(73,377,'Quit Program');
End;


{***************************<Graph_Quadant>*********************************}
Procedure Graph_Quadant(Y:integer);
Begin
     Setcolor(Y);
{Y}  Line(450,100,450,343);
{X}  Line(330,221,570,221);
End;

{****************************<Graph Conic>*************************}
Procedure Graph_Conic;
var X,D  : Integer;
    quit : boolean;
begin
     quit := false;
     X    := 0;
     d    := 0;
     repeat
          ch := #0;
          if x <> 50 then
          begin
               setcolor(0);
               line(450-x,120,450+x,320);
               line(450+x,120,450-x,320);
                  inc(x);
               setcolor(74);
               line(450-x,120,450+x,320);
               line(450+x,120,450-x,320);
               yjjdelay(30);
          end;

          if x=50 then
          begin
               ellipse(450,120,0,d,50,15);
               ellipse(450,120,180,180+d,50,15);
               ellipse(450,320,360-d,360,50,15);
               yjjdelay(10);
               inc(d);
          end;
          if keypressed or (d=180) then
          repeat
               ch := readkey;
               if ch in [#13,#27] then quit := true else
               if ch = #0 then
               begin
                    ch := readkey;
                    if ch in [#72,#80] then quit := true;
               end;
          until quit or (d <> 180);
     until quit;
End;


{****************************<graph_paraX>*************************}
procedure Graph_paraX(Cx:integer);
var y,c,ya,xa,x: integer;
    quit       : boolean;
Begin
     ch := #0;
     quit := false;
     C  := Cx;
     Ya := -74;
     Xa := round((Ya*Ya)/(4*C));
     Y := -74;
     repeat
          ch := #0;
          X := round((Y*Y)/(4*C));
          setcolor(44);
          yjjdelay(20);
          line(380+xa,221-ya,380+x,221-y);
          xa:=x;
          ya:=y;
          inc(y);
          if keypressed or (y=75) then
          repeat
               ch := readkey;
               if ch in [#13,#27] then quit := true else
               if ch = #0 then
               begin
                    ch := readkey;
                    if ch in [#72,#80] then quit := true;
               end;
          until quit or (y <> 75)
     until quit
End;

{****************************<graph_paraY>*************************}
Procedure Graph_ParaY(Cx : Integer);
var x,y,c,xa,ya : integer;
    quit : boolean;
Begin
     ch := #0;
     quit := false;
     C  := Cx;
     xa := -64;
     ya := round((xa*xa)/(4*c));
     X := -64;
     repeat
           Y := round((X*X)/(4*C));
           setcolor(11);
           yjjdelay(20);
           line(450+xa,280-ya,450+x,280-y);
           xa:=x;
           ya:=y;
           inc(x);

          if keypressed or (x=65) then
          repeat
               ch := readkey;
               if ch in [#13,#27] then quit := true else
               if ch = #0 then
               begin
                    ch := readkey;
                    if ch in [#72,#80] then quit := true;
               end;
          until (x<>65) or quit;
     until quit
End;
{********************<Graph_Circle>*********************}
procedure Graph_Circle;
var d: integer;
   quit : boolean;
begin
     ch := #0;
     quit := false;
     d := 1;
     repeat
          setcolor(94);
          ellipse(450,221,0,d,80,80);
          ellipse(450,221,180,180+d,80,80);
          yjjdelay(10);
          inc(d);

          if keypressed or (d=181) then
          repeat
               ch := readkey;
               if ch in [#13,#27] then quit := true else
               if ch = #0 then
               begin
                    ch := readkey;
                    if ch in [#72,#80] then quit := true;
               end;
          until quit or (d <> 180);
     until quit;
end;
{********************</Graph_Circle>*********************}

{********************<Graph_Ellipse_X>*********************}
procedure Graph_Ellipse_X;
var d : integer;
    quit : boolean;
begin
     ch := #0;
     quit := false;
     d := 1;
     repeat
          setcolor(86);
          ellipse(450,220,0,d,100,60);
          ellipse(450,220,180,180+d,100,60);
          yjjdelay(10);
          inc(d);

          if keypressed or (d=181) then
          repeat
               ch := readkey;
               if ch in [#13,#27] then quit := true else
               if ch = #0 then
               begin
                    ch := readkey;
                    if ch in [#72,#80] then quit := true;
               end;
          until quit or (d<>180);
     until quit;
end;
{********************</Graph_Ellipse_X>*********************}

{********************<Graph_Ellipse_Y>*********************}
procedure Graph_Ellipse_Y;
var d  : integer;
    quit : boolean;
begin
     ch := #0;
     quit := false;
     d := 1;
     repeat
          setcolor(37);
          ellipse(450,220,0,d,60,100);
          ellipse(450,220,180,180+d,60,100);
          yjjdelay(10);
          inc(d);

          if keypressed or (d=181) then
          repeat
               ch := readkey;
               if ch in [#13,#27] then quit := true else
               if ch = #0 then
               begin
                    ch := readkey;
                    if ch in [#72,#80] then quit := true;
               end;
          until quit or (d<>180);

     until quit;
end;
{********************</Graph_Ellipse_Y>*********************}

{***********************<Graph_Compare>*********************}
procedure Graph_compare;
var d,c,xa,ya  : integer;
    quit : boolean;
begin
     C  := 10;
     xa := -64;
     ya := round((xa*xa)/(4*c));
     X := -70;
     ch := #0;
     quit := false;
     d := 1;
     repeat
          setcolor(43);
          ellipse(430,250,0,d,80,50);
          ellipse(430,250,180,180+d,80,50);
          yjjdelay(5);
          inc(d);
          Y := round((X*X)/(4*C));
          setcolor(11);
          yjjdelay(10);
          line(470+xa,260-ya,470+x,260-y);
          xa:=x;
          ya:=y;
          if x < 71 then inc(x);

          if keypressed or (d=181) then
          repeat
               ch := readkey;
               if ch in [#13,#27] then quit := true else
               if ch = #0 then
               begin
                    ch := readkey;
                    if ch in [#72,#80] then quit := true;
               end;
          until quit or (d<>180);

     until quit;
end;

{***************************<vab_preview>***********************************}
Procedure vab_preview;
begin
   setfillstyle(1,0);
   bar(320,90,580,353);
   yjjboard(45,85,185,117,23,27,28);
   settextstyle(1,0,3);
   setcolor(0);
   outtextxy(70,94,'Preview');
   setcolor(0);
   outtextxy(71,95,'Preview');
   setcolor(0);
   outtextxy(72,96,'Preview');
   setcolor(14);
   outtextxy(73,97,'Preview');
   Graph_Conic;
end;
{***************************<vab_Para_Y>***********************************}
Procedure vab_Para_Y;
begin
     setfillstyle(1,0);
        bar(320,90,580,353);
     yjjboard(45,125,185,158,23,27,28);
     settextstyle(1,0,3);
     setcolor(0);
     outtextxy(70,134,'Parabola-Y');
     setcolor(0);
     outtextxy(71,135,'Parabola-Y');
     setcolor(0);
     outtextxy(72,136,'Parabola-Y');
     setcolor(14);
     outtextxy(73,137,'Parabola-Y');
     Graph_Quadant(173);
     Graph_ParaY(8);
End;
{***************************<vab_Para_X>***********************************}
Procedure vab_Para_X;
begin
   setfillstyle(1,0);
   bar(320,90,580,353);
   yjjboard(45,165,185,198,23,27,28);
   settextstyle(1,0,3);
   setcolor(0);
   outtextxy(70,174,'Parabola-X');
   setcolor(0);
   outtextxy(71,175,'Parabola-X');
   setcolor(0);
   outtextxy(72,176,'Parabola-X');
   setcolor(14);
   outtextxy(73,177,'Parabola-X');
   Graph_Quadant(173);
   Graph_ParaX(10);
end;
{***************************<vab_Circle>***********************************}
Procedure vab_Circle;
begin
   setfillstyle(1,0);
   bar(320,90,580,353);
   yjjboard(45,205,185,238,23,27,28);
   settextstyle(1,0,3);
   setcolor(0);
   outtextxy(70,214,'Circle');
   setcolor(0);
   outtextxy(71,215,'Circle');
   setcolor(0);
   outtextxy(72,216,'Circle');
   setcolor(14);
   outtextxy(73,217,'Circle');
   Graph_Quadant(173);
   Graph_Circle{(44)};
End;
{***************************<vab_Ellipse_X>******************************}
Procedure vab_Ellipse_X;
begin
   setfillstyle(1,0);
   bar(320,90,580,353);
   yjjboard(45,245,185,278,23,27,28);
   settextstyle(1,0,3);
   setcolor(0);
   outtextxy(70,254,'Ellipse-X');
   setcolor(0);
   outtextxy(71,255,'Ellipse-X');
   setcolor(0);
   outtextxy(72,256,'Ellipse-X');
   setcolor(14);
   outtextxy(73,257,'Ellipse-X');
   Graph_Quadant(173);
   Graph_Ellipse_X;
End;
{***************************<vab_Ellipse_Y>********************************}
Procedure vab_Ellipse_Y;
begin
   setfillstyle(1,0);
   bar(320,90,580,353);
   yjjboard(45,285,185,318,23,27,28);
   settextstyle(1,0,3);
   setcolor(0);
   outtextxy(70,294,'Ellipse-Y');
   setcolor(0);
   outtextxy(71,295,'Ellipse-Y');
   setcolor(0);
   outtextxy(72,296,'Ellipse-Y');
   setcolor(14);
   outtextxy(73,297,'Ellipse-Y');
   Graph_Quadant(173);
   Graph_Ellipse_Y;
End;
{***************************<vab_Compare>**********************************}
Procedure vab_compare;
var quit : boolean;
    a : byte;
begin
   ch := #0;
   quit := false;
   setfillstyle(1,0);bar(320,90,580,353);
   yjjboard(45,325,185,358,23,27,28);
   settextstyle(1,0,3);
   setcolor(0);
   outtextxy(70,334,'Compare');
   setcolor(0);
   outtextxy(71,335,'Compare');
   setcolor(0);
   outtextxy(72,336,'Compare');
   setcolor(14);
   outtextxy(73,337,'Compare');
   setcolor(54);
   graph_quadant(173);
   graph_compare;
End;

{***************************<vab_Quit>*************************************}
Procedure vab_Quit;
var quit : boolean;
    a : byte;
begin
   ch := #0;
   quit := false;
   setfillstyle(1,0);
   bar(320,90,580,353);
   yjjborder(320,90,580,353,249,254);
   yjjboard(45,365,185,398,23,27,28);
   settextstyle(1,0,3);
   setcolor(0);
   outtextxy(70,374,'Quit Program');
   setcolor(0);
   outtextxy(71,375,'Quit Program');
   setcolor(0);
   outtextxy(72,376,'Quit Program');
   setcolor(14);
   outtextxy(73,377,'Quit Program');
   setcolor(54);
   settextstyle(2,0,10);
   setcolor(22);outtextxy(357,200,'GOOD BYE');
   setcolor(25);outtextxy(358,201,'GOOD BYE');
   setcolor(28);outtextxy(359,202,'GOOD BYE');
   setcolor(31);outtextxy(360,203,'GOOD BYE');
   setcolor(28);outtextxy(361,204,'GOOD BYE');
   setcolor(25);outtextxy(362,205,'GOOD BYE');
   setcolor(22);outtextxy(363,206,'GOOD BYE');

   repeat
          if keypressed then
          begin
               ch := readkey;
               if ch in [#13,#27] then quit := true else
               if ch = #0 then
               begin
                    ch := readkey;
                    if ch in [#72,#80] then quit := true;
               end;
          end;
   until quit;
End;

{--------------------------+****MAINMENU****+-------------------------------}
Procedure MainMenu;
var choice,one,onea : byte;
               onex : boolean;
Procedure Exitmain;
var chexit    : char;
    checkexit : boolean;
    w,row,col : integer;
     Procedure Sim_Yes;
     begin
        yjjboard(160,225,290,275,21,27,27);
        setcolor(100);
        writexypixel(22,240,'ออกจากโปรแกรม');
     end;
     Procedure Vab_Yes;
     begin
        yjjboard(160,225,290,275,25,31,31);
        setcolor(4);
        writexypixel(22,240,'ออกจากโปรแกรม');
     end;
     Procedure Sim_No;
     begin
        yjjboard(365,225,495,275,21,27,27);
        setcolor(100);
        writexypixel(51,240,'ยกเลิก');
     end;
     Procedure Vab_No;
     begin
        yjjboard(365,225,495,275,25,31,31);
        setcolor(4);
        writexypixel(51,240,'ยกเลิก');
     end;

begin
     exit := false;
     onex := false;
     setfillstyle(4,25);
     w := 2;
     row := 0;
     one := 0;
     onea:= 0;
     repeat
          yjjboard(320-one,250-onea,330+one,250+onea,18,27,56);
          inc(onea);
          inc(one,2);
          if onea = 50 then onea := 49;
          if one = 220 then begin one := 219; onex := true; end;
     until onex;
     Sim_Yes;
     Sim_No;
     chexit := #77;
     Repeat
{left}      if chexit = #75 then
               begin
                   Vab_Yes;
                   Sim_No;
                   exit := true;
               end;
{right}        if chexit = #77 then
               begin
                  Vab_no;
                  Sim_Yes;
                  exit := false;
               end;
       chexit := readkey;
       if chexit = #0 then chexit := readkey;
     Until (chexit=#13);
end;

begin
REPEAT
     cleardevice;
     initrgb;
     fadein(0);
       MenuProgramBorder;
         Sim_preview;
         Sim_para_Y;
         Sim_para_X;
         Sim_Circle;
         Sim_Ellipse_X;
         Sim_Ellipse_Y;
         Sim_Compare;
         Sim_Quit;
     fadeout(100);
     choice := 1;
     ch := #0;
     exit := false;
     repeat
{down}      if ch = #80 then
               begin
                    if choice = 8 then choice := 0;
                    inc(choice);
               end;
{up}        if ch = #72 then
               begin
                    if choice = 1 then choice := 9;
                    dec(choice);
               end;
               case choice of
                1 :  begin
                          if ch=#80 then Sim_quit;
                          if ch=#72 then Sim_Para_y;
                          vab_preview;
                     end;
                2 :  begin
                          if ch=#80 then Sim_preview;
                          if ch=#72 then Sim_para_x;
                          vab_Para_Y;
                     end;
                3 :  begin
                          if ch=#80 then Sim_Para_y;
                          if ch=#72 then Sim_circle;
                          vab_Para_X;
                     end;
                4 :  begin
                          if ch=#80 then Sim_para_x;
                          if ch=#72 then Sim_Ellipse_x;
                          vab_Circle;
                     end;
                5 :  begin
                          if ch=#80 then Sim_circle;
                          if ch=#72 then Sim_Ellipse_y;
                          vab_Ellipse_X;
                     end;
                6 :  begin
                          if ch=#80 then Sim_Ellipse_X;
                          if ch=#72 then Sim_Compare;
                          vab_Ellipse_Y;
                     end;
                7 :  begin
                          if ch=#80 then Sim_Ellipse_y;
                          if ch=#72 then Sim_Quit;
                          vab_Compare;
                     end;
                8 :  begin
                          if ch=#80 then Sim_Compare;
                          if ch=#72 then Sim_Preview;
                          vab_Quit;
                     end;
                end;{case}
     until ch in [#13];
     Case Choice of
        1 : Preview;
        2 : Begin Swapvectors; Exec('ParaY.exe',''); Swapvectors; End;
        3 : Begin Swapvectors; Exec('ParaX.exe',''); Swapvectors; End;
        4 : Begin Swapvectors; Exec('Circle.exe',''); Swapvectors; End;
        5 : Begin Swapvectors; Exec('EllipseX.exe',''); Swapvectors; End;
        6 : Begin Swapvectors; Exec('EllipseY.exe',''); Swapvectors; End;
        7 : Begin Swapvectors; Exec('Compare.exe',''); Swapvectors; End;
        8 : Exitmain;
     end;
UNTIL (exit);
end;

{******YJJ-+-YJJ-+-YJJ-+-YJJ-+-YJJ-+-YJJ-+-YJJ-+-YJJ-+-YJJ-+-YJJ-+-YJJ******}

BEGIN
      uses_svga256_color;               {Opengraph and use Svga256.bgi}
      Start_Delay(real_delay2);
      loadfont('normal.fon');
           Start;                      {Begin Program}
     closegraph;
     uses_svga256_color;
     if keypressed then
     ch := readkey;
           Mainmenu;                   {Select choice by PRESS Up or Down}
     row := -2;
     repeat
       inc(row,2);
       setcolor(19);
          SetLineStyle(5,5,5);
          line(1,row,640,row);
          yjjdelay(25);
     until(row>480);
          SetLineStyle(0,0,0);
          repeat
           setfillstyle(random(10),random(255));
           x := random(640);
           y := random(480);
           bar(x,y,x+random(20),y+random(20));
     until keypressed;
     fadein(100);
     closegraph;
end.
{******YJJ-+-YJJ-+-YJJ-+-YJJ-+-YJJ-+-YJJ-+-YJJ-+-YJJ-+-YJJ-+-YJJ-+-YJJ******}
