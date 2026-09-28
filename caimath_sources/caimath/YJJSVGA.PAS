Unit YjjSvga;
interface

 Uses graph,crt,dos,kvga;

Var
   real_delay,real_delay2 : real;
   ch,ikey                : char;
   valout,x,y             : integer;
   exit                   : boolean;

procedure uses_svga256_color;
Procedure YJJdelay(ms : word);
Procedure pause;
Procedure color;
Procedure Start_Delay(var real_delay : real);
Procedure YJJBorder(X1,Y1,X2,Y2,color_begin,color_end : integer);
Procedure Yim(x1,y1,x2,y2,cb,cs,ce,wd : integer);
Procedure YJJBoard(X1,Y1,X2,Y2:integer; color_begin,color_end,color_bar : byte);
procedure valinput(var valin : integer; range : byte;Xinput,Yinput,cinput : integer);
procedure Nominusinput(var valin : integer; range : byte;Xinput,Yinput,cinput : integer);

Implementation

{$f+}
 function vidd:integer;
begin
     vidd:=2;  {1=640*400*256 , 2=640*480*256 , 3=800*600*256}
end;
{$f-}


procedure  uses_svga256_color;
var i,install,graphdriver,graphmode : integer;
begin
     install:=installuserdriver('svga256',@vidd);
     graphdriver := detect;initgraph(graphdriver,graphmode,'svga256');

     for i := 248 to 255 do
     setrgbpalette(i,(i-248)*4,0,0);
end;

Procedure YJJdelay(ms : word);
var Xdelay : word;
begin
     Xdelay := round((real_delay2*ms)/5000);
     delay(Xdelay);
end;

Procedure pause;
 var ch : char;
 begin
    ch := readkey;
    if ch = #0 then ch := readkey;
 end;

Procedure color;
var  x,y       : integer;
     color     : byte;
     scolor    : string;
begin
       cleardevice;
        y     := 1;
        color := 1;
        repeat
              x := 1;
              repeat
                    setcolor(color);
                    str(color,scolor);
                    outtextxy(x,y,scolor);
                    inc(x,30);
                    inc(color);
              Until (x  >= 620) or (color = 255);
              inc(y,15);
        Until color >= 255;
        pause;
end;

Procedure Start_Delay(var real_delay : real);
var  com_time : longint absolute $40:$6c;
     Stime,Ftime : longint;
begin
     Stime := com_time;
     delay(10000);
     Ftime := com_time;
     real_delay := 10000/((Ftime-Stime)/18.2);
end;
                                  {17..31}  {31..17}
Procedure YJJBorder(X1,Y1,X2,Y2,color_begin,color_end : integer);
var bordercolor,i,shadeup : byte;
begin
     {17++++++31}
     shadeup := 0;
     if color_begin < color_end then
     begin
          for bordercolor := color_begin to color_end do
          begin
               setcolor(bordercolor);
               line(X1+shadeup,Y1+shadeup,X2-shadeup,Y1+shadeup);
               line(X1+shadeup,Y2-shadeup,X2-shadeup,Y2-shadeup);
               line(X1+shadeup,Y1+shadeup,X1+shadeup,Y2-shadeup);
               line(X2-shadeup,Y1+shadeup,X2-shadeup,Y2-shadeup);
               inc(shadeup);
          end;
     end
     ELSE
     begin
          for bordercolor := color_begin downto color_end do
          begin
               setcolor(bordercolor);
               line(X1+shadeup,Y1+shadeup,X2-shadeup,Y1+shadeup);
               line(X1+shadeup,Y2-shadeup,X2-shadeup,Y2-shadeup);
               line(X1+shadeup,Y1+shadeup,X1+shadeup,Y2-shadeup);
               line(X2-shadeup,Y1+shadeup,X2-shadeup,Y2-shadeup);
               inc(shadeup);
          end;
     end

end;

{+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++}

{++++++++++++++++++++++++++++++YIM******************************************}
Procedure Yim(x1,y1,x2,y2,cb,cs,ce,wd : integer);
var w : integer;
begin
     if cs > ce then
     begin
          setfillstyle(1,cb);
          bar(x1,y1,x2,y2);
          repeat
                w := 0;
                for w := 1 to wd do
                begin
                     inc(x2);
                     setcolor(cs);line(x2,y1,x2,y2);
                end;
                dec(cs);
          until cs = ce;
     end;
     if ce > cs then
     begin
          setfillstyle(1,cb);
          bar(x1,y1,x2,y2);
          repeat
                w := 0;
                for w := 1 to wd do
                begin
                     inc(x2);
                     setcolor(cs);line(x2,y1,x2,y2);
                end;
                inc(cs);
          until cs = ce;
     end;
end;


Procedure YJJBoard(X1,Y1,X2,Y2:integer; color_begin,color_end,color_bar : byte);
var bordercolor,i,shadeup : byte;
begin
     {17++++++31}
     shadeup := 0;
     if color_begin < color_end then
     begin
          for bordercolor := color_begin to color_end do
          begin
               setcolor(bordercolor);
               line(X1+shadeup,Y1+shadeup,X2-shadeup,Y1+shadeup);
               line(X1+shadeup,Y2-shadeup,X2-shadeup,Y2-shadeup);
               line(X1+shadeup,Y1+shadeup,X1+shadeup,Y2-shadeup);
               line(X2-shadeup,Y1+shadeup,X2-shadeup,Y2-shadeup);
               inc(shadeup);
          end;
          setfillstyle(1,color_bar);
          bar(x1+shadeup,y1+shadeup,x2-shadeup,y2-shadeup);

     end
     ELSE
     begin
          for bordercolor := color_begin downto color_end do
          begin
               setcolor(bordercolor);
               line(X1+shadeup,Y1+shadeup,X2-shadeup,Y1+shadeup);
               line(X1+shadeup,Y2-shadeup,X2-shadeup,Y2-shadeup);
               line(X1+shadeup,Y1+shadeup,X1+shadeup,Y2-shadeup);
               line(X2-shadeup,Y1+shadeup,X2-shadeup,Y2-shadeup);
               inc(shadeup);
          end;
          setfillstyle(1,color_bar);
          bar(x1+shadeup,y1+shadeup,x2-shadeup,y2-shadeup);

     end
end;

{+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++}
                   {=====Input Value NUMBER=====}

procedure valinput(var valin : integer; range : byte;Xinput,Yinput,cinput : integer);
var icount,rcount  : byte;
    namein,nameout : string;
    xcode          : integer;
begin
     nameout := '';
     icount  := 0;
     rcount  := 0;
     repeat
           ikey := readkey;
           if ((rcount < range) and (ikey >= #48) and (ikey <= #57))
              or ((ikey='-') and (icount=0)) then
           begin
                if ikey in [#48..#57] then inc(rcount);
                inc(icount);
                setcolor(Cinput);writexypixel(xinput+icount,yinput,ikey);
                nameout := nameout + ikey;
           end;
           if (ikey = #8) and (icount > 0) then
           begin
                delete(nameout,icount,1);
                setcolor(0);writexypixel(xinput+icount,yinput,nameout[icount]);
                if nameout[icount] in [#48..#57] then dec(rcount);
                dec(icount);
           end;
           if (ikey = #0) then
           begin
                ikey := readkey;
           end;
     until ((ikey = #13) and (rcount<>0)) or (ikey = #27);
     val(nameout,valout,xcode);
     valin := valout;
end;
                {=====No Minus Input Value NUMBER=====}

procedure Nominusinput(var valin : integer; range : byte;Xinput,Yinput,cinput : integer);
   var icount,rcount  : byte;
       namein,nameout : string;
       xcode          : integer;
  begin
     nameout := '';
     icount  := 0;
     rcount  := 0;
     repeat
           ikey := readkey;
           if (rcount < range) and (ikey >= #48) and (ikey <= #57) then
           begin
                if ikey in [#48..#57] then inc(rcount);
                inc(icount);
                setcolor(Cinput);writexypixel(xinput+icount,yinput,ikey);
                nameout := nameout + ikey;
           end;
           if (ikey = #8) and (icount > 0) then
           begin
                delete(nameout,icount,1);
                setcolor(0);writexypixel(xinput+icount,yinput,nameout[icount]);
                if nameout[icount] in [#48..#57] then dec(rcount);
                dec(icount);
           end;
           if (ikey = #0) then
           begin
                ikey := readkey;
           end;
     until ((ikey = #13) and (rcount<>0)) or (ikey = #27);
     val(nameout,valout,xcode);
     valin := valout;
   end;
end.
