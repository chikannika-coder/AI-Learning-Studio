{$M 16384,0,130720}
Program Graph_Ellipse_xaxis;
uses crt,dos,kvga,kfade,graph,yjjsvga;
Var exch  :  char;
    exh,exk,exa,exb,exd,exc                                  : integer;
    Sexh,Sexk,Sexa,Sexb,major,minor,latus,focus1,focus2,elec : string;

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
            line(22,215-korigin,22+ci,215-korigin);
            line(horigin+165,70,horigin+165,70+ci);
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


Procedure Menu_Ellipsex_Border;
begin
     yjjborder(1,1,640,50,17,26);
        yjjborder(621,51,640,480,17,26);
        yjjborder(450,51,469,480,17,26);
        yjjborder(1,51,20,480,17,26);
        setcolor(15);
        settextstyle(2,0,10);
        outtextxy(70,225,'Ellipse X axis');
        setcolor(87);
        outtextxy(72,225,'Ellipse X axis');
        outtextxy(73,225,'Ellipse X axis');
        outtextxy(74,225,'Ellipse X axis');
        setcolor(14); writexypixel(63,350,'F1 = Help');
        setcolor(51); writexypixel(63,380,chr(135));
                      writexypixel(65,383,'ขึ้น');
        setcolor(47); writexypixel(69,383,chr(136));
                      writexypixel(71,383,'ลง');
        setcolor(100); writexypixel(63,408,'เลือกเมนู');
        setcolor(57); writexypixel(61,443,'Enter เพื่อเข้าเมนู');
     yjjborder(1,51,640,480,17,26);
     setcolor(82);
end;

Procedure writetextmenu;
begin
     settextstyle(1,0,2); setcolor(52);outtextxy(26,13,'Ellipse   axis');
                          setcolor(37);outtextxy(97,13,'X');
                          setcolor(10);outtextxy(480,13,'Conic Section');
    setcolor(79);writexypixel(21,15,'วงรี แกน X');
end;

Procedure Sim_DataEllipseX;
begin
     yjjboard(480,80,610,118,20,25,57);
          setcolor(80); writexypixel(64,87,'เนื้อหาวงรี');
end;

Procedure Sim_CreatingGraphEllipseX;
begin
     yjjboard(480,125,610,163,20,25,57);
          setcolor(80); writexypixel(64,132,'สร้างกราฟ');
end;

Procedure Sim_ExitEllipseX;
begin
     yjjboard(480,170,610,208,20,25,57);
          setcolor(80); writexypixel(61,177,'กลับสู่ Main Menu');
end;

Procedure vab_DataEllipseX;
begin
     yjjboard(480,80,610,118,23,28,99);
          setcolor(9); writexypixel(64,87,'เนื้อหาวงรี');
end;

Procedure vab_CreatingGraphEllipseX;
begin
     yjjboard(480,125,610,163,23,28,99);
          setcolor(9); writexypixel(64,132,'สร้างกราฟ');
end;

Procedure vab_ExitEllipseX;
begin
     yjjboard(480,170,610,208,23,28,99);
          setcolor(9); writexypixel(61,177,'กลับสู่ Main Menu');
end;

Procedure Data_Ellipse_X;
Var Exch  :  char;
    Exxa,Exc,Exx,Exy,Exya,bExxa,Exh,Exk,Exdatachoice : integer;

Procedure page1;
var Exy,bExya,exc,exa,exb : integer;
begin
     setfillstyle(1,0);bar(20,65,450,465);
     yjjborder(40,70,435,170,100,101);
     setcolor(0); writexypixel(63,350,'F1 = Help');
     setcolor(53); writexypixel(8,80,'     วงรี คือเซตของจุดทุกจุดบนระนาบซึ่งผลบวกของระยะ');
     setcolor(74); writexypixel(8,100,'นิยาม');
     setcolor(53); writexypixel(8,100,'     ทางจากจุดเหล่านี้ไปยังจุดคงที่  2  จุดบนระนาบมีค่า');
     setcolor(53); writexypixel(8,120,'     คงตัวเสมอและค่าคงตัวนี้  มากกว่าระยะห่างระหว่าง');
     setcolor(53); writexypixel(8,140,'     จุดคงที่ทั้ง 2 จุดนั้น');
     exa := 80;
     exb := 50;
     setcolor(61); ellipse(250,230,0,359,exa,exb);
     exc:= round(sqrt(exa*exa-exb*exb));
     setcolor(87); line(250-exc,230,299,190);
                   line(250+exc,230,299,190);
     setcolor(9);  writexypixel(24,235,'F''            F');

                   writexypixel(38,175,'P');
     setcolor(96); writexypixel(5,300,'ผลรวมของระยะ F''P กับระยะ FP จะเท่ากันเสมอไม่ว่าจุด P');
                   writexypixel(5,330,'จะอยู่บนจุดใดของวงรี');
     setcolor(53); writexypixel(5,370,'จุดคงที่ คือ จุดโฟกัสทั้ง 2 จุด รวมเรียกว่า foci');
     setcolor(37); writexypixel(5,370,'                                 foci');
     yjjborder(40,410,100,440,82,83); writexypixel(7,413,'PgDn');
end;

Procedure page2;
var Exy,bExya,exa,exb,exc : integer;
begin
          exa := 60;
          exb := 40;
          exc:= round(sqrt(exa*exa-exb*exb));
          setfillstyle(1,0);bar(20,65,450,465);
          setcolor(25); line(150,130,310,130);
                        line(230,70,230,190);

          setcolor(38); line(170,130,290,130);
          setcolor(90); line(230,90,230,170);
          setcolor(99); ellipse(230,130,0,360,60,40);
          setcolor(29); line(230+60+10,90,230+60+10,130);
          setcolor(29); line(230+60+7,90,230+60+13,90);
                        line(230+60+7,130,230+60+13,130);
                        writexypixel(38,100,'b');
          setcolor(29); line(230-60,130+40+10,230,130+40+10);
          setcolor(29); line(230-60,130+40+7,230-60,130+40+13);
                        line(230,130+40+7,230,130+40+13);
                        writexypixel(25,130+40+7,'a');
          setcolor(39); line(230,130+40+10,230+exc,130+40+10);
                        line(230+exc,130+40+7,230+exc,130+40+13);
                        writexypixel(31,130+40+7,'c');
          setcolor(14); line(130,90,200,90);
                        line(200,90,230,120);
          setcolor(102); writexypixel(10,77,'แกนโท');
                         writexypixel(6,92,'(Minor axis)');
          setcolor(14); line(130,150,200,150);
                        line(200,150,220,130);
          setcolor(102); writexypixel(9,140,'แกนเอก');
                         writexypixel(6,155,'(Major axis)');
          setcolor(10); line(230+exc,103,230+exc,155);
          setcolor(14); line(230+exc,140,230+exc+20,160);
          setcolor(14); line(230+exc+20,160,230+exc+50,160);
          setcolor(102);writexypixel(42,145,'ไดเรกตริก');
                        writexypixel(41,160,'(Directric)');
          setcolor(74);
          writexypixel(5,215,'                          2   2   2');
          writexypixel(5,225,'ความสัมพันธ์ระหว่าง a,b,c คือ c = a - b   โดยที่ a>c,a>b');
          setcolor(53);
          writexypixel(5,255,'ความแกนเอก (Major axis) = 2a');
          writexypixel(5,285,'ความแกนโท  (Minor axis) = 2b');
          writexypixel(5,315,'สมการมาตรฐานของวงรีที่มีจุดศูนย์กลางอยู่ที่จุด (0,0) คือ');
          yjjborder(158,355,295,415,55,56);
          setcolor(14);
          writexypixel(22,355,'  2     2');
          writexypixel(22,365,' X     Y');
          writexypixel(22,370,' _  +  _  = 1');
          writexypixel(22,380,'  2     2');
          writexypixel(22,390,' a     b');

     yjjborder(390,70,440,100,82,83); writexypixel(50,75,'PgUp');
     yjjborder(40,410,100,440,82,83); writexypixel(7,413,'PgDn');
end;
Procedure page3;
var exa,exb,exc : integer;
begin
          setfillstyle(1,0);bar(20,65,450,465);
          exa := 60;
          exb := 40;
          exc:= round(sqrt(exa*exa-exb*exb));
          setcolor(15); line(140,150,320,150);
                        line(200,70,200,190);
          setcolor(53); line(140,130,320,130);
                        line(230,70,230,190);
                        writexypixel(30,105,'(h,k)');
          setcolor(99); ellipse(230,130,0,360,60,40);
          writexypixel(5,205,'สมการมาตรฐานของวงรีที่มีจุดศูนย์กลางอยู่ที่จุด (h,k) คือ');
          yjjborder(138,235,315,300,82,83);
          setcolor(73);
          writexypixel(20,235,'     2       2');
          writexypixel(20,245,'(x-h)   (y-k)');
          writexypixel(20,250,'      +       = 1');
          line(158,265,193,265);
          line(220,265,255,265);
          writexypixel(20,260,'   2       2');
          writexypixel(20,270,'  a       b');
          setcolor(93); writexypixel(5,320,'สมการทั่วไปของวงรี คือ');
          setcolor(43); writexypixel(5,310,'                     2    2');
          setcolor(43); writexypixel(5,320,'                   Ax + By + Cx + Dy + E = 0');
          setcolor(93); writexypixel(5,350,'เมื่อ A,B เป็นจำนวนบวกหรือลบทั้งคู่');
          setcolor(82); writexypixel(5,380,'                 c');
          setcolor(82); writexypixel(5,390,'ค่า Electricity = - ');
          setcolor(82); writexypixel(5,400,'                 a');
          setcolor(82); writexypixel(5,405,'                         2');
          setcolor(82); writexypixel(5,410,'                        b');
          setcolor(82); writexypixel(5,420,'ความยาว Latusrectum =  2-');
          setcolor(82); writexypixel(5,430,'                        a ');

     yjjborder(390,70,440,100,82,83); writexypixel(50,75,'PgUp');
end;

Begin
     setfillstyle(1,0);
     setcolor(0);
     bar(480,370,615,465);
     yjjborder(475,375,515,400,6,8);setcolor(51); writexypixel(60,375,'Esc   = ออก');
     yjjborder(475,405,515,430,6,8);setcolor(51); writexypixel(60,405,'PgUp  = เลือกหน้าขึ้น');
     yjjborder(475,435,515,460,6,8);setcolor(51); writexypixel(60,435,'PgDn  = เลือกหน้าลง');
     Exdatachoice := 1;
     repeat
           if Exch = #81 then if Exdatachoice <> 3 then inc(Exdatachoice);
           if Exch = #73 then if Exdatachoice <> 1 then dec(Exdatachoice);
           case Exdatachoice of
                1 : page1;
                2 : page2;
                3 : page3;
           end; {case}
           Exch := readkey; if Exch = #0 then Exch := readkey;
     until Exch = #27;
     yjjboard(418,408,472,442,0,0,0);
End;




Procedure EllipseX_Menu_Input;

begin
     SlideMenu(74);
     yjjborder(487,78,615,136,23,28);
     setcolor(11);settextstyle(2,0,4);outtextxy(500,86,'      2      2  ');
                  settextstyle(2,0,5);outtextxy(500,94,'(x-h)+(y-k) = 1');
                  line(500,109,530,109);line(545,109,575,109);
                  settextstyle(2,0,4);outtextxy(500,110,'    2      2  ');
                  settextstyle(2,0,5);outtextxy(500,114,'  a    b');
     ikey := #0;
          yjjborder(540,160,585,190,67,69);
          setcolor(84); writexypixel(62,165,'h =     0');
          yjjborder(540,200,585,230,67,69);
          setcolor(78); writexypixel(62,205,'k =     0');
          writexypixel(64,380,'1 < a < 61');
          writexypixel(64,410,'0 < b < a');
     if ikey <> #27 then
     begin
          repeat
                yjjboard(540,240,585,270,67,69,0);
                setcolor(80); writexypixel(62,245,'a = ');
                              nominusinput(exa,2,68,245,87);
          until (exa > 1)and(exa <= 60) or (ikey = #27);
     end;

     if ikey <> #27 then
     begin
     repeat
          yjjboard(540,280,585,310,67,69,0);
          setcolor(82); writexypixel(62,285,'b = ');
                        nominusinput(exb,2,68,285,87);
     until ((exa>exb) and (exb<>0) and (exb <= 60)) or (ikey = #27);
     end;
     exh := 0;
     exk := 0;

    if ikey <> #27 then
    begin
         setcolor(85);
         for exD := 1   to 180 do
         begin
              ellipse(230+exH,265-exK,0,exD,exa,exb);
              ellipse(230+exH,265-exK,180,180+exD,exa,exb);
              yjjdelay(10);
         end;
         setcolor(89);outtextxy(230+exh+5,265-exk+5,'(h,k)');
         exc := round(sqrt(exa*exa-exb*exb));
    end;

    if ikey <> #27 then
    begin
         SlideMenu(100);
         str(exh,Sexh);
         str(exk,Sexk);
         str(exa,Sexa);
         str(exb,Sexb);
         str(2*exa,major);
         str(2*exb,minor);
         str((2*exb*exb)/exa:1:2,latus);
         str(exh-exc,focus1);
         str(exh+exc,focus2);
         str((exc/exa):1:2,elec);

         setcolor(62);writexypixel(60,80,'h');
              setcolor(46);writexypixel(65,80,'= '+Sexh);
         setcolor(62);writexypixel(60,110,'k');
              setcolor(48);writexypixel(65,110,'= '+Sexk);
         setcolor(62);writexypixel(60,140,'a');
              setcolor(50);writexypixel(65,140,'= '+Sexa);
         setcolor(62);writexypixel(60,170,'b');
              setcolor(52);writexypixel(65,170,'= '+Sexb);
         setcolor(62);writexypixel(60,200,'ความยาวแกนเอก');
              setcolor(54);writexypixel(65,220,'= '+major);
         setcolor(62);writexypixel(60,250,'ความยาวแกนโท');
              setcolor(56);writexypixel(65,270,'= '+minor);
         setcolor(62);writexypixel(60,300,'ความยาวLatusrectum');
              setcolor(58);writexypixel(65,320,'= '+latus);
         setcolor(62);writexypixel(60,350,'จุดโฟกัส (Focus)');
              setcolor(36);
              writexypixel(65,370,'= ('+focus1+','+sexk+')');
              writexypixel(65,400,'= ('+focus2+','+sexk+')');
         setcolor(62);writexypixel(60,430,'ค่า Electricity');
              setcolor(38);writexypixel(65,450,'= '+elec);
    end; {Chech Esc}
    if ikey <> #27 then
    begin
         ikey := readkey;
         if ikey = #0 then ikey := readkey;
    end;
     if ikey <> #27 then
     begin
       SlideMenu(74);
       yjjborder(487,78,615,136,23,28);
       setcolor(11);settextstyle(2,0,4);outtextxy(500,86,'      2      2  ');
                    settextstyle(2,0,5);outtextxy(500,94,'(x-h)+(y-k) = 1');
                    line(500,109,530,109);line(545,109,575,109);
                    settextstyle(2,0,4);outtextxy(500,110,'    2      2  ');
                    settextstyle(2,0,5);outtextxy(500,114,'  a    b');
          yjjboard(540,240,585,270,67,69,0);
          setcolor(80); writexypixel(62,245,'a =    '+ sexa);
          yjjboard(540,280,585,310,67,69,0);
          setcolor(82); writexypixel(62,285,'b =    '+ sexb);
          writexypixel(62,380,'-61 < h < 60');
          writexypixel(62,410,'-61 < k < 60');
          repeat
                yjjboard(540,160,585,190,67,69,0);
                setcolor(84); writexypixel(62,165,'h = ');
                              valinput(exh,2,68,165,87);
          until(exh <= 60)and(exh >= -60 );
     end;

     if ikey <> #27 then
     begin
       repeat
          yjjboard(540,200,585,230,67,69,0);
          setcolor(78); writexypixel(62,205,'k = ');
                        valinput(exk,2,68,205,87);
       until(exk <= 60)and(exk >= -60 );
          setfillstyle(1,0);bar(20,65,450,465);
          Draw_Quadant(230,265,30,185);
          Draw_Quadant_hk(exh,exk,25);
     end;

    if ikey <> #27 then
    begin
    setcolor(85);
    for exD := 1   to 180 do
    begin
         ellipse(230+exH,265-exK,0,exD,exa,exb);
         ellipse(230+exH,265-exK,180,180+exD,exa,exb);
         yjjdelay(10);
    end;

    setcolor(89);outtextxy(230+exh+5,265-exk+5,'(h,k)');

    exc := round(sqrt(exa*exa-exb*exb));
    end;

    if ikey <> #27 then
    begin
         SlideMenu(100);

         str(exh,Sexh);
         str(exk,Sexk);
         str(exa,Sexa);
         str(exb,Sexb);
         str(2*exa,major);
         str(2*exb,minor);
         str((2*exb*exb)/exa:1:2,latus);
         str(exh-exc,focus1);
         str(exh+exc,focus2);
         str((exc/exa):1:2,elec);

         setcolor(62);writexypixel(60,80,'h');
              setcolor(46);writexypixel(65,80,'= '+Sexh);
         setcolor(62);writexypixel(60,110,'k');
              setcolor(48);writexypixel(65,110,'= '+Sexk);
         setcolor(62);writexypixel(60,140,'a');
              setcolor(50);writexypixel(65,140,'= '+Sexa);
         setcolor(62);writexypixel(60,170,'b');
              setcolor(52);writexypixel(65,170,'= '+Sexb);
         setcolor(62);writexypixel(60,200,'ความยาวแกนเอก');
              setcolor(54);writexypixel(65,220,'= '+major);
         setcolor(62);writexypixel(60,250,'ความยาวแกนโท');
              setcolor(56);writexypixel(65,270,'= '+minor);
         setcolor(62);writexypixel(60,300,'ความยาวLatusrectum');
              setcolor(58);writexypixel(65,320,'= '+latus);
         setcolor(62);writexypixel(60,350,'จุดโฟกัส (Focus)');
              setcolor(36);
              writexypixel(65,370,'= ('+focus1+','+sexk+')');
              writexypixel(65,400,'= ('+focus2+','+sexk+')');
         setcolor(62);writexypixel(60,430,'ค่า Electricity');
              setcolor(38);writexypixel(65,450,'= '+elec);

    end; {Chech Esc}

    if ikey <> #27 then pause;
end;

Procedure Creating_Graph_Ellipsex;
Begin
     setfillstyle(1,0);bar(20,65,450,465);
     Draw_Quadant(230,265,30,185);
     Ellipsex_menu_input;
     if ikey <> #27 then
     begin
          setfillstyle(1,0);bar(25,61,622,470);
          yjjborder(319,61,321,469,6,7);
          yjjborder(19,370,628,370,7,6);
          draw_quadant(165,215,30,145);
          draw_quadant(473,215,30,145);
          setcolor(85);
          for exD := 1   to 180 do
          begin
               ellipse(165+exh,215-exk,0,exD,exa,exb);
               ellipse(165+exh,215-exk,180,180+exD,exa,exb);
               yjjdelay(10);
          end;
          setcolor(89);outtextxy(165+5+exh,215+5-exk,'(h,k)');

          draw_quadant_hk2(exh,exk,25);

         str(exh,Sexh);
         str(exk,Sexk);
         str(exa,Sexa);
         str(exb,Sexb);
         str(2*exa,major);
         str(2*exb,minor);
         str((2*exb*exb)/exa:1:2,latus);
         str(exh-exc,focus1);
         str(exh+exc,focus2);
         str((exc/exa):1:2,elec);

         setcolor(62);writexypixel(9,375,'h');
              setcolor(46);writexypixel(12,375,'= '+Sexh);
         setcolor(62);writexypixel(19,375,'k');
              setcolor(48);writexypixel(22,375,'= '+Sexk);
         setcolor(62);writexypixel(9,395,'a');
              setcolor(50);writexypixel(12,395,'= '+Sexa);
         setcolor(62);writexypixel(19,395,'b');
              setcolor(52);writexypixel(22,395,'= '+Sexb);
         setcolor(62);writexypixel(7,415,'จุดโฟกัส (Focus)');
              setcolor(36);
              writexypixel(22,415,'= ('+focus1+','+sexk+')');
              writexypixel(22,435,'= ('+focus2+','+sexk+')');

          setcolor(85);
          for exD := 1   to 180 do
          begin
               ellipse(473,215,0,exD,exa,exb);
               ellipse(473,215,180,180+exD,exa,exb);
               yjjdelay(10);
          end;
          setcolor(89);outtextxy(473+5,215+5,'(0,0)');

         exh := 0;
         exk := 0;
         str(exh,Sexh);
         str(exk,Sexk);
         str(exa,Sexa);
         str(exb,Sexb);
         str(2*exa,major);
         str(2*exb,minor);
         str((2*exb*exb)/exa:1:2,latus);
         str(exh-exc,focus1);
         str(exh+exc,focus2);
         str((exc/exa):1:2,elec);

         setcolor(62);writexypixel(49,375,'h');
              setcolor(46);writexypixel(52,375,'= '+Sexh);
         setcolor(62);writexypixel(59,375,'k');
              setcolor(48);writexypixel(62,375,'= '+Sexk);
         setcolor(62);writexypixel(49,395,'a');
              setcolor(50);writexypixel(52,395,'= '+Sexa);
         setcolor(62);writexypixel(59,395,'b');
              setcolor(52);writexypixel(62,395,'= '+Sexb);
         setcolor(62);writexypixel(47,415,'จุดโฟกัส (Focus)');
              setcolor(36);
              writexypixel(62,415,'= ('+focus1+','+sexk+')');
              writexypixel(62,435,'= ('+focus2+','+sexk+')');
    end;
    if ikey <> #27 then pause;
end;

Procedure EllipseX_SubMenu;
var choice : byte;
    chex   : char;
begin
Repeat
     cleardevice;
     initrgb;
     fadein(0);
       Menu_Ellipsex_border;
     fadeout(100);
     Sim_CreatingGraphEllipsex;
     Sim_ExitEllipsex;
     writetextmenu;
     choice := 1;
     chex := #0;
     repeat
{down}      if chex = #80 then
               begin
                    if choice = 3 then choice := 0;
                    inc(choice);
               end;
{up}        if chex = #72 then
               begin
                    if choice = 1 then choice := 4;
                    dec(choice);
               end;
               case choice of
                1 :  begin
                          if chex=#72 then Sim_CreatingGraphEllipsex;
                          if chex=#80 then Sim_ExitEllipsex;
                          vab_DataEllipsex;
                     end;
                2 :  begin
                          if chex=#72 then Sim_ExitEllipsex;
                          if chex=#80 then Sim_DataEllipsex;
                          vab_CreatingGraphEllipsex;
                     end;
                3 :  begin
                          if chex=#72 then Sim_DataEllipsex;
                          if chex=#80 then Sim_CreatingGraphEllipsex;
                          vab_ExitEllipsex;
                     end;

                end;{case}
                repeat
                      chex := readkey;
                      if chex = #0 then chex := readkey;
                until chex in [#13,#72,#80,#59];
                if chex = #59 then help;
     until chex in [#13];
     Case Choice of
       1 : data_Ellipse_X;
       2 : Creating_Graph_Ellipsex;
     end;
Until (choice = 3) or ( chex in [#27]);
end;

begin
     uses_svga256_color;
     initrgb;
     loadfont('normal.fon');
     start_delay(real_delay2);
     EllipseX_SubMenu;
end.