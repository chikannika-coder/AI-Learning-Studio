Program Compare;
uses crt,dos,kvga,kfade,graph;
var coChoice,coChoice2 : integer;
    real_delay,real_delay2 : real;
    ch,ikey                : char;
    valout,x,y             : integer;
    exit,Quit              : boolean;
    coch,coch2             : char;

{$f+}
function vidd:integer;
begin
     vidd:=2;  {1=640*400*256 , 2=640*480*256 , 3=800*600*256}
end;
{$f-}

procedure  uses_svga256_color;
var i,install,graphdriver,graphmode : integer;
begin
     install:=installuserdriver('svga256',@vidd);
     graphdriver := detect;initgraph(graphdriver,graphmode,'svga256');

     for i := 248 to 255 do
     setrgbpalette(i,(i-248)*4,0,0);
end;


Procedure pause;
 var ch : char;
 begin
    ch := readkey;
    if ch = #0 then ch := readkey;
 end;

Procedure color;
var  x,y       : integer;
     color     : byte;
     scolor    : string;
begin
       cleardevice;
        y     := 1;
        color := 1;
        repeat
              x := 1;
              repeat
                    setcolor(color);
                    str(color,scolor);
                    outtextxy(x,y,scolor);
                    inc(x,30);
                    inc(color);
              Until (x  >= 620) or (color = 255);
              inc(y,15);
        Until color >= 255;
        pause;
end;

Procedure Start_Delay(var real_delay : real);
var  com_time : longint absolute $40:$6c;
     Stime,Ftime : longint;
begin
     Stime := com_time;
     delay(10000);
     Ftime := com_time;
     real_delay := 10000/((Ftime-Stime)/18.2);
end;

Procedure YJJdelay(ms : word);
var Xdelay : word;
begin
     Xdelay := round((real_delay2*ms)/5000);
     delay(Xdelay);
end;
                                  {17..31}  {31..17}
Procedure YJJBorder(X1,Y1,X2,Y2,color_begin,color_end : integer);
var bordercolor,i,shadeup : byte;
begin
     {17++++++31}
     shadeup := 0;
     if color_begin < color_end then
     begin
          for bordercolor := color_begin to color_end do
          begin
               setcolor(bordercolor);
               line(X1+shadeup,Y1+shadeup,X2-shadeup,Y1+shadeup);
               line(X1+shadeup,Y2-shadeup,X2-shadeup,Y2-shadeup);
               line(X1+shadeup,Y1+shadeup,X1+shadeup,Y2-shadeup);
               line(X2-shadeup,Y1+shadeup,X2-shadeup,Y2-shadeup);
               inc(shadeup);
          end;
     end
     ELSE
     begin
          for bordercolor := color_begin downto color_end do
          begin
               setcolor(bordercolor);
               line(X1+shadeup,Y1+shadeup,X2-shadeup,Y1+shadeup);
               line(X1+shadeup,Y2-shadeup,X2-shadeup,Y2-shadeup);
               line(X1+shadeup,Y1+shadeup,X1+shadeup,Y2-shadeup);
               line(X2-shadeup,Y1+shadeup,X2-shadeup,Y2-shadeup);
               inc(shadeup);
          end;
     end

end;

{+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++}

{++++++++++++++++++++++++++++++YIM******************************************}
Procedure Yim(x1,y1,x2,y2,cb,cs,ce,wd : integer);
var w : integer;
begin
     if cs > ce then
     begin
          setfillstyle(1,cb);
          bar(x1,y1,x2,y2);
          repeat
                w := 0;
                for w := 1 to wd do
                begin
                     inc(x2);
                     setcolor(cs);line(x2,y1,x2,y2);
                end;
                dec(cs);
          until cs = ce;
     end;
     if ce > cs then
     begin
          setfillstyle(1,cb);
          bar(x1,y1,x2,y2);
          repeat
                w := 0;
                for w := 1 to wd do
                begin
                     inc(x2);
                     setcolor(cs);line(x2,y1,x2,y2);
                end;
                inc(cs);
          until cs = ce;
     end;
end;

Procedure YJJBoard(X1,Y1,X2,Y2:integer; color_begin,color_end,color_bar : byte);
var bordercolor,i,shadeup : byte;
begin
     {17++++++31}
     shadeup := 0;
     if color_begin < color_end then
     begin
          for bordercolor := color_begin to color_end do
          begin
               setcolor(bordercolor);
               line(X1+shadeup,Y1+shadeup,X2-shadeup,Y1+shadeup);
               line(X1+shadeup,Y2-shadeup,X2-shadeup,Y2-shadeup);
               line(X1+shadeup,Y1+shadeup,X1+shadeup,Y2-shadeup);
               line(X2-shadeup,Y1+shadeup,X2-shadeup,Y2-shadeup);
               inc(shadeup);
          end;
          setfillstyle(1,color_bar);
          bar(x1+shadeup,y1+shadeup,x2-shadeup,y2-shadeup);

     end
     ELSE
     begin
          for bordercolor := color_begin downto color_end do
          begin
               setcolor(bordercolor);
               line(X1+shadeup,Y1+shadeup,X2-shadeup,Y1+shadeup);
               line(X1+shadeup,Y2-shadeup,X2-shadeup,Y2-shadeup);
               line(X1+shadeup,Y1+shadeup,X1+shadeup,Y2-shadeup);
               line(X2-shadeup,Y1+shadeup,X2-shadeup,Y2-shadeup);
               inc(shadeup);
          end;
          setfillstyle(1,color_bar);
          bar(x1+shadeup,y1+shadeup,x2-shadeup,y2-shadeup);

     end
end;

{+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++}

Procedure YJJcircle(X1,Y1,X2,Y2,color_begin,color_end : integer);
var bordercolor,i,shadeup : byte;
begin
     {17++++++31}
     shadeup := 1;
     if color_begin < color_end then
     begin
          for bordercolor := color_begin to color_end do
          begin
               setcolor(bordercolor);
               ellipse(round(x1+(x2-x1)/2),round(y1+(y2-y1)/2),0,360,
                       round((x2-x1)/2)-shadeup,round((y2-y1)/2)-shadeup);
               inc(shadeup);
          end;
     end
     ELSE
     begin
          for bordercolor := color_begin downto color_end do
          begin
               setcolor(bordercolor);
               ellipse(round(x1+(x2-x1)/2),round(y1+(y2-y1)/2),0,360,
                       round((x2-x1)/2)-shadeup,round((y2-y1)/2)-shadeup);
               inc(shadeup);
          end;
     end;
end;

Procedure Draw_Quadant(xorigin,yorigin,colorquadant : integer);
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
     until ci = 185;
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

{+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++}

                   {=====Input Value NUMBER=====}

procedure valinput(var valin : integer; range : byte;Xinput,Yinput,cinput : integer);
var icount,rcount  : byte;
    namein,nameout : string;
    xcode          : integer;
begin
     nameout := '';
     icount  := 0;
     rcount  := 0;
     repeat
           ikey := readkey;
           if ((rcount < range) and (ikey >= #48) and (ikey <= #57))
              or ((ikey='-') and (icount=0)) then
           begin
                if ikey in [#48..#57] then inc(rcount);
                inc(icount);
                setcolor(Cinput);writexypixel(xinput+icount,yinput,ikey);
                nameout := nameout + ikey;
           end;
           if (ikey = #8) and (icount > 0) then
           begin
                delete(nameout,icount,1);
                setcolor(0);writexypixel(xinput+icount,yinput,nameout[icount]);
                if nameout[icount] in [#48..#57] then dec(rcount);
                dec(icount);
           end;
           if (ikey = #0) then
           begin
                ikey := readkey;
                ikey := #0;
           end;
     until ((ikey = #13) and (rcount<>0)) or (ikey = #27);
     val(nameout,valout,xcode);
     valin := valout;
end;
                {=====No Minus Input Value NUMBER=====}

procedure Nominusinput(var valin : integer; range : byte;Xinput,Yinput,cinput : integer);
var icount,rcount  : byte;
    namein,nameout : string;
    xcode          : integer;
begin
     nameout := '';
     icount  := 0;
     rcount  := 0;
     repeat
           ikey := readkey;
           if (rcount < range) and (ikey >= #48) and (ikey <= #57) then
           begin
                if ikey in [#48..#57] then inc(rcount);
                inc(icount);
                setcolor(Cinput);writexypixel(xinput+icount,yinput,ikey);
                nameout := nameout + ikey;
           end;
           if (ikey = #8) and (icount > 0) then
           begin
                delete(nameout,icount,1);
                setcolor(0);writexypixel(xinput+icount,yinput,nameout[icount]);
                if nameout[icount] in [#48..#57] then dec(rcount);
                dec(icount);
           end;
           if (ikey = #0) then
           begin
                ikey := readkey;
                ikey := #0;
           end;
     until ((ikey = #13) and (rcount<>0)) or (ikey = #27);
     val(nameout,valout,xcode);
     valin := valout;
end;
{###########################################################################}

Procedure writetextmenu;
begin
     settextstyle(1,0,2); setcolor(52);outtextxy(26,13,'Compare');
                          setcolor(10);outtextxy(480,13,'Conic Section');
     setcolor(79);writexypixel(25,15,'เปรียบเทียบกราฟ');
end;

Procedure Menu_compare_border;
begin
     yjjborder(1,1,640,50,17,26);
     yjjborder(15,418,625,425,20,28);
        yjjborder(621,51,640,480,17,26);
        yjjborder(1,51,20,480,17,26);
        setcolor(51);  writexypixel(5,440,chr(135));
                       writexypixel(7,440,'ขึ้น');
        setcolor(47);  writexypixel(10,440,chr(136));
                       writexypixel(12,440,'ลง');
        setcolor(57);  writexypixel(60,440,'Enter เพื่อเลือกกราฟ');
        yjjborder(1,51,640,480,17,26);
        writetextMenu;
end;

{***************************<sim_ParaY>***********************************}
Procedure Sim_ParaY;
begin
     yjjboard(90,125,230,158,17,21,21);
     setcolor(100); settextstyle(1,0,3);
     outtextxy(108,137,'Parabola-Y');
End;
{***************************<Sim_ParaX>***********************************}
Procedure Sim_ParaX;
begin
     yjjboard(90,165,230,198,17,21,21);
     setcolor(100); settextstyle(1,0,3);
     outtextxy(108,177,'Parabola-X');
end;
{***************************<Sim_Circle>***********************************}
Procedure Sim_Circle;
begin
     yjjboard(90,205,230,238,17,21,21);
     setcolor(100); settextstyle(1,0,3);
     outtextxy(108,217,'Circle');
End;
{***************************<Sim_EllipseX>******************************}
Procedure Sim_EllipseX;
begin
     yjjboard(90,245,230,278,17,21,21);
     setcolor(100); settextstyle(1,0,3);
     outtextxy(108,257,'Ellipse-X');
End;
{***************************<Sim_EllipseY>********************************}
Procedure Sim_EllipseY;
begin
     yjjboard(90,285,230,318,17,21,21);
     setcolor(100); settextstyle(1,0,3);
     outtextxy(108,297,'Ellipse-Y');
End;
{***************************<vab_Para_Y>***********************************}
Procedure vab_ParaY;
begin
     yjjboard(90,125,230,158,23,27,28);
     settextstyle(1,0,3);
     setcolor(0);
     outtextxy(105,134,'Parabola-Y');
     setcolor(0);
     outtextxy(106,135,'Parabola-Y');
     setcolor(0);
     outtextxy(107,136,'Parabola-Y');
     setcolor(14);
     outtextxy(108,137,'Parabola-Y');
End;
{***************************<vab_Para_X>***********************************}
Procedure vab_ParaX;
begin
   yjjboard(90,165,230,198,23,27,28);
   settextstyle(1,0,3);
   setcolor(0);
   outtextxy(105,174,'Parabola-X');
   setcolor(0);
   outtextxy(106,175,'Parabola-X');
   setcolor(0);
   outtextxy(107,176,'Parabola-X');
   setcolor(14);
   outtextxy(108,177,'Parabola-X');
end;
{***************************<vab_Circle>***********************************}
Procedure vab_Circle;
begin
   yjjboard(90,205,230,238,23,27,28);
   settextstyle(1,0,3);
   setcolor(0);
   outtextxy(105,214,'Circle');
   setcolor(0);
   outtextxy(106,215,'Circle');
   setcolor(0);
   outtextxy(107,216,'Circle');
   setcolor(14);
   outtextxy(108,217,'Circle');
End;
{***************************<vab_Ellipse_X>******************************}
Procedure vab_EllipseX;
begin
   yjjboard(90,245,230,278,23,27,28);
   settextstyle(1,0,3);
   setcolor(0);
   outtextxy(105,254,'Ellipse-X');
   setcolor(0);
   outtextxy(106,255,'Ellipse-X');
   setcolor(0);
   outtextxy(107,256,'Ellipse-X');
   setcolor(14);
   outtextxy(108,257,'Ellipse-X');
End;
{***************************<vab_Ellipse_Y>********************************}
Procedure vab_EllipseY;
begin
   yjjboard(90,285,230,318,23,27,28);
   settextstyle(1,0,3);
   setcolor(0);
   outtextxy(105,294,'Ellipse-Y');
   setcolor(0);
   outtextxy(106,295,'Ellipse-Y');
   setcolor(0);
   outtextxy(107,296,'Ellipse-Y');
   setcolor(14);
   outtextxy(108,297,'Ellipse-Y');
End;

{***************************<sim_ParaY>***********************************}
Procedure Sim_ParaY2;
begin
     yjjboard(400,125,540,158,17,21,21);
     setcolor(100); settextstyle(1,0,3);
     outtextxy(428,137,'Parabola-Y');
End;
{***************************<Sim_ParaX>***********************************}
Procedure Sim_ParaX2;
begin
     yjjboard(400,165,540,198,17,21,21);
     setcolor(100); settextstyle(1,0,3);
     outtextxy(428,177,'Parabola-X');
end;
{***************************<Sim_Circle>***********************************}
Procedure Sim_Circle2;
begin
     yjjboard(400,205,540,238,17,21,21);
     setcolor(100); settextstyle(1,0,3);
     outtextxy(428,217,'Circle');
End;
{***************************<Sim_EllipseX>******************************}
Procedure Sim_EllipseX2;
begin
     yjjboard(400,245,540,278,17,21,21);
     setcolor(100); settextstyle(1,0,3);
     outtextxy(428,257,'Ellipse-X');
End;
{***************************<Sim_EllipseY>********************************}
Procedure Sim_EllipseY2;
begin
     yjjboard(400,285,540,318,17,21,21);
     setcolor(100); settextstyle(1,0,3);
     outtextxy(428,297,'Ellipse-Y');
End;
{***************************<vab_Para_Y>***********************************}
Procedure vab_ParaY2;
begin
     yjjboard(400,125,540,158,23,27,28);
     settextstyle(1,0,3);
     setcolor(0);
     outtextxy(425,134,'Parabola-Y');
     setcolor(0);
     outtextxy(426,135,'Parabola-Y');
     setcolor(0);
     outtextxy(427,136,'Parabola-Y');
     setcolor(14);
     outtextxy(428,137,'Parabola-Y');
End;
{***************************<vab_Para_X>***********************************}
Procedure vab_ParaX2;
begin
   yjjboard(400,165,540,198,23,27,28);
   settextstyle(1,0,3);
   setcolor(0);
   outtextxy(425,174,'Parabola-X');
   setcolor(0);
   outtextxy(426,175,'Parabola-X');
   setcolor(0);
   outtextxy(427,176,'Parabola-X');
   setcolor(14);
   outtextxy(428,177,'Parabola-X');
end;
{***************************<vab_Circle>***********************************}
Procedure vab_Circle2;
begin
   yjjboard(400,205,540,238,23,27,28);
   settextstyle(1,0,3);
   setcolor(0);
   outtextxy(425,214,'Circle');
   setcolor(0);
   outtextxy(426,215,'Circle');
   setcolor(0);
   outtextxy(427,216,'Circle');
   setcolor(14);
   outtextxy(428,217,'Circle');
End;
{***************************<vab_Ellipse_X>******************************}
Procedure vab_EllipseX2;
begin
   yjjboard(400,245,540,278,23,27,28);
   settextstyle(1,0,3);
   setcolor(0);
   outtextxy(425,254,'Ellipse-X');
   setcolor(0);
   outtextxy(426,255,'Ellipse-X');
   setcolor(0);
   outtextxy(427,256,'Ellipse-X');
   setcolor(14);
   outtextxy(428,257,'Ellipse-X');
End;
{***************************<vab_Ellipse_Y>********************************}
Procedure vab_EllipseY2;
begin
   yjjboard(400,285,540,318,23,27,28);
   settextstyle(1,0,3);
   setcolor(0);
   outtextxy(425,294,'Ellipse-Y');
   setcolor(0);
   outtextxy(426,295,'Ellipse-Y');
   setcolor(0);
   outtextxy(427,296,'Ellipse-Y');
   setcolor(14);
   outtextxy(428,297,'Ellipse-Y');
End;

{$I coparay.pas}
{$I coparax.pas}
{$I cocircle.pas}
{$I CoEx.pas}
{$I CoEy.pas}

Procedure Menu_compare;
var exit   : boolean;

    Procedure Compare_Exit;
    begin
         exit := true;
    end;

begin
     fadein(0);
         Sim_paraY;
         Sim_paraX;
         Sim_Circle;
         Sim_EllipseX;
         Sim_EllipseY;
         Sim_paraY2;
         Sim_paraX2;
         Sim_Circle2;
         Sim_EllipseX2;
         Sim_EllipseY2;
     fadeout(100);
     cochoice := 1;
     coch := #0;
     exit := false;
     repeat
{down}      if coch = #80 then
               begin
                    if cochoice = 5 then cochoice := 0;
                    inc(cochoice);
               end;
{up}        if coch = #72 then
               begin
                    if cochoice = 1 then cochoice := 6;
                    dec(cochoice);
               end;
               case cochoice of
                1 :  begin
                          if coch=#80 then Sim_EllipseY;
                          if coch=#72 then Sim_Parax;
                          vab_Paray;
                     end;
                2 :  begin
                          if coch=#80 then Sim_paray;
                          if coch=#72 then Sim_circle;
                          vab_Parax;
                     end;
                3 :  begin
                          if coch=#80 then Sim_Parax;
                          if coch=#72 then Sim_Ellipsex;
                          vab_circle;
                     end;
                4 :  begin
                          if coch=#80 then Sim_circle;
                          if coch=#72 then Sim_EllipseY;
                          vab_EllipseX;
                     end;
                5 :  begin
                          if coch=#80 then Sim_Ellipsex;
                          if coch=#72 then Sim_paray;
                          vab_Ellipsey;
                     end;
                end;      {case}
                repeat
                      coch := readkey;
                      if coch = #0 then coch := readkey;
                until coch in[#13,#72,#80,#68];
     until coch in [#13,#68];
end;

Procedure Menu_compare2;
var exit2   : boolean;

Procedure Compare_Exit2;
begin
     exit2 := true;
end;

begin
         Sim_paraY2;
         Sim_paraX2;
         Sim_Circle2;
         Sim_EllipseX2;
         Sim_EllipseY2;
     cochoice2 := 1;
     coch2 := #0;
     exit2 := false;
     repeat
{down}      if coch2 = #80 then
               begin
                    if cochoice2 = 5 then cochoice2 := 0;
                    inc(cochoice2);
               end;
{up}        if coch2 = #72 then
               begin
                    if cochoice2 = 1 then cochoice2 := 6;
                    dec(cochoice2);
               end;
               case cochoice2 of
                1 :  begin
                          if coch2=#80 then Sim_EllipseY2;
                          if coch2=#72 then Sim_Parax2;
                          vab_Paray2;
                     end;
                2 :  begin
                          if coch2=#80 then Sim_paray2;
                          if coch2=#72 then Sim_circle2;
                          vab_Parax2;
                     end;
                3 :  begin
                          if coch2=#80 then Sim_Parax2;
                          if coch2=#72 then Sim_Ellipsex2;
                          vab_circle2;
                     end;
                4 :  begin
                          if coch2=#80 then Sim_circle2;
                          if coch2=#72 then Sim_EllipseY2;
                          vab_EllipseX2;
                     end;
                5 :  begin
                          if coch2=#80 then Sim_Ellipsex2;
                          if coch2=#72 then Sim_paray2;
                          vab_Ellipsey2;
                     end;
                end;{case}
                repeat
                      coch2 := readkey;
                      if coch2 = #0 then coch2 := readkey;
                until coch2 in[#13,#72,#80,#68];
     until coch2 in [#13,#68];
end;

Procedure Real_Compare;
Procedure Choose_coChoice2;
begin
     if (coch2 <> #27) and (ikey <> #27) then
     case coChoice2 of
          1 : begin
                   draw_quadant(230,265,30);
                   pyMenu_Input;
              end;
          2 : begin
                   draw_quadant(230,265,30);
                   pxMenu_Input;
              end;
          3 : begin
                   draw_quadant(230,265,30);
                   cMenu_Input;
              end;
          4 : begin
                   draw_quadant(230,265,30);
                   exMenu_Input;
              end;
          5 : begin
                   draw_quadant(230,265,30);
                   eyMenu_Input;
              end;
     end;  {case}
end;

begin
     Menu_Compare_Border;
     case coChoice of
          1 : begin
                   creating_graphparay;
                   Choose_coChoice2;
              end;
          2 : begin
                   creating_graphparax;
                   Choose_coChoice2;
              end;
          3 : begin
                   creating_graphcircle;
                   Choose_coChoice2;
              end;
          4 : begin
                   creating_graphEllipsex;
                   Choose_coChoice2;
              end;
          5 : begin
                   creating_graphEllipsey;
                   Choose_coChoice2;
              end;
     end;
end;
Procedure Link;
var LinkBy,LinkEy : integer;
begin
     case cochoice of
          1 : LinkBy := 140;
          2 : LinkBy := 180;
          3 : LinkBy := 220;
          4 : LinkBy := 260;
          5 : LinkBy := 300;
     end;  {Case}
     setcolor(45);
     for x := 235 to 310 do
     begin
          line(245,linkby,x,linkby);
          yjjdelay(50);
     end;
     case cochoice2 of
          1 : LinkEy := 140;
          2 : LinkEy := 180;
          3 : LinkEy := 220;
          4 : LinkEy := 260;
          5 : LinkEy := 300;
     end;  {Case}
     if linkey < linkby then
     begin
          for y := linkby downto linkey do
          begin
               line(310,linkby,310,y);
               yjjdelay(50);
          end;
     end;
     if linkey > linkby then
     begin
          for y := linkby to linkey do
          begin
               line(310,linkby,310,y);
               yjjdelay(50);
          end;
     end;
     for x := 310 to 395 do
     begin
          line(310,linkey,x,linkey);
          yjjdelay(50);
     end;
     yjjdelay(1000);
end;

BEGIN
     uses_svga256_color;
     initrgb;
     loadfont('normal.fon');
     start_delay(real_delay2);
     ikey  := #0;
     coch  := #0;
     coch2 := #0;
     Quit  := false;
     repeat
           ikey  := #0;
           coch  := #0;
           coch2 := #0;
           if (ikey<>#27) and (coch<>#27) and (coch2<>#27) then
              setfillstyle(1,0);bar(1,1,640,480);
           if (ikey<>#27) and (coch<>#27) and (coch2<>#27) then
              Menu_compare_border;
           if (ikey<>#27) and (coch<>#27) and (coch2<>#27) then
              Menu_compare;
           if (coch<>#68) and (coch2<>#68) then
              Menu_compare2;
           if (ikey<>#27) and (coch<>#27) and (coch2<>#27) and
              (coch<>#68) and (coch2<>#68) then
              link;
           if (ikey<>#27) and (coch<>#27) and (coch2<>#27) and
              (coch<>#68) and (coch2<>#68) then
              Real_Compare;
     if (ikey=#68) or (coch=#68) or (coch2=#68) then Quit := true;
     until Quit;
     closegraph;
END.


