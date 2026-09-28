Procedure Menu_Circle_Border;
begin
     setfillstyle(1,0);bar(1,1,640,480);
     yjjborder(1,1,640,50,17,26);
     yjjborder(621,51,640,480,17,26);
     yjjborder(450,51,469,480,17,26);
     yjjborder(1,51,20,480,17,26);
     yjjborder(1,51,640,480,17,26);
{        setcolor(14); writexypixel(63,350,'F1 = Help');
        setcolor(51); writexypixel(63,380,chr(135));
                      writexypixel(65,383,'ขึ้น');
        setcolor(47); writexypixel(69,383,chr(136));
                      writexypixel(71,383,'ลง');
        setcolor(100); writexypixel(63,408,'เลือกเมนู');
        setcolor(57); writexypixel(61,443,'Enter เพื่อเข้าเมนู');}
end;

Procedure cwritetextmenu;
begin
     settextstyle(1,0,2); setcolor(52);outtextxy(26,13,'Circle');
                          setcolor(10);outtextxy(480,13,'Conic Section');
     setcolor(79);writexypixel(12,15,'วงกลม');
end;

Procedure cMenu_Input;
var cr,ch,ck,dcr,dch,dck,cd : integer;
    Senrobvong,AreaCircle,
    VolumeCircle            : real;
    SSenrobvong,SAreaCircle,
    SVolumeCircle,
    Scr,Sch,Sck          : string;

begin
     SlideMenu(74);
     yjjborder(487,78,615,120,23,28);
     setcolor(11);settextstyle(2,0,4);outtextxy(500,86,'      2      2  2');
                  settextstyle(2,0,5);outtextxy(500,94,'(x-h)+(y-k)=r');
     ikey := #0;

     if ikey <> #27 then
     begin
          repeat
                yjjboard(540,160,585,190,67,69,0);
                setcolor(10); writexypixel(62,165,'r = ');
                              nominusinput(CR,2,68,165,85);
                if cr < 1 then yjjboard(540,160,585,190,67,69,0);
          until ((cr>=1) and (cr<=80)) or (ikey = #27);
     end;

     if ikey <> #27 then
     begin
          yjjborder(540,200,585,230,67,69);
          setcolor(59); writexypixel(62,205,'h = ');
                        valinput(CH,2,68,205,86);
     end;

     if ikey <> #27 then
     begin
          yjjborder(540,240,585,270,67,69);
          setcolor(39); writexypixel(62,245,'k = ');
                        valinput(CK,2,68,245,87);
     end;

    setcolor(10);
    if ikey <> #27 then
    for CD := 1   to 180 do
    begin
         ellipse(230+CH,265-CK,0,CD,CR,CR);
         ellipse(230+CH,265-CK,180,180+CD,CR,CR);
         yjjdelay(10);
    end;

    setcolor(84);outtextxy(230+ch+5,265-ck+5,'(h,k)');

    if ikey <> #27 then
    begin
         Draw_Quadant_hk(ch,ck,25);
    end;
    if ikey <> #27 then pause;
end;

Procedure Creating_Graphcircle;
Begin
     fadein(100);
        Menu_Circle_border;
        cWritetextMenu;
     fadeout(100);
     Draw_Quadant(230,265,30);
     cMenu_Input;
end;
