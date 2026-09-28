Procedure Preview;

Procedure Menu_Preview;
begin
     yjjborder(1,1,640,50,17,26);
        yjjborder(621,51,640,480,17,26);
        yjjborder(160,51,179,480,17,26);
        yjjborder(1,51,20,480,17,26);
        setcolor(51); writexypixel(5,380,chr(135));
                      writexypixel(7,385,'ขึ้น');
        setcolor(47); writexypixel(12,385,chr(136));
                      writexypixel(14,385,'ลง');
        setcolor(100);writexypixel(7,405,'เลือกเมนู');
        setcolor(57);writexypixel(4,435,'Esc กลับสู่เมนูหลัก');
     yjjborder(1,51,640,480,17,26);
     setcolor(82);
end;

Procedure writetextmenu;
begin
     settextstyle(1,0,2); setcolor(52);outtextxy(26,13,'Preview');
                          setcolor(10);outtextxy(480,13,'Conic Section');
    setcolor(79);writexypixel(15,15,'แนะนำภาคตัดกรวย');
end;

Procedure Spre_paraY;
begin
     yjjboard(25,80,155,118,20,25,57);
          setcolor(80); writexypixel(4,87,'พาราโบลา แกน Y');
          setfillstyle(1,0);
          bar(180,70,615,465);
end;

Procedure SPre_parax;
begin
     yjjboard(25,125,155,163,20,25,57);
          setcolor(80); writexypixel(4,132,'พาราโบลา แกน X');
          setfillstyle(1,0);
          bar(180,70,615,465);

end;

Procedure SPre_circle;
begin
     yjjboard(25,170,155,208,20,25,57);
          setcolor(80); writexypixel(8,177,'วงกลม');
          setfillstyle(1,0);
          bar(180,70,615,465);
end;

Procedure Spre_ellipseX;
begin
     yjjboard(25,215,155,253,20,25,57);
          setcolor(80); writexypixel(6,222,'วงรี แกน X');
          setfillstyle(1,0);
          bar(180,70,615,465);
end;

Procedure SPre_ellipseY;
begin
     yjjboard(25,260,155,298,20,25,57);
          setcolor(80); writexypixel(6,267,'วงรี แกน Y');
          setfillstyle(1,0);
          bar(180,70,615,465);
end;

Procedure SPre_Exit;
begin
     yjjboard(25,305,155,343,20,25,57);
          setcolor(80); writexypixel(4,312,'กลับสู่ Main Menu');
          setfillstyle(1,0);
          bar(180,70,615,465);
end;

Procedure Vpre_paraY;
var x,c,xa,ya,y : integer;
begin
     C  := 7;
     xa := -50;
     ya := round((xa*xa)/(4*c));
     yjjboard(25,80,155,118,23,28,68);
        setcolor(9); writexypixel(4,87,'พาราโบลา แกน Y');
        yjjboard(400,345,560,400,6,9,0);
        setcolor(45); writexypixel(53,350,'พาราโบลา แกน Y');
                      writexypixel(53,370,'Parabola Y axis');
        setcolor(15);
        line(350,120,250,320);
        line(250,120,350,320);
        ellipse(300,120,0,360,50,15);
        ellipse(300,320,180,360,50,15);
        setcolor(12); setlinestyle(DottedLn,0,NormWidth);line(325,80,325,220);
       SetLineStyle(0,0,0);
       setcolor(12);line(400,160,600,160);
       line(500,70,500,260);
     For X := -50 to 50 do
     begin
           Y := round((X*X)/(4*C));
           setcolor(15);
           line(500+xa,159-ya,500+x,159-y);
           xa:=x;
           ya:=y;
     end;
End;

Procedure Vpre_parax;
var y,c,ya,xa,x : integer;
begin
     C  := 7;
     Ya := -50;
     Xa := round((Ya*Ya)/(4*C));
     yjjboard(25,125,155,163,23,28,68);
        setcolor(9); writexypixel(4,132,'พาราโบลา แกน X');
        yjjboard(430,365,595,420,6,9,0);
        setcolor(45); writexypixel(57,370,'พาราโบลา แกน X');
                      writexypixel(57,390,'Parabola X axis');
        setcolor(15);
        line(230,90,450,190);
        line(230,190,450,90);
        ellipse(450,140,0,360,15,50);
        ellipse(230,140,90,270,15,50);
        setcolor(12); setlinestyle(DottedLn,0,NormWidth);
        line(350,120,475,120);
        SetLineStyle(0,0,0);
        setcolor(12);line(300,225,300,425);
        line(200,325,400,325);
     For Y := -50 to 50 do
     begin
          X := round((Y*Y)/(4*C));
          setcolor(15);
          line(301+xa,325-ya,301+x,325-y);
          xa:=x;
          ya:=y;
     end;
End;


Procedure VPre_circle;
begin
     yjjboard(25,170,155,208,23,28,68);
          setcolor(9); writexypixel(8,177,'วงกลม');
        yjjboard(400,345,560,400,6,9,0);
        setcolor(45); writexypixel(57,350,'วงกลม');
                      writexypixel(57,370,'Circle');
        setcolor(15);
        line(350,120,250,320);
        line(250,120,350,320);
        ellipse(300,120,0,360,50,15);
        ellipse(300,320,180,360,50,15);
        setcolor(12); setlinestyle(DottedLn,0,NormWidth);
        line(248,165,349,165);
        SetLineStyle(0,0,0);
        line(400,160,600,160);
        line(500,70,500,260);
          setcolor(15);
          ellipse(500,160,0,360,60,60);
end;

Procedure Vpre_ellipseX;
begin
     yjjboard(25,215,155,253,23,28,68);
          setcolor(9); writexypixel(6,222,'วงรี แกน X');
        yjjboard(400,345,560,400,6,9,0);
        setcolor(45); writexypixel(55,350,'วงรี แกน Y');
                      writexypixel(53,370,'Ellipse Y axis');
        setcolor(15);
        line(350,120,250,320);
        line(250,120,350,320);
        ellipse(300,120,0,360,50,15);
        ellipse(300,320,180,360,50,15);
        setcolor(12); setlinestyle(DottedLn,0,NormWidth);
        line(230,125,350,200);
        SetLineStyle(0,0,0);
        line(400,160,600,160);
        line(500,70,500,260);
        setcolor(15);
        ellipse(500,160,0,360,75,50);
end;

Procedure VPre_ellipseY;
begin
     yjjboard(25,260,155,298,23,28,68);
          setcolor(9); writexypixel(6,267,'วงรี แกน Y');
        yjjboard(430,365,595,420,6,9,0);
        setcolor(45); writexypixel(59,370,'วงรี แกน Y');
                      writexypixel(57,390,'Ellipse Y axis');
        setcolor(15);
        line(230,90,450,190);
        line(230,190,450,90);
        ellipse(450,140,0,360,15,50);
        ellipse(230,140,90,270,15,50);
        setcolor(12); setlinestyle(DottedLn,0,NormWidth);
        line(360,180,430,80);
        SetLineStyle(0,0,0);
        line(300,225,300,425);
        line(200,325,400,325);
        setcolor(15);
        ellipse(300,325,0,360,50,75);
end;

Procedure VPre_Exit;
begin
     yjjboard(25,305,155,343,23,28,68);
          setcolor(9); writexypixel(4,312,'กลับสู่ Main Menu');
end;


Procedure Preview_SubMenu;
var choice : byte;
    chpw   : char;
begin
Repeat
     cleardevice;
     initrgb;
     fadein(0);
       Menu_Preview;
     fadeout(100);
     SPre_paraY;
     SPre_paraX;
     SPre_circle;
     SPre_EllipseX;
     SPre_EllipseY;
     writetextmenu;
     choice := 1;
     chpw := #0;
     repeat
{down}      if chpw = #80 then
               begin
                    if choice = 5 then choice := 0;
                    inc(choice);
               end;
{up}        if chpw = #72 then
               begin
                    if choice = 1 then choice := 6;
                    dec(choice);
               end;
               case choice of
                1 :  begin
                          if chpw=#72 then SPre_ParaX;
                          if chpw=#80 then SPre_ellipsey;
                          VPre_paraY;
                     end;
                2 :  begin
                          if chpw=#72 then SPre_Circle;
                          if chpw=#80 then SPre_paraY;
                          VPre_paraX;
                     end;
                3 :  begin
                          if chpw=#72 then SPre_EllipseX;
                          if chpw=#80 then SPre_paraX;
                          VPre_Circle;
                     end;

                4 :  begin
                          if chpw=#72 then SPre_EllipseY;
                          if chpw=#80 then SPre_Circle;
                          VPre_EllipseX;
                     end;
                5 :  begin
                          if chpw=#72 then SPre_paray;
                          if chpw=#80 then SPre_EllipseX;
                          VPre_EllipseY;
                     end;
                end;{case}
                repeat
                      chpw := readkey;
                      if chpw = #0 then chpw := readkey;
                until chpw in [#27,#72,#80];
     until chpw in [#27];
Until chpw in [#27];
end;

begin
     Preview_SubMenu;
end;