{$M 16384,0,130720}
Program Graph_Parabola_Yaxis;
uses crt,dos,kvga,kfade,graph,yjjsvga;
Var pych  :  char;
    pyxa,pyc,pyx,pyy,pyya,bpyxa,pyh,pyk,pydatachoice : integer;
    real_delay,real_delay2                           : real;
    Spyc,Spyh,Spyk,Sdirec,Sfocus,Slatus              : string;

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

Procedure Menu_ParaY_Border;
begin
     yjjborder(1,1,640,50,17,26);
        yjjborder(621,51,640,480,17,26);
        yjjborder(450,51,469,480,17,26);
        yjjborder(1,51,20,480,17,26);
        setcolor(14);  writexypixel(63,350,'F1 = Help');
        setcolor(51); writexypixel(63,380,chr(135));
                      writexypixel(65,383,'ขึ้น');
        setcolor(47); writexypixel(69,383,chr(136));
                      writexypixel(71,383,'ลง');
        setcolor(100); writexypixel(63,408,'เลือกเมนู');
        setcolor(57); writexypixel(61,443,'Enter เพื่อเข้าเมนู');
        setcolor(15);
        settextstyle(2,0,10);
        outtextxy(55,225,'Parabola Y axis');
        setcolor(45);
        outtextxy(57,225,'Parabola Y axis');
        outtextxy(58,225,'Parabola Y axis');
        outtextxy(59,225,'Parabola Y axis');
     yjjborder(1,51,640,480,17,26);
     setcolor(82);
end;

Procedure writetextmenu;
begin
     settextstyle(1,0,2); setcolor(52);outtextxy(26,13,'Parabola   axis');
                          setcolor(37);outtextxy(120,13,'Y');
                          setcolor(10);outtextxy(480,13,'Conic Section');
    setcolor(79);writexypixel(25,15,'พาราโบลา แกน Y');
end;

Procedure Sim_DataParaY;
begin
     yjjboard(480,80,610,118,20,25,57);
          setcolor(80); writexypixel(62,87,'เนื้อหาพาราโบลา');
end;

Procedure Sim_CreatingGraphParaY;
begin
     yjjboard(480,125,610,163,20,25,57);
          setcolor(80); writexypixel(64,132,'สร้างกราฟ');
end;

Procedure Sim_ExitParaY;
begin
     yjjboard(480,170,610,208,20,25,57);
          setcolor(80); writexypixel(61,177,'กลับสู่ Main Menu');
end;

Procedure vab_DataParaY;
begin
     yjjboard(480,80,610,118,23,28,99);
          setcolor(9); writexypixel(62,87,'เนื้อหาพาราโบลา');
end;

Procedure vab_CreatingGraphParaY;
begin
     yjjboard(480,125,610,163,23,28,99);
          setcolor(9); writexypixel(64,132,'สร้างกราฟ');
end;

Procedure vab_ExitParaY;
begin
     yjjboard(480,170,610,208,23,28,99);
          setcolor(9); writexypixel(61,177,'กลับสู่ Main Menu');
end;

Procedure pyDirectric(h,k,c,beginX,color : integer);
var i : integer;
begin
     i := 0;
     setcolor(color);
     repeat
           inc(i);
           line(230+h+beginX,265-k+c,230+h+beginx+i,265-k+c);
           yjjdelay(10);
     until i = beginX*(-2)+3;
end;

Procedure pyDirectric2(x1,h,k,c,beginX,color : integer);
var i : integer;
begin
     i := 0;
     setcolor(color);
     repeat
           inc(i);
           line(x1+h+beginx,215-k+c,x1+h+beginx+i,215-k+c);
           yjjdelay(10);
     until i = beginX*(-2);
end;

Procedure Data_ParaY;
Procedure page1;
var pyx,bpyxa : integer;
begin
     setfillstyle(1,0);bar(20,65,450,465);
     yjjborder(40,70,435,150,100,101);
     setcolor(0);  writexypixel(63,350,'F1 = Help');
     setcolor(53); writexypixel(8,80,'      พาราโบลา  คือ เซตของจุดทุกจุดบนระนาบซึ่งทำให้');
     setcolor(74); writexypixel(8,100,'นิยาม');
     setcolor(53); writexypixel(8,100,'      ระยะทางที่จุดเหล่านี้อยู่ห่างจากเส้นคงที่เส้นหนึ่งเท่า');
     setcolor(53); writexypixel(8,120,'      กับระยะทางที่จุดเหล่านี้อยู่ห่างจากจุดคงที่จุดหนึ่ง');
     setcolor(53); writexypixel(5,160,'สมการของพาราโบลาแกน Y ที่จุดศูนย์กลางที่จุด (0,0) คือ');
     yjjborder(150,188,350,223,83,84);
     setcolor(62); writexypixel(24,190,'    2 ');
     setcolor(62); writexypixel(24,200,'   X  = 4CY  ');

     setcolor(25); line(250,235,250,425);
                   line(155,330,345,330);
                   setcolor(99);
                   writexypixel(44,318,'X');writexypixel(30,220,'Y');

          setcolor(91);
          bpyxa := -50;
          pyc   := 10;
          pyh   := 0;
          pyk   := 0;
          pyxa  := bpyxa;
          pyc   := pyc;
          pyya  := round((pyxa*pyxa)/(4*pyc));
          For pyX := bpyxa to (-1)*bpyxa+1 do
          begin
               pyy := round((pyxa*pyxa)/(4*pyc));
               line(250+pyxa+pyh,330-pyya-pyk,250+pyx+pyh,330-pyy-pyk);
               pyxa := pyx;
               pyya := pyy;
           end;
     setcolor(82);line(250-50,330+pyc,250+50,330+pyc);
     setcolor(53);writexypixel(5,350,'เส้นไดเรกตริก (Directric)');
     setcolor(42);line(250,330,280,370);
     setcolor(37);writexypixel(35,370,'จุดยอด');
     setcolor(60);line(225,363,245,345);
     yjjborder(40,410,100,440,82,83); writexypixel(7,413,'PgDn');
end;
Procedure page2;
var pyx,bpyxa : integer;
begin
          setfillstyle(1,0);bar(20,65,450,465);
          setcolor(68); writexypixel(4,70,'เส้นคงที่ เรียกว่า ไดเรกตริกซ์ (Directic Line)');
                        writexypixel(4,90,'จุดคงที่  เรียกว่า โฟกัสพาราโบลา (Focus)');
          setcolor(73); writexypixel(4,120,'จุดที่พาราโบลาตัดแกนของพาราโบลา เรียกว่า จุดยอดของพาราโบลา');
                        writexypixel(4,140,'ส่วนของเส้นตรงที่ผานโฟกัสและมีจุดปลายทั้งสองอยู่บนพาราโบลา และ');
                        writexypixel(4,160,'ตั้งฉากกับแกน Y เรียกว่า ลาตัสเรกตัม');

          setcolor(25); line(250,220,250,430);
                        line(100,330,400,330);
          setcolor(91);
          bpyxa := -100;
          pyc   := 25;
          pyh   := 0;
          pyk   := 0;
          pyxa  := bpyxa;
          pyc   := pyc;
          pyya  := round((pyxa*pyxa)/(4*pyc));
          For pyX := bpyxa to (-1)*bpyxa+1 do
          begin
               pyy := round((pyxa*pyxa)/(4*pyc));
               line(250+pyxa+pyh,330-pyya-pyk,250+pyx+pyh,330-pyy-pyk);
               pyxa := pyx;
               pyya := pyy;
          end;
          setcolor(82);  line(150-50,330+pyc,350+50,330+pyc);
          setcolor(100); line(250-50,330-pyc,250+50,330-pyc);
          setcolor(43);  writexypixel(23,293,'A');
                         writexypixel(39,293,'B');
          setcolor(71);  writexypixel(28,292,'|');
          setcolor(71);  writexypixel(34,292,'|');
          setcolor(54);  line(242,330,242,354);
                         line(242,330,242,306);
          setcolor(68);  writexypixel(29,303,'c');
                         writexypixel(29,328,'c');
          setcolor(60);  line(250,355,225,380);
          setcolor(53);  writexypixel(5,370,'เส้นไดเรกตริก (Directric)');
          setcolor(42);  line(250,330,280,370);
          setcolor(37);  writexypixel(35,366,'จุดยอด(h,k)');
          setcolor(45);  line(250,305,330,265);
                         line(330,265,330,355);
                         line(330,348,337,348);
                         line(337,348,337,355);
          setcolor(15);  writexypixel(36,271,'\');
                         line(325,310,335,310);
          setcolor(53);  writexypixel(6,270,'ความยาว Latusrectum');
          setcolor(82);  line(200,285,218,305);
     yjjborder(390,70,440,100,82,83); writexypixel(50,75,'PgUp');
     yjjborder(40,410,100,440,82,83); writexypixel(7,413,'PgDn');
end;
Procedure page3;
var pyx,bpyxa : integer;
begin
          setfillstyle(1,0);bar(20,65,450,465);
          setcolor(11); line(50,150,300,150);
                        line(100,100,100,300);
          setcolor(25); line(50,120,300,120);
                        line(150,100,150,300);
          setcolor(91);
          bpyxa := -85;
          pyc   := -10;
          pyh   := 50;
          pyk   := 30;
          pyxa  := bpyxa;
          pyc   := pyc;
          pyya  := round((pyxa*pyxa)/(4*pyc));
          For pyX := bpyxa to (-1)*bpyxa do
          begin
               pyy := round((pyxa*pyxa)/(4*pyc));
               line(100+pyxa+pyh,150-pyya-pyk,100+pyx+pyh,150-pyy-pyk);
               pyxa := pyx;
               pyya := pyy;
          end;
          setcolor(102); writexypixel(40,100,'     2      ');
          setcolor(102); writexypixel(40,110,'(x-h) = 4c(y-k)');
          setcolor(102); writexypixel(40,140,'โดยที่ c < 0 ');
          setcolor(102); writexypixel(30,170,'จะสังเกตได้ว่าค่า c เป็นลบ จะทำ');
          setcolor(102); writexypixel(30,200,'ให้กราฟมีลักษณะเป็น');
          setcolor(43);  writexypixel(30,200,'                 กราฟคว่ำ');
          setcolor(60);  writexypixel(5,310,'สมการมาตรฐาน คือ ');
          setcolor(94);  writexypixel(5,305,'                       2');
          setcolor(94);  writexypixel(5,310,'                  (x-h) = 4c(y-k)');
          setcolor(60);  writexypixel(5,340,'สมการทั่วไป คือ  ');
          setcolor(94);  writexypixel(5,335,'               2');
          setcolor(94);  writexypixel(5,340,'              x + Ax + By + c = 0');
          setcolor(94);  writexypixel(5,370,'              โดยที่ A,B,C เป็นค่าคงตัว และ B = 0');
          setcolor(94);  writexypixel(5,370,'                                         /');

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
          setcolor(95);  writexypixel(5,220,'จุดโฟกัส    = (h+c,k)');
          setcolor(43);  writexypixel(5,250,'ลักษณะกราฟจะเป็น กราฟ หงาย เมื่อ C > 0');
          setcolor(43);  writexypixel(5,280,'ลักษณะกราฟจะเป็น กราฟ คว่ำ  เมื่อ C < 0');

     yjjborder(390,70,440,100,82,83); writexypixel(50,75,'PgUp');
end;

Begin
     setfillstyle(1,0);
     setcolor(0);
     bar(480,370,615,465);

     yjjborder(475,375,515,400,6,8);setcolor(51); writexypixel(60,375,'Esc   = ออก');
     yjjborder(475,405,515,430,6,8);setcolor(51); writexypixel(60,405,'PgUp  = เลือกหน้าขึ้น');
     yjjborder(475,435,515,460,6,8);setcolor(51); writexypixel(60,435,'PgDn  = เลือกหน้าลง');
     pydatachoice := 1;
     repeat
           if pych = #81 then if pydatachoice <> 4 then inc(pydatachoice);
           if pych = #73 then if pydatachoice <> 1 then dec(pydatachoice);
           case pydatachoice of
                1 : page1;
                2 : page2;
                3 : page3;
                4 : page4;
           end; {case}
           pych := readkey; if pych = #0 then pych := readkey;
     until pych = #27;
     yjjboard(418,408,472,442,0,0,0);
End;


Procedure pyMenu_Input;

begin
     SlideMenu(82);
     yjjborder(487,78,615,120,23,28);
     setcolor(11);settextstyle(2,0,4);outtextxy(500,86,'      2   ');
                  settextstyle(2,0,5);outtextxy(500,94,'(x-h) = 4c(y-k)');
     ikey := #0;

     if ikey <> #27 then
     begin
                   yjjborder(540,200,585,230,67,69);
                   setcolor(59); writexypixel(62,205,'h = '+'    0');
                   yjjborder(540,240,585,270,67,69);
                   setcolor(39); writexypixel(62,245,'k = '+'    0');
                   setcolor(10);
                   writexypixel(63,395,'-61 < c < 60');
          repeat
                   yjjboard(540,160,585,190,67,69,0);
                   setcolor(10); writexypixel(62,165,'c = ');
                                 valinput(pyc,2,68,165,85);
          until (pyc <> 0)and(pyc <= 60)and(pyc >= -60) or (ikey = #27);
     end;

  if ikey <> #27 then
   begin
     pyh := 0;
     pyk := 0;
     {graph 1}
     case pyc of
          1,-1   : bpyxa := -20;
          2,-2   : bpyxa := -28;
          3,-3   : bpyxa := -32;
          4,-4   : bpyxa := -37;
          5,-5   : bpyxa := -41;
          6,-6   : bpyxa := -45;
          7,-7   : bpyxa := -50;
          8,-8   : bpyxa := -52;
          9,-9   : bpyxa := -55;
          10,-10 : bpyxa := -57;
          11..13,-13..-11   : bpyxa := -59;
          14..16,-16..-14   : bpyxa := -63;
          17..20,-20..-17   : bpyxa := -67;
          21..25,-25..-21   : bpyxa := -71;
          26..30,-31..-26   : bpyxa := -75;
          31..35,-35..-31   : bpyxa := -79;
          36..40,-40..-36   : bpyxa := -83;
          41..50,-50..-41   : bpyxa := -87;
          51..60,-60..-51   : bpyxa := -91;
          61..80,-80..-61   : bpyxa := -95;
          81..99,-99..-81   : bpyxa := -100;
     end; {---CASE---}
   end;

    if ikey <> #27 then
     begin
          pyxa := bpyxa;
          pyya := round((pyxa*pyxa)/(4*pyc));
          setcolor(10);
          For pyX := bpyxa to (-1)*bpyxa+1 do
          begin
               pyy := round((pyxa*pyxa)/(4*pyc));
               setcolor(10);
               yjjdelay(50);
               line(230+pyxa+pyh,265-pyya-pyk,230+pyx+pyh,265-pyy-pyk);
               pyxa := pyx;
               pyya := pyy;
          end;
        pyDirectric(pyh,pyk,pyc,bpyxa,63);
     end;

    if ikey <> #27 then
    begin
         SlideMenu(70);
         str(pyc,Spyc);
         str(pyh,Spyh);
         str(pyk,Spyk);
         str(pyk-pyc,Sdirec);
         str(pyc+pyk,sfocus);
         str(abs(4*pyc),Slatus);

    setcolor(102);writexypixel(60,80,'c');
         setcolor(44);writexypixel(65,80,'= '+Spyc);
    setcolor(102);writexypixel(60,110,'h');
         setcolor(44);writexypixel(65,110,'= '+Spyh);
    setcolor(102);writexypixel(60,140,'k');
         setcolor(44);writexypixel(65,140,'= '+Spyk);

    setcolor(102);writexypixel(60,170,'สมการ Directric');
         setcolor(44);writexypixel(60,190,':  y = '+Sdirec);
    setcolor(102);writexypixel(60,220,'จุดโฟกัส (Focus)');
         setcolor(44);writexypixel(60,240,'=  ('+Spyh+','+Sfocus+')');
    setcolor(102);writexypixel(60,270,'ความยาวLatusrectum');
         setcolor(44);writexypixel(60,290,'=  '+Slatus);
  end;
{graph h,k}
         if ikey <> #27 then
         begin
              ikey := readkey;
              if ikey = #0 then ikey := readkey;
         end;
             if ikey <> #27 then
                begin
                   SlideMenu(70);
                   yjjborder(487,78,615,120,23,28);
                   setcolor(11);settextstyle(2,0,4);outtextxy(500,86,'      2   ');
                   settextstyle(2,0,5);outtextxy(500,94,'(x-h) = 4c(y-k)');
                   yjjboard(540,160,585,190,67,69,0);
                   setcolor(10); writexypixel(62,165,'c =    '+spyc);
                   setcolor(59);
                   writexypixel(63,380,'-61 < h < 60');
                   setcolor(39);
                   writexypixel(63,410,'-61 < k < 60');
                   repeat
                         yjjboard(540,200,585,230,67,69,0);
                         setcolor(59); writexypixel(62,205,'h = ');
                         valinput(pyH,2,68,205,86);
                   until(pyh <= 60)and(pyh >= -60);
                end;

             if ikey <> #27 then
                repeat
                    yjjboard(540,240,585,270,67,69,0);
                    setcolor(39); writexypixel(62,245,'k = ');
                    valinput(pyK,2,68,245,87);
                until(pyk <= 60)and(pyk >= -60);

             if ikey <> #27 then
                begin
                {write graph h,k}
                       setfillstyle(1,0);bar(20,65,450,465);
                       Draw_Quadant(230,265,30,185);
                       Draw_Quadant_hk(pyh,pyk,25);
                       pyxa := bpyxa;
                       pyya := round((pyxa*pyxa)/(4*pyc));
                       setcolor(10);
                       For pyX := bpyxa to (-1)*bpyxa+1 do
                       begin
                            pyy := round((pyxa*pyxa)/(4*pyc));
                            setcolor(10);
                            yjjdelay(50);
                            line(230+pyxa+pyh,265-pyya-pyk,230+pyx+pyh,265-pyy-pyk);
                            pyxa := pyx;
                            pyya := pyy;
                       end;
                       pyDirectric(pyh,pyk,pyc,bpyxa,63);
                end;  {Check Esc }

             if ikey <> #27 then
                begin
                     SlideMenu(70);
                     str(pyc,Spyc);
                     str(pyh,Spyh);
                     str(pyk,Spyk);
                     str(pyk-pyc,Sdirec);
                     str(pyc+pyk,sfocus);
                     str(abs(4*pyc),Slatus);

                 setcolor(102);writexypixel(60,80,'c');
                     setcolor(44);writexypixel(65,80,'= '+Spyc);
                 setcolor(102);writexypixel(60,110,'h');
                     setcolor(44);writexypixel(65,110,'= '+Spyh);
                 setcolor(102);writexypixel(60,140,'k');
                     setcolor(44);writexypixel(65,140,'= '+Spyk);

                 setcolor(102);writexypixel(60,170,'สมการ Directric');
                 setcolor(44);writexypixel(60,190,':  y = '+Sdirec);
                 setcolor(102);writexypixel(60,220,'จุดโฟกัส (Focus)');
                 setcolor(44);writexypixel(60,240,'=  ('+Spyh+','+Sfocus+')');
                 setcolor(102);writexypixel(60,270,'ความยาวLatusrectum');
                 setcolor(44);writexypixel(60,290,'=  '+Slatus);
             end;
    if ikey <> #27 then pause;
end;

Procedure Creating_GraphParaY;
var pyx : integer;
Begin
     setfillstyle(1,0);bar(20,65,448,465);
     Draw_Quadant(230,265,30,185);
     pyMenu_Input;
     if ikey <> #27 then
     begin
          setfillstyle(1,0);bar(25,61,622,470);
          yjjborder(319,61,321,469,6,7);
          yjjborder(19,370,628,370,7,6);
          Draw_quadant(165,215,30,145);
          Draw_Quadant(473,215,30,145);
          if ikey <> #27 then
          begin
               draw_quadant_hk2(pyh,pyk,25);
               pyxa := bpyxa;
               pyya := round((pyxa*pyxa)/(4*pyc));
               setcolor(10);
               For pyX := bpyxa to (-1)*bpyxa+1 do
               begin
                    pyy := round((pyxa*pyxa)/(4*pyc));
                    setcolor(10);
                    yjjdelay(50);
                    line(165+pyxa+pyh,215-pyya-pyk,165+pyx+pyh,215-pyy-pyk);
                    pyxa := pyx;
                    pyya := pyy;
               end;
               pyDirectric2(165,pyh,pyk,pyc,bpyxa,63);

    setcolor(102);writexypixel(5,375,'c');
         setcolor(44);writexypixel(10,375,'= '+Spyc);
    setcolor(102);writexypixel(17,375,'h');
         setcolor(44);writexypixel(21,375,'= '+Spyh);
    setcolor(102);writexypixel(28,375,'k');
         setcolor(44);writexypixel(33,375,'= '+Spyk);

    setcolor(102);writexypixel(5,395,'สมการ Directric');
         setcolor(44);writexypixel(25,395,':  y = '+Sdirec);
    setcolor(102);writexypixel(5,415,'จุดโฟกัส (Focus)');
         setcolor(44);writexypixel(25,415,'=  ('+Spyh+','+Sfocus+')');
    setcolor(102);writexypixel(5,435,'ความยาวLatusrectum');
         setcolor(44);writexypixel(25,435,'=  '+Slatus);

          end;

         if ikey <> #27 then
         begin
              pyxa := bpyxa;
              pyya := round((pyxa*pyxa)/(4*pyc));
              setcolor(10);
              For pyX := bpyxa to (-1)*bpyxa+1 do
              begin
                   pyy := round((pyxa*pyxa)/(4*pyc));
                   setcolor(10);
                   yjjdelay(50);
                   line(473+pyxa,215-pyya,473+pyx,215-pyy);
                   pyxa := pyx;
                   pyya := pyy;
              end;
              pyDirectric2(473,0,0,pyc,bpyxa,63);
         pyh := 0;
         pyk := 0;
         str(pyc,Spyc);
         str(pyh,Spyh);
         str(pyk,Spyk);
         str(pyk-pyc,Sdirec);
         str(pyc+pyk,sfocus);
         str(abs(4*pyc),Slatus);

    setcolor(102);writexypixel(42,375,'c');
         setcolor(44);writexypixel(47,375,'= '+Spyc);
    setcolor(102);writexypixel(54,375,'h');
         setcolor(44);writexypixel(59,375,'= '+Spyh);
    setcolor(102);writexypixel(66,375,'k');
         setcolor(44);writexypixel(71,375,'= '+Spyk);

    setcolor(102);writexypixel(42,395,'สมการ Directric');
         setcolor(44);writexypixel(62,395,':  y = '+Sdirec);
    setcolor(102);writexypixel(42,415,'จุดโฟกัส (Focus)');
         setcolor(44);writexypixel(62,415,'=  ('+Spyh+','+Sfocus+')');
    setcolor(102);writexypixel(42,435,'ความยาวLatusrectum');
         setcolor(44);writexypixel(62,435,'=  '+Slatus);

         end;  {Check Esc }
        pause;
     end;
end;

Procedure ParaY_SubMenu;
var choice : byte;
    chpy   : char;
begin
Repeat
     cleardevice;
     initrgb;
     fadein(0);
       Menu_Paray_border;
     fadeout(100);
     Sim_CreatingGraphParaY;
     Sim_ExitParaY;
     writetextmenu;
     choice := 1;
     chpy := #0;
     repeat
{down}      if chpy = #80 then
               begin
                    if choice = 3 then choice := 0;
                    inc(choice);
               end;
{up}        if chpy = #72 then
               begin
                    if choice = 1 then choice := 4;
                    dec(choice);
               end;
               case choice of
                1 :  begin
                          if chpy=#72 then Sim_CreatingGraphParaY;
                          if chpy=#80 then Sim_ExitParaY;
                          vab_DataParaY;;
                     end;
                2 :  begin
                          if chpy=#72 then Sim_ExitParaY;
                          if chpy=#80 then Sim_DataParaY;
                          vab_CreatingGraphParay;
                     end;
                3 :  begin
                          if chpy=#72 then Sim_DataParaY;
                          if chpy=#80 then Sim_CreatingGraphParaY;
                          vab_ExitParaY;
                     end;

                end;{case}
                repeat
                      chpy := readkey;
                      if chpy = #0 then chpy := readkey;
                until chpy in [#59,#13,#72,#80];
                if chpy = #59 then help;
     until chpy in [#13];
     Case Choice of
         1 : data_ParaY;
         2 : Creating_GraphParaY;
     end;
Until (choice = 3) or ( chpy in [#27]);
end;

begin
     uses_svga256_color;
     initrgb;
     start_delay(real_delay2);
     loadfont('normal.fon');
     ParaY_SubMenu;
end.