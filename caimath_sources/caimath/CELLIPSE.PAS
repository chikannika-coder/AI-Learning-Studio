Procedure Menu_Ellipsex_Border;
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
     setcolor(57); writexypixel(61,443,'Enter เพื่อเข้าเมนู');}
     yjjborder(1,51,640,480,17,26);
end;

Procedure exwritetextmenu;
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

Procedure exMenu_Input;
var exh,exk,exa,exb,exd,exc                                  : integer;
    Sexh,Sexk,Sexa,Sexb,major,minor,latus,focus1,focus2,elec : string;

begin
     SlideMenu(74);
     yjjborder(487,78,615,136,23,28);
     setcolor(11);settextstyle(2,0,4);outtextxy(500,86,'      2      2  ');
                  settextstyle(2,0,5);outtextxy(500,94,'(x-h)+(y-k) = 1');
                  line(500,109,530,109);line(545,109,575,109);
                  settextstyle(2,0,4);outtextxy(500,110,'    2      2  ');
                  settextstyle(2,0,5);outtextxy(500,114,'  a    b');
     ikey := #0;

     if ikey <> #27 then
     begin
          yjjborder(540,160,585,190,67,69);
          setcolor(84); writexypixel(62,165,'h = ');
                        valinput(exh,2,68,165,87);
     end;

     if ikey <> #27 then
     begin
          yjjborder(540,200,585,230,67,69);
          setcolor(78); writexypixel(62,205,'k = ');
                        valinput(exk,2,68,205,87);
     end;

     if ikey <> #27 then
     begin
          repeat
          yjjboard(540,240,585,270,67,69,0);
          setcolor(80); writexypixel(62,245,'a = ');
                        nominusinput(exa,2,68,245,87);
          until (exa > 1) or (ikey = #27);
     end;

     if ikey <> #27 then
     begin
          repeat
                yjjboard(540,280,585,310,67,69,0);
                setcolor(82); writexypixel(62,285,'b = ');
                              nominusinput(exb,3,68,285,87);
          until ((exa>exb) and (exb<>0)) or (ikey = #27);
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
    end;
    setcolor(89);outtextxy(230+exh+5,265-exk+5,'(h,k)');
    draw_Quadant_hk(exh,exk,25);
    if ikey <> #27 then pause;
end;

Procedure Creating_GraphEllipseX;
Begin
     fadein(100);
        Menu_ellipseX_border;
        exWritetextMenu;
     fadeout(100);
     Draw_Quadant(230,265,30);
     exMenu_Input;
end;
