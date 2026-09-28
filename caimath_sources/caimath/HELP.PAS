Procedure Help;
begin
     setfillstyle(1,0);bar(20,65,450,465);
     setcolor(46); writexypixel(25,65,'HELP');
     setcolor(79); writexypixel(5,100,'1. ในการรับค่าจะต้องใส่ค่าเป็นจำนวนเต็มเท่านั้น');
                   writexypixel(5,130,'2. ค่า c (ในพาราโบลา) สามารถรับค่าได้ตั้งแต่ -60 ถึง 60 ');
                   writexypixel(5,160,'   แต่ c จะต้องไม่เท่ากับ 0');
                   writexypixel(5,190,'3. ค่า r (รัศมีของวงกลม) สามารถรับค่าได้ตั้งแต่ 1 -> 60');
                   writexypixel(5,220,'4. ค่า h,k สามารถรับค่าได้ตั้งแต่ -60 -> 60');
                   writexypixel(5,250,'5. ค่า a,b สามารถรับค่าได้ตั้งแต่ 1 -> 60 โดยที่ a จะต้อง');
                   writexypixel(5,280,'   มากกว่า b เสมอ');
end;

