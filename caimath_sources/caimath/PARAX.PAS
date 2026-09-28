{$M 16384,0,130720}
Program Graph_Parabola_Xaxis;
uses crt,dos,kvga,kfade,graph,yjjsvga;
Var pxch  :  char;
    pxxa,pxc,pxx,pxy,pxya,bpxxa,pxh,pxk,pxdatachoice : integer;
    real_delay,real_delay2                           : real;
    Spxc,Spxh,Spxk,Sdirec,Sfocus,Slatus              : string;

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
var pxi : integer;
begin
     for pxi := 622 downto 469 do
     begin
          setcolor(cc);line(pxi,65,pxi,468);
          setcolor(0); line(pxi+5,65,pxi+5,468);
          yjjdelay(10);
     end;
end;

Procedure Menu_ParaX_Border;
begin
     yjjborder(1,1,640,50,17,26);
        yjjborder(621,51,640,480,17,26);
        yjjborder(450,51,469,480,17,26);
        yjjborder(1,51,20,480,17,26);
        setcolor(15);
        settextstyle(2,0,10);
        outtextxy(55,225,'Parabola X axis');
        setcolor(60);
        outtextxy(57,225,'Parabola X axis');
        outtextxy(58,225,'Parabola X axis');
        outtextxy(59,225,'Parabola X axis');
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

Procedure writetextmenu_paraX;
begin
     settextstyle(1,0,2); setcolor(52);outtextxy(26,13,'Parabola   axis');
                          setcolor(37);outtextxy(120,13,'X');
                          setcolor(10);outtextxy(480,13,'Conic Section');
   setcolor(79); writexypixel(25,15,'พาราโบลา แกน X');
end;

Procedure Sim_DataParaX;
begin
     yjjboard(480,80,610,118,20,25,57);
          setcolor(80); writexypixel(62,87,'เนื้อหาพาราโบลา');
end;

Procedure Sim_CreatingGraphParaX;
begin
     yjjboard(480,125,610,163,20,25,57);
          setcolor(80); writexypixel(64,132,'สร้างกราฟ');
end;

Procedure Sim_ExitParaX;
begin
     yjjboard(480,170,610,208,20,25,57);
          setcolor(80); writexypixel(61,177,'กลับสู่ Main Menu');
end;

Procedure vab_DataParaX;
begin
     yjjboard(480,80,610,118,23,28,99);
          setcolor(9); writexypixel(62,87,'เนื้อหาพาราโบลา');
end;

Procedure vab_CreatingGraphParaX;
begin
     yjjboard(480,125,610,163,23,28,99);
          setcolor(9); writexypixel(64,132,'สร้างกราฟ');
end;

Procedure vab_ExitParaX;
begin
     yjjboard(480,170,610,208,23,28,99);
          setcolor(9); writexypixel(61,177,'กลับสู่ Main Menu');
end;
Procedure pxDirectric(h,k,c,beginx,color : integer);
var i : integer;
begin
     i := 0;
     setcolor(color);
     repeat
           inc(i);
           line(230+h-c,265-k-beginX,230+h-c,265-k-beginX-i);
           yjjdelay(10);
     until i = beginX*(-2)+3;
end;

Procedure pxDirectric2(x1,h,k,c,beginy,color : integer);
var i : integer;
begin
     i := 0;
     setcolor(color);
     repeat
           inc(i);
           line(x1+h-c,215-k-beginy,x1+h-c,215-k-i-beginY);
           yjjdelay(10);
     until i = beginy*(-2);
end;

Procedure Data_Parax;
Var pxch  :  char;
    pxxa,pxc,pxx,pxy,pxya,bpxxa,pxh,pxk,pxdatachoice : integer;

Procedure page1;
var pxy,bpxya : integer;
begin
     setfillstyle(1,0);bar(20,65,450,465);
     yjjborder(40,70,435,150,100,101);
     setcolor(0); writexypixel(63,350,'F1 = Help');
     setcolor(53); writexypixel(8,80,'      พาราโบลา  คือ เซตของจุดทุกจุดบนระนาบซึ่งทำให้');
     setcolor(74); writexypixel(8,100,'นิยาม');
     setcolor(53); writexypixel(8,100,'      ระยะทางที่จุดเหล่านี้อยู่ห่างจากเส้นคงที่เส้นหนึ่งเท่า');
     setcolor(53); writexypixel(8,120,'      กับระยะทางที่จุดเหล่านี้อยู่ห่างจากจุดคงที่จุดหนึ่ง');
     setcolor(53); writexypixel(5,160,'สมการของพาราโบลาแกน X ที่จุดศูนย์กลางที่จุด (0,0) คือ');
     yjjborder(150,188,350,223,83,84);
     setcolor(62); writexypixel(24,190,'    2 ');
     setcolor(62); writexypixel(24,200,'   Y  = 4CX  ');

     setcolor(25); line(250,235,250,425);
                   line(155,330,345,330);
                   setcolor(99);
                   writexypixel(44,318,'X');writexypixel(30,220,'Y');

          setcolor(91);
          bpxya := -50;
          pxc   := 10;
          pxh   := 0;
          pxk   := 0;
          pxya  := bpxya;
          pxc   := pxc;
          pxxa  := round((pxya*pxya)/(4*pxc));
          For pxy := bpxya to (-1)*bpxya+1 do
          begin
               pxx := round((pxya*pxya)/(4*pxc));
               line(250+pxxa+pxh,330-pxya-pxk,250+pxx+pxh,330-pxy-pxk);
               pxxa := pxx;
               pxya := pxy;
           end;
     setcolor(82);line(250-pxc,330-50,250-pxc,330+50);
     setcolor(53);writexypixel(5,350,'เส้นไดเรกตริก (Directric)');
     setcolor(42);line(250,330,280,350);
     setcolor(37);writexypixel(36,336,'จุดยอด');
     setcolor(60);line(225,363,240,340);
     yjjborder(40,410,100,440,82,83); writexypixel(7,413,'PgDn');
end;
Procedure page2;
var pxy,bpxya : integer;
begin
          setfillstyle(1,0);bar(20,65,450,465);
          setcolor(68); writexypixel(4,70,'เส้นคงที่ เรียกว่า ไดเรกตริกซ์ (Directic Line)');
                        writexypixel(4,90,'จุดคงที่  เรียกว่า โฟกัสพาราโบลา (Focus)');
          setcolor(73); writexypixel(4,120,'จุดที่พาราโบลาตัดแกนของพาราโบลา เรียกว่า จุดยอดของพาราโบลา');
                        writexypixel(4,140,'ส่วนของเส้นตรงที่ผานโฟกัสและมีจุดปลายทั้งสองอยู่บนพาราโบลา และ');
                        writexypixel(4,160,'ตั้งฉากกับแกน X เรียกว่า ลาตัสเรกตัม');
          setcolor(25); line(250,220,250,430);
                        line(100,330,400,330);
          setcolor(91);
          bpxya := -100;
          pxc   := 25;
          pxh   := 0;
          pxk   := 0;
          pxya  := bpxya;
          pxc   := pxc;
          pxxa  := round((pxya*pxya)/(4*pxc));
          For pxY := bpxya to (-1)*bpxya+1 do
          begin
               pxx := round((pxya*pxya)/(4*pxc));
               line(250+pxxa+pxh,330-pxya-pxk,250+pxx+pxh,330-pxy-pxk);
               pxxa := pxx;
               pxya := pxy;
          end;
          setcolor(82);  line(250-pxc,330-110,250-pxc,330+100);
          setcolor(76);  line(250+pxc,330-50,250+pxc,330+50);
          setcolor(12);  line(273,310,277,310);
                         line(273,348,277,348);
          setcolor(48);  line(208,283,250,283);
                         line(250,283,275,313);
          setcolor(53);  writexypixel(6,270,'ความยาว Latusrectum');
          setcolor(53);  writexypixel(5,370,'เส้นไดเรกตริก (Directric)');
          setcolor(40);  line(200,353,230,353);
                         line(230,353,248,332);
          setcolor(37);  writexypixel(15,340,'จุดยอด(h,k)');
          setcolor(68);  line(225,323,275,323);
          setcolor(79);  writexypixel(32,305,'c');
                         writexypixel(29,305,'c');
          setcolor(44);  line(250-pxc,246,320,246);
                         line(320,246,276,330);
                         line(225,255,234,255);
                         line(234,255,234,246);
          setcolor(40);line(278,242,278,250);
                         line(293,289,300,293);

     yjjborder(390,70,440,100,82,83); writexypixel(50,75,'PgUp');
     yjjborder(40,410,100,440,82,83); writexypixel(7,413,'PgDn');
end;
Procedure page3;
var pxy,bpxya : integer;
begin
          setfillstyle(1,0);bar(20,65,450,465);
          setcolor(11); line(50,150,260,150);
                        line(100,100,100,300);
          setcolor(25); line(50,170,260,170);
                        line(80,100,80,300);
          setcolor(91);
          bpxya := -83;
          pxc   := 10;
          pxh   := 50;
          pxk   := 30;
          pxya  := bpxya;
          pxc   := pxc;
          pxxa  := round((pxya*pxya)/(4*pxc));
          For pxY := bpxya to (-1)*bpxya do
          begin
               pxx := round((pxya*pxya)/(4*pxc));
               line(30+pxxa+pxh,200-pxya-pxk,30+pxx+pxh,200-pxy-pxk);
               pxxa := pxx;
               pxya := pxy;
          end;
          setcolor(102); writexypixel(30,110,'     2      ');
          setcolor(102); writexypixel(30,120,'(y-k) = 4c(x-h) โดยที่ c < 0 ');
          setcolor(102); writexypixel(28,180,'จะสังเกตได้ว่าค่า c เป็นลบ จะทำให้');
          setcolor(102); writexypixel(28,210,'กราฟมีลักษณะเป็น');
          setcolor(43);  writexypixel(28,210,'               กราฟเปิดทางขวา');
          setcolor(60);  writexypixel(5,320,'สมการมาตรฐาน คือ ');
          setcolor(94);  writexypixel(5,315,'                       2');
          setcolor(94);  writexypixel(5,320,'                  (y-k) = 4c(x-h)');
          setcolor(60);  writexypixel(5,350,'สมการทั่วไป คือ  ');
          setcolor(94);  writexypixel(5,345,'               2');
          setcolor(94);  writexypixel(5,350,'              y + Ay + Bx + c = 0');
          setcolor(94);  writexypixel(5,380,'              โดยที่ A,B,C เป็นค่าคงตัว และ B = 0');
          setcolor(94);  writexypixel(5,380,'                                         /');

     yjjborder(40,410,100,440,82,83); writexypixel(7,413,'PgDn');
     yjjborder(390,70,440,100,82,83); writexypixel(50,75,'PgUp');
end;

Procedure page4;
var pyx,bpyxa : integer;
begin
          setfillstyle(1,0);bar(20,65,450,465);
          setcolor(69);  writexypixel(5,100,'สูตรที่น่าสนใจ');
          setcolor(53);  writexypixel(5,130,'สมการไดเรกตริก (Directric) : y = -C');
          setcolor(71);  writexypixel(5,130,'                            y = -C');
          setcolor(53);  writexypixel(5,160,'ความยาวลาตัสเรกตัม (Latusrectum) =   4c  ');
          setcolor(71);  writexypixel(5,160,'                                   4c  ');
                         line(312,167,312,177);
                         line(342,167,342,177);
          setcolor(95);  writexypixel(5,190,'แกนสมมาตร x = h');
          setcolor(95);  writexypixel(5,220,'จุดโฟกัส    = (h,k+c)');
          setcolor(43);  writexypixel(5,250,'ลักษณะกราฟจะเป็น กราฟ เปิดขวา  เมื่อ C > 0');
          setcolor(43);  writexypixel(5,280,'ลักษณะกราฟจะเป็น กราฟ เปิดซ้าย  เมื่อ C < 0');

     yjjborder(390,70,440,100,82,83); writexypixel(50,75,'PgUp');
end;

Begin
     setfillstyle(1,0);
     setcolor(0);
     bar(480,370,615,465);
     yjjborder(475,375,515,400,6,8);setcolor(51); writexypixel(60,375,'Esc   = ออก');
     yjjborder(475,405,515,430,6,8);setcolor(51); writexypixel(60,405,'PgUp  = เลือกหน้าขึ้น');
     yjjborder(475,435,515,460,6,8);setcolor(51); writexypixel(60,435,'PgDn  = เลือกหน้าลง');
     pxdatachoice := 1;
     repeat
           if pxch = #81 then if pxdatachoice <> 4 then inc(pxdatachoice);
           if pxch = #73 then if pxdatachoice <> 1 then dec(pxdatachoice);
           case pxdatachoice of
                1 : page1;
                2 : page2;
                3 : page3;
                4 : page4;
           end; {case}
           pxch := readkey; if pxch = #0 then pxch := readkey;
     until pxch = #27;
     yjjboard(418,408,472,442,0,0,0);
End;

Procedure pxMenu_Input;
begin
     SlideMenu(82);
     yjjborder(487,78,615,120,23,28);
     setcolor(11);settextstyle(2,0,4);outtextxy(500,86,'      2   ');
                  settextstyle(2,0,5);outtextxy(500,94,'(y-k) = 4c(x-h)');
     ikey := #0;

     if ikey <> #27 then
     begin
          repeat
                yjjboard(540,160,585,190,67,69,0);
                setcolor(10); writexypixel(62,165,'c = ');
                yjjborder(540,200,585,230,67,69);
                setcolor(59); writexypixel(62,205,'h = '+'    0');
                yjjborder(540,240,585,270,67,69);
                setcolor(39); writexypixel(62,245,'k = '+'    0');
                setcolor(10);
                writexypixel(63,395,'-61 < c < 60');

                              valinput(pxc,2,68,165,85);
          until (pxc <> 0)and(pxc <= 60)and(pxc >= -60) or (ikey = #27);
     end;

     pxh := 0;
     pxk := 0;
     case pxc of
          1,-1   : bpxxa := -20;
          2,-2   : bpxxa := -28;
          3,-3   : bpxxa := -32;
          4,-4   : bpxxa := -37;
          5,-5   : bpxxa := -41;
          6,-6   : bpxxa := -45;
          7,-7   : bpxxa := -50;
          8,-8   : bpxxa := -52;
          9,-9   : bpxxa := -55;
          10,-10 : bpxxa := -57;
          11..13,-13..-11   : bpxxa := -59;
          14..16,-16..-14   : bpxxa := -63;
          17..20,-20..-17   : bpxxa := -67;
          21..25,-25..-21   : bpxxa := -71;
          26..30,-31..-26   : bpxxa := -75;
          31..35,-35..-31   : bpxxa := -79;
          36..40,-40..-36   : bpxxa := -83;
          41..50,-50..-41   : bpxxa := -87;
          51..60,-60..-51   : bpxxa := -91;
          61..80,-80..-61   : bpxxa := -95;
          81..99,-99..-81   : bpxxa := -100;

     end; {---CASE---}
     if ikey <> #27 then
     begin
          pxya := bpxxa;
          pxxa := round((pxya*pxya)/(4*pxc));
          setcolor(10);
          For pxY := bpxxa to (-1)*bpxxa+1 do
          begin
               pxx := round((pxya*pxya)/(4*pxc));
               setcolor(87);
               yjjdelay(50);
               line(230+pxxa+pxh,265-pxya-pxk,230+pxx+pxh,265-pxy-pxk);
               pxxa := pxx;
               pxya := pxy;
          end;
          pxDirectric(pxh,pxk,pxc,bpxxa,37);
    end; { Check Esc }

    if ikey <> #27 then
    begin
         SlideMenu(70);
         str(pxc,Spxc);
         str(pxh,Spxh);
         str(pxk,Spxk);
         str(pxh-pxc,Sdirec);
         str(pxh+pxc,Sfocus);
         str(abs(4*pxc),Slatus);


    setcolor(102);writexypixel(60,80,'c');
         setcolor(44);writexypixel(65,80,'= '+Spxc);
    setcolor(102);writexypixel(60,110,'h');
         setcolor(44);writexypixel(65,110,'= '+Spxh);
    setcolor(102);writexypixel(60,140,'k');
         setcolor(44);writexypixel(65,140,'= '+Spxk);

    setcolor(102);writexypixel(60,170,'สมการ Directric');
         setcolor(44);writexypixel(60,190,':  x = '+Sdirec);
    setcolor(102);writexypixel(60,220,'จุดโฟกัส (Focus)');
         setcolor(44);writexypixel(60,240,'=  ('+Sfocus+','+Spxk+')');
    setcolor(102);writexypixel(60,270,'ความยาวLatusrectum');
         setcolor(44);writexypixel(60,290,'=  '+Slatus);
    if (ikey <> #27) then
    begin
         ikey := readkey;
         if ikey = #0 then ikey := readkey;
    end;
    if ikey <> #27 then
     begin
          SlideMenu(82);
          yjjborder(487,78,615,120,23,28);
          setcolor(11);settextstyle(2,0,4);outtextxy(500,86,'      2   ');
                       settextstyle(2,0,5);outtextxy(500,94,'(y-k) = 4c(x-h)');
          yjjboard(540,160,585,190,67,69,0);
          setcolor(10); writexypixel(62,165,'c =    '+spxc);
                   setcolor(59);
                   writexypixel(63,380,'-61 < h < 60');
                   setcolor(39);
                   writexypixel(63,410,'-61 < k < 60');

          repeat
                yjjboard(540,200,585,230,67,69,0);
                setcolor(59); writexypixel(62,205,'h = ');
                              valinput(pxH,2,68,205,86);
          until(pxh <= 60)and(pxh >= -60);
     end;

     if ikey <> #27 then
        repeat
              yjjboard(540,240,585,270,67,69,0);
              setcolor(39); writexypixel(62,245,'k = ');
                            valinput(pxK,2,68,245,87);
        until(pxk <= 60)and(pxk >= -60);
     if ikey <> #27 then
     begin
          setfillstyle(1,0);bar(20,65,450,465);
          Draw_Quadant(230,265,30,185);
          Draw_Quadant_hk(pxh,pxk,25);
          pxya := bpxxa;
          pxxa := round((pxya*pxya)/(4*pxc));
          setcolor(10);
          For pxY := bpxxa to (-1)*bpxxa+1 do
          begin
               pxx := round((pxya*pxya)/(4*pxc));
               setcolor(87);
               yjjdelay(50);
               line(230+pxxa+pxh,265-pxya-pxk,230+pxx+pxh,265-pxy-pxk);
               pxxa := pxx;
               pxya := pxy;
          end;
          pxDirectric(pxh,pxk,pxc,bpxxa,37);
    end; { Check Esc }

    if ikey <> #27 then
    begin
         SlideMenu(70);
         str(pxc,Spxc);
         str(pxh,Spxh);
         str(pxk,Spxk);
         str(pxh-pxc,Sdirec);
         str(pxh+pxc,Sfocus);
         str(abs(4*pxc),Slatus);

    setcolor(102);writexypixel(60,80,'c');
         setcolor(44);writexypixel(65,80,'= '+Spxc);
    setcolor(102);writexypixel(60,110,'h');
         setcolor(44);writexypixel(65,110,'= '+Spxh);
    setcolor(102);writexypixel(60,140,'k');
         setcolor(44);writexypixel(65,140,'= '+Spxk);

    setcolor(102);writexypixel(60,170,'สมการ Directric');
         setcolor(44);writexypixel(60,190,':  x = '+Sdirec);
    setcolor(102);writexypixel(60,220,'จุดโฟกัส (Focus)');
         setcolor(44);writexypixel(60,240,'=  ('+Sfocus+','+Spxk+')');
    setcolor(102);writexypixel(60,270,'ความยาวLatusrectum');
         setcolor(44);writexypixel(60,290,'=  '+Slatus);
    end;
    if ikey <> #27 then pause;
    end;
 end;
Procedure Creating_GraphParaX;
var pxx  : integer;
Begin
     setfillstyle(1,0);bar(20,65,448,465);
     Draw_Quadant(230,265,30,185);
     pxMenu_Input;
     if ikey <> #27 then
     begin
          setfillstyle(1,0);bar(25,61,622,470);
          yjjborder(319,61,321,469,6,7);
          yjjborder(19,370,628,370,7,6);
          draw_quadant(165,215,30,145);
          draw_quadant(473,215,30,145);
          Draw_Quadant_hk2(pxh,pxk,25);
          pxya := bpxxa;
          pxxa := round((pxya*pxya)/(4*pxc));
          setcolor(10);
          For pxY := bpxxa to (-1)*bpxxa+1 do
          begin
               pxx := round((pxya*pxya)/(4*pxc));
               setcolor(87);
               yjjdelay(50);
               line(165+pxxa+pxh,215-pxya-pxk,165+pxx+pxh,215-pxy-pxk);
               pxxa := pxx;
               pxya := pxy;
          end;
          pxDirectric2(165,pxh,pxk,pxc,bpxxa,37);

    setcolor(102);writexypixel(5,375,'c');
         setcolor(44);writexypixel(10,375,'= '+Spxc);
    setcolor(102);writexypixel(17,375,'h');
         setcolor(44);writexypixel(21,375,'= '+Spxh);
    setcolor(102);writexypixel(28,375,'k');
         setcolor(44);writexypixel(33,375,'= '+Spxk);

    setcolor(102);writexypixel(5,395,'สมการ Directric');
         setcolor(44);writexypixel(25,395,':  x = '+Sdirec);
    setcolor(102);writexypixel(5,415,'จุดโฟกัส (Focus)');
         setcolor(44);writexypixel(25,415,'=  ('+Spxh+','+Sfocus+')');
    setcolor(102);writexypixel(5,435,'ความยาวLatusrectum');
         setcolor(44);writexypixel(25,435,'=  '+Slatus);


     end;

     if ikey <> #27 then
     begin
          pxya := bpxxa;
          pxxa := round((pxya*pxya)/(4*pxc));
          setcolor(10);
          For pxY := bpxxa to (-1)*bpxxa+1 do
          begin
               pxx := round((pxya*pxya)/(4*pxc));
               setcolor(87);
               yjjdelay(50);
               line(473+pxxa,215-pxya,473+pxx,215-pxy);
               pxxa := pxx;
               pxya := pxy;
          end;
          pxDirectric2(473,0,0,pxc,bpxxa,37);

         pxh := 0;
         pxk := 0;
         str(pxc,Spxc);
         str(pxh,Spxh);
         str(pxk,Spxk);
         str(pxk-pxc,Sdirec);
         str(pxc+pxk,sfocus);
         str(abs(4*pxc),Slatus);

    setcolor(102);writexypixel(42,375,'c');
         setcolor(44);writexypixel(47,375,'= '+Spxc);
    setcolor(102);writexypixel(54,375,'h');
         setcolor(44);writexypixel(59,375,'= '+Spxh);
    setcolor(102);writexypixel(66,375,'k');
         setcolor(44);writexypixel(71,375,'= '+Spxk);

    setcolor(102);writexypixel(42,395,'สมการ Directric');
         setcolor(44);writexypixel(62,395,':  x = '+Sdirec);
    setcolor(102);writexypixel(42,415,'จุดโฟกัส (Focus)');
         setcolor(44);writexypixel(62,415,'=  ('+Spxh+','+Sfocus+')');
    setcolor(102);writexypixel(42,435,'ความยาวLatusrectum');
         setcolor(44);writexypixel(62,435,'=  '+Slatus);
          pause;
    end; { Check Esc }
end;


Procedure ParaX_SubMenu;
var choice : byte;
    chpx   : char;
begin
Repeat
     cleardevice;
     initrgb;
     fadein(0);
       Menu_Parax_border;
     fadeout(100);
     Sim_CreatingGraphParaX;
     Sim_ExitParaX;
     writetextmenu_paraX;
     choice := 1;
     chpx := #0;
     repeat
{down}      if chpx = #80 then
               begin
                    if choice = 3 then choice := 0;
                    inc(choice);
               end;
{up}        if chpx = #72 then
               begin
                    if choice = 1 then choice := 4;
                    dec(choice);
               end;
               case choice of
                1 :  begin
                          if chpx=#72 then Sim_CreatingGraphParaX;
                          if chpx=#80 then Sim_ExitParaX;
                          vab_DataParaX;;
                     end;
                2 :  begin
                          if chpx=#72 then Sim_ExitParaX;
                          if chpx=#80 then Sim_DataParaX;
                          vab_CreatingGraphParaX;
                     end;
                3 :  begin
                          if chpx=#72 then Sim_DataParaX;
                          if chpx=#80 then Sim_CreatingGraphParaX;
                          vab_ExitParaX;
                     end;

                end;{case}
                repeat
                      chpx := readkey;
                      if chpx = #0 then chpx := readkey;
                until chpx in [#13,#72,#80,#59];
               if chpx = #59 then help;
     until chpx in [#13];
     Case Choice of
         1 : data_ParaX;
         2 : Creating_GraphParaX;
     end;
Until (choice = 3) or ( chpx in [#27]);
end;

begin
     uses_svga256_color;
     initrgb;
     start_delay(real_delay2);
     loadfont('normal.fon');
     ParaX_SubMenu;
end.