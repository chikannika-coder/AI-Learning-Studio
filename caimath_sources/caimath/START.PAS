Procedure Start;
var install,gd,gm,
    x,y,c,ya,xa,i,d,co,l,p,xx,yy : integer;
    st        : string;
    ch        : char;

Procedure Title_ParaX(Cx : Integer);
var y : integer;
Begin
     C  := Cx;
     Ya := -88;
     Xa := round((Ya*Ya)/(4*C));

     For Y := -88 to 88 do
     begin
          X := round((Y*Y)/(4*C));
          setcolor(13);
          yjjdelay(50);
          line(320+xa,240-ya,320+x,240-y);
          line(320-xa,240+ya,320-x,240+y);
          xa:=x;
          ya:=y;
     end;
End;

Procedure Title_ParaY(Cx : Integer);
var x : integer;
Begin
     C  := Cx;
     xa := -88;
     ya := round((xa*xa)/(4*c));
     For X := -88 to 88 do
     begin
           Y := round((X*X)/(4*C));
           setcolor((10));
           yjjdelay(50);
           line(320+xa,240-ya,320+x,240-y);
           xa:=x;
           ya:=y;
     end;
End;

Procedure Title_ParaYHK(Cx : Integer);
var x : integer;
Begin
     C  := Cx;
     Xa := -105;
     Ya := round((Xa*Xa)/(4*C));
     For X := -105 to 105 do
     begin
           Y := round((X*X)/(4*C));
           setcolor(38);
           yjjdelay(50);
           line(350+Xa,330-Ya,350+X,330-Y);
           Xa:=X;
           Ya:=Y;
     end;
End;

Procedure Title_sin;
var  x : integer;
begin
     Xa := -125;
     Ya := round(100*sin(Xa/20));
     For X := -125 to 125 do
     Begin
          Y :=  round(100*sin(X/20));
          setcolor(11);
          yjjdelay(10);
          line(Xa+320,240-Ya,X+320,240-Y);
          Xa:=X;
          Ya:=Y;
     end;
End;

Procedure Title_sin2;
var  x : integer;
begin
     Xa := -300;
     Ya := round(50*sin(Xa/30));
     For X := -300  to 125 do
     Begin
          Y :=  round(50*sin(X/30));
          setcolor(34);
          yjjdelay(20);
          line(Xa+370,220-Ya,X+370,220-Y);
          Xa:=X;
          Ya:=Y;
     end;
End;

Procedure Quadant;
Begin
    setcolor(30);
    line(120,240,520,240);
    line(320,50,320,430);
End;

procedure fade_graph(color:integer);
var i : integer;
begin
     for i := 50 downto 0 do
     begin
          setrgbpalette(color,i,i,i);
          quadant;
          yjjdelay(50);
     end;
end;

procedure Title_ellipse;
var d: integer;
begin
     for d := 1 to 179 do
     Begin
          setcolor(83);
          ellipse(320,240,0,d,140,70);
          ellipse(320,240,180,180+d,140,70);
          yjjdelay(50);
     End;
end;

procedure Title_Circle;
var d: integer;
begin
     for d := 1 to 179 do
     Begin
          setcolor(11);
          ellipse(320,240,0,d,80,80);
          ellipse(320,240,180,180+d,80,80);
          yjjdelay(50);
     End;
end;

procedure Title_Hyper;
var d : integer;
begin
     for d := 1 to 179 do
     Begin
          setcolor(34);
          ellipse(150,240,270,270+d,140,70);
          ellipse(490,240,90,90+d,140,70);
          yjjdelay(50);
     End;
end;

procedure spectrum;
var p,x,y : integer;
begin
    for p := 1 to 60 do
    begin
         x:=1; y:=1; i:=p;
         for x:=1 to 64 do
         begin
             setcolor(i); inc(i);
             line(1,480,x*10,1);
         end;
         for y:=1 to 48 do
         begin
              setcolor(i); inc(i);
              line(1,480,640,y*10);
         end;
    end;

    for p := 60 downto 1 do
    begin
         x:=1; y:=1; i:=p;
         for x:=1 to 64 do
         begin
              setcolor(i); inc(i);
              line(1,480,x*10,1);
         end;
         for y:=1 to 48 do
         begin
              setcolor(i); inc(i);
              line(1,480,640,y*10);
         end;
    end;
end;
{++++++++++++++++++++++++++++++Main_Title+++++++++++++++++++++++++++++++++++}

begin
     cleardevice;
     initrgb;
     Title_sin2;
             x :=100; y :=100;
             xx:=110; yy:=110;
             repeat
                   inc(x);inc(y,2);
                   inc(xx,2);inc(yy);
                   if x  < 540 then begin putpixel(x,230,30); yjjdelay(5); end;
                   if y  < 380 then begin putpixel(200,y,30); yjjdelay(5); end;
                   if xx < 550 then begin putpixel(xx,240,25);yjjdelay(5); end;
                   if yy < 390 then begin putpixel(210,yy,25);yjjdelay(5); end;
             until x=540;
                       setcolor(38);settextstyle(2,0,6);
           if not(keypressed) then
           begin
                yjjdelay(500);outtextxy(135,230,'C');
                yjjdelay(500);outtextxy(150,245,'A');
                yjjdelay(500);outtextxy(165,260,'I');
                yjjdelay(500);outtextxy(180,250,'.');
                yjjdelay(500);outtextxy(190,230,'M');
                yjjdelay(500);outtextxy(200,210,'A');
                yjjdelay(500);outtextxy(212,197,'T');
                yjjdelay(500);outtextxy(225,177,'H');
                yjjdelay(500);outtextxy(247,165,'E');
                yjjdelay(500);outtextxy(267,175,'M');
                yjjdelay(500);outtextxy(280,190,'A');
                yjjdelay(500);outtextxy(290,210,'T');
                yjjdelay(500);outtextxy(302,228,'I');
                yjjdelay(500);outtextxy(317,245,'C');
                yjjdelay(500);outtextxy(348,262,'C');
                yjjdelay(500);outtextxy(364,248,'O');
                yjjdelay(500);outtextxy(378,232,'N');
                yjjdelay(500);outtextxy(388,212,'I');
                yjjdelay(500);outtextxy(399,195,'C');
                yjjdelay(500);outtextxy(443,165,'S');
                yjjdelay(500);outtextxy(455,177,'E');
                yjjdelay(500);outtextxy(465,191,'C');
                yjjdelay(500);outtextxy(472,207,'T');
                yjjdelay(500);outtextxy(481,223,'I');
                yjjdelay(500);outtextxy(492,239,'O');
                yjjdelay(500);outtextxy(504,255,'N');
           yjjdelay(5000);
           end;
     cleardevice;
     if not(keypressed) then
     begin
                 fadein(0);
                         setcolor(38);settextstyle(2,0,15);
                         outtextxy(160,200,'CAI MATHMATIC');
                 fadeout(100);fadein(100);
     cleardevice;
     end;
     if not(keypressed) then
     begin
                 fadein(0);
                           setcolor(48);settextstyle(2,0,15);
                           outtextxy(170,200,'Conic Section');
                 fadeout(100);fadein(100);
     cleardevice;
     end;
     if not(keypressed) then
     begin
                 setcolor(11);settextstyle(2,0,15);
                 fadein(0);
                           outtextxy(200,200,'Graph Circle');
                 fadeout(50);fadein(50);
     cleardevice;
     end;
     if not(keypressed) then
     begin
                 Quadant;
                 fadeout(30);
                             Title_Circle;fade_graph(11);
     cleardevice;
     end;
     if not(keypressed) then
     begin
                 setcolor(10);settextstyle(2,0,15);
                 fadein(0);
                           outtextxy(180,200,'Graph Parabola');
                 fadeout(50);fadein(50);
     cleardevice;
     end;
     if not(keypressed) then
     begin
                 fadeout(30);
                 Quadant;
                 Title_paraY(10);fade_graph(10);

     end;
     if not(keypressed) then
     begin
                 Title_paraX(10);fade_graph(13);
     end;
     if not(keypressed) then
     begin

                 Title_paraYHK(10);fade_graph(38);
     end;
     if not(keypressed) then
     begin
     cleardevice;
                 setcolor(13);settextstyle(2,0,15);
                 fadein(0);
                           outtextxy(190,200,'Graph Ellipse');
                 fadeout(50);fadein(50);
     end;
     if not(keypressed) then
     begin
          cleardevice;
                 fadeout(30);
                 Quadant;
                 Title_ellipse;fade_graph(83);
     end;
     if not(keypressed) then
     begin
          cleardevice;
                 setcolor(34);settextstyle(2,0,15);
                 fadein(0);
                           outtextxy(160,200,'Graph Hyperbola');
                 fadeout(50);fadein(50);
     end;
     if not(keypressed) then
     begin
          cleardevice;
                 fadeout(30);
                 Quadant;
                 Title_Hyper;fade_graph(34);
          yjjdelay(500);
     end;
     if not(keypressed) then
     begin
          cleardevice;
                 setcolor(51);settextstyle(3,0,3);
                 fadein(0);
                           outtextxy(250,200,'Present to');
                 fadeout(100);fadein(100);
          cleardevice;
     end;
     if not(keypressed) then
     begin
          cleardevice;
                 setcolor(14);settextstyle(3,0,3);
                 fadein(0);
                           outtextxy(205,200,'Mr. Chirasak Suwanno');
                 fadeout(100);fadein(100);
          cleardevice;
     end;
     if not(keypressed) then
     begin
          cleardevice;
                 setcolor(35);settextstyle(3,0,3);
                 fadein(0);
                           outtextxy(280,200,'BY');
                 fadeout(50);fadein(50);

     end;
     if not(keypressed) then
     begin
          cleardevice;
                 setcolor(32);settextstyle(3,0,3);
                 fadein(0);
                           outtextxy(200,200,'Mr Jeerawat Ngamsawai');
                 fadeout(100);fadein(100);
     end;
     if not(keypressed) then
     begin
          cleardevice;
                 setcolor(32);settextstyle(3,0,3);
                 fadein(0);
                           outtextxy(200,200,'Miss Jariya Sabuyen');
                 fadeout(100);fadein(100);
     end;
     if not(keypressed) then
     begin
          cleardevice;
                 setcolor(32);settextstyle(3,0,3);
                 fadein(0);
                           outtextxy(150,200,'Miss Tatsaneewan Rattanapornsan');
                 fadeout(100);fadein(100);
          cleardevice;
     end;
end;