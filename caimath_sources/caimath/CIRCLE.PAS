{$M 16384,0,130720}
Program Graph_CircleR;
uses crt,dos,kvga,kfade,graph,yjjsvga;
Var cch  :  char;
    cr,ch,ck,dcr,dch,dck,cd : integer;
    Senrobvong,AreaCircle,
    VolumeCircle            : real;
    SSenrobvong,SAreaCircle,
    SVolumeCircle,
    Scr,Sch,Sck          : string;

{$I help.pas}

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

Procedure Draw_Quadant_hk2(horigin,korigin,colorquadant : integer);
var ci   : integer;
    Quit : boolean;
begin
     quit := false;
     ci   := 0;
     setcolor(colorquadant);
     repeat
            line(22{328},215-korigin,22+ci,215-korigin);
            line(horigin+{473}165,70,horigin+{473}165,70+ci);
            inc(ci);
            yjjdelay(10);
      until ci = 290;
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

Procedure Menu_Circle_Border;
begin
     yjjborder(1,1,640,50,17,26);
        yjjborder(621,51,640,480,17,26);
        yjjborder(450,51,469,480,17,26);
        yjjborder(1,51,20,480,17,26);
        yjjborder(1,51,640,480,17,26);
        setcolor(15);
        settextstyle(2,0,10);
        outtextxy(150,225,'Circle');
        setcolor(14);
        outtextxy(152,225,'Circle');
        outtextxy(153,225,'Circle');
        outtextxy(154,225,'Circle');
        setcolor(14); writexypixel(63,350,'F1 = Help');
        setcolor(51); writexypixel(63,380,chr(135));
                      writexypixel(65,383,'ขึ้น');
        setcolor(47); writexypixel(69,383,chr(136));
                      writexypixel(71,383,'ลง');
        setcolor(100); writexypixel(63,408,'เลือกเมนู');
        setcolor(57); writexypixel(61,443,'Enter เพื่อเข้าเมนู');
     setcolor(82);
end;

Procedure writetextmenu_Circle;
begin
     settextstyle(1,0,2); setcolor(52);outtextxy(26,13,'Circle');
                          setcolor(10);outtextxy(480,13,'Conic Section');
     setcolor(79);writexypixel(12,15,'วงกลม');

end;

Procedure Sim_DataCircle;
begin
     yjjboard(480,80,610,118,20,25,57);
          setcolor(80); writexypixel(63,87,'เนื้อหาวงกลม');
          setfillstyle(1,0);
end;

Procedure Sim_CreatingGraphCircle;
begin
     yjjboard(480,125,610,163,20,25,57);
          setcolor(80); writexypixel(64,132,'สร้างกราฟ');
          setfillstyle(1,0);
end;

Procedure Sim_ExitCircle;
begin
     yjjboard(480,170,610,208,20,25,57);
          setcolor(80); writexypixel(61,177,'กลับสู่ Main Menu');
          setfillstyle(1,0);
end;

Procedure vab_DataCircle;
begin
     yjjboard(480,80,610,118,23,28,99);
          setcolor(9); writexypixel(63,87,'เนื้อหาวงกลม');
end;

Procedure vab_CreatingGraphCircle;
begin
     yjjboard(480,125,610,163,23,28,99);
          setcolor(9); writexypixel(64,132,'สร้างกราฟ');
end;

Procedure vab_ExitCircle;
begin
     yjjboard(480,170,610,208,23,28,99);
          setcolor(9); writexypixel(61,177,'กลับสู่ Main Menu');
end;

Procedure Data_Circle;
Var cch  :  char;
Begin
     setfillstyle(1,0);
     setcolor(0);
     bar(480,370,615,465);
     setcolor(0); writexypixel(63,350,'F1 = Help');
     yjjborder(475,375,515,400,6,8);setcolor(51); writexypixel(60,375,'Esc   = ออก');
     yjjborder(475,405,515,430,6,8);setcolor(51); writexypixel(60,405,'PgUp  = เลือกหน้าขึ้น');
     yjjborder(475,435,515,460,6,8);setcolor(51); writexypixel(60,435,'PgDn  = เลือกหน้าลง');

     REPEAT
     setfillstyle(1,0);bar(20,65,450,465);
     yjjborder(40,70,420,130,100,101);
     setcolor(53); writexypixel(8,80,'นิยาม  วงกลม คือ เซตของจุดทุกจุดบนระนาบซึ่งอยู่ห่าง');
     setcolor(74); writexypixel(8,80,'นิยาม');
     setcolor(53); writexypixel(8,100,'      จากจุดคงที่จุดหนึ่งเป็นระยะทางที่เท่ากัน');
     setcolor(53); writexypixel(5,140,'สมการของวงกลมที่จุดศูนย์กลางที่จุด (0,0) และมีรัศมีเท่ากับ r คือ');
     yjjborder(150,168,350,203,83,84);
     setcolor(62); writexypixel(24,170,' 2      2     2');
     setcolor(62); writexypixel(24,180,'X   +  Y  =  r  ');
     setcolor(25); line(250,220,250,420);
                   line(150,320,350,320);
     setcolor(91); ellipse(250,320,0,360,50,50);
     setcolor(96); writexypixel(10,250,'รัศมี (r)');
     setcolor(94); line(140,263,200,263);
                   line(200,263,218,283);
     setcolor(80); line(218,283,250,320);
     setcolor(100); writexypixel(32,323,'(0,0)');
     yjjborder(40,410,100,440,82,83); writexypixel(7,413,'PgDn');
     if cch <> #27 then
         repeat
               cch := readkey;
               if cch  = #0 then cch := readkey;
         until cch in [#81,#27];
     if cch <> #27 then
     begin
          setfillstyle(1,0);bar(20,65,450,465);
          setcolor(53);
          writexypixel(7,70,'ในกรณีที่จุดศูนย์กลางอยู่ที่จุดเลื่อนไปอยู่ที่จุด(h,k)');
          writexypixel(7,90,' และรัศมีเท่ากับ r หน่วย คือ');
         yjjborder(120,140,350,176,15,16);
          setcolor(43); writexypixel(23,140,'2          2     2');
          setcolor(43); writexypixel(18,150,'(x-h)   +  (y-k)  =  r  ');
          setcolor(42);
                  writexypixel(22,200,' r   คือ ความยาวของรัศมีของวงกลม');
          setcolor(11);
                  writexypixel(20,220,' (h,k) คือ คู่อันดับของจุดศูนย์กลางของวงกลม');
          setcolor(91); ellipse(80,250,0,360,50,50);
          setcolor(25); line(50,180,50,320);
                        line(20,280,155,280);
          setcolor(42);
          writexypixel(12,215,'r');
          setcolor(15);
          writexypixel(6,158,'Y');
          writexypixel(20,268,'X');
          setcolor(60);
                        line(80,248,123,224);
          setcolor(103);
          setlinestyle(dottedln,0,normwidth);
          line(80,249,80,280);
          line(50,250,80,250);
          setlinestyle(0,0,0);
          setcolor(76);
          writexypixel(11,240,'(h,k)');
          setcolor(59);
          writexypixel(7,310,'สมการทั่วไปของวงกลม คือ ');
          setcolor(48);
          writexypixel(10,340,'2   2');
          writexypixel(8,350,'x + y + Ax + By + C = 0');
          yjjborder(40,340,430,380,15,16);
          setcolor(61);
          writexypixel(32,350,'เมื่อ A,B,C เป็นค่าคงตัว');
          writexypixel(4,390,'สูตรที่น่าสนใจ');
          writexypixel(7,410,'                          2                    3');
          writexypixel(16,420,chr(137));
          writexypixel(31,420,chr(137));
          writexypixel(52,420,chr(137));
          writexypixel(51,415,'4');
          writexypixel(51,430,'3');
          writexypixel(51,418,'_');
          writexypixel(4,420,'เส้นรอบวง = 2 r  พื้นที่วงกลม =  r   ปริมาตรวงกลม =    r ');

     yjjborder(390,70,440,100,82,83); writexypixel(50,75,'PgUp');

     end;
     if cch <> #27 then
     repeat
           cch := readkey;
           if cch = #0 then cch := readkey;
     until cch in [#27,#73];

     UNTIL cch = #27;
     yjjboard(418,408,472,442,0,0,0);
End;

Procedure circle_Menu_Input;

begin
     SlideMenu(74);
     yjjborder(487,78,615,120,23,28);
     setcolor(11);settextstyle(2,0,4);outtextxy(500,86,'      2      2  2');
                  settextstyle(2,0,5);outtextxy(500,94,'(x-h)+(y-k)=r');
     ikey := #0;

     if ikey <> #27 then
     begin
                yjjborder(540,200,585,230,67,69);
                setcolor(59); writexypixel(62,205,'h =      0');
                yjjborder(540,240,585,270,67,69);
                setcolor(39); writexypixel(62,245,'k =      0');
                setcolor(10);
                writexypixel(63,395,'0 < r < 61');
          repeat
                yjjboard(540,160,585,190,67,69,0);
                setcolor(10); writexypixel(62,165,'r = ');
                              nominusinput(CR,2,68,165,85);
                if cr < 1 then yjjboard(540,160,585,190,67,69,0);
          until ((cr>=1) and (cr<=60)) or (ikey = #27);
          ch := 0;
          ck := 0;
     end;

     if ikey <> #27 then
     begin
          setcolor(10);
          for CD := 1   to 180 do
          begin
               ellipse(230+CH,265-CK,0,CD,CR,CR);
               ellipse(230+CH,265-CK,180,180+CD,CR,CR);
               yjjdelay(10);
          end;
          setcolor(84);outtextxy(230+ch+5,265-ck+5,'(h,k)');
     end;

    if ikey <> #27 then
    begin
         SlideMenu(70);
         senrobvong   :=  (2*22/7*cr);
         AreaCircle   :=  22/7*cr*cr;
         VolumeCircle :=  4/3*22/7*cr*cr*cr;
         str(cr,Scr);
         str(ch,Sch);
         str(ck,Sck);
         str(Senrobvong:1:2,SSenrobvong);
         str(Areacircle:1:2,SAreacircle);
         str(Volumecircle:1:2,SvolumeCircle);
         setcolor(102);writexypixel(60,80,'r');
              setcolor(44);writexypixel(65,80,'= '+Scr);
         setcolor(102);writexypixel(60,110,'h');
              setcolor(44);writexypixel(65,110,'= '+Sch);
         setcolor(102);writexypixel(60,140,'k');
              setcolor(44);writexypixel(65,140,'= '+Sck);
         setcolor(102);writexypixel(60,170,'ความยาวเส้นรอบวง');
              setcolor(44);writexypixel(65,190,'= '+SSenrobvong);
         setcolor(102);writexypixel(60,220,'พื้นที่วงกลม');
              setcolor(44);writexypixel(65,240,'= '+SAreacircle);
         setcolor(102);writexypixel(60,270,'ปริมาตรวงกลม');
              setcolor(44);writexypixel(65,290,'= '+SVolumeCircle);
     end;

     if ikey <> #27 then
     begin
          ikey := readkey;
          if ikey = #0 then ikey := readkey;
     end;

     if ikey <> #27 then
     begin
          SlideMenu(74);
          yjjborder(487,78,615,120,23,28);
          setcolor(11); settextstyle(2,0,4);outtextxy(500,86,'      2      2  2');
                        settextstyle(2,0,5);outtextxy(500,94,'(x-h)+(y-k)=r');
          yjjboard(540,160,585,190,67,69,0);
          setcolor(10); writexypixel(62,165,'r =    '+ scr);
          setcolor(59); writexypixel(64,380,'-61 < h < 61');
          setcolor(39); writexypixel(64,410,'-61 < k < 61');

          repeat
                yjjboard(540,200,585,230,67,69,0);
                setcolor(59); writexypixel(62,205,'h = ');
                              valinput(CH,2,68,205,86);
          until(ch <= 60)and(ch >= -60);
     end;

     if ikey <> #27 then
     begin
         repeat
               yjjboard(540,240,585,270,67,69,0);
               setcolor(39); writexypixel(62,245,'k = ');
                             valinput(CK,2,68,245,87);
         until(ck <= 60)and(ck >= -60);
         setfillstyle(1,0);bar(20,65,450,465);
         Draw_Quadant(230,265,30,185);
         Draw_Quadant_hk(ch,ck,25);
     end;

     if ikey <> #27 then
     begin
          setcolor(10);
          for CD := 1 to 180 do
          begin
               ellipse(230+CH,265-CK,0,CD,CR,CR);
               ellipse(230+CH,265-CK,180,180+CD,CR,CR);
               yjjdelay(10);
          end;
          setcolor(84);outtextxy(230+ch+5,265-ck+5,'(h,k)');
     end;
     if ikey <> #27 then
     begin
          SlideMenu(70);

          senrobvong   :=  (2*22/7*cr);
          AreaCircle   :=  22/7*cr*cr;
          VolumeCircle :=  4/3*22/7*cr*cr*cr;
          str(cr,Scr);
          str(ch,Sch);
          str(ck,Sck);
          str(Senrobvong:1:2,SSenrobvong);
          str(Areacircle:1:2,SAreacircle);
          str(Volumecircle:1:2,SvolumeCircle);
          setcolor(102);writexypixel(60,80,'r');
              setcolor(44);writexypixel(65,80,'= '+Scr);
          setcolor(102);writexypixel(60,110,'h');
              setcolor(44);writexypixel(65,110,'= '+Sch);
          setcolor(102);writexypixel(60,140,'k');
              setcolor(44);writexypixel(65,140,'= '+Sck);
          setcolor(102);writexypixel(60,170,'ความยาวเส้นรอบวง');
               setcolor(44);writexypixel(65,190,'= '+SSenrobvong);
          setcolor(102);writexypixel(60,220,'พื้นที่วงกลม');
               setcolor(44);writexypixel(65,240,'= '+SAreacircle);
          setcolor(102);writexypixel(60,270,'ปริมาตรวงกลม');
               setcolor(44);writexypixel(65,290,'= '+SVolumeCircle);
    end;

    if ikey <> #27 then pause;
end;

Procedure Creating_Graph_Circle;
Begin
     setfillstyle(1,0);bar(20,65,450,465);
     Draw_Quadant(230,265,30,185);
     circle_menu_input;
     if ikey <> #27 then
     begin
          setfillstyle(1,0);bar(25,61,622,470);
          draw_quadant(165,215,30,145);
          draw_quadant(473,215,30,145);
          yjjborder(319,61,321,469,6,7);
          yjjborder(19,370,628,370,7,6);
          setcolor(36);
          for CD := 1 to 180 do
          begin
               ellipse(165+ch,215-ck,0,CD,CR,CR);
               ellipse(165+ch,215-ck,180,180+CD,CR,CR);
               yjjdelay(10);
          end;
          setcolor(84);outtextxy(165+5+ch,215+5-ck,'(h,k)');

          str(Senrobvong:1:2,SSenrobvong);
          str(Areacircle:1:2,SAreacircle);
          str(Volumecircle:1:2,SvolumeCircle);

          setcolor(102);writexypixel(7,375,'r');
              setcolor(44);writexypixel(10,375,'= '+Scr);
          setcolor(102);writexypixel(17,375,'h');
              setcolor(44);writexypixel(20,375,'= '+Sch);
          setcolor(102);writexypixel(27,375,'k');
              setcolor(44);writexypixel(30,375,'= '+Sck);
          setcolor(102);writexypixel(7,395,'ความยาวเส้นรอบวง');
               setcolor(44);writexypixel(27,395,'= '+SSenrobvong);
          setcolor(102);writexypixel(7,415,'พื้นที่วงกลม');
               setcolor(44);writexypixel(27,415,'= '+SAreacircle);
          setcolor(102);writexypixel(7,435,'ปริมาตรวงกลม');
               setcolor(44);writexypixel(27,435,'= '+SVolumeCircle);

          draw_quadant_hk2(ch,ck,25);
          setcolor(36);
          for CD := 1 to 180 do
          begin
               ellipse(473,215,0,CD,CR,CR);
               ellipse(473,215,180,180+CD,CR,CR);
               yjjdelay(10);
          end;
          setcolor(84);outtextxy(473+5,215+5,'(0,0)');

          ch := 0;
          ck := 0;
          senrobvong   :=  (2*22/7*cr);
          AreaCircle   :=  22/7*cr*cr;
          VolumeCircle :=  4/3*22/7*cr*cr*cr;
          str(cr,Scr);
          str(ch,Sch);
          str(ck,Sck);
          str(Senrobvong:1:2,SSenrobvong);
          str(Areacircle:1:2,SAreacircle);
          str(Volumecircle:1:2,SvolumeCircle);
          setcolor(102);writexypixel(44,375,'r');
               setcolor(44);writexypixel(47,375,'= '+Scr);
          setcolor(102);writexypixel(54,375,'h');
               setcolor(44);writexypixel(57,375,'= '+Sch);
          setcolor(102);writexypixel(64,375,'k');
               setcolor(44);writexypixel(67,375,'= '+Sck);
          setcolor(102);writexypixel(44,395,'ความยาวเส้นรอบวง');
               setcolor(44);writexypixel(64,395,'= '+SSenrobvong);
          setcolor(102);writexypixel(44,415,'พื้นที่วงกลม');
               setcolor(44);writexypixel(64,415,'= '+SAreacircle);
          setcolor(102);writexypixel(44,435,'ปริมาตรวงกลม');
               setcolor(44);writexypixel(64,435,'= '+SVolumeCircle);
     end;
     if ikey <> #27 then pause;
end;

Procedure Circle_SubMenu;
var choice : byte;
    chpC   : char;
begin
Repeat
     cleardevice;
     initrgb;
     fadein(0);
       Menu_Circle_border;
     fadeout(100);
     Sim_CreatingGraphCircle;
     Sim_ExitCircle;
     writetextmenu_Circle;
     choice := 1;
     chpC := #0;
     repeat
{down}      if chpC = #80 then
               begin
                    if choice = 3 then choice := 0;
                    inc(choice);
               end;
{up}        if chpC = #72 then
               begin
                    if choice = 1 then choice := 4;
                    dec(choice);
               end;
               case choice of
                1 :  begin
                          if chpC=#72 then Sim_CreatingGraphCircle;
                          if chpC=#80 then Sim_ExitCircle;
                          vab_DataCircle;
                     end;
                2 :  begin
                          if chpC=#72 then Sim_ExitCircle;
                          if chpC=#80 then Sim_DataCircle;
                          vab_CreatingGraphCircle;
                     end;
                3 :  begin
                          if chpC=#72 then Sim_DataCircle;
                          if chpC=#80 then Sim_CreatingGraphCircle;
                          vab_ExitCircle;
                     end;

                end;{case}
                repeat
                      chpC := readkey;
                      if chpC = #0 then chpC := readkey;
                until chpC in [#13,#27,#72,#80,#59];
                if chpc = #59 then help;
     until chpC in [#13];
     Case Choice of
          1 : data_Circle;
          2 : Creating_Graph_Circle;
     end;
Until (choice = 3);
end;

begin
     uses_svga256_color;
     initrgb;
     start_delay(real_delay2);
     loadfont('normal.fon');
     Circle_SubMenu;
end.