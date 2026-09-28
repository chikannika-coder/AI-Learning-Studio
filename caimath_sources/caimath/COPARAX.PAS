Procedure Menu_ParaX_Border;
begin
     setfillstyle(1,0);bar(1,1,640,480);
     yjjborder(1,1,640,50,17,26);
     yjjborder(621,51,640,480,17,26);
     yjjborder(450,51,469,480,17,26);
     yjjborder(1,51,20,480,17,26);
{     setcolor(14); writexypixel(63,350,'F1 = Help');
     setcolor(51); writexypixel(63,380,chr(135));
                   writexypixel(65,383,'ขึ้น');
     setcolor(47); writexypixel(69,383,chr(136));
                   writexypixel(71,383,'ลง');
     setcolor(100); writexypixel(63,408,'เลือกเมนู');
     setcolor(57); writexypixel(61,443,'Enter เพื่อเข้าเมนู'); }
     yjjborder(1,51,640,480,17,26);
end;

Procedure pxWritetextmenu;
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

Procedure pxMenu_Input;
var pxc,pxh,pxk,pxi,pxxa,pxya,pxx,pxa,pxy,bpxya : integer;
    Spxc,Spxh,Spxk,Sdirec,Sfocus,Slatus          : string;

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
                              valinput(pxc,2,68,165,85);
          until (pxc <> 0) or (ikey = #27);
     end;

     if ikey <> #27 then
     begin
          yjjborder(540,200,585,230,67,69);
          setcolor(59); writexypixel(62,205,'h = ');
                        valinput(pxH,2,68,205,86);
     end;

     if ikey <> #27 then
     begin
          yjjborder(540,240,585,270,67,69);
          setcolor(39); writexypixel(62,245,'k = ');
                        valinput(pxK,2,68,245,87);
     end;

     case pxc of
          1,-1   : bpxya := -20;
          2,-2   : bpxya := -28;
          3,-3   : bpxya := -32;
          4,-4   : bpxya := -37;
          5,-5   : bpxya := -41;
          6,-6   : bpxya := -45;
          7,-7   : bpxya := -50;
          8,-8   : bpxya := -52;
          9,-9   : bpxya := -55;
          10,-10 : bpxya := -57;
          11..13,-13..-11   : bpxya := -59;
          14..16,-16..-14   : bpxya := -63;
          17..20,-20..-17   : bpxya := -67;
          21..25,-25..-21   : bpxya := -71;
          26..30,-31..-26   : bpxya := -75;
          31..35,-35..-31   : bpxya := -79;
          36..40,-40..-36   : bpxya := -83;
          41..50,-50..-41   : bpxya := -87;
          51..60,-60..-51   : bpxya := -91;
          61..80,-80..-61   : bpxya := -95;
          81..99,-99..-81   : bpxya := -100;

     end; {---CASE---}
     if ikey <> #27 then
     begin
          pxya := bpxya;
          pxxa := round((pxya*pxya)/(4*pxc));
          setcolor(10);
          For pxY := bpxya to (-1)*bpxya+1 do
          begin
               pxx := round((pxya*pxya)/(4*pxc));
               setcolor(87);
               yjjdelay(50);
               line(230+pxxa+pxh,265-pxya-pxk,230+pxx+pxh,265-pxy-pxk);
               pxxa := pxx;
               pxya := pxy;
          end;
     if ikey <> #27 then
     begin
          Draw_Quadant_hk(pxh,pxk,25);
          pxDirectric(pxh,pxk,pxc,bpxya,37);
     end;
    end; { Check Esc }

    if ikey <> #27 then pause;
end;

Procedure Creating_GraphParaX;
Begin
     fadein(100);
        Menu_paraX_border;
        pxWritetextMenu;
     fadeout(100);
     Draw_Quadant(230,265,30);
     pxMenu_Input;
end;
