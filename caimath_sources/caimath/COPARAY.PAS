Procedure Menu_ParaY_Border;
begin
     setfillstyle(1,0);bar(1,1,640,480);
     yjjborder(1,1,640,50,17,26);
     yjjborder(621,51,640,480,17,26);
     yjjborder(450,51,469,480,17,26);
     yjjborder(1,51,20,480,17,26);
{    setcolor(14); writexypixel(63,350,'F1 = Help');
     setcolor(51); writexypixel(63,380,chr(135));
                   writexypixel(65,383,'ขึ้น');
     setcolor(47); writexypixel(69,383,chr(136));
                   writexypixel(71,383,'ลง');
     setcolor(100); writexypixel(63,408,'เลือกเมนู');
     setcolor(57); writexypixel(61,443,'Enter เพื่อเข้าเมนู'); }
     yjjborder(1,51,640,480,17,26);
end;

Procedure pyWritetextmenu;
begin
     settextstyle(1,0,2); setcolor(52);outtextxy(26,13,'Parabola   axis');
                          setcolor(37);outtextxy(120,13,'Y');
                          setcolor(10);outtextxy(480,13,'Conic Section');
    setcolor(79);writexypixel(25,15,'พาราโบลา แกน Y');
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

Procedure pyMenu_Input;
var pyc,pyh,pyk,pyi,pyxa,pyya,pyx,pya,pyy,bpyxa : integer;
    Spyc,Spyh,Spyk,Sdirec,Sfocus,Slatus          : string;

begin
     SlideMenu(82);
     yjjborder(487,78,615,120,23,28);
     setcolor(11);settextstyle(2,0,4);outtextxy(500,86,'      2   ');
                  settextstyle(2,0,5);outtextxy(500,94,'(x-h) = 4c(y-k)');
     ikey := #0;

     if ikey <> #27 then
     begin
          repeat
                yjjboard(540,160,585,190,67,69,0);
                setcolor(10); writexypixel(62,165,'c = ');
                              valinput(pyc,2,68,165,85);
          until (pyc <> 0) or (ikey = #27);
     end;

     if ikey <> #27 then
     begin
          yjjborder(540,200,585,230,67,69);
          setcolor(59); writexypixel(62,205,'h = ');
                        valinput(pyH,2,68,205,86);
     end;

     if ikey <> #27 then
     begin
          yjjborder(540,240,585,270,67,69);
          setcolor(39); writexypixel(62,245,'k = ');
                        valinput(pyK,2,68,245,87);
     end;
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
     if ikey <> #27 then
     begin
          Draw_Quadant_hk(pyh,pyk,25);
          pyDirectric(pyh,pyk,pyc,bpyxa,63);
     end;

    end; { Check Esc }

    if ikey <> #27 then pause;
end;

Procedure Creating_GraphParaY;
Begin
     fadein(100);
        Menu_paray_border;
        pyWritetextMenu;
     fadeout(100);
     Draw_Quadant(230,265,30);
     pyMenu_Input;
end;
