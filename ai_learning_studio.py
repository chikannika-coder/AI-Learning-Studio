import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import math, random, statistics, json, csv, wave, os, zipfile, re, time
try:
    import sympy as sp
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
except Exception:
    sp = None
    parse_expr = None
    standard_transformations = ()
    implicit_multiplication_application = convert_xor = None
try:
    import cv2
except Exception:
    cv2 = None

try:
    from PIL import Image, ImageTk
except Exception:
    Image = ImageTk = None
try:
    import serial
    from serial.tools import list_ports
except Exception:
    serial = list_ports = None

APP='AI Learning Studio — v5.9 • Windows Edition'
BG='#f4f7fb'; NAV='#15243b'; BLUE='#20a4d8'; TEXT='#14213d'; MUTED='#66758a'; BORDER='#dce5ef'; GREEN='#15803d'; ORANGE='#c2410c'

class Studio(tk.Tk):
    def __init__(self):
        super().__init__(); self.title(APP); self.geometry('1420x880'); self.minsize(1100,720); self.configure(bg=BG)
        self.class_data={'A':[],'B':[]}; self.features={'A':[],'B':[]}; self.model=None; self.last_metrics={}; self.progress={str(i):0 for i in range(1,9)}
        self.robot=(260,180); self.robot_serial=None; self.sim=True; self.lesson_score=0; self.scores={str(i):0 for i in range(1,9)}; self.student_name='Student'; self.tc_zip=self._find_tc_zip(); self.webcam_cap=None; self.museum_scores={k:0 for k in ['Circle','Parabola','Ellipse','Sorting','Statistics','Probability','Decision Tree']}
        self._style(); self._layout(); self.home()
    def _style(self):
        s=ttk.Style(self)
        try:s.theme_use('clam')
        except:pass
        s.configure('Primary.TButton',font=('Segoe UI Semibold',10),padding=(12,8)); s.configure('TButton',font=('Segoe UI',10),padding=(9,7)); s.configure('TNotebook.Tab',font=('Segoe UI Semibold',10),padding=(12,8))
    def _layout(self):
        self.side=tk.Frame(self,bg=NAV,width=230); self.side.pack(side='left',fill='y'); self.side.pack_propagate(False)
        tk.Label(self.side,text='AI',font=('Segoe UI Black',30),fg='#68d7ff',bg=NAV).pack(anchor='w',padx=22,pady=(20,0)); tk.Label(self.side,text='LEARNING STUDIO',font=('Segoe UI Semibold',12),fg='white',bg=NAV).pack(anchor='w',padx=22,pady=(0,18))
        items=[('⌂  Home',self.home),('01  Coding & Algorithm',self.lesson1),('02  Dataset Lab',self.lesson2),('03  Image AI',self.lesson3),('04  Sound AI',self.lesson4),('05  Live AI + Math',self.lesson5),('06  Robot AI',self.lesson6),('07  AI Agent',self.lesson7),('08  Project Studio',self.lesson8),('🏛  TC Math Museum',self.tc_math_museum),('📷  v4 Vision → Robot Lab',self.lesson6),('🎛  v5.8 Robot Command Center',self.robot_command_center_lab),('🤖  v5.7 AI → Robot Control',self.ai_robot_control_lab),('🧪  v5.7 Hardware Check',self.hardware_check_lab),('📖  v5.6 Line → Lesson → TC Menu',self.line_lesson_tc_lab),('🤖  v5.5 Adaptive AI Tutor',self.adaptive_tutor_lab),('🧠  v5.4 Auto TC Exercises',self.auto_tc_exercise_lab),('📝  v5.3 Student Exercises',self.student_exercise_lab),('👩‍🏫  v5.3 Teacher Mode',self.teacher_v53_lab),('🧩  v5.2 Four-Panel Learning',self.four_panel_learning_lab),('🔗  v5.1 TC Source → Live Math',self.tc_live_math_lab),('🎞  v5 Math Animation Lab',self.math_animation_lab),('🖼  TC Math Gallery',self.math_gallery_lab),('🧭  Equation Atlas (All Files)',self.equation_atlas_lab),('∫  Auto Equation Lab',self.auto_equation_lab),('∑  Math Comparison',self.math_lab),('⌘  TC Code Lab',self.tc_code_lab),('▣  Teacher Mode',self.teacher_mode),('▤  Worksheets',self.worksheets)]
        for t,c in items:
            tk.Button(self.side,text=t,command=c,bg=NAV,fg='#e8eef8',activebackground='#223957',activeforeground='white',bd=0,font=('Segoe UI',10),anchor='w',padx=20,pady=9,cursor='hand2').pack(fill='x')
        tk.Label(self.side,text='Math • Image AI • Webcam • Robot • Windows Edition • v5.9',font=('Segoe UI',9),fg='#8293ab',bg=NAV).pack(side='bottom',pady=16)
        self.main=tk.Frame(self,bg=BG); self.main.pack(side='left',fill='both',expand=True)
    def clear(self):
        for w in self.main.winfo_children(): w.destroy()
    def header(self,title,sub=''):
        top=tk.Frame(self.main,bg='white',height=84); top.pack(fill='x'); top.pack_propagate(False)
        tk.Label(top,text=title,font=('Segoe UI Semibold',22),fg=TEXT,bg='white').pack(anchor='w',padx=28,pady=(13,0)); tk.Label(top,text=sub,font=('Segoe UI',10),fg=MUTED,bg='white').pack(anchor='w',padx=29)
    def scrollbody(self):
        outer=tk.Frame(self.main,bg=BG); outer.pack(fill='both',expand=True)
        cv=tk.Canvas(outer,bg=BG,highlightthickness=0); sb=ttk.Scrollbar(outer,orient='vertical',command=cv.yview); cv.configure(yscrollcommand=sb.set); sb.pack(side='right',fill='y'); cv.pack(side='left',fill='both',expand=True)
        f=tk.Frame(cv,bg=BG); win=cv.create_window((0,0),window=f,anchor='nw'); f.bind('<Configure>',lambda e:cv.configure(scrollregion=cv.bbox('all'))); cv.bind('<Configure>',lambda e:cv.itemconfigure(win,width=e.width)); return f
    def card(self,parent,title,text=''):
        f=tk.Frame(parent,bg='white',highlightbackground=BORDER,highlightthickness=1); f.pack(fill='x',padx=28,pady=8)
        tk.Label(f,text=title,font=('Segoe UI Semibold',14),fg=TEXT,bg='white').pack(anchor='w',padx=18,pady=(14,3))
        if text: tk.Label(f,text=text,font=('Segoe UI',10),fg=MUTED,bg='white',justify='left',wraplength=1050).pack(anchor='w',padx=18,pady=(0,12))
        return f
    def done(self,n,p=100): self.progress[str(n)]=max(self.progress[str(n)],p)
    def home(self):
        self.clear(); self.header('AI Learning Studio v5.8','INPUT → AI → DECISION → COMMAND → ROBOT → FEEDBACK')
        b=self.scrollbody(); hero=self.card(b,'เรียน AI โดย “ลงมือทำ”','แต่ละบทมี Learn → Try → Challenge → Explain Math → Apply นักเรียนสามารถเริ่มจาก Dataset A/B แล้วใช้โมเดลเดียวกันต่อไปถึง Robot AI')
        ttk.Button(hero,text='เริ่มบทที่ 01',style='Primary.TButton',command=self.lesson1).pack(anchor='w',padx=18,pady=(0,16))
        grid=tk.Frame(b,bg=BG); grid.pack(fill='x',padx=20,pady=8)
        names=['Coding & Algorithm','Dataset Lab','Image AI','Sound AI','Live AI + Math','Robot AI','AI Agent','Project Studio']
        cmds=[self.lesson1,self.lesson2,self.lesson3,self.lesson4,self.lesson5,self.lesson6,self.lesson7,self.lesson8]
        for i,(name,cmd) in enumerate(zip(names,cmds),1):
            f=tk.Frame(grid,bg='white',highlightbackground=BORDER,highlightthickness=1,width=300,height=130); f.grid(row=(i-1)//2,column=(i-1)%2,padx=8,pady=8,sticky='nsew'); f.grid_propagate(False); grid.columnconfigure((i-1)%2,weight=1)
            tk.Label(f,text=f'{i:02d}',font=('Segoe UI Black',18),fg=BLUE,bg='white').pack(anchor='w',padx=16,pady=(12,0)); tk.Label(f,text=name,font=('Segoe UI Semibold',13),fg=TEXT,bg='white').pack(anchor='w',padx=16); tk.Label(f,text=f'Progress {self.progress[str(i)]}%',font=('Segoe UI',9),fg=MUTED,bg='white').pack(anchor='w',padx=16); ttk.Button(f,text='เปิดบทเรียน →',command=cmd).pack(anchor='e',padx=14,pady=5)
    def lesson1(self):
        self.clear(); self.header('01 • Coding & Algorithm','จาก Logic / Flowchart / Sorting ใน TC สู่แนวคิด Sense → Decide → Act')
        b=self.scrollbody(); self.card(b,'LEARN','Algorithm คือชุดขั้นตอนที่ชัดเจน เช่น “ถ้าค่า sensor > threshold ให้ STOP” ซึ่งเป็นรากฐานเดียวกับการตัดสินใจของ AI/Robot')
        c=self.card(b,'TRY • สร้าง Threshold Algorithm','เลื่อนค่าจำลอง Sensor แล้วสังเกตผล IF/ELSE')
        v=tk.IntVar(value=45); out=tk.StringVar()
        def calc(*_): out.set('DANGER → STOP' if v.get()>=60 else 'SAFE → FORWARD')
        ttk.Scale(c,from_=0,to=100,variable=v,command=lambda x:calc()).pack(fill='x',padx=18,pady=8); tk.Label(c,textvariable=out,font=('Consolas',14,'bold'),fg=BLUE,bg='white').pack(pady=8); calc()
        q=self.card(b,'CHALLENGE','ถ้า sensor = 75 และ threshold = 60 หุ่นยนต์ควรทำอะไร?')
        ans=tk.StringVar();
        for t in ['FORWARD','STOP','LEFT']: ttk.Radiobutton(q,text=t,value=t,variable=ans).pack(anchor='w',padx=20)
        def check():
            ok=ans.get()=='STOP'; messagebox.showinfo('ผล', 'ถูกต้อง: 75 ≥ 60 จึง STOP' if ok else 'ลองใหม่: เปรียบเทียบ 75 กับ 60'); self.done(1,100 if ok else 40)
        ttk.Button(q,text='ตรวจคำตอบ',command=check).pack(anchor='w',padx=18,pady=12)
    def lesson2(self):
        self.clear(); self.header('02 • Dataset Lab','สร้าง Class A / Class B, Label ข้อมูล และตรวจสมดุล Dataset')
        b=self.scrollbody(); self.card(b,'LEARN','Dataset = ตัวอย่างที่ AI ใช้เรียนรู้ • Label = คำตอบกำกับ • Class = กลุ่มคำตอบ เช่น A=Cat, B=Dog')
        c=self.card(b,'TRY • Class A / Class B')
        top=tk.Frame(c,bg='white'); top.pack(fill='x',padx=18,pady=8)
        self.ds_labels={}
        for col,cl in enumerate(['A','B']):
            f=tk.LabelFrame(top,text=f'Class {cl}',bg='white',fg=TEXT,font=('Segoe UI Semibold',11)); f.grid(row=0,column=col,padx=8,sticky='nsew'); top.columnconfigure(col,weight=1)
            lb=tk.Listbox(f,height=8,font=('Segoe UI',9)); lb.pack(fill='both',expand=True,padx=8,pady=8); self.ds_labels[cl]=lb
            ttk.Button(f,text=f'+ เพิ่มภาพ Class {cl}',command=lambda x=cl:self.add_images(x)).pack(pady=(0,8))
            for p in self.class_data[cl]: lb.insert('end',Path(p).name)
        stat=tk.StringVar(); tk.Label(c,textvariable=stat,bg='white',fg=MUTED,font=('Segoe UI',10)).pack(anchor='w',padx=18,pady=6)
        def refresh():
            a,bn=len(self.class_data['A']),len(self.class_data['B']); stat.set(f'A = {a} ภาพ | B = {bn} ภาพ | Balance difference = {abs(a-bn)}')
        ttk.Button(c,text='ตรวจ Dataset',command=lambda:(refresh(),self.done(2,100 if min(map(len,self.class_data.values()))>=2 else 50))).pack(anchor='w',padx=18,pady=(0,14)); refresh()
        self.card(b,'CHALLENGE','เป้าหมาย: เพิ่มอย่างน้อย Class ละ 2 ภาพ และพยายามให้จำนวน A/B ใกล้เคียงกัน เพื่อลดปัญหา class imbalance')
    def add_images(self,cl):
        fs=filedialog.askopenfilenames(title=f'เลือกภาพ Class {cl}',filetypes=[('Images','*.png *.jpg *.jpeg *.bmp *.gif')]);
        if not fs:return
        self.class_data[cl].extend(fs)
        for p in fs:self.ds_labels[cl].insert('end',Path(p).name)
    def imgfeat(self,p):
        if Image is None: raise RuntimeError('ต้องติดตั้ง Pillow: pip install pillow')
        im=Image.open(p).convert('RGB').resize((32,32)); px=list(im.getdata()); n=len(px)
        means=[sum(q[i] for q in px)/n/255 for i in range(3)]; bright=sum(sum(q)/3 for q in px)/n/255
        vars=[sum((q[i]/255-means[i])**2 for q in px)/n for i in range(3)]
        return means+[bright]+vars
    def lesson3(self):
        self.clear(); self.header('03 • Image AI','ฝึก Image Classification จริงด้วย Feature + k-Nearest Neighbors')
        b=self.scrollbody(); self.card(b,'LEARN','โปรแกรมย่อภาพเป็น 32×32 แล้วคำนวณ Mean RGB, Brightness และ Variance เป็น Feature vector จากนั้นใช้ระยะห่างทางคณิตศาสตร์หาเพื่อนบ้านที่ใกล้ที่สุด (k-NN)')
        c=self.card(b,'TRAIN • Model จริง'); status=tk.StringVar(value=f'Dataset: A={len(self.class_data["A"])} | B={len(self.class_data["B"])}'); tk.Label(c,textvariable=status,bg='white',fg=MUTED).pack(anchor='w',padx=18,pady=8)
        metric=tk.StringVar(value='euclidean'); ttk.Combobox(c,textvariable=metric,values=['euclidean','manhattan','cosine'],state='readonly',width=18).pack(anchor='w',padx=18)
        def train():
            if min(len(self.class_data['A']),len(self.class_data['B']))<2: messagebox.showwarning('Dataset','กรุณาเพิ่มภาพ Class A และ B อย่างน้อย Class ละ 2 ภาพในบท 02'); return
            try:self.features={cl:[(self.imgfeat(p),p) for p in self.class_data[cl]] for cl in ['A','B']}
            except Exception as e: messagebox.showerror('Image AI',str(e));return
            self.model={'type':'knn','metric':metric.get(),'k':3}; status.set(f'Trained ✓  samples={sum(map(len,self.class_data.values()))} | metric={metric.get()} | k=3'); self.done(3,100)
        ttk.Button(c,text='▶ TRAIN IMAGE AI',style='Primary.TButton',command=train).pack(anchor='w',padx=18,pady=12)
        t=self.card(b,'TEST • เลือกภาพใหม่'); pred=tk.StringVar(value='Prediction: -'); tk.Label(t,textvariable=pred,font=('Segoe UI Semibold',14),fg=BLUE,bg='white').pack(anchor='w',padx=18,pady=8)
        def test():
            if not self.model: messagebox.showwarning('Model','Train model ก่อน');return
            p=filedialog.askopenfilename(filetypes=[('Images','*.png *.jpg *.jpeg *.bmp *.gif')]);
            if not p:return
            cl,conf,detail=self.predict(self.imgfeat(p)); pred.set(f'Prediction: Class {cl} | confidence ≈ {conf:.1%} | {detail}')
        ttk.Button(t,text='เลือกภาพเพื่อทดสอบ',command=test).pack(anchor='w',padx=18,pady=(0,14))
    def dist(self,a,b,m):
        if m=='manhattan': return sum(abs(x-y) for x,y in zip(a,b))
        if m=='cosine':
            d=math.sqrt(sum(x*x for x in a))*math.sqrt(sum(y*y for y in b)); return 1-(sum(x*y for x,y in zip(a,b))/d if d else 0)
        return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))
    def predict(self,f,metric=None):
        m=metric or self.model['metric']; arr=[]
        for cl in ['A','B']:
            for x,p in self.features[cl]: arr.append((self.dist(f,x,m),cl))
        arr.sort(); k=min(3,len(arr)); near=arr[:k]; ca=sum(x[1]=='A' for x in near); cb=k-ca; cl='A' if ca>=cb else 'B'; conf=max(ca,cb)/k
        return cl,conf,'nearest=' + ', '.join(f'{c}:{d:.3f}' for d,c in near)
    def lesson4(self):
        self.clear(); self.header('04 • Sound AI','เรียนรู้ Waveform, RMS Energy, Zero Crossing และ Sound Feature')
        b=self.scrollbody(); self.card(b,'LEARN','ใน tc(2) มีสื่อเสียง เช่น Bird, Cat, Dog, Duck ฯลฯ บทนี้ใช้ WAV เพื่อแสดงว่าคอมพิวเตอร์เปลี่ยน “เสียง” ให้เป็นตัวเลขอย่างไร')
        c=self.card(b,'TRY • วิเคราะห์ WAV'); result=tk.StringVar(value='เลือกไฟล์ .wav'); tk.Label(c,textvariable=result,bg='white',fg=TEXT,font=('Consolas',10),justify='left').pack(anchor='w',padx=18,pady=8)
        def openwav():
            p=filedialog.askopenfilename(filetypes=[('WAV','*.wav')]);
            if not p:return
            try:
                with wave.open(p,'rb') as w:
                    n=w.getnframes(); rate=w.getframerate(); sw=w.getsampwidth(); ch=w.getnchannels(); raw=w.readframes(min(n,rate*5))
                if sw==1: vals=[x-128 for x in raw]
                elif sw==2:
                    import struct; vals=list(struct.unpack('<'+'h'*(len(raw)//2),raw))
                else: vals=[]
                if vals:
                    rms=math.sqrt(sum(x*x for x in vals)/len(vals)); zc=sum((vals[i]>=0)!=(vals[i-1]>=0) for i in range(1,len(vals)))/len(vals)
                    result.set(f'{Path(p).name}\nSample rate={rate} Hz | channels={ch} | duration={n/rate:.2f}s\nRMS Energy={rms:.1f} | Zero-crossing rate={zc:.4f}'); self.done(4,100)
                else: result.set('รองรับ WAV PCM 8/16-bit ในบทเรียนนี้')
            except Exception as e: result.set(str(e))
        ttk.Button(c,text='เลือก WAV และวิเคราะห์',command=openwav).pack(anchor='w',padx=18,pady=12)
        self.card(b,'MATH','RMS = √mean(x²) ใช้วัดพลังงานของสัญญาณ • Zero Crossing = สัดส่วนครั้งที่สัญญาณเปลี่ยนเครื่องหมาย ใช้อธิบายลักษณะความถี่อย่างง่าย')
    def lesson5(self):
        self.clear(); self.header('05 • Live AI + Math','ทดลอง Prediction และเปรียบเทียบคณิตศาสตร์ของ Distance Metric')
        b=self.scrollbody(); self.card(b,'LEARN','โมเดลเดียวกันสามารถให้ผลต่างกันเมื่อเปลี่ยนวิธีวัด “ความใกล้” นี่คือจุดเชื่อม Math ↔ AI')
        c=self.card(b,'EXPERIMENT • ภาพเดียว 3 วิธี'); out=tk.Text(c,height=10,font=('Consolas',10)); out.pack(fill='x',padx=18,pady=8)
        def compare():
            if not self.model: messagebox.showwarning('Model','กรุณา Train Image AI ในบท 03 ก่อน');return
            p=filedialog.askopenfilename(filetypes=[('Images','*.png *.jpg *.jpeg *.bmp *.gif')]);
            if not p:return
            f=self.imgfeat(p); out.delete('1.0','end'); out.insert('end',f'Test: {Path(p).name}\n\n')
            for m in ['euclidean','manhattan','cosine']:
                cl,cf,de=self.predict(f,m); out.insert('end',f'{m:10s} → Class {cl} | confidence {cf:.1%}\n')
            self.done(5,100)
        ttk.Button(c,text='เลือกภาพและเปรียบเทียบ',style='Primary.TButton',command=compare).pack(anchor='w',padx=18,pady=12)
        ttk.Button(c,text='เปิด Math Comparison Lab',command=self.math_lab).pack(anchor='w',padx=18,pady=(0,12))
    def lesson6(self):
        self.clear(); self.header('06 • v4 Vision → AI → Robot Lab','Simulation + Manual Control + AI Decision → Robot Command')
        b=self.scrollbody(); self.card(b,'LEARN','Robot AI = Sense → Predict → Decide → Act. ใน Simulation นักเรียนเห็นผลทันที ก่อนเชื่อม Arduino/KidBright จริง')
        c=self.card(b,'ROBOT SIMULATOR'); area=tk.Frame(c,bg='white'); area.pack(fill='x',padx=18,pady=8)
        cv=tk.Canvas(area,width=560,height=330,bg='#eef5f8',highlightthickness=1,highlightbackground=BORDER); cv.grid(row=0,column=0,rowspan=3,padx=(0,18)); self.robot=(280,165)
        def draw():
            cv.delete('all'); cv.create_rectangle(8,8,552,322,outline='#b8c7d4'); x,y=self.robot; cv.create_oval(x-22,y-22,x+22,y+22,fill='#20a4d8',outline=''); cv.create_polygon(x,y-30,x-9,y-15,x+9,y-15,fill='#14213d'); cv.create_text(280,20,text='Robot World  •  Simulation',fill=MUTED)
        log=tk.Text(area,width=48,height=11,font=('Consolas',9)); log.grid(row=0,column=1,sticky='nsew')
        def move(cmd):
            x,y=self.robot; step=25
            if cmd=='FORWARD': y=max(40,y-step)
            elif cmd=='BACKWARD': y=min(295,y+step)
            elif cmd=='LEFT': x=max(35,x-step)
            elif cmd=='RIGHT': x=min(525,x+step)
            self.robot=(x,y); draw(); log.insert('end',f'AI/Student → {cmd}\n'); log.see('end'); self.done(6,70)
            if self.robot_serial:
                try:self.robot_serial.write((cmd+'\n').encode())
                except:pass
        pad=tk.Frame(area,bg='white'); pad.grid(row=1,column=1,pady=8)
        ttk.Button(pad,text='▲ FORWARD',command=lambda:move('FORWARD')).grid(row=0,column=1); ttk.Button(pad,text='◀ LEFT',command=lambda:move('LEFT')).grid(row=1,column=0); ttk.Button(pad,text='■ STOP',command=lambda:move('STOP')).grid(row=1,column=1); ttk.Button(pad,text='RIGHT ▶',command=lambda:move('RIGHT')).grid(row=1,column=2); ttk.Button(pad,text='▼ BACK',command=lambda:move('BACKWARD')).grid(row=2,column=1); draw()
        ai=tk.Frame(c,bg='white'); ai.pack(fill='x',padx=18,pady=8); tk.Label(ai,text='AI Rule:',bg='white').pack(side='left'); rule=tk.StringVar(value='Class A → LEFT | Class B → RIGHT'); tk.Label(ai,textvariable=rule,bg='white',fg=BLUE).pack(side='left',padx=10)
        def airobot():
            if not self.model: messagebox.showwarning('AI','Train Image AI ก่อน');return
            p=filedialog.askopenfilename(filetypes=[('Images','*.png *.jpg *.jpeg *.bmp *.gif')]);
            if p:
                cl,cf,_=self.predict(self.imgfeat(p)); cmd='LEFT' if cl=='A' else 'RIGHT'; log.insert('end',f'Prediction Class {cl} ({cf:.0%}) → {cmd}\n'); move(cmd); self.done(6,100)
        ttk.Button(ai,text='เลือกภาพ → AI สั่ง Robot',style='Primary.TButton',command=airobot).pack(side='left')
    def lesson7(self):
        self.clear(); self.header('07 • AI Agent','Sense → Think → Decide → Act → Feedback')
        b=self.scrollbody(); self.card(b,'LEARN','Agent ไม่ได้หยุดที่ Prediction แต่รับสถานะ → ใช้เหตุผล/กฎ → เลือก Action → ตรวจ Feedback แล้ววนซ้ำ')
        c=self.card(b,'AGENT SIMULATION'); sensor=tk.IntVar(value=30); goal=tk.StringVar(value='Avoid danger'); out=tk.Text(c,height=9,font=('Consolas',10)); out.pack(fill='x',padx=18,pady=8)
        ttk.Scale(c,from_=0,to=100,variable=sensor).pack(fill='x',padx=18)
        def run():
            s=sensor.get(); action='STOP' if s>=70 else ('SLOW' if s>=45 else 'FORWARD'); out.delete('1.0','end'); out.insert('end',f'SENSE    sensor={s}\nTHINK    goal={goal.get()}\nDECIDE   risk={"high" if s>=70 else "medium" if s>=45 else "low"}\nACT      {action}\nFEEDBACK observe next sensor value\n'); self.done(7,100)
        ttk.Button(c,text='Run Agent Cycle',style='Primary.TButton',command=run).pack(anchor='w',padx=18,pady=12)
    def lesson8(self):
        self.clear(); self.header('08 • Project Studio','เปลี่ยนสิ่งที่เรียนเป็น Mini Project พร้อม Design Canvas')
        b=self.scrollbody(); self.card(b,'PROJECT CHALLENGE','สร้างระบบ AI ที่มีอย่างน้อย 1 Dataset + 1 Model + 1 Math explanation + 1 Decision + 1 Output/Robot')
        c=self.card(b,'PROJECT CANVAS'); fields={}
        for lab in ['Project name','Problem / ผู้ใช้','Input / Sensor','Class A','Class B','Math used','AI decision','Robot / Output','How to evaluate']:
            r=tk.Frame(c,bg='white'); r.pack(fill='x',padx=18,pady=4); tk.Label(r,text=lab,width=18,anchor='w',bg='white',fg=TEXT).pack(side='left'); e=ttk.Entry(r); e.pack(side='left',fill='x',expand=True); fields[lab]=e
        def save():
            d={k:e.get().strip() for k,e in fields.items()};
            if not d['Project name']: messagebox.showwarning('Project','กรุณาตั้งชื่อ Project');return
            p=filedialog.asksaveasfilename(defaultextension='.json',filetypes=[('Project JSON','*.json')]);
            if p:
                Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8'); self.done(8,100); messagebox.showinfo('Saved','บันทึก Project Canvas แล้ว')
        ttk.Button(c,text='Save Project Canvas',style='Primary.TButton',command=save).pack(anchor='w',padx=18,pady=14)
        self.card(b,'ตัวอย่าง','AI Sorting Robot: กล้องรับภาพวัตถุ → Image AI แยก Class A/B → เปรียบเทียบ Euclidean/Cosine → เลือก Class → Servo/Robot แยกวัตถุ → วัด Accuracy และ Confusion Matrix')
    def _find_tc_zip(self):
        for p in [Path('/mnt/data/TC(1).zip'),Path('/mnt/data/tc(2).zip'),Path('TC(1).zip'),Path('tc(2).zip'),Path('tc.zip')]:
            if p.exists(): return str(p)
        return ''
    def _tc_entries(self):
        if not self.tc_zip or not Path(self.tc_zip).exists(): return []
        try:
            with zipfile.ZipFile(self.tc_zip) as z:
                return [n for n in z.namelist() if n.lower().endswith(('.pas','.c','.cpp','.h'))]
        except:return []
    def _read_tc(self,name):
        with zipfile.ZipFile(self.tc_zip) as z: data=z.read(name)
        for enc in ('utf-8','cp874','latin1'):
            try:return data.decode(enc)
            except:pass
        return data.decode('latin1','replace')
    def tc_code_lab(self):
        self.clear(); self.header('⌘ • TC Code Lab','เปิด Source Code เดิม → หา Math/Algorithm → ทดลองแนวคิดเดียวกันแบบสมัยใหม่')
        b=self.scrollbody(); intro=self.card(b,'WHY TC MATTERS','เราไม่ทิ้ง code เดิม แต่ใช้เป็น “computational archaeology”: อ่าน Pascal/C → ระบุสูตร/algorithm → ทดลองด้วย Python/AI → อธิบายว่าคณิตศาสตร์เดิมเชื่อมกับ AI อย่างไร')
        c=self.card(b,'SOURCE BROWSER'); bar=tk.Frame(c,bg='white'); bar.pack(fill='x',padx=18,pady=8)
        tk.Label(bar,text='TC ZIP:',bg='white').pack(side='left'); zvar=tk.StringVar(value=self.tc_zip or 'ยังไม่พบไฟล์'); ttk.Entry(bar,textvariable=zvar,width=65).pack(side='left',padx=8)
        def pickzip():
            p=filedialog.askopenfilename(filetypes=[('ZIP','*.zip')]);
            if p: self.tc_zip=p; zvar.set(p); loadlist()
        ttk.Button(bar,text='เลือก ZIP',command=pickzip).pack(side='left')
        panes=tk.PanedWindow(c,orient='horizontal',bg='white',sashwidth=5); panes.pack(fill='both',expand=True,padx=18,pady=8)
        left=tk.Frame(panes,bg='white'); right=tk.Frame(panes,bg='white'); panes.add(left,minsize=280); panes.add(right,minsize=650)
        search=tk.StringVar(); ttk.Entry(left,textvariable=search).pack(fill='x',pady=(0,5)); lb=tk.Listbox(left,height=23,font=('Consolas',9)); lb.pack(fill='both',expand=True)
        txt=tk.Text(right,height=23,font=('Consolas',9),wrap='none'); txt.pack(fill='both',expand=True)
        info=tk.StringVar(value='เลือกไฟล์ เช่น CIRCLE.PAS, PARAX.PAS, COMPARE.PAS, SORT.PAS, MCALC.C'); tk.Label(c,textvariable=info,bg='white',fg=BLUE,justify='left',wraplength=1050).pack(anchor='w',padx=18,pady=(0,8))
        allnames=[]
        def loadlist(*_):
            nonlocal allnames; lb.delete(0,'end'); allnames=self._tc_entries(); q=search.get().lower().strip()
            preferred=['caimath','sort','math','stat','calc','robot','graph','tree','genetic']
            names=[n for n in allnames if not q or q in n.lower()]; names.sort(key=lambda n:(0 if any(k in n.lower() for k in preferred) else 1,n.lower()))
            for n in names[:1500]: lb.insert('end',n)
        def openone(_=None):
            if not lb.curselection():return
            n=lb.get(lb.curselection()[0]); code=self._read_tc(n); txt.delete('1.0','end'); txt.insert('1.0',code[:80000])
            low=n.lower(); links=[]
            if 'circle' in low: links=['Geometry: x²+y²=r²','Area=πr²','ใช้สร้าง radial feature / distance ใน AI']
            elif 'para' in low: links=['Parabola / quadratic','y=ax²+bx+c','เชื่อม Polynomial Regression / loss curve']
            elif 'ellipse' in low: links=['Ellipse','normalized distance','เชื่อม covariance / confidence ellipse']
            elif 'sort' in low: links=['Sorting','comparison + complexity','เชื่อม ranking nearest neighbors ใน k-NN']
            elif 'calc' in low: links=['Expression/Calculation','parser + numerical computation','เชื่อม feature engineering pipeline']
            elif 'math' in low or 'stat' in low: links=['Math/Statistics library','functions + numerical errors','เชื่อม normalization, probability, model metrics']
            else: links=['Algorithm → inputs → process → outputs','ให้นักเรียนระบุ Math ที่พบและสร้าง modern experiment']
            info.set(' • '.join(links)); self.done(1,100)
        search.trace_add('write',loadlist); lb.bind('<<ListboxSelect>>',openone); loadlist()
        lab=self.card(b,'MODERN MATH EXPERIMENT • Geometry → AI Distance','ปรับจุด (x,y) แล้วเปรียบเทียบ Euclidean กับ Manhattan และดูว่าแนวคิด “ระยะ” เชื่อมจากกราฟเรขาคณิตใน TC ไปยัง k-NN อย่างไร')
        row=tk.Frame(lab,bg='white'); row.pack(fill='x',padx=18,pady=8); vals=[]
        for label,val in [('x1','1'),('y1','2'),('x2','5'),('y2','7')]:
            tk.Label(row,text=label,bg='white').pack(side='left'); e=ttk.Entry(row,width=7);e.insert(0,val);e.pack(side='left',padx=4);vals.append(e)
        out=tk.StringVar(); tk.Label(lab,textvariable=out,bg='white',fg=TEXT,font=('Consolas',11)).pack(anchor='w',padx=18,pady=5)
        def calc():
            try:
                x1,y1,x2,y2=[float(e.get()) for e in vals]; eu=math.hypot(x2-x1,y2-y1); ma=abs(x2-x1)+abs(y2-y1); out.set(f'Euclidean = {eu:.4f}   |   Manhattan = {ma:.4f}   → k-NN ใช้แนวคิด distance แบบเดียวกัน')
            except: out.set('กรุณาใส่ตัวเลข')
        ttk.Button(lab,text='คำนวณและเชื่อมกับ AI',command=calc).pack(anchor='w',padx=18,pady=(0,12)); calc()
    def teacher_mode(self):
        self.clear(); self.header('▣ • Teacher Mode','ดูความก้าวหน้า คะแนน และสร้าง/ส่งออกผลการเรียน')
        b=self.scrollbody(); c=self.card(b,'CLASS / STUDENT DASHBOARD'); row=tk.Frame(c,bg='white'); row.pack(fill='x',padx=18,pady=8)
        tk.Label(row,text='ชื่อนักเรียน',bg='white').pack(side='left'); name=tk.StringVar(value=self.student_name); ttk.Entry(row,textvariable=name,width=30).pack(side='left',padx=8)
        table=tk.Frame(c,bg='white'); table.pack(fill='x',padx=18,pady=8)
        names=['Coding','Dataset','Image AI','Sound AI','AI + Math','Robot AI','AI Agent','Project']
        scorevars=[]
        for i,n in enumerate(names,1):
            tk.Label(table,text=f'{i:02d} {n}',width=22,anchor='w',bg='white').grid(row=i-1,column=0,sticky='w',pady=3); v=tk.IntVar(value=self.scores[str(i)]); scorevars.append(v); ttk.Spinbox(table,from_=0,to=100,textvariable=v,width=7).grid(row=i-1,column=1); tk.Label(table,text=f'progress {self.progress[str(i)]}%',bg='white',fg=MUTED).grid(row=i-1,column=2,padx=12)
        total=tk.StringVar(); tk.Label(c,textvariable=total,bg='white',fg=BLUE,font=('Segoe UI Semibold',12)).pack(anchor='w',padx=18,pady=8)
        def update():
            self.student_name=name.get().strip() or 'Student';
            for i,v in enumerate(scorevars,1): self.scores[str(i)]=max(0,min(100,int(v.get())))
            avg=sum(self.scores.values())/8; total.set(f'Average score = {avg:.1f}/100  |  Completed progress = {sum(self.progress.values())/8:.1f}%')
        def export():
            update(); p=filedialog.asksaveasfilename(defaultextension='.csv',filetypes=[('CSV','*.csv')]);
            if p:
                with open(p,'w',newline='',encoding='utf-8-sig') as f:
                    w=csv.writer(f); w.writerow(['Student','Module','Score','Progress']);
                    for i,n in enumerate(names,1):w.writerow([self.student_name,f'{i:02d} {n}',self.scores[str(i)],self.progress[str(i)]])
                messagebox.showinfo('Teacher Mode','ส่งออกคะแนนแล้ว')
        ttk.Button(c,text='Update scores',command=update).pack(side='left',padx=18,pady=12); ttk.Button(c,text='Export CSV',command=export).pack(side='left',pady=12); update()
        self.card(b,'ASSESSMENT RUBRIC','แนะนำ 100 คะแนน/บท: Concept 20 • Experiment 25 • Math explanation 25 • Code/Algorithm 15 • Reflection 15\nครูสามารถปรับคะแนนเองได้ เพื่อรองรับทั้งงานเดี่ยวและงานกลุ่ม')
    def worksheets(self):
        self.clear(); self.header('▤ • Worksheets','ใบงาน 01–08 เชื่อม TC Code → Math → AI → Robot')
        b=self.scrollbody(); topics=[
        ('01 Algorithm','เปิด SORT.PAS หรือ code sorting จาก TC • วาด flowchart • อธิบาย comparison • ทดลองเรียง 8 ตัวเลข'),
        ('02 Dataset','สร้าง Class A/B อย่างน้อย 10 ตัวอย่าง • อธิบาย label และ class imbalance • บันทึกจำนวนข้อมูล'),
        ('03 Image AI','Train k-NN • อธิบาย feature RGB/brightness/variance • ทดสอบอย่างน้อย 10 ภาพ'),
        ('04 Sound AI','เลือก WAV • คำนวณ RMS และ Zero Crossing • อธิบายว่า feature แทนเสียงอย่างไร'),
        ('05 Math + AI','เปรียบเทียบ Euclidean/Manhattan/Cosine • Mean/Variance/Z-score • Confusion Matrix + Precision/Recall/F1'),
        ('06 Robot AI','กำหนด Class→Action • ทดลอง simulator • เขียน pseudocode และทดสอบ Serial/Arduino เมื่อพร้อม'),
        ('07 AI Agent','ออกแบบ Sense→Think→Decide→Act→Feedback • เปลี่ยน threshold แล้วบันทึกพฤติกรรม'),
        ('08 Project','เลือก code TC อย่างน้อย 1 ชิ้น • อธิบาย Math เดิม • ดัดแปลงเป็น AI/Robot project • ประเมินผลด้วย metric')]
        for t,d in topics:self.card(b,t,d)
        c=self.card(b,'EXPORT WORKSHEET','สร้างไฟล์ข้อความใบงานสำหรับแจกนักเรียนหรือแก้ไขต่อใน Word')
        def export():
            p=filedialog.asksaveasfilename(defaultextension='.txt',filetypes=[('Text','*.txt')]);
            if not p:return
            lines=['AI LEARNING STUDIO — TC MATH WORKSHEETS','Name: __________________  Class: __________','']
            for t,d in topics: lines += [t,d,'Evidence / Answer:','____________________________________________________________','']
            Path(p).write_text('\n'.join(lines),encoding='utf-8'); messagebox.showinfo('Worksheets','สร้างใบงานแล้ว')
        ttk.Button(c,text='Export Student Worksheet',style='Primary.TButton',command=export).pack(anchor='w',padx=18,pady=12)

    def _museum_source(self, candidates):
        zips=[]
        for x in [self.tc_zip,'/mnt/data/tc(2).zip','/mnt/data/TC(1).zip','tc(2).zip','TC(1).zip']:
            if x and Path(x).exists() and x not in zips: zips.append(x)
        for zp in zips:
            try:
                with zipfile.ZipFile(zp) as z:
                    names=z.namelist()
                    for c in candidates:
                        hit=next((n for n in names if n.lower().endswith(c.lower())),None)
                        if hit:
                            data=z.read(hit)
                            for enc in ('utf-8','cp874','latin1'):
                                try:return hit,data.decode(enc)
                                except:pass
            except: pass
        return '', 'ไม่พบ source ใน ZIP ที่เลือก'

    def tc_math_museum(self):
        self.clear(); self.header('🏛 • TC Math Museum','Original TC/Pascal/C → Formula → Interactive Graph → Modern AI Connection → Challenge')
        b=self.scrollbody(); self.card(b,'แนวคิดของ Museum','นักเรียนไม่ได้เพียงอ่าน code เก่า แต่ทดลองสมการที่ code ใช้ แล้วเชื่อมไปยัง AI สมัยใหม่ ทุก Exhibit มี Source, Math, Simulation, Python idea และโจทย์')
        nb=ttk.Notebook(b); nb.pack(fill='both',expand=True,padx=28,pady=12)
        exhibits=[
          ('Circle',['/caimath/CIRCLE.PAS','/EXAMPLES/CIRCLE.CPP'],'x² + y² = r²','Euclidean distance → k-NN / clustering'),
          ('Parabola',['/caimath/PARAX.PAS','/caimath/PARAY.PAS'],'y = ax² + bx + c','Quadratic model → regression / loss curve'),
          ('Ellipse',['/caimath/ELLIPSEX.PAS','/caimath/ELLIPSEY.PAS'],'x²/a² + y²/b² = 1','Normalized distance → covariance / anomaly boundary'),
          ('Sorting',['/SORT/BUBBLE.PAS','/SORT/HEAP.PAS','/SORT/ALLSORT.PAS'],'compare → swap → repeat','Rank distances → nearest neighbors / top-k'),
          ('Statistics',['/EXAMPLES/MCALC.C','/INCLUDE/MATH.H','/INCLUDE/SYS/STAT.H'],'mean, variance, standard deviation, z-score','Feature scaling → anomaly detection / model metrics'),
          ('Probability',['/EXAMPLES/MCALC.C','/INCLUDE/MATH.H'],'P(class|x), exp(score)/Σexp(score)','Scores → Softmax probability / confidence'),
          ('Decision Tree',['/TREE/TREE.C','/TREE/BINTREE.C','/TREE/BST.C'],'if feature ≤ threshold → branch','Node / branch / leaf → classification')]
        for title,cands,formula,ai in exhibits:
            f=tk.Frame(nb,bg='white'); nb.add(f,text=title)
            path,src=self._museum_source(cands)
            top=tk.Frame(f,bg='white'); top.pack(fill='x',padx=14,pady=10)
            tk.Label(top,text=formula,font=('Segoe UI Semibold',13),fg=BLUE,bg='white').pack(anchor='w')
            tk.Label(top,text='AI connection: '+ai,font=('Segoe UI',10),fg=MUTED,bg='white').pack(anchor='w')
            pan=tk.PanedWindow(f,orient='horizontal',sashwidth=5,bg='white'); pan.pack(fill='both',expand=True,padx=14,pady=6)
            left=tk.Frame(pan,bg='white'); right=tk.Frame(pan,bg='white'); pan.add(left,minsize=430); pan.add(right,minsize=430)
            tk.Label(left,text='Original TC source  •  '+(path or 'not found'),bg='white',fg=TEXT,font=('Segoe UI Semibold',10)).pack(anchor='w')
            st=tk.Text(left,height=22,font=('Consolas',8),wrap='none'); st.pack(fill='both',expand=True); st.insert('1.0',src[:14000]); st.configure(state='disabled')
            cv=tk.Canvas(right,width=480,height=260,bg='#f7fafc',highlightbackground=BORDER,highlightthickness=1); cv.pack(fill='x',pady=(0,8))
            controls=tk.Frame(right,bg='white'); controls.pack(fill='x'); val=tk.DoubleVar(value=50); ttk.Scale(controls,from_=10,to=90,variable=val).pack(side='left',fill='x',expand=True,padx=(0,8))
            out=tk.StringVar(); tk.Label(right,textvariable=out,bg='white',fg=TEXT,font=('Consolas',9),justify='left').pack(anchor='w',pady=5)
            def draw(_=None, title=title, cv=cv, val=val, out=out):
                cv.delete('all'); w=max(460,cv.winfo_width()); h=260; cx=w/2; cy=h/2; k=val.get()/50
                cv.create_line(10,cy,w-10,cy,fill='#cbd5e1'); cv.create_line(cx,10,cx,h-10,fill='#cbd5e1')
                if title=='Circle':
                    r=35+val.get(); cv.create_oval(cx-r,cy-r,cx+r,cy+r,outline=BLUE,width=3); out.set(f'r={r:.1f}   area=πr²={math.pi*r*r:.1f}   distance from center = √(x²+y²)')
                elif title=='Parabola':
                    pts=[]; a=.004*k
                    for x in range(20,int(w-20),3):
                        xx=x-cx; y=cy+a*xx*xx-70
                        pts += [x,y]
                    cv.create_line(*pts,fill=BLUE,width=3,smooth=True); out.set(f'a={a:.4f}   y=ax²-70   larger a → narrower curve')
                elif title=='Ellipse':
                    a=60+val.get(); bb=35+val.get()/2; cv.create_oval(cx-a,cy-bb,cx+a,cy+bb,outline=BLUE,width=3); out.set(f'a={a:.1f}, b={bb:.1f}   normalized boundary: x²/a² + y²/b² = 1')
                elif title=='Sorting':
                    random.seed(int(val.get())); arr=[random.randint(15,100) for _ in range(8)]; sw=sorted(arr); bw=(w-40)/8
                    for i,n in enumerate(arr): cv.create_rectangle(20+i*bw,h-20-n,15+(i+1)*bw,h-20,fill='#94a3b8',outline='')
                    out.set('input  = '+str(arr)+'\nsorted = '+str(sw)+'\nAI: sort distances then choose the k smallest')
                elif title=='Statistics':
                    xs=[10,12,13,15,20,int(val.get())]; mu=statistics.mean(xs); sd=statistics.pstdev(xs); bw=(w-40)/len(xs)
                    for i,n in enumerate(xs): cv.create_rectangle(20+i*bw,h-20-n*4,15+(i+1)*bw,h-20,fill='#94a3b8',outline='')
                    out.set(f'data={xs}\nmean={mu:.2f}  std={sd:.2f}  z(last)={(xs[-1]-mu)/sd if sd else 0:.2f}')
                elif title=='Probability':
                    scores=[1.0,val.get()/30,0.5]; ex=[math.exp(x) for x in scores]; sm=[x/sum(ex) for x in ex]; bw=(w-60)/3
                    for i,pv in enumerate(sm):
                        x0=30+i*bw; cv.create_rectangle(x0,h-25-pv*170,x0+bw-18,h-25,fill='#94a3b8',outline=''); cv.create_text(x0+(bw-18)/2,h-12,text=f'{pv:.2f}')
                    out.set('scores='+str([round(x,2) for x in scores])+'\nsoftmax='+str([round(x,3) for x in sm])+'   ΣP=1.000')
                else:
                    th=val.get(); x=val.get()+12; decision='Class B' if x>th else 'Class A'
                    cv.create_line(cx,65,cx,85,width=3,fill='#64748b'); cv.create_oval(cx-45,20,cx+45,65,outline=BLUE,width=3); cv.create_text(cx,42,text=f'x ≤ {th:.0f}?')
                    cv.create_line(cx,85,cx-110,145,width=3,fill='#64748b'); cv.create_line(cx,85,cx+110,145,width=3,fill='#64748b'); cv.create_text(cx-70,105,text='Yes'); cv.create_text(cx+70,105,text='No')
                    cv.create_rectangle(cx-155,145,cx-65,190,outline='#64748b'); cv.create_rectangle(cx+65,145,cx+155,190,outline='#64748b'); cv.create_text(cx-110,167,text='Class A'); cv.create_text(cx+110,167,text='Class B')
                    out.set(f'threshold={th:.1f}, test x={x:.1f} → {decision}\nDecision tree = repeated IF/ELSE branches')
            val.trace_add('write',draw); cv.bind('<Configure>',draw); draw()
            py=tk.Text(right,height=6,font=('Consolas',9),bg='#f8fafc'); py.pack(fill='x',pady=5)
            snippets={'Circle':'d = math.sqrt((x-cx)**2 + (y-cy)**2)\n# k-NN ranks nearby samples', 'Parabola':'y = a*x*x + b*x + c\n# regression learns coefficients', 'Ellipse':'score = (x/a)**2 + (y/b)**2\ninside = score <= 1\n# normalized boundary', 'Sorting':'distances.sort(key=lambda item: item[0])\nneighbors = distances[:k]\n# top-k nearest samples', 'Statistics':'mu = statistics.mean(x)\nsd = statistics.pstdev(x)\nz = [(v-mu)/sd for v in x]\n# standardization', 'Probability':'e = [math.exp(s) for s in scores]\np = [v/sum(e) for v in e]\n# softmax probability', 'Decision Tree':'if feature <= threshold:\n    prediction = "Class A"\nelse:\n    prediction = "Class B"'}
            py.insert('1.0',snippets[title]); py.configure(state='disabled')
            ttk.Button(right,text='ทำ Exhibit นี้สำเร็จ ✓ (+100)',command=lambda t=title:self._museum_complete(t)).pack(anchor='w',pady=5)
        q=self.card(b,'MUSEUM CHALLENGE','คำถาม: ถ้าเราคำนวณระยะจากภาพทดสอบไปยังตัวอย่างทุกภาพ แล้วเรียงจากน้อยไปมาก ขั้นตอนนี้เชื่อม TC Sorting กับ AI อะไร?')
        av=tk.StringVar(); ttk.Combobox(q,textvariable=av,values=['k-Nearest Neighbors','Random number','Audio playback'],state='readonly',width=28).pack(anchor='w',padx=18,pady=6)
        ttk.Button(q,text='ตรวจคำตอบ',command=lambda:messagebox.showinfo('Challenge','ถูกต้อง — Sorting ใช้จัดอันดับ distance เพื่อหา nearest neighbors' if av.get()=='k-Nearest Neighbors' else 'ลองใหม่: คิดถึงการเลือกตัวอย่างที่ “ใกล้ที่สุด”')).pack(anchor='w',padx=18,pady=8)

    def _museum_complete(self,title):
        self.museum_scores[title]=100
        total=sum(self.museum_scores.values())
        self.done(5,min(100,round(total/7)))
        messagebox.showinfo('Museum Progress',f'{title}: 100/100\nคะแนน Museum รวม {total}/700')

    def webcam_robot_lab(self):
        self.clear(); self.header('📷 • Webcam → AI → Robot Lab','Live camera → Feature/Prediction → Decision → Simulator + Serial Robot')
        b=self.scrollbody(); self.card(b,'PIPELINE','Webcam frame → RGB/brightness features → trained Class A/B (ถ้ามี) → A=LEFT, B=RIGHT → Robot simulator → optional Serial/Arduino/KidBright')
        c=self.card(b,'LIVE LAB'); row=tk.Frame(c,bg='white'); row.pack(fill='x',padx=18,pady=8)
        view=tk.Label(row,text='Webcam preview\nกด Start Camera',bg='#111827',fg='white',width=70,height=20); view.grid(row=0,column=0,rowspan=3,padx=(0,16),sticky='nsew')
        side=tk.Frame(row,bg='white'); side.grid(row=0,column=1,sticky='nsew'); status=tk.StringVar(value='Camera: stopped'); pred=tk.StringVar(value='Prediction: —'); cmdv=tk.StringVar(value='Robot command: STOP')
        for v in (status,pred,cmdv): tk.Label(side,textvariable=v,bg='white',fg=TEXT,font=('Segoe UI Semibold',10),wraplength=330,justify='left').pack(anchor='w',pady=4)
        sim=tk.Canvas(side,width=330,height=220,bg='#eef5f8',highlightbackground=BORDER,highlightthickness=1); sim.pack(pady=8); pos=[165,110]
        def drawbot():
            sim.delete('all'); sim.create_rectangle(8,8,322,212,outline='#cbd5e1'); x,y=pos; sim.create_oval(x-18,y-18,x+18,y+18,fill=BLUE,outline=''); sim.create_text(165,18,text='Robot simulation',fill=MUTED)
        drawbot(); running={'on':False}; cap={'obj':None}; last={'cmd':'STOP','t':0}
        def send(cmd):
            now=time.time(); cmdv.set('Robot command: '+cmd)
            if now-last['t']>.35 or cmd!=last['cmd']:
                x,y=pos
                if cmd=='LEFT':x=max(30,x-12)
                elif cmd=='RIGHT':x=min(300,x+12)
                elif cmd=='FORWARD':y=max(35,y-12)
                elif cmd=='BACKWARD':y=min(190,y+12)
                pos[:]=[x,y]; drawbot(); last.update(cmd=cmd,t=now)
                if self.robot_serial:
                    try:self.robot_serial.write((cmd+'\n').encode())
                    except Exception as e: status.set('Serial error: '+str(e))
        def feature_frame(frame):
            small=cv2.resize(frame,(64,64)); b0,g0,r0=[float(x) for x in cv2.mean(small)[:3]]; gray=cv2.cvtColor(small,cv2.COLOR_BGR2GRAY); return [r0/255,g0/255,b0/255,float(gray.mean())/255,float(gray.std())/128]
        def tick():
            if not running['on']: return
            ok,frame=cap['obj'].read() if cap['obj'] is not None else (False,None)
            if not ok: status.set('อ่านภาพจากกล้องไม่ได้'); running['on']=False; return
            feat=feature_frame(frame)
            if self.model:
                cl,cf,_=self.predict(feat); cmd='LEFT' if cl=='A' else 'RIGHT'; pred.set(f'Prediction: Class {cl}  confidence {cf:.1%}')
            else:
                bright=feat[3]; cl='A' if bright<.5 else 'B'; cf=abs(bright-.5)*2; cmd='LEFT' if cl=='A' else 'RIGHT'; pred.set(f'Demo brightness: {bright:.2f} → Class {cl}  confidence {cf:.1%}\n(Train Image AI เพื่อใช้ dataset จริง)')
            send(cmd)
            rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB); rgb=cv2.resize(rgb,(640,360))
            if Image is not None:
                im=Image.fromarray(rgb); photo=ImageTk.PhotoImage(im); view.configure(image=photo,text=''); view.image=photo
            if running['on']: self.after(60,tick)
        def start():
            if cv2 is None or Image is None: messagebox.showerror('Webcam','ต้องติดตั้ง: pip install opencv-python pillow'); return
            if running['on']: return
            cap['obj']=cv2.VideoCapture(0)
            if not cap['obj'].isOpened(): cap['obj'].release(); cap['obj']=None; messagebox.showerror('Webcam','เปิดกล้องไม่ได้ กรุณาตรวจ permission หรือ camera index'); return
            running['on']=True; status.set('Camera: LIVE'); tick()
        def stop():
            running['on']=False
            if cap['obj'] is not None: cap['obj'].release(); cap['obj']=None
            status.set('Camera: stopped'); send('STOP'); view.configure(image='',text='Webcam preview\nCamera stopped'); view.image=None
        btn=tk.Frame(side,bg='white'); btn.pack(fill='x',pady=5); ttk.Button(btn,text='▶ Start Camera',style='Primary.TButton',command=start).pack(side='left'); ttk.Button(btn,text='■ Stop',command=stop).pack(side='left',padx=6)
        serialbox=self.card(b,'REAL ROBOT • Serial / Bluetooth COM','Protocol: LEFT, RIGHT, FORWARD, BACKWARD, STOP ตามด้วย newline. ใช้ Simulation ได้แม้ยังไม่มีบอร์ด')
        sr=tk.Frame(serialbox,bg='white'); sr.pack(fill='x',padx=18,pady=8); port=tk.StringVar(); baud=tk.StringVar(value='9600'); cb=ttk.Combobox(sr,textvariable=port,width=20); cb.pack(side='left'); ttk.Combobox(sr,textvariable=baud,values=['9600','115200'],width=10,state='readonly').pack(side='left',padx=6)
        def refresh(): cb['values']=[p.device for p in list_ports.comports()] if list_ports else []
        def connect():
            if serial is None: messagebox.showerror('Serial','ติดตั้ง pyserial: pip install pyserial'); return
            try:
                if self.robot_serial: self.robot_serial.close()
                self.robot_serial=serial.Serial(port.get(),int(baud.get()),timeout=.1); status.set('Serial connected: '+port.get())
            except Exception as e: messagebox.showerror('Serial',str(e))
        ttk.Button(sr,text='Refresh COM',command=refresh).pack(side='left'); ttk.Button(sr,text='Connect Robot',command=connect).pack(side='left',padx=6); refresh()
        rule=self.card(b,'STUDENT EXPERIMENT','1) Train Class A/B ใน Image AI  2) เปิด Webcam  3) นำวัตถุ A/B หน้ากล้อง  4) ดู Prediction และ Robot  5) เปลี่ยน Dataset แล้วเปรียบเทียบผล\nMath ที่กำลังทำงาน: feature vector → distance → sort → nearest neighbors → vote → confidence → action')
        ttk.Button(rule,text='เปิด TC Math Museum เพื่อดู Math เบื้องหลัง',command=lambda:(stop(),self.tc_math_museum())).pack(anchor='w',padx=18,pady=10)
        self.protocol('WM_DELETE_WINDOW', lambda:(stop(), self.destroy()))

    def _analyze_tc_math(self, name, source):
        """Conservative pattern matcher: source stays original; visual is a verified teaching model."""
        s=(name+'\n'+source).lower()
        rules=[
            ('Circle', ['circle','radius','sqr(','sqrt('], 'x² + y² = r²', 'Euclidean distance → k-NN', 'circle'),
            ('Ellipse', ['ellipse','ellipsex','ellipsey'], 'x²/a² + y²/b² = 1', 'normalized distance → anomaly boundary', 'ellipse'),
            ('Parabola', ['parax','paray','parab','quadratic'], 'y = ax² + bx + c', 'regression / loss curve', 'parabola'),
            ('Sorting', ['bubble','heapsort','quicksort','allsort','swap'], 'compare → swap → repeat', 'rank distance → top-k / k-NN', 'sorting'),
            ('Statistics', ['mean','variance','std','stat.h','average'], 'μ=Σx/n,  σ=√(Σ(x-μ)²/n)', 'normalization / anomaly detection', 'statistics'),
            ('Tree', ['btree','binary tree','left','right','node'], 'feature ≤ threshold → branch', 'Decision Tree classification', 'tree'),
            ('Trigonometry', ['sin(','cos(','tan('], 'sin θ, cos θ, tan θ', 'angles / periodic features / vision geometry', 'trig'),
        ]
        for title,keys,formula,ai,kind in rules:
            if any(k in s for k in keys): return title,formula,ai,kind
        return 'Generic Numeric Code','f(x) / numeric operations','inspect variables → features → AI','generic'

    def _draw_tc_visual(self, cv, kind, value, info):
        cv.delete('all'); w=max(620,cv.winfo_width()); h=max(330,cv.winfo_height()); cx=w/2; cy=h/2
        cv.create_line(35,cy,w-25,cy,fill='#cbd5e1'); cv.create_line(cx,25,cx,h-25,fill='#cbd5e1')
        v=float(value)
        if kind=='circle':
            r=35+v*1.5; cv.create_oval(cx-r,cy-r,cx+r,cy+r,outline=BLUE,width=3)
            cv.create_line(cx,cy,cx+r,cy,fill=ORANGE,width=3); cv.create_text(cx+r/2,cy-12,text=f'r={r:.0f}')
            info.set(f'Area = πr² = {math.pi*r*r:.1f}\nEuclidean distance from center uses √(x²+y²).')
        elif kind=='ellipse':
            a=70+v*1.8; bb=40+v*.7; cv.create_oval(cx-a,cy-bb,cx+a,cy+bb,outline=BLUE,width=3)
            info.set(f'a={a:.1f}, b={bb:.1f}\nBoundary score = x²/a² + y²/b²; score ≤ 1 means inside.')
        elif kind=='parabola':
            a=.0015+.000055*v; pts=[]
            for x in range(35,int(w-25),3):
                xx=x-cx; y=cy-90+a*xx*xx; pts += [x,y]
            if len(pts)>3: cv.create_line(*pts,fill=BLUE,width=3,smooth=True)
            info.set(f'y = {a:.5f}x² - 90\nChanging coefficient changes curvature — the same idea used when fitting a model.')
        elif kind=='sorting':
            random.seed(int(v)); arr=[random.randint(25,180) for _ in range(9)]; bw=(w-70)/9
            for i,n in enumerate(arr):
                x=35+i*bw; cv.create_rectangle(x,h-35-n,x+bw-8,h-35,fill='#94a3b8',outline=''); cv.create_text(x+(bw-8)/2,h-20,text=str(n),font=('Segoe UI',8))
            ordered=sorted(arr); info.set('Original: '+str(arr)+'\nSorted:   '+str(ordered)+'\nAI use: sort distances and select the k smallest.')
        elif kind=='statistics':
            xs=[18,22,28,35,42,50,int(20+v*1.5)]; mu=statistics.mean(xs); sd=statistics.pstdev(xs); scale=max(xs); bw=(w-80)/len(xs)
            for i,n in enumerate(xs):
                x=40+i*bw; hh=(n/scale)*(h-100); cv.create_rectangle(x,h-45-hh,x+bw-10,h-45,fill='#94a3b8',outline='')
            y=h-45-(mu/scale)*(h-100); cv.create_line(30,y,w-25,y,fill=ORANGE,width=3); cv.create_text(100,y-12,text=f'mean={mu:.1f}',fill=ORANGE)
            info.set(f'Mean={mu:.3f}   Std={sd:.3f}\nZ(last)={(xs[-1]-mu)/sd if sd else 0:.3f} → compare values on a standardized scale.')
        elif kind=='tree':
            th=v; test=65; cv.create_oval(cx-60,35,cx+60,90,outline=BLUE,width=3); cv.create_text(cx,62,text=f'x ≤ {th:.0f}?')
            cv.create_line(cx,90,cx-150,165,width=3,fill='#64748b'); cv.create_line(cx,90,cx+150,165,width=3,fill='#64748b')
            cv.create_rectangle(cx-205,165,cx-95,220,outline='#64748b'); cv.create_rectangle(cx+95,165,cx+205,220,outline='#64748b'); cv.create_text(cx-150,192,text='Class A'); cv.create_text(cx+150,192,text='Class B')
            info.set(f'test x={test}; threshold={th:.1f} → '+('Class A' if test<=th else 'Class B')+'\nA decision tree is a sequence of threshold tests.')
        elif kind=='trig':
            amp=70; pts=[]
            for x in range(35,int(w-25),2):
                t=(x-35)/(w-60)*4*math.pi; y=cy-math.sin(t)*amp; pts += [x,y]
            cv.create_line(*pts,fill=BLUE,width=3,smooth=True); info.set('Sine wave: periodic geometry.\nAI/vision use: angles, rotations, cyclic signals and feature engineering.')
        else:
            cv.create_text(cx,cy,text='เลือก source ที่มีรูปแบบ Math ที่รู้จัก\nCircle • Parabola • Ellipse • Sort • Statistics • Tree • Trigonometry',fill=TEXT,font=('Segoe UI',14),justify='center')
            info.set('Analyzer ไม่แก้ไข source และไม่อ้างว่าแปล Pascal/C ได้ทุกโปรแกรม\nแต่จับ pattern แล้วเปิด visual experiment ที่ตรวจสอบไว้สำหรับการสอน')

    def math_lab(self):
        self.clear(); self.header('∑ • Visual Math Comparison Lab','TC .PAS/.C → Code Analyzer → Formula → Graph/Animation → Python/AI Connection')
        b=self.scrollbody(); intro=self.card(b,'VISUAL MATH LAB','เลือก source จาก TC ZIP หรือไฟล์ .PAS/.C ของนักเรียน แล้ว Python จะวิเคราะห์ pattern ทางคณิตศาสตร์และสร้างภาพทดลองที่เหมาะสม โดยยังคงแสดง Original Source ไว้เพื่อเปรียบเทียบ')
        nb=ttk.Notebook(b); nb.pack(fill='both',expand=True,padx=28,pady=12)

        # TC source visualizer
        t=tk.Frame(nb,bg='white'); nb.add(t,text='TC Code → Visual')
        toolbar=tk.Frame(t,bg='white'); toolbar.pack(fill='x',padx=14,pady=10)
        selected=tk.StringVar(value='ยังไม่ได้เลือก source'); formula=tk.StringVar(value='Formula: —'); ai=tk.StringVar(value='AI connection: —'); kind={'v':'generic'}
        ttk.Button(toolbar,text='Open .PAS / .C',command=lambda:self._tc_visual_open_file(selected,formula,ai,kind,source_box,graph,slider,visual_info)).pack(side='left')
        ttk.Button(toolbar,text='Choose from TC ZIP',command=lambda:self._tc_visual_from_zip(selected,formula,ai,kind,source_box,graph,slider,visual_info)).pack(side='left',padx=6)
        tk.Label(toolbar,textvariable=selected,bg='white',fg=MUTED,font=('Segoe UI',9)).pack(side='left',padx=10)
        pan=tk.PanedWindow(t,orient='horizontal',sashwidth=5,bg='white'); pan.pack(fill='both',expand=True,padx=14,pady=(0,10))
        lf=tk.Frame(pan,bg='white'); rf=tk.Frame(pan,bg='white'); pan.add(lf,minsize=430); pan.add(rf,minsize=560)
        tk.Label(lf,text='Original Pascal / C source',bg='white',fg=TEXT,font=('Segoe UI Semibold',11)).pack(anchor='w')
        source_box=tk.Text(lf,height=30,font=('Consolas',8),wrap='none'); source_box.pack(fill='both',expand=True); source_box.insert('1.0','เลือก CIRCLE.PAS, PARAX.PAS, BUBBLE.PAS, STAT.H หรือ source อื่นจาก TC')
        tk.Label(rf,textvariable=formula,bg='white',fg=BLUE,font=('Segoe UI Semibold',13)).pack(anchor='w'); tk.Label(rf,textvariable=ai,bg='white',fg=MUTED,font=('Segoe UI',10)).pack(anchor='w',pady=(2,7))
        graph=tk.Canvas(rf,height=350,bg='#f8fafc',highlightbackground=BORDER,highlightthickness=1); graph.pack(fill='both',expand=True)
        slider=tk.DoubleVar(value=50); ttk.Scale(rf,from_=5,to=95,variable=slider,command=lambda _ : self._draw_tc_visual(graph,kind['v'],slider.get(),visual_info)).pack(fill='x',pady=8)
        visual_info=tk.StringVar(value='เลือก source เพื่อเริ่ม Visual Experiment'); tk.Label(rf,textvariable=visual_info,bg='white',fg=TEXT,font=('Consolas',9),justify='left',wraplength=620).pack(anchor='w')
        graph.bind('<Configure>',lambda e:self._draw_tc_visual(graph,kind['v'],slider.get(),visual_info))

        # distance comparison with graph
        d=tk.Frame(nb,bg='white'); nb.add(d,text='Distance Graph')
        tk.Label(d,text='เปรียบเทียบ Euclidean / Manhattan / Cosine บนข้อมูลเดียวกัน',bg='white',fg=TEXT,font=('Segoe UI Semibold',12)).pack(anchor='w',padx=18,pady=(16,4))
        row=tk.Frame(d,bg='white'); row.pack(fill='x',padx=18); ea=ttk.Entry(row); eb=ttk.Entry(row); ea.insert(0,'0.2,0.5,0.9'); eb.insert(0,'0.8,0.4,0.3'); ea.pack(side='left',fill='x',expand=True); eb.pack(side='left',fill='x',expand=True,padx=(8,0))
        dcv=tk.Canvas(d,height=350,bg='#f8fafc',highlightbackground=BORDER,highlightthickness=1); dcv.pack(fill='x',padx=18,pady=10); dro=tk.StringVar(); tk.Label(d,textvariable=dro,bg='white',fg=TEXT,font=('Consolas',10),justify='left').pack(anchor='w',padx=18)
        def distance_graph():
            try:
                a=[float(x.strip()) for x in ea.get().split(',')]; z=[float(x.strip()) for x in eb.get().split(',')]; assert a and len(a)==len(z)
                vals=[('Euclidean',self.dist(a,z,'euclidean')),('Manhattan',self.dist(a,z,'manhattan')),('Cosine',self.dist(a,z,'cosine'))]
                dcv.delete('all'); w=max(600,dcv.winfo_width()); h=350; mx=max(v for _,v in vals) or 1; bw=(w-120)/3
                for i,(name,v) in enumerate(vals):
                    x=60+i*bw; hh=v/mx*230; dcv.create_rectangle(x,h-55-hh,x+bw-35,h-55,fill='#94a3b8',outline=''); dcv.create_text(x+(bw-35)/2,h-35,text=name); dcv.create_text(x+(bw-35)/2,h-65-hh,text=f'{v:.4f}',font=('Segoe UI Semibold',10))
                dro.set('\n'.join(f'{n:10s} = {v:.6f}' for n,v in vals)+'\n\nค่าน้อยกว่า = ใกล้กว่า แต่ metric แต่ละแบบนิยาม “ความใกล้” ต่างกัน')
            except Exception: dro.set('กรุณาใส่ vector ที่เป็นตัวเลขและมีจำนวนมิติเท่ากัน')
        ttk.Button(d,text='Draw comparison',style='Primary.TButton',command=distance_graph).pack(anchor='w',padx=18,pady=8); distance_graph()

        # statistics visual
        s=tk.Frame(nb,bg='white'); nb.add(s,text='Statistics Graph'); es=ttk.Entry(s); es.insert(0,'10,12,13,15,20,30'); es.pack(fill='x',padx=18,pady=(18,6)); scv=tk.Canvas(s,height=350,bg='#f8fafc',highlightbackground=BORDER,highlightthickness=1); scv.pack(fill='x',padx=18,pady=8); so=tk.StringVar(); tk.Label(s,textvariable=so,bg='white',fg=TEXT,font=('Consolas',10),justify='left').pack(anchor='w',padx=18)
        def stats_graph():
            try:
                x=[float(v.strip()) for v in es.get().split(',')]; mu=statistics.mean(x); sd=statistics.pstdev(x); z=[(v-mu)/sd if sd else 0 for v in x]; scv.delete('all'); w=max(600,scv.winfo_width()); h=350; lo=min(x); hi=max(x); span=(hi-lo) or 1
                for i,v in enumerate(x):
                    px=45+(w-90)*i/max(1,len(x)-1); py=h-55-(v-lo)/span*220; scv.create_oval(px-6,py-6,px+6,py+6,fill=BLUE,outline=''); scv.create_text(px,h-30,text=str(round(v,2)),font=('Segoe UI',8))
                my=h-55-(mu-lo)/span*220; scv.create_line(35,my,w-30,my,fill=ORANGE,width=3); scv.create_text(100,my-12,text=f'Mean {mu:.2f}',fill=ORANGE)
                so.set(f'Mean={mu:.4f}   Std={sd:.4f}\nZ-score={[round(v,3) for v in z]}\nกราฟช่วยให้เห็น outlier และเหตุผลที่ AI มัก normalize features')
            except Exception: so.set('ข้อมูลไม่ถูกต้อง')
        ttk.Button(s,text='Draw statistics',command=stats_graph).pack(anchor='w',padx=18,pady=6); stats_graph()

        # probability visual
        p=tk.Frame(nb,bg='white'); nb.add(p,text='Softmax Graph'); ep=ttk.Entry(p); ep.insert(0,'1.2,2.4,0.7'); ep.pack(fill='x',padx=18,pady=(18,6)); pcv=tk.Canvas(p,height=350,bg='#f8fafc',highlightbackground=BORDER,highlightthickness=1); pcv.pack(fill='x',padx=18,pady=8); po=tk.StringVar(); tk.Label(p,textvariable=po,bg='white',fg=TEXT,font=('Consolas',10)).pack(anchor='w',padx=18)
        def softmax_graph():
            try:
                z=[float(v.strip()) for v in ep.get().split(',')]; mx=max(z); ex=[math.exp(v-mx) for v in z]; sm=[v/sum(ex) for v in ex]; pcv.delete('all'); w=max(600,pcv.winfo_width()); h=350; bw=(w-90)/len(sm)
                for i,v in enumerate(sm):
                    x=45+i*bw; hh=v*240; pcv.create_rectangle(x,h-55-hh,x+bw-18,h-55,fill='#94a3b8',outline=''); pcv.create_text(x+(bw-18)/2,h-70-hh,text=f'{v:.1%}'); pcv.create_text(x+(bw-18)/2,h-30,text=f'Class {i+1}')
                po.set('Softmax = '+str([round(v,4) for v in sm])+'   ΣP = '+f'{sum(sm):.3f}')
            except Exception: po.set('ข้อมูลไม่ถูกต้อง')
        ttk.Button(p,text='Draw probabilities',command=softmax_graph).pack(anchor='w',padx=18,pady=6); softmax_graph()

        # metrics visual confusion matrix
        m=tk.Frame(nb,bg='white'); nb.add(m,text='AI Metrics Visual'); er=tk.Frame(m,bg='white'); er.pack(anchor='w',padx=18,pady=(16,6)); entries={}
        for name,val in [('TP','40'),('FP','5'),('FN','10'),('TN','45')]:
            tk.Label(er,text=name,bg='white').pack(side='left'); e=ttk.Entry(er,width=7); e.insert(0,val); e.pack(side='left',padx=(3,10)); entries[name]=e
        mcv=tk.Canvas(m,height=370,bg='#f8fafc',highlightbackground=BORDER,highlightthickness=1); mcv.pack(fill='x',padx=18,pady=8); mo=tk.StringVar(); tk.Label(m,textvariable=mo,bg='white',fg=TEXT,font=('Consolas',10),justify='left').pack(anchor='w',padx=18)
        def metrics_graph():
            try:
                tp,fp,fn,tn=[float(entries[x].get()) for x in ['TP','FP','FN','TN']]; total=tp+fp+fn+tn; acc=(tp+tn)/total if total else 0; pre=tp/(tp+fp) if tp+fp else 0; rec=tp/(tp+fn) if tp+fn else 0; f1=2*pre*rec/(pre+rec) if pre+rec else 0
                mcv.delete('all'); w=max(600,mcv.winfo_width()); x0=w/2-170; y0=55; cell=120
                labels=[('TP',tp,0,0),('FP',fp,1,0),('FN',fn,0,1),('TN',tn,1,1)]
                mx=max([tp,fp,fn,tn,1])
                for lab,v,c,r in labels:
                    shade=int(245-120*(v/mx)); fill=f'#{shade:02x}{shade:02x}{shade:02x}'
                    xx=x0+c*cell; yy=y0+r*cell; mcv.create_rectangle(xx,yy,xx+cell,yy+cell,fill=fill,outline='#64748b'); mcv.create_text(xx+cell/2,yy+45,text=lab,font=('Segoe UI Semibold',12)); mcv.create_text(xx+cell/2,yy+75,text=f'{v:.0f}',font=('Segoe UI',16))
                mcv.create_text(x0+cell,y0-25,text='Predicted',font=('Segoe UI Semibold',10)); mcv.create_text(x0-55,y0+cell,text='Actual',angle=90,font=('Segoe UI Semibold',10))
                mo.set(f'Accuracy={acc:.3f}   Precision={pre:.3f}   Recall={rec:.3f}   F1={f1:.3f}')
            except Exception: mo.set('ข้อมูลไม่ถูกต้อง')
        ttk.Button(m,text='Draw confusion matrix',command=metrics_graph).pack(anchor='w',padx=18,pady=6); metrics_graph()

    def _tc_visual_set(self, name, source, selected, formula, ai, kind, source_box, graph, slider, visual_info):
        title,form,conn,k=self._analyze_tc_math(name,source); selected.set(name+'  →  '+title); formula.set('Math: '+form); ai.set('AI connection: '+conn); kind['v']=k
        source_box.configure(state='normal'); source_box.delete('1.0','end'); source_box.insert('1.0',source[:30000]); source_box.configure(state='disabled'); self._draw_tc_visual(graph,k,slider.get(),visual_info)

    def _tc_visual_open_file(self, selected, formula, ai, kind, source_box, graph, slider, visual_info):
        path=filedialog.askopenfilename(title='Open Pascal / C source',filetypes=[('Pascal / C','*.pas *.c *.cpp *.h'),('All files','*.*')])
        if not path:return
        data=Path(path).read_bytes(); text=''
        for enc in ('utf-8','cp874','latin1'):
            try:text=data.decode(enc);break
            except Exception:pass
        self._tc_visual_set(Path(path).name,text,selected,formula,ai,kind,source_box,graph,slider,visual_info)

    def _tc_visual_from_zip(self, selected, formula, ai, kind, source_box, graph, slider, visual_info):
        zp=filedialog.askopenfilename(title='Choose TC ZIP',filetypes=[('ZIP','*.zip')]) or (str(self.tc_zip) if self.tc_zip else '')
        if not zp:return
        try:
            with zipfile.ZipFile(zp) as z:
                names=[n for n in z.namelist() if n.lower().endswith(('.pas','.c','.cpp','.h'))]
            win=tk.Toplevel(self); win.title('Select TC source'); win.geometry('760x560'); q=tk.StringVar(); ent=ttk.Entry(win,textvariable=q); ent.pack(fill='x',padx=12,pady=8); lb=tk.Listbox(win,font=('Consolas',9)); lb.pack(fill='both',expand=True,padx=12,pady=4)
            def fill(*_):
                term=q.get().lower(); lb.delete(0,'end'); [lb.insert('end',n) for n in names if term in n.lower()][:500]
            def choose(*_):
                if not lb.curselection():return
                name=lb.get(lb.curselection()[0]);
                with zipfile.ZipFile(zp) as z:data=z.read(name)
                text=''
                for enc in ('utf-8','cp874','latin1'):
                    try:text=data.decode(enc);break
                    except Exception:pass
                win.destroy(); self._tc_visual_set(name,text,selected,formula,ai,kind,source_box,graph,slider,visual_info)
            q.trace_add('write',fill); ent.bind('<Return>',choose); lb.bind('<Double-Button-1>',choose); ttk.Button(win,text='Open selected source',command=choose).pack(pady=8); fill()
        except Exception as e: messagebox.showerror('TC ZIP',str(e))

    # ==================== v4.2 AUTOMATIC EQUATION READER ====================
    def _strip_legacy_comments(self, source):
        """Remove common Pascal/C comments without changing the original source shown to students."""
        s = re.sub(r'/\*.*?\*/', ' ', source, flags=re.S)
        s = re.sub(r'//.*?$', ' ', s, flags=re.M)
        s = re.sub(r'\{.*?\}', ' ', s, flags=re.S)
        s = re.sub(r'\(\*.*?\*\)', ' ', s, flags=re.S)
        return s

    def _legacy_expr_to_math(self, expr):
        """Conservative Pascal/C -> SymPy expression normalization."""
        e = expr.strip()
        e = re.sub(r'\bSQR\s*\(([^()]*)\)', r'(\1)^2', e, flags=re.I)
        e = re.sub(r'\bSQRT\s*\(', 'sqrt(', e, flags=re.I)
        e = re.sub(r'\bSIN\s*\(', 'sin(', e, flags=re.I)
        e = re.sub(r'\bCOS\s*\(', 'cos(', e, flags=re.I)
        e = re.sub(r'\bTAN\s*\(', 'tan(', e, flags=re.I)
        e = re.sub(r'\bEXP\s*\(', 'exp(', e, flags=re.I)
        e = re.sub(r'\bLN\s*\(', 'log(', e, flags=re.I)
        e = re.sub(r'\bABS\s*\(', 'Abs(', e, flags=re.I)
        e = re.sub(r'\bPI\b', 'pi', e, flags=re.I)
        e = re.sub(r'\bDIV\b', '/', e, flags=re.I)
        e = re.sub(r'\bMOD\b', '%', e, flags=re.I)
        e = e.replace('&&', ' and ').replace('||', ' or ')
        # Remove simple C casts such as (float), (double), (int)
        e = re.sub(r'\((?:float|double|int|long|short)\)\s*', '', e, flags=re.I)
        return e

    def _extract_equations_auto(self, source):
        """
        Extract assignment-style equations from Pascal/C/C++.
        This intentionally does not claim full source-code translation.
        """
        cleaned = self._strip_legacy_comments(source)
        candidates = []
        # Pascal/C assignments ending in ;. Avoid ==, <=, >=, !=.
        pat = re.compile(r'(?m)^\s*([A-Za-z_]\w*)\s*(?::=|(?<![<>=!])=(?!=))\s*([^;\n]+)\s*;?')
        for m in pat.finditer(cleaned):
            lhs, rhs = m.group(1), m.group(2).strip()
            if len(rhs) > 180 or '"' in rhs or "'" in rhs:
                continue
            if re.search(r'\b(if|while|for|printf|scanf|write|writeln|read|readln|return)\b', rhs, re.I):
                continue
            norm = self._legacy_expr_to_math(rhs)
            rec = {'lhs': lhs, 'raw': rhs, 'norm': norm, 'expr': None, 'latex': '', 'status': 'text'}
            if sp is not None and parse_expr is not None:
                try:
                    names = set(re.findall(r'\b[A-Za-z_]\w*\b', norm))
                    funcs = {'sqrt':sp.sqrt,'sin':sp.sin,'cos':sp.cos,'tan':sp.tan,
                             'exp':sp.exp,'log':sp.log,'Abs':sp.Abs,'pi':sp.pi}
                    local = dict(funcs)
                    for n in names:
                        if n not in local and n not in {'and','or'}:
                            local[n] = sp.Symbol(n, real=True)
                    tr = standard_transformations + (implicit_multiplication_application, convert_xor)
                    ex = parse_expr(norm, local_dict=local, transformations=tr, evaluate=True)
                    if getattr(ex, 'is_Boolean', False):
                        raise ValueError("boolean")
                    rec['expr'] = ex
                    rec['latex'] = sp.latex(sp.Eq(sp.Symbol(lhs), ex))
                    rec['status'] = 'parsed'
                except Exception:
                    pass
            candidates.append(rec)
        # Remove exact duplicates while preserving order.
        out, seen = [], set()
        for r in candidates:
            key = (r['lhs'].lower(), r['norm'].lower())
            if key not in seen:
                seen.add(key); out.append(r)
        return out[:250]

    def _equation_classification(self, rec):
        if sp is None or rec.get('expr') is None:
            return "Numeric / symbolic assignment"
        ex = rec['expr']
        syms = list(ex.free_symbols)
        try:
            if any(ex.has(f) for f in (sp.sin, sp.cos, sp.tan)):
                return "Trigonometric / periodic"
            if len(syms) == 1:
                p = sp.Poly(ex, syms[0])
                deg = p.degree()
                return {0:"Constant",1:"Linear",2:"Quadratic / parabola",3:"Cubic polynomial"}.get(deg, f"Polynomial degree {deg}")
        except Exception:
            pass
        if ex.has(sp.sqrt):
            return "Radical / distance-like"
        return "Multivariable / nonlinear"

    def _plot_equation_canvas(self, cv, recs, selected_indices, x_min, x_max, info_var):
        cv.delete('all')
        w=max(760, cv.winfo_width()); h=max(430, cv.winfo_height())
        pad=55
        cv.create_rectangle(0,0,w,h,fill='#fbfdff',outline='')
        if sp is None:
            cv.create_text(w/2,h/2,text='ต้องติดตั้ง SymPy: pip install sympy',fill=TEXT,font=('Segoe UI',14))
            return
        chosen=[recs[i] for i in selected_indices if 0 <= i < len(recs) and recs[i].get('expr') is not None]
        if not chosen:
            cv.create_text(w/2,h/2,text='เลือกสมการที่ Parse ได้อย่างน้อย 1 สมการ',fill=MUTED,font=('Segoe UI',13))
            return

        # Prefer x as independent variable; otherwise use the first free symbol.
        x_symbol = sp.Symbol('x', real=True)
        all_y=[]
        sampled=[]
        params_used=[]
        for rec in chosen[:5]:
            ex=rec['expr']
            free=sorted(list(ex.free_symbols), key=lambda s:s.name)
            indep = next((s for s in free if s.name.lower()=='x'), free[0] if free else None)
            if indep is None:
                continue
            # Other symbols are teaching parameters. Set them to 1 unless a numeric assignment exists.
            subs={s:1.0 for s in free if s != indep}
            try:
                fn=sp.lambdify(indep, ex.subs(subs), modules=['math'])
                pts=[]
                for j in range(401):
                    xv=x_min+(x_max-x_min)*j/400
                    try:
                        yv=float(fn(xv))
                        if math.isfinite(yv) and abs(yv)<1e6:
                            pts.append((xv,yv)); all_y.append(yv)
                    except Exception:
                        pass
                if len(pts)>1:
                    sampled.append((rec,pts,subs))
                    if subs: params_used.append(', '.join(f'{k}=1' for k in subs))
            except Exception:
                pass
        if not sampled:
            cv.create_text(w/2,h/2,text='สมการนี้ยังไม่สามารถวาดเป็น y=f(x) แบบ 2 มิติได้\nแต่ยังแสดงสมการเชิงสัญลักษณ์ได้ถูกต้อง',fill=MUTED,font=('Segoe UI',12),justify='center')
            return

        # Robust y-range: use 2nd–98th percentiles to prevent a single asymptote from flattening the graph.
        ys=sorted(all_y)
        lo=ys[max(0,int(.02*(len(ys)-1)))]
        hi=ys[min(len(ys)-1,int(.98*(len(ys)-1)))]
        if abs(hi-lo)<1e-9: lo-=1; hi+=1
        margin=.12*(hi-lo); y_min=lo-margin; y_max=hi+margin

        def sx(x): return pad+(x-x_min)/(x_max-x_min)*(w-2*pad)
        def sy(y): return h-pad-(y-y_min)/(y_max-y_min)*(h-2*pad)

        # Grid and mathematically scaled axes.
        for k in range(11):
            xv=x_min+(x_max-x_min)*k/10
            px=sx(xv); cv.create_line(px,pad,px,h-pad,fill='#e8eef5')
            cv.create_text(px,h-pad+18,text=f'{xv:.2g}',fill=MUTED,font=('Segoe UI',8))
        for k in range(9):
            yv=y_min+(y_max-y_min)*k/8
            py=sy(yv); cv.create_line(pad,py,w-pad,py,fill='#e8eef5')
            cv.create_text(pad-8,py,text=f'{yv:.2g}',anchor='e',fill=MUTED,font=('Segoe UI',8))
        if x_min<=0<=x_max: cv.create_line(sx(0),pad,sx(0),h-pad,fill='#64748b',width=2)
        if y_min<=0<=y_max: cv.create_line(pad,sy(0),w-pad,sy(0),fill='#64748b',width=2)

        palette=['#2563eb','#dc2626','#059669','#7c3aed','#d97706']
        legend=[]
        for idx,(rec,pts,subs) in enumerate(sampled):
            color=palette[idx%len(palette)]
            seg=[]; last=None
            for xv,yv in pts:
                if yv<y_min or yv>y_max:
                    if len(seg)>=4: cv.create_line(*seg,fill=color,width=3,smooth=False)
                    seg=[]; last=None; continue
                px,py=sx(xv),sy(yv)
                if last is not None and abs(py-last[1]) > (h-2*pad)*.65:
                    if len(seg)>=4: cv.create_line(*seg,fill=color,width=3)
                    seg=[]
                seg += [px,py]; last=(px,py)
            if len(seg)>=4: cv.create_line(*seg,fill=color,width=3)
            legend.append((color, f"{rec['lhs']} = {str(rec['expr'])[:65]}"))
        yleg=16
        for color,label in legend:
            cv.create_line(pad,yleg,pad+24,yleg,fill=color,width=4)
            cv.create_text(pad+32,yleg,text=label,anchor='w',fill=TEXT,font=('Segoe UI',9))
            yleg+=19
        note = f"x-range [{x_min:g}, {x_max:g}] • y-range [{y_min:.3g}, {y_max:.3g}]"
        if params_used: note += " • พารามิเตอร์ที่ยังไม่ทราบถูกตั้งเป็น 1 เพื่อการแสดงกราฟ"
        info_var.set(note)

    def auto_equation_lab(self):
        self.clear()
        self.header('∫ • Automatic Equation Reader','เปิด .PAS/.C/.CPP/.H → ตรวจสมการอัตโนมัติ → ตรวจชนิดคณิตศาสตร์ → กราฟที่มีแกน/สเกลถูกต้อง → เปรียบเทียบหลายสมการ')
        b=self.scrollbody()
        c=self.card(b,'หลักการของ Analyzer',
                    'โปรแกรมเก็บ Original Source ไว้เสมอ แล้วอ่านเฉพาะ assignment ทางคณิตศาสตร์ เช่น y:=a*x*x+b*x+c; หรือ d=sqrt(x*x+y*y); '
                    'จากนั้นใช้ SymPy ตรวจโครงสร้างสมการก่อนวาดกราฟ จึงไม่ถือว่าเป็นการแปล Pascal/C ทั้งโปรแกรมเป็น Python อัตโนมัติ')
        top=tk.Frame(c,bg='white'); top.pack(fill='x',padx=18,pady=(0,14))
        source_name=tk.StringVar(value='ยังไม่ได้เลือก source')
        ttk.Button(top,text='Open .PAS / .C',style='Primary.TButton').pack(side='left')
        open_btn=top.winfo_children()[-1]
        ttk.Button(top,text='Choose from TC ZIP').pack(side='left',padx=6)
        zip_btn=top.winfo_children()[-1]
        tk.Label(top,textvariable=source_name,bg='white',fg=MUTED,font=('Segoe UI',9)).pack(side='left',padx=10)

        pane=tk.PanedWindow(b,orient='horizontal',sashwidth=5,bg=BG); pane.pack(fill='both',expand=True,padx=28,pady=8)
        left=tk.Frame(pane,bg='white',highlightbackground=BORDER,highlightthickness=1)
        right=tk.Frame(pane,bg='white',highlightbackground=BORDER,highlightthickness=1)
        pane.add(left,minsize=500); pane.add(right,minsize=650)

        tk.Label(left,text='Original TC Source',bg='white',fg=TEXT,font=('Segoe UI Semibold',12)).pack(anchor='w',padx=12,pady=(12,5))
        srcbox=tk.Text(left,height=18,font=('Consolas',8),wrap='none'); srcbox.pack(fill='both',expand=True,padx=12,pady=(0,10))
        srcbox.insert('1.0','เลือกไฟล์จาก TC เพื่อเริ่มวิเคราะห์สมการ')

        tk.Label(left,text='Detected equations',bg='white',fg=TEXT,font=('Segoe UI Semibold',12)).pack(anchor='w',padx=12)
        eqlist=tk.Listbox(left,height=12,selectmode='extended',font=('Consolas',9),exportselection=False)
        eqlist.pack(fill='x',padx=12,pady=6)
        eqdetail=tk.StringVar(value='—')
        tk.Label(left,textvariable=eqdetail,bg='white',fg=MUTED,font=('Segoe UI',9),justify='left',wraplength=500).pack(anchor='w',padx=12,pady=(0,12))

        tk.Label(right,text='Mathematical visualization',bg='white',fg=TEXT,font=('Segoe UI Semibold',12)).pack(anchor='w',padx=12,pady=(12,4))
        controls=tk.Frame(right,bg='white'); controls.pack(fill='x',padx=12,pady=4)
        tk.Label(controls,text='x min',bg='white').pack(side='left'); xmin=ttk.Entry(controls,width=8); xmin.insert(0,'-10'); xmin.pack(side='left',padx=(3,10))
        tk.Label(controls,text='x max',bg='white').pack(side='left'); xmax=ttk.Entry(controls,width=8); xmax.insert(0,'10'); xmax.pack(side='left',padx=(3,10))
        drawbtn=ttk.Button(controls,text='Draw selected',style='Primary.TButton'); drawbtn.pack(side='left',padx=6)
        selectall=ttk.Button(controls,text='Compare first 5'); selectall.pack(side='left')

        cv=tk.Canvas(right,height=470,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1)
        cv.pack(fill='both',expand=True,padx=12,pady=8)
        graphinfo=tk.StringVar(value='กราฟจะแสดงแกน x/y, grid, scale และ legend')
        tk.Label(right,textvariable=graphinfo,bg='white',fg=MUTED,font=('Segoe UI',9),justify='left',wraplength=700).pack(anchor='w',padx=12,pady=(0,12))

        state={'recs':[]}

        def refresh_list(name, source):
            source_name.set(name)
            srcbox.configure(state='normal'); srcbox.delete('1.0','end'); srcbox.insert('1.0',source[:50000]); srcbox.configure(state='disabled')
            recs=self._extract_equations_auto(source); state['recs']=recs
            eqlist.delete(0,'end')
            for i,r in enumerate(recs):
                mark='✓' if r['status']=='parsed' else '•'
                shown = (sp.pretty(sp.Eq(sp.Symbol(r['lhs']),r['expr']), use_unicode=True) if sp is not None and r.get('expr') is not None else f"{r['lhs']} = {r['raw']}")
                shown=' '.join(shown.split())
                eqlist.insert('end',f"{mark} {i+1:02d}  {shown[:105]}")
            if recs:
                eqlist.selection_set(0)
                show_detail()
            else:
                eqdetail.set('ไม่พบ assignment ทางคณิตศาสตร์ที่ Analyzer อ่านได้ในไฟล์นี้')
                graphinfo.set('ลองเลือกไฟล์ Math อื่น เช่น PARAX.PAS, CIRCLE.PAS, MCALC.C หรือ source ที่มี assignment')
                cv.delete('all')

        def show_detail(*_):
            if not eqlist.curselection(): return
            r=state['recs'][eqlist.curselection()[0]]
            typ=self._equation_classification(r)
            latex=r.get('latex') or f"{r['lhs']} = {r['raw']}"
            eqdetail.set(f"ประเภท: {typ}\nOriginal: {r['lhs']} = {r['raw']}\nNormalized: {r['lhs']} = {r['norm']}\nLaTeX: {latex}")

        def draw():
            try:
                a=float(xmin.get()); z=float(xmax.get())
                if not math.isfinite(a) or not math.isfinite(z) or a>=z: raise ValueError
            except Exception:
                messagebox.showerror('Graph range','กรุณาใส่ x min < x max เป็นตัวเลข'); return
            inds=list(eqlist.curselection())
            self._plot_equation_canvas(cv,state['recs'],inds,a,z,graphinfo)

        def compare5():
            eqlist.selection_clear(0,'end')
            parsed=[i for i,r in enumerate(state['recs']) if r.get('expr') is not None][:5]
            for i in parsed: eqlist.selection_set(i)
            draw()

        def open_file():
            path=filedialog.askopenfilename(title='Open Pascal / C source',filetypes=[('Pascal / C','*.pas *.c *.cpp *.h'),('All files','*.*')])
            if not path:return
            data=Path(path).read_bytes(); source=''
            for enc in ('utf-8','cp874','latin1'):
                try: source=data.decode(enc); break
                except Exception: pass
            refresh_list(Path(path).name,source)

        def choose_zip():
            zp=filedialog.askopenfilename(title='Choose TC ZIP',filetypes=[('ZIP','*.zip')]) or (str(self.tc_zip) if self.tc_zip else '')
            if not zp:return
            try:
                with zipfile.ZipFile(zp) as z:
                    names=[n for n in z.namelist() if n.lower().endswith(('.pas','.c','.cpp','.h'))]
                win=tk.Toplevel(self); win.title('Select TC source'); win.geometry('800x600')
                q=tk.StringVar(); ent=ttk.Entry(win,textvariable=q); ent.pack(fill='x',padx=12,pady=8)
                lb=tk.Listbox(win,font=('Consolas',9)); lb.pack(fill='both',expand=True,padx=12,pady=4)
                def fill(*_):
                    term=q.get().lower(); lb.delete(0,'end')
                    for n in [n for n in names if term in n.lower()][:800]: lb.insert('end',n)
                def choose(*_):
                    if not lb.curselection(): return
                    name=lb.get(lb.curselection()[0])
                    with zipfile.ZipFile(zp) as z: data=z.read(name)
                    source=''
                    for enc in ('utf-8','cp874','latin1'):
                        try: source=data.decode(enc); break
                        except Exception: pass
                    win.destroy(); refresh_list(name,source)
                q.trace_add('write',fill); ent.bind('<Return>',choose); lb.bind('<Double-Button-1>',choose)
                ttk.Button(win,text='Open selected source',command=choose).pack(pady=8); fill(); ent.focus_set()
            except Exception as e: messagebox.showerror('TC ZIP',str(e))

        open_btn.configure(command=open_file); zip_btn.configure(command=choose_zip)
        eqlist.bind('<<ListboxSelect>>',show_detail)
        drawbtn.configure(command=draw); selectall.configure(command=compare5)
        cv.bind('<Configure>',lambda e: draw() if state['recs'] and eqlist.curselection() else None)

        note=self.card(b,'MATHEMATICAL CORRECTNESS',
            'กราฟใช้ symbolic expression ที่ SymPy parse ได้จริง • แกนและสเกลคำนวณจากช่วง x ที่กำหนด • '
            'กรณีมีพารามิเตอร์ที่ source ยังไม่ได้กำหนด Analyzer จะตั้งค่าเป็น 1 เฉพาะเพื่อ visualization และจะแจ้งใต้กราฟ • '
            'สมการที่เป็น implicit/multivariable หรือ control-flow ซับซ้อนจะไม่ถูกบังคับให้วาดเป็น y=f(x) เพื่อหลีกเลี่ยงภาพที่ผิดหลักคณิตศาสตร์')
        tk.Label(note,text='คำแนะนำ: เริ่มจาก PARAX.PAS / PARAY.PAS / CIRCLE.PAS / MCALC.C แล้วเปรียบเทียบ Original → Normalized → Graph',
                 bg='white',fg=BLUE,font=('Segoe UI Semibold',10)).pack(anchor='w',padx=18,pady=(0,14))

    # ==================== v4.3 SMART EQUATION ATLAS ====================
    def _v43_decode(self, data):
        for enc in ('utf-8','utf-8-sig','cp874','cp1252','latin1'):
            try:
                return data.decode(enc), enc
            except Exception:
                pass
        return data.decode('latin1', errors='replace'), 'latin1'

    def _v43_language(self, name):
        ext=Path(name).suffix.lower()
        return {'.pas':'Pascal','.pp':'Pascal','.c':'C','.h':'C Header',
                '.cpp':'C++','.cc':'C++','.cxx':'C++','.hpp':'C++ Header'}.get(ext,'Source')

    def _v43_math_tags(self, source, recs):
        s=source.lower()
        tags=[]
        rules=[
            ('Circle / distance', r'\bcircle\b|\bradius\b|\bsqrt\s*\(|\bsqr\s*\('),
            ('Conic / quadratic', r'\bellipse\b|\bparab|\bhyperbol|x\s*\*\s*x|y\s*\*\s*y|\bsqr\s*\(\s*[xy]'),
            ('Trigonometry', r'\bsin\s*\(|\bcos\s*\(|\btan\s*\(|\barctan|\basin|\bacos'),
            ('Log / exponential', r'\bexp\s*\(|\blog\s*\(|\bln\s*\('),
            ('Statistics', r'\bmean\b|\baverage\b|\bvariance\b|\bstd|\bsigma\b|\bzscore|\bz_score'),
            ('Probability', r'\bprob|\brandom\b|\brand\s*\(|\bsoftmax\b'),
            ('Vector / geometry', r'\bvector\b|\bdot\b|\bcross\b|\bdistance\b|\bangle\b'),
            ('Matrix / linear algebra', r'\bmatrix\b|\bmatmul\b|\bdetermin|\binverse\b'),
            ('Calculus / numerical', r'\bderiv|\bintegral|\bdiff|\bgradient\b|\bnewton\b|\beuler\b|\brunge'),
            ('Sorting / ranking', r'\bsort\b|\bbubble\b|\bheap\b|\bquick\b|\bswap\b'),
            ('Decision / tree', r'\btree\b|\bnode\b|\bthreshold\b'),
        ]
        for label,pat in rules:
            if re.search(pat,s,re.I): tags.append(label)
        # Add structural tags inferred from parsed expressions.
        if sp is not None:
            for r in recs:
                ex=r.get('expr')
                if ex is None: continue
                try:
                    if any(ex.has(f) for f in (sp.sin,sp.cos,sp.tan)) and 'Trigonometry' not in tags:
                        tags.append('Trigonometry')
                    if ex.has(sp.exp) and 'Log / exponential' not in tags:
                        tags.append('Log / exponential')
                    syms=list(ex.free_symbols)
                    if len(syms)>=2 and 'Multivariable' not in tags:
                        tags.append('Multivariable')
                except Exception: pass
        return tags or ['General arithmetic / algorithm']

    def _v43_ai_connection(self, tags):
        pairs=[
            ('Circle / distance','k-NN, clustering, nearest-target vision'),
            ('Conic / quadratic','regression, geometric vision, region modelling'),
            ('Trigonometry','robot pose, rotation, periodic signals'),
            ('Log / exponential','loss functions, likelihood, softmax'),
            ('Statistics','normalization, anomaly detection, model evaluation'),
            ('Probability','classification confidence, Bayesian reasoning'),
            ('Vector / geometry','computer vision, embeddings, cosine similarity'),
            ('Matrix / linear algebra','neural-network layers and transformations'),
            ('Calculus / numerical','gradient descent and optimization'),
            ('Sorting / ranking','nearest-neighbor ranking and search'),
            ('Decision / tree','decision trees and rule-based agents'),
            ('Multivariable','multi-feature machine learning')
        ]
        out=[]
        for key,val in pairs:
            if key in tags: out.append(val)
        return '; '.join(out) if out else 'feature engineering and computational thinking'

    def _v43_equation_kind(self, rec):
        if sp is None or rec.get('expr') is None:
            return 'Assignment'
        ex=rec['expr']; syms=sorted(ex.free_symbols,key=lambda s:s.name)
        try:
            if any(ex.has(f) for f in (sp.sin,sp.cos,sp.tan)):
                return 'Trigonometric'
            if ex.has(sp.exp) or ex.has(sp.log):
                return 'Exponential / logarithmic'
            if len(syms)==0: return 'Constant'
            if len(syms)==1:
                deg=sp.Poly(ex,syms[0]).degree()
                return {0:'Constant',1:'Linear',2:'Quadratic',3:'Cubic'}.get(deg,f'Polynomial degree {deg}')
            if len(syms)>1:
                try:
                    deg=sp.Poly(ex,*syms).total_degree()
                    return f'Multivariable polynomial degree {deg}'
                except Exception:
                    return 'Multivariable nonlinear'
        except Exception:
            pass
        if ex.has(sp.sqrt): return 'Radical / distance'
        return 'Symbolic expression'

    def _v43_scan_zip(self, zip_path, progress=None):
        """Scan every supported Pascal/C family source in a ZIP and build a math/equation atlas."""
        rows=[]; supported=('.pas','.pp','.c','.h','.cpp','.cc','.cxx','.hpp')
        with zipfile.ZipFile(zip_path) as z:
            names=[n for n in z.namelist() if n.lower().endswith(supported) and not n.endswith('/')]
            total=max(1,len(names))
            for idx,name in enumerate(names):
                try:
                    data=z.read(name)
                    # Bound pathological files while retaining normal educational sources.
                    if len(data)>2_000_000:
                        rows.append({'file':name,'lang':self._v43_language(name),'encoding':'—',
                                     'equations':[],'tags':['Skipped: >2 MB'],'ai':'—','source':''})
                        continue
                    source,enc=self._v43_decode(data)
                    recs=self._extract_equations_auto(source)
                    tags=self._v43_math_tags(source,recs)
                    rows.append({'file':name,'lang':self._v43_language(name),'encoding':enc,
                                 'equations':recs,'tags':tags,'ai':self._v43_ai_connection(tags),
                                 'source':source[:120000]})
                except Exception as e:
                    rows.append({'file':name,'lang':self._v43_language(name),'encoding':'error',
                                 'equations':[],'tags':['Read error'],'ai':'—','source':str(e)})
                if progress and (idx%10==0 or idx==len(names)-1):
                    progress(idx+1,len(names))
        return rows

    def _v43_draw_smart_preview(self, canvas, row, rec_index=0):
        canvas.delete('all')
        w=max(720,canvas.winfo_width()); h=max(390,canvas.winfo_height())
        canvas.create_rectangle(0,0,w,h,fill='#fbfdff',outline='')
        recs=row.get('equations',[])
        if not recs:
            canvas.create_text(w/2,h/2,text='ไฟล์นี้ไม่พบ assignment ที่แปลงเป็น symbolic equation ได้\nดู Math Tags และ Original Source ประกอบ',
                               fill=MUTED,font=('Segoe UI',12),justify='center')
            return
        rec=recs[min(rec_index,len(recs)-1)]
        ex=rec.get('expr')
        title=f"{rec['lhs']} = {rec.get('expr') if ex is not None else rec['raw']}"
        canvas.create_text(24,20,text=title[:115],anchor='nw',fill=TEXT,font=('Segoe UI Semibold',11))
        canvas.create_text(24,46,text=f"Type: {self._v43_equation_kind(rec)}",anchor='nw',fill=MUTED,font=('Segoe UI',9))
        if sp is None or ex is None:
            canvas.create_text(w/2,h/2,text='ติดตั้ง SymPy เพื่อสร้าง mathematical preview',fill=MUTED,font=('Segoe UI',12))
            return
        free=sorted(ex.free_symbols,key=lambda s:s.name)
        if not free:
            canvas.create_text(w/2,h/2,text=f'ค่าคงที่ = {sp.N(ex,6)}',fill=BLUE,font=('Segoe UI Semibold',20))
            return
        indep=next((s for s in free if s.name.lower()=='x'),free[0])
        subs={s:1.0 for s in free if s!=indep}
        try:
            fn=sp.lambdify(indep,ex.subs(subs),modules=['math'])
            pts=[]; ys=[]
            for j in range(501):
                x=-10+20*j/500
                try:
                    y=float(fn(x))
                    if math.isfinite(y) and abs(y)<1e7:
                        pts.append((x,y)); ys.append(y)
                except Exception: pass
            if len(pts)<2: raise ValueError('not graphable')
            ys2=sorted(ys)
            lo=ys2[max(0,int(.02*(len(ys2)-1)))]; hi=ys2[min(len(ys2)-1,int(.98*(len(ys2)-1)))]
            if abs(hi-lo)<1e-9: lo-=1; hi+=1
            m=.12*(hi-lo); lo-=m; hi+=m
            L,R,T,B=60,w-28,78,h-48
            def sx(x): return L+(x+10)/20*(R-L)
            def sy(y): return B-(y-lo)/(hi-lo)*(B-T)
            for k in range(11):
                x=-10+2*k; px=sx(x)
                canvas.create_line(px,T,px,B,fill='#e5eaf0')
                canvas.create_text(px,B+15,text=str(x),fill=MUTED,font=('Segoe UI',8))
            for k in range(9):
                y=lo+(hi-lo)*k/8; py=sy(y)
                canvas.create_line(L,py,R,py,fill='#e5eaf0')
                canvas.create_text(L-7,py,text=f'{y:.2g}',anchor='e',fill=MUTED,font=('Segoe UI',8))
            canvas.create_line(sx(0),T,sx(0),B,fill='#64748b',width=2)
            if lo<=0<=hi: canvas.create_line(L,sy(0),R,sy(0),fill='#64748b',width=2)
            seg=[]; last=None
            for x,y in pts:
                if not lo<=y<=hi:
                    if len(seg)>=4: canvas.create_line(*seg,fill='#2563eb',width=3)
                    seg=[]; last=None; continue
                px,py=sx(x),sy(y)
                if last and abs(py-last[1])>(B-T)*.65:
                    if len(seg)>=4: canvas.create_line(*seg,fill='#2563eb',width=3)
                    seg=[]
                seg += [px,py]; last=(px,py)
            if len(seg)>=4: canvas.create_line(*seg,fill='#2563eb',width=3)
            if subs:
                canvas.create_text(24,h-18,text='Visualization assumption: '+', '.join(f'{s}=1' for s in subs),
                                   anchor='sw',fill=MUTED,font=('Segoe UI',8))
        except Exception:
            canvas.create_text(w/2,h/2,text='สมการนี้เป็น symbolic/multivariable แต่ไม่เหมาะกับกราฟ y=f(x) 2 มิติแบบตรงไปตรงมา\nระบบจึงไม่สร้างกราฟที่อาจทำให้เข้าใจผิด',
                               fill=MUTED,font=('Segoe UI',11),justify='center')

    def equation_atlas_lab(self):
        self.clear()
        self.header('🧭 • Equation Atlas — All TC Source Files',
                    'สแกนทุก .PAS/.C/.H/.CPP ในชุดข้อมูล → ดึงสมการ → จำแนกคณิตศาสตร์ → Smart Preview → AI Connection')
        b=self.scrollbody()
        intro=self.card(b,'เป้าหมาย v4.3',
            'หน้านี้ไม่ได้จำกัดเฉพาะ CIRCLE.PAS หรือ PARAX.PAS แต่พยายามอ่านทุก source file ในตระกูล Pascal/C ภายใน ZIP '
            'และสร้าง “แผนที่สมการ” โดยเก็บชื่อไฟล์ ภาษา source สมการที่ตรวจพบ Math Tags และความเชื่อมโยงกับ AI')
        bar=tk.Frame(intro,bg='white'); bar.pack(fill='x',padx=18,pady=(0,14))
        ttk.Button(bar,text='Scan TC ZIP — All Source Files',style='Primary.TButton').pack(side='left')
        scanbtn=bar.winfo_children()[-1]
        status=tk.StringVar(value='พร้อมสแกนชุดข้อมูล')
        tk.Label(bar,textvariable=status,bg='white',fg=MUTED,font=('Segoe UI',9)).pack(side='left',padx=12)

        filters=self.card(b,'ค้นหาและกรอง Equation Atlas','ค้นด้วยชื่อไฟล์ ภาษา ประเภทคณิตศาสตร์ หรือข้อความในสมการ')
        fr=tk.Frame(filters,bg='white'); fr.pack(fill='x',padx=18,pady=(0,12))
        query=tk.StringVar()
        ent=ttk.Entry(fr,textvariable=query); ent.pack(side='left',fill='x',expand=True)
        lang=tk.StringVar(value='All')
        combo=ttk.Combobox(fr,textvariable=lang,values=['All','Pascal','C','C Header','C++','C++ Header'],state='readonly',width=14)
        combo.pack(side='left',padx=6)

        body=tk.PanedWindow(b,orient='horizontal',sashwidth=5,bg=BG); body.pack(fill='both',expand=True,padx=28,pady=8)
        left=tk.Frame(body,bg='white',highlightbackground=BORDER,highlightthickness=1)
        right=tk.Frame(body,bg='white',highlightbackground=BORDER,highlightthickness=1)
        body.add(left,minsize=510); body.add(right,minsize=680)

        cols=('file','lang','eq','tags')
        tree=ttk.Treeview(left,columns=cols,show='headings',height=21)
        for col,title,width in [('file','Source file',260),('lang','Language',80),('eq','Eq.',45),('tags','Math',220)]:
            tree.heading(col,text=title); tree.column(col,width=width,anchor='w')
        tree.pack(fill='both',expand=True,padx=8,pady=8)

        tk.Label(right,text='Smart mathematical preview',bg='white',fg=TEXT,font=('Segoe UI Semibold',12)).pack(anchor='w',padx=12,pady=(10,2))
        meta=tk.StringVar(value='เลือก source file จากรายการ')
        tk.Label(right,textvariable=meta,bg='white',fg=MUTED,font=('Segoe UI',9),justify='left',wraplength=690).pack(anchor='w',padx=12)
        eqcombo=ttk.Combobox(right,state='readonly')
        eqcombo.pack(fill='x',padx=12,pady=6)
        cv=tk.Canvas(right,height=410,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1)
        cv.pack(fill='both',expand=True,padx=12,pady=6)
        srcbox=tk.Text(right,height=10,font=('Consolas',8),wrap='none')
        srcbox.pack(fill='x',padx=12,pady=(0,12)); srcbox.insert('1.0','Original source จะปรากฏที่นี่'); srcbox.configure(state='disabled')

        state={'rows':[],'visible':[]}

        def populate():
            term=query.get().strip().lower(); want=lang.get()
            tree.delete(*tree.get_children()); state['visible']=[]
            for idx,row in enumerate(state['rows']):
                eqtext=' '.join((r['lhs']+' '+r['raw']) for r in row['equations'])
                hay=(row['file']+' '+row['lang']+' '+' '.join(row['tags'])+' '+eqtext).lower()
                if term and term not in hay: continue
                if want!='All' and row['lang']!=want: continue
                iid=str(len(state['visible'])); state['visible'].append(idx)
                tree.insert('', 'end', iid=iid, values=(row['file'],row['lang'],len(row['equations']),', '.join(row['tags'][:3])))

        def select_row(*_):
            sel=tree.selection()
            if not sel:return
            row=state['rows'][state['visible'][int(sel[0])]]
            meta.set(f"{row['file']}  |  {row['lang']} / {row['encoding']}\nMath: {', '.join(row['tags'])}\nAI: {row['ai']}")
            vals=[]
            for i,r in enumerate(row['equations']):
                vals.append(f"{i+1:02d} • {r['lhs']} = {str(r.get('expr') if r.get('expr') is not None else r['raw'])[:100]} [{self._v43_equation_kind(r)}]")
            eqcombo['values']=vals or ['No parsed assignment']
            eqcombo.current(0)
            srcbox.configure(state='normal'); srcbox.delete('1.0','end'); srcbox.insert('1.0',row['source']); srcbox.configure(state='disabled')
            self._v43_draw_smart_preview(cv,row,0)

        def eq_changed(*_):
            sel=tree.selection()
            if not sel:return
            row=state['rows'][state['visible'][int(sel[0])]]
            self._v43_draw_smart_preview(cv,row,max(0,eqcombo.current()))

        def scan():
            zp=filedialog.askopenfilename(title='Select TC ZIP',filetypes=[('ZIP','*.zip')])
            if not zp:return
            scanbtn.configure(state='disabled'); status.set('กำลังสแกน...')
            self.update_idletasks()
            def prog(i,n):
                status.set(f'กำลังอ่าน {i:,}/{n:,} source files...')
                self.update_idletasks()
            try:
                rows=self._v43_scan_zip(zp,prog); state['rows']=rows; populate()
                files=len(rows); eqs=sum(len(r['equations']) for r in rows)
                parsed=sum(sum(1 for e in r['equations'] if e.get('expr') is not None) for r in rows)
                status.set(f'เสร็จแล้ว: {files:,} files • {eqs:,} assignments • {parsed:,} symbolic equations')
            except Exception as e:
                messagebox.showerror('Equation Atlas',str(e)); status.set('สแกนไม่สำเร็จ')
            finally:
                scanbtn.configure(state='normal')

        scanbtn.configure(command=scan)
        query.trace_add('write',lambda *_:populate()); combo.bind('<<ComboboxSelected>>',lambda e:populate())
        tree.bind('<<TreeviewSelect>>',select_row); eqcombo.bind('<<ComboboxSelected>>',eq_changed)
        cv.bind('<Configure>',lambda e:eq_changed())

        guide=self.card(b,'ขอบเขตความถูกต้อง',
            'v4.3 อ่านทุก source file ที่เป็น Pascal/C/C++ family ใน ZIP แต่ “ทุกบรรทัดของโปรแกรม” ไม่ใช่สมการคณิตศาสตร์ '
            'ระบบจึงเก็บทุกไฟล์ไว้ใน Atlas และดึงเฉพาะ assignment ที่มีรูปแบบเหมาะสมสำหรับ symbolic math. '
            'Control flow, pointer, graphics API, I/O และโค้ดเฉพาะ compiler จะไม่ถูกบังคับให้เป็นสมการ. '
            'สำหรับสมการที่ parse ได้ ระบบใช้ SymPy ตรวจโครงสร้างก่อนสร้างกราฟ และจะไม่วาดกราฟ 2 มิติเมื่อ representation นั้นไม่เหมาะสม')
        tk.Label(guide,text='รองรับภาษา source: Turbo Pascal/Pascal, C, C headers, C++ และ C++ headers',
                 bg='white',fg=BLUE,font=('Segoe UI Semibold',10)).pack(anchor='w',padx=18,pady=(0,14))

    # ==================== v4.4 TC MATH GALLERY ====================
    def _v44_gallery_categories(self):
        return [
            ('Circle & Distance','x² + y² = r²','Geometry',
             'Euclidean distance, k-NN, nearest target',
             'CIRCLE / RADIUS / DISTANCE / SQRT',
             lambda x: math.sqrt(max(0.0,25-x*x)) if abs(x)<=5 else None),
            ('Parabola & Regression','y = ax² + bx + c','Algebra',
             'Regression, curve fitting, loss minimization',
             'PARAX / PARAY / QUADRATIC',
             lambda x: 0.35*x*x-1.2*x-2),
            ('Ellipse & Normalization','x²/a² + y²/b² = 1','Geometry',
             'Feature normalization, anomaly boundary',
             'ELLIPSE / CONIC',
             lambda x: 3*math.sqrt(max(0.0,1-(x*x/25))) if abs(x)<=5 else None),
            ('Trigonometry','y = sin(x), cos(x)','Trigonometry',
             'Robot angle, periodic signal, pose',
             'SIN / COS / TAN / ANGLE',
             lambda x: math.sin(x)),
            ('Exponential & Log','y = exp(x), log(x)','Functions',
             'Softmax, likelihood, loss functions',
             'EXP / LOG / LN',
             lambda x: math.exp(x/3)),
            ('Statistics & Z-score','z = (x-μ)/σ','Statistics',
             'Scaling, anomaly detection, preprocessing',
             'MEAN / VAR / STD / SIGMA / STAT',
             lambda x: (x-1.5)/2.0),
            ('Probability','P(A), Σpᵢ = 1','Probability',
             'Classification confidence, Bayesian reasoning',
             'PROB / RANDOM / SOFTMAX',
             lambda x: 1/(1+math.exp(-x))),
            ('Vector & Geometry','v = (x,y), ‖v‖ = √(x²+y²)','Linear algebra',
             'Embeddings, vision coordinates, cosine similarity',
             'VECTOR / DOT / CROSS / DISTANCE',
             lambda x: 0.7*x+1),
            ('Matrix','Y = WX + b','Linear algebra',
             'Neural-network layers, transforms',
             'MATRIX / MAT / DET / INVERSE',
             lambda x: 1.4*x-1),
            ('Calculus','dy/dx, ∫f(x)dx','Calculus',
             'Gradient descent, optimization',
             'DERIV / DIFF / INTEGRAL / GRADIENT / NEWTON',
             lambda x: x*x/5),
            ('Sorting & Ranking','d₁ ≤ d₂ ≤ … ≤ dₙ','Algorithm',
             'k-NN ranking, retrieval, search',
             'SORT / BUBBLE / HEAP / QUICK / SWAP',
             lambda x: x),
            ('Decision Tree','if x < t → A else B','Decision mathematics',
             'Decision trees, AI agents, rule systems',
             'TREE / NODE / THRESHOLD',
             lambda x: -2 if x<0 else 2),
        ]

    def _v44_match_category(self, row, category):
        title,formula,domain,ai,keys,_=category
        hay=(row.get('file','')+' '+' '.join(row.get('tags',[]))+' '+row.get('source','')[:25000]).lower()
        words=[w.strip().lower() for w in keys.split('/') if w.strip()]
        return any(w in hay for w in words)

    def _v44_draw_gallery_graph(self, cv, category):
        cv.delete('all')
        w=max(520,cv.winfo_width()); h=max(300,cv.winfo_height())
        cv.create_rectangle(0,0,w,h,fill='#fbfdff',outline='')
        title,formula,domain,ai,keys,fn=category
        L,R,T,B=52,w-22,42,h-42
        xmin,xmax=-6,6
        pts=[]; ys=[]
        for i in range(481):
            x=xmin+(xmax-xmin)*i/480
            try:
                y=fn(x)
                if y is not None and math.isfinite(y) and abs(y)<100:
                    pts.append((x,y)); ys.append(y)
            except Exception: pass
        if not ys:
            cv.create_text(w/2,h/2,text='No 2D preview',fill=MUTED,font=('Segoe UI',11)); return
        lo=min(ys); hi=max(ys)
        if abs(hi-lo)<1e-9: lo-=1; hi+=1
        m=.18*(hi-lo); lo-=m; hi+=m
        def sx(x): return L+(x-xmin)/(xmax-xmin)*(R-L)
        def sy(y): return B-(y-lo)/(hi-lo)*(B-T)
        for k in range(7):
            x=xmin+(xmax-xmin)*k/6; px=sx(x)
            cv.create_line(px,T,px,B,fill='#e8edf3')
            cv.create_text(px,B+14,text=f'{x:.0f}',fill=MUTED,font=('Segoe UI',8))
        for k in range(7):
            y=lo+(hi-lo)*k/6; py=sy(y)
            cv.create_line(L,py,R,py,fill='#e8edf3')
            cv.create_text(L-6,py,text=f'{y:.2g}',anchor='e',fill=MUTED,font=('Segoe UI',8))
        if xmin<=0<=xmax: cv.create_line(sx(0),T,sx(0),B,fill='#64748b',width=2)
        if lo<=0<=hi: cv.create_line(L,sy(0),R,sy(0),fill='#64748b',width=2)
        seg=[]
        last=None
        for x,y in pts:
            if not lo<=y<=hi:
                if len(seg)>=4: cv.create_line(*seg,fill='#2563eb',width=3)
                seg=[]; last=None; continue
            px,py=sx(x),sy(y)
            if last and abs(py-last[1])>(B-T)*.65:
                if len(seg)>=4: cv.create_line(*seg,fill='#2563eb',width=3)
                seg=[]
            seg += [px,py]; last=(px,py)
        if len(seg)>=4: cv.create_line(*seg,fill='#2563eb',width=3)
        cv.create_text(L,18,text=formula,anchor='w',fill=TEXT,font=('Segoe UI Semibold',11))

    def _v44_python_equivalent(self, category):
        title=category[0]
        examples={
            'Circle & Distance':"d = math.sqrt((x2-x1)**2 + (y2-y1)**2)\ninside = x*x + y*y <= r*r",
            'Parabola & Regression':"y = a*x**2 + b*x + c\nloss = sum((y_true-y_pred)**2) / n",
            'Ellipse & Normalization':"score = (x/a)**2 + (y/b)**2\ninside = score <= 1.0",
            'Trigonometry':"y1 = math.sin(x)\ny2 = math.cos(x)",
            'Exponential & Log':"y = math.exp(x)\nz = math.log(x) if x > 0 else None",
            'Statistics & Z-score':"mu = statistics.mean(data)\nsigma = statistics.stdev(data)\nz = (x-mu)/sigma",
            'Probability':"p = 1/(1+math.exp(-x))\n# probabilities should be in [0,1]",
            'Vector & Geometry':"norm = math.sqrt(x*x+y*y)\ndot = ax*bx + ay*by",
            'Matrix':"Y = W @ X + b   # NumPy notation",
            'Calculus':"dy_dx ≈ (f(x+h)-f(x-h))/(2*h)\nintegral ≈ sum(f(x)*dx for x in grid)",
            'Sorting & Ranking':"ranked = sorted(items, key=lambda p: p['distance'])",
            'Decision Tree':"prediction = 'A' if x < threshold else 'B'",
        }
        return examples.get(title,'# Python equivalent depends on the source expression')

    def math_gallery_lab(self):
        self.clear()
        self.header('🖼 • TC Math Gallery',
                    'Original TC code → Mathematical idea → Formula → Graph → Python equivalent → AI application')
        b=self.scrollbody()
        intro=self.card(b,'Math Gallery v4.4',
            'Gallery นี้จัดคณิตศาสตร์จาก source code เก่าให้เป็นบทเรียนภาพ นักเรียนเลือกหัวข้อ แล้วดูสูตร กราฟ '
            'Python equivalent และตัวอย่างว่าแนวคิดเดียวกันถูกใช้ใน AI อย่างไร พร้อมค้น source file ที่สัมพันธ์กับหัวข้อนั้นจาก TC ZIP')
        toolbar=tk.Frame(intro,bg='white'); toolbar.pack(fill='x',padx=18,pady=(0,14))
        ttk.Button(toolbar,text='Load / Scan TC ZIP',style='Primary.TButton').pack(side='left')
        loadbtn=toolbar.winfo_children()[-1]
        scanstatus=tk.StringVar(value='ยังไม่ได้สแกน TC ZIP — Gallery ตัวอย่างใช้งานได้ทันที')
        tk.Label(toolbar,textvariable=scanstatus,bg='white',fg=MUTED,font=('Segoe UI',9)).pack(side='left',padx=10)

        categories=self._v44_gallery_categories()
        body=tk.PanedWindow(b,orient='horizontal',sashwidth=5,bg=BG); body.pack(fill='both',expand=True,padx=28,pady=8)
        nav=tk.Frame(body,bg='white',highlightbackground=BORDER,highlightthickness=1)
        detail=tk.Frame(body,bg='white',highlightbackground=BORDER,highlightthickness=1)
        body.add(nav,minsize=270); body.add(detail,minsize=760)

        tk.Label(nav,text='Mathematics collection',bg='white',fg=TEXT,font=('Segoe UI Semibold',12)).pack(anchor='w',padx=12,pady=(12,6))
        lb=tk.Listbox(nav,font=('Segoe UI',10),height=24,exportselection=False)
        lb.pack(fill='both',expand=True,padx=10,pady=(0,10))
        for cat in categories: lb.insert('end',cat[0])
        lb.selection_set(0)

        titlev=tk.StringVar(); formulav=tk.StringVar(); domainv=tk.StringVar(); aiv=tk.StringVar()
        tk.Label(detail,textvariable=titlev,bg='white',fg=TEXT,font=('Segoe UI Semibold',17)).pack(anchor='w',padx=16,pady=(12,0))
        tk.Label(detail,textvariable=formulav,bg='white',fg=BLUE,font=('Cambria Math',16)).pack(anchor='w',padx=16,pady=4)
        tk.Label(detail,textvariable=domainv,bg='white',fg=MUTED,font=('Segoe UI',9)).pack(anchor='w',padx=16)

        cv=tk.Canvas(detail,height=330,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1)
        cv.pack(fill='both',expand=True,padx=16,pady=10)

        lower=tk.PanedWindow(detail,orient='horizontal',sashwidth=4,bg='white'); lower.pack(fill='x',padx=16,pady=(0,12))
        p1=tk.Frame(lower,bg='#f8fafc'); p2=tk.Frame(lower,bg='#f8fafc')
        lower.add(p1,minsize=330); lower.add(p2,minsize=330)
        tk.Label(p1,text='Python equivalent',bg='#f8fafc',fg=TEXT,font=('Segoe UI Semibold',10)).pack(anchor='w',padx=10,pady=(8,3))
        pybox=tk.Text(p1,height=7,font=('Consolas',9),wrap='word'); pybox.pack(fill='both',expand=True,padx=10,pady=(0,8))
        tk.Label(p2,text='AI connection',bg='#f8fafc',fg=TEXT,font=('Segoe UI Semibold',10)).pack(anchor='w',padx=10,pady=(8,3))
        tk.Label(p2,textvariable=aiv,bg='#f8fafc',fg=TEXT,font=('Segoe UI',10),justify='left',wraplength=360).pack(anchor='w',padx=10,pady=(0,8))

        matches=self.card(b,'Matching TC source files','หลังสแกน ZIP รายการนี้จะแสดง source code ที่สัมพันธ์กับหัวข้อ Gallery ที่เลือก')
        matchlb=tk.Listbox(matches,height=9,font=('Consolas',9),exportselection=False)
        matchlb.pack(fill='x',padx=18,pady=(0,8))
        sourcebox=tk.Text(matches,height=12,font=('Consolas',8),wrap='none')
        sourcebox.pack(fill='x',padx=18,pady=(0,14)); sourcebox.insert('1.0','เลือก source file เพื่อดู Original Pascal/C'); sourcebox.configure(state='disabled')

        state={'rows':[],'matches':[]}

        def refresh(*_):
            idx=lb.curselection()[0] if lb.curselection() else 0
            cat=categories[idx]
            title,formula,domain,ai,keys,_=cat
            titlev.set(title); formulav.set(formula); domainv.set('Mathematics: '+domain); aiv.set(ai)
            pybox.configure(state='normal'); pybox.delete('1.0','end'); pybox.insert('1.0',self._v44_python_equivalent(cat)); pybox.configure(state='disabled')
            self._v44_draw_gallery_graph(cv,cat)
            state['matches']=[r for r in state['rows'] if self._v44_match_category(r,cat)]
            matchlb.delete(0,'end')
            for r in state['matches'][:300]:
                matchlb.insert('end',f"{r['file']}   [{len(r['equations'])} eq]")
            if not state['matches']:
                matchlb.insert('end','— ยังไม่มีผล scan หรือไม่พบ source ที่ตรงกับหัวข้อนี้ —')

        def show_source(*_):
            if not matchlb.curselection() or not state['matches']: return
            i=matchlb.curselection()[0]
            if i>=len(state['matches']): return
            r=state['matches'][i]
            sourcebox.configure(state='normal'); sourcebox.delete('1.0','end')
            sourcebox.insert('1.0',f"FILE: {r['file']}\nLANGUAGE: {r['lang']}\nMATH: {', '.join(r['tags'])}\nAI: {r['ai']}\n\n{r['source']}")
            sourcebox.configure(state='disabled')

        def load_zip():
            zp=filedialog.askopenfilename(title='Select TC ZIP',filetypes=[('ZIP','*.zip')])
            if not zp:return
            loadbtn.configure(state='disabled'); scanstatus.set('กำลังสร้าง Math Gallery จาก source files...')
            self.update_idletasks()
            def prog(i,n):
                scanstatus.set(f'กำลังอ่าน {i:,}/{n:,} files...')
                self.update_idletasks()
            try:
                state['rows']=self._v43_scan_zip(zp,prog)
                eqs=sum(len(r['equations']) for r in state['rows'])
                scanstatus.set(f"พร้อมใช้งาน: {len(state['rows']):,} source files • {eqs:,} detected assignments")
                refresh()
            except Exception as e:
                messagebox.showerror('Math Gallery',str(e)); scanstatus.set('สแกนไม่สำเร็จ')
            finally:
                loadbtn.configure(state='normal')

        loadbtn.configure(command=load_zip)
        lb.bind('<<ListboxSelect>>',refresh); matchlb.bind('<<ListboxSelect>>',show_source)
        cv.bind('<Configure>',lambda e:refresh())
        refresh()

        pedagogy=self.card(b,'เส้นทางการเรียนรู้',
            '1) อ่าน Original Pascal/C → 2) ระบุ mathematical idea → 3) ดูสูตรมาตรฐาน → 4) ทดลองกราฟ → '
            '5) อ่าน Python equivalent → 6) เชื่อมกับ AI application. '
            'Gallery ใช้กราฟมาตรฐานที่กำหนดไว้สำหรับแต่ละแนวคิดเพื่อไม่ให้ source code ที่ไม่สมบูรณ์สร้างภาพทางคณิตศาสตร์ที่ผิด')
        tk.Label(pedagogy,text='TC Legacy Code  →  Mathematics  →  Visualization  →  Python  →  Artificial Intelligence',
                 bg='white',fg=BLUE,font=('Segoe UI Semibold',11)).pack(anchor='w',padx=18,pady=(0,14))

    # ==================== v5 MATH ANIMATION LAB ====================
    def math_animation_lab(self):
        self.clear()
        self.header('🎞 • v5 Math Animation Laboratory',
                    'ลำดับการเรียน: Parabola → Circle → Vector → Matrix → Derivative พร้อม Animation, Formula และ AI Connection')
        b=self.scrollbody()
        intro=self.card(b,'Visual Mathematics → AI',
            'ปรับพารามิเตอร์ด้วย Slider แล้วกราฟจะเปลี่ยนทันที กด Animate เพื่อดูการเปลี่ยนแปลงต่อเนื่อง '
            'ทุกบทแสดงสมการ ค่าที่คำนวณได้ และความเชื่อมโยงกับ AI/Robot โดยใช้ coordinate system และ scale ที่สอดคล้องกัน')
        nav=tk.Frame(intro,bg='white'); nav.pack(fill='x',padx=18,pady=(0,14))
        lessons=['1 • Parabola','2 • Circle','3 • Vector','4 • Matrix','5 • Derivative']
        lesson=tk.StringVar(value=lessons[0])
        for name in lessons:
            ttk.Radiobutton(nav,text=name,value=name,variable=lesson).pack(side='left',padx=4)

        work=tk.PanedWindow(b,orient='horizontal',sashwidth=5,bg=BG); work.pack(fill='both',expand=True,padx=28,pady=8)
        controls=tk.Frame(work,bg='white',highlightbackground=BORDER,highlightthickness=1)
        visual=tk.Frame(work,bg='white',highlightbackground=BORDER,highlightthickness=1)
        work.add(controls,minsize=330); work.add(visual,minsize=720)

        ctl_title=tk.Label(controls,text='',bg='white',fg=TEXT,font=('Segoe UI Semibold',15))
        ctl_title.pack(anchor='w',padx=14,pady=(14,5))
        formula=tk.StringVar()
        tk.Label(controls,textvariable=formula,bg='white',fg=BLUE,font=('Cambria Math',14),wraplength=300,justify='left').pack(anchor='w',padx=14,pady=(0,10))
        sliders=tk.Frame(controls,bg='white'); sliders.pack(fill='x',padx=14)
        values=tk.StringVar()
        tk.Label(controls,textvariable=values,bg='white',fg=TEXT,font=('Consolas',9),justify='left',wraplength=300).pack(anchor='w',padx=14,pady=10)
        ai=tk.StringVar()
        box=tk.Frame(controls,bg='#f8fafc'); box.pack(fill='x',padx=14,pady=8)
        tk.Label(box,text='AI / Robot Connection',bg='#f8fafc',fg=TEXT,font=('Segoe UI Semibold',10)).pack(anchor='w',padx=10,pady=(8,2))
        tk.Label(box,textvariable=ai,bg='#f8fafc',fg=TEXT,font=('Segoe UI',9),wraplength=285,justify='left').pack(anchor='w',padx=10,pady=(0,8))
        btnrow=tk.Frame(controls,bg='white'); btnrow.pack(fill='x',padx=14,pady=10)
        animbtn=ttk.Button(btnrow,text='▶ Animate',style='Primary.TButton'); animbtn.pack(side='left')
        resetbtn=ttk.Button(btnrow,text='Reset'); resetbtn.pack(side='left',padx=6)

        cv=tk.Canvas(visual,height=560,bg='#fbfdff',highlightthickness=0)
        cv.pack(fill='both',expand=True,padx=12,pady=12)
        caption=tk.StringVar()
        tk.Label(visual,textvariable=caption,bg='white',fg=MUTED,font=('Segoe UI',9),wraplength=700,justify='left').pack(anchor='w',padx=14,pady=(0,12))

        state={'scales':{},'running':False,'after':None,'phase':0.0}

        def cancel_anim():
            state['running']=False
            if state.get('after'):
                try:self.after_cancel(state['after'])
                except Exception:pass
                state['after']=None
            animbtn.configure(text='▶ Animate')

        def scale(parent,label,frm,to,val,res=.1):
            row=tk.Frame(parent,bg='white'); row.pack(fill='x',pady=4)
            var=tk.DoubleVar(value=val)
            tk.Label(row,text=label,bg='white',fg=TEXT,width=8,anchor='w').pack(side='left')
            sc=ttk.Scale(row,from_=frm,to=to,variable=var)
            sc.pack(side='left',fill='x',expand=True,padx=5)
            lab=tk.Label(row,text=f'{val:.2f}',bg='white',fg=MUTED,width=7)
            lab.pack(side='right')
            var.trace_add('write',lambda *_v,v=var,l=lab: (l.configure(text=f'{v.get():.2f}'),draw()))
            return var

        def axes(xmin=-6,xmax=6,ymin=-6,ymax=6):
            cv.delete('all'); w=max(680,cv.winfo_width()); h=max(480,cv.winfo_height())
            L,R,T,B=55,w-25,30,h-45
            cv.create_rectangle(0,0,w,h,fill='#fbfdff',outline='')
            def sx(x):return L+(x-xmin)/(xmax-xmin)*(R-L)
            def sy(y):return B-(y-ymin)/(ymax-ymin)*(B-T)
            for k in range(13):
                x=xmin+(xmax-xmin)*k/12; px=sx(x)
                cv.create_line(px,T,px,B,fill='#e7edf3')
                if k%2==0:cv.create_text(px,B+15,text=f'{x:.1f}',fill=MUTED,font=('Segoe UI',8))
            for k in range(13):
                y=ymin+(ymax-ymin)*k/12; py=sy(y)
                cv.create_line(L,py,R,py,fill='#e7edf3')
                if k%2==0:cv.create_text(L-7,py,text=f'{y:.1f}',anchor='e',fill=MUTED,font=('Segoe UI',8))
            if xmin<=0<=xmax:cv.create_line(sx(0),T,sx(0),B,fill='#64748b',width=2)
            if ymin<=0<=ymax:cv.create_line(L,sy(0),R,sy(0),fill='#64748b',width=2)
            return sx,sy,L,R,T,B

        def polyline(points,sx,sy,color='#2563eb',width=3):
            seg=[]
            for x,y in points:
                px,py=sx(x),sy(y)
                seg += [px,py]
            if len(seg)>=4:cv.create_line(*seg,fill=color,width=width,smooth=True)

        def arrow(x1,y1,x2,y2,sx,sy,color='#2563eb',width=4):
            cv.create_line(sx(x1),sy(y1),sx(x2),sy(y2),fill=color,width=width,arrow='last',arrowshape=(12,14,5))

        def setup(*_):
            cancel_anim()
            for child in sliders.winfo_children():child.destroy()
            state['scales']={}
            name=lesson.get()
            if name.startswith('1'):
                ctl_title.configure(text='Parabola Animation')
                formula.set('y = ax² + bx + c')
                state['scales']['a']=scale(sliders,'a',-3,3,1,.05)
                state['scales']['b']=scale(sliders,'b',-6,6,0,.1)
                state['scales']['c']=scale(sliders,'c',-6,6,0,.1)
                ai.set('Quadratic curves → regression, loss surfaces และ trajectory planning')
                caption.set('สังเกต a ควบคุมทิศและความกว้าง, b เลื่อนตำแหน่ง vertex และ c คือ y-intercept')
            elif name.startswith('2'):
                ctl_title.configure(text='Circle Animation')
                formula.set('(x-h)² + (y-k)² = r²')
                state['scales']['h']=scale(sliders,'h',-4,4,0,.1)
                state['scales']['k']=scale(sliders,'k',-4,4,0,.1)
                state['scales']['r']=scale(sliders,'r',.5,5,3,.05)
                ai.set('Circle/distance → target zones, collision radius, k-NN และ object tracking')
                caption.set('ศูนย์กลาง (h,k) และรัศมี r เปลี่ยน geometry โดยตรง; จุดบนวงกลมห่างจากศูนย์กลางเท่ากับ r')
            elif name.startswith('3'):
                ctl_title.configure(text='Vector Animation')
                formula.set('v = (vx, vy),  |v| = √(vx²+vy²),  θ = atan2(vy,vx)')
                state['scales']['vx']=scale(sliders,'vx',-5,5,3,.1)
                state['scales']['vy']=scale(sliders,'vy',-5,5,2,.1)
                ai.set('Vector → image coordinates, robot direction, embeddings และ cosine similarity')
                caption.set('ลูกศรแสดงทั้งขนาดและทิศทางของเวกเตอร์; มุมคำนวณด้วย atan2')
            elif name.startswith('4'):
                ctl_title.configure(text='Matrix Transformation')
                formula.set('[x′ y′]ᵀ = [[a,b],[c,d]] [x y]ᵀ')
                for key,label,val in [('a','a',1),('b','b',0),('c','c',0),('d','d',1)]:
                    state['scales'][key]=scale(sliders,label,-2.5,2.5,val,.05)
                ai.set('Matrix → neural-network layers, image transforms, coordinate transforms และ robotics')
                caption.set('กริดเดิมและฐานเวกเตอร์ถูกแปลงด้วยเมทริกซ์ 2×2; determinant บอกการย่อ/ขยายพื้นที่และการกลับทิศ')
            else:
                ctl_title.configure(text='Derivative & Tangent')
                formula.set("f(x)=x²/2   →   f′(x)=x")
                state['scales']['x0']=scale(sliders,'x₀',-4,4,1,.05)
                ai.set('Derivative → gradient, gradient descent, optimization และ training ของโมเดล AI')
                caption.set('เส้น tangent มีความชันเท่ากับ derivative ณ x₀; จุดจะเคลื่อนบนกราฟเมื่อปรับ x₀')
            draw()

        def draw():
            if not state['scales']:return
            name=lesson.get()
            if name.startswith('1'):
                a=state['scales']['a'].get();bb=state['scales']['b'].get();c=state['scales']['c'].get()
                sx,sy,*_=axes(-6,6,-8,8)
                pts=[(x,a*x*x+bb*x+c) for x in [(-6+i*.03) for i in range(401)] if -8<=a*x*x+bb*x+c<=8]
                polyline(pts,sx,sy)
                if abs(a)>1e-8:
                    xv=-bb/(2*a);yv=a*xv*xv+bb*xv+c
                    if -6<=xv<=6 and -8<=yv<=8:
                        cv.create_oval(sx(xv)-5,sy(yv)-5,sx(xv)+5,sy(yv)+5,fill='#dc2626',outline='')
                        cv.create_text(sx(xv)+8,sy(yv)-10,text=f'V({xv:.2f},{yv:.2f})',anchor='w',fill='#dc2626')
                disc=bb*bb-4*a*c
                values.set(f'a={a:.3f}, b={bb:.3f}, c={c:.3f}\nDiscriminant Δ=b²−4ac = {disc:.3f}')
            elif name.startswith('2'):
                h=state['scales']['h'].get();k=state['scales']['k'].get();r=state['scales']['r'].get()
                sx,sy,*_=axes(-7,7,-7,7)
                pts=[(h+r*math.cos(t),k+r*math.sin(t)) for t in [i*2*math.pi/240 for i in range(241)]]
                polyline(pts,sx,sy)
                cv.create_oval(sx(h)-5,sy(k)-5,sx(h)+5,sy(k)+5,fill='#dc2626',outline='')
                arrow(h,k,h+r,k,sx,sy,'#059669',3)
                values.set(f'center=({h:.2f},{k:.2f}), r={r:.2f}\nArea=πr²={math.pi*r*r:.3f}\nCircumference=2πr={2*math.pi*r:.3f}')
            elif name.startswith('3'):
                vx=state['scales']['vx'].get();vy=state['scales']['vy'].get()
                sx,sy,*_=axes(-6,6,-6,6);arrow(0,0,vx,vy,sx,sy)
                mag=math.hypot(vx,vy);ang=math.degrees(math.atan2(vy,vx)) if mag>1e-12 else 0
                cv.create_text(sx(vx)+8,sy(vy)-8,text=f'v=({vx:.2f},{vy:.2f})',anchor='w',fill=TEXT)
                values.set(f'vx={vx:.3f}, vy={vy:.3f}\n|v|={mag:.3f}\nθ={ang:.2f}°')
            elif name.startswith('4'):
                a=state['scales']['a'].get();bb=state['scales']['b'].get();c=state['scales']['c'].get();d=state['scales']['d'].get()
                sx,sy,*_=axes(-7,7,-7,7)
                # original grid
                for q in range(-4,5):
                    polyline([(q,-4),(q,4)],sx,sy,'#cbd5e1',1);polyline([(-4,q),(4,q)],sx,sy,'#cbd5e1',1)
                # transformed grid
                def tr(x,y):return a*x+bb*y,c*x+d*y
                for q in range(-4,5):
                    polyline([tr(q,-4),tr(q,4)],sx,sy,'#93c5fd',2);polyline([tr(-4,q),tr(4,q)],sx,sy,'#93c5fd',2)
                e1=tr(1,0);e2=tr(0,1);arrow(0,0,*e1,sx,sy,'#dc2626',4);arrow(0,0,*e2,sx,sy,'#059669',4)
                det=a*d-bb*c
                values.set(f'M=[[{a:.2f},{bb:.2f}],[{c:.2f},{d:.2f}]]\ndet(M)={det:.3f}\n|det| = area scale factor')
            else:
                x0=state['scales']['x0'].get();sx,sy,*_=axes(-5,5,-2,12)
                f=lambda x:x*x/2
                pts=[(x,f(x)) for x in [(-5+i*.025) for i in range(401)] if -2<=f(x)<=12]
                polyline(pts,sx,sy)
                y0=f(x0);m=x0
                x1=max(-5,x0-2.5);x2=min(5,x0+2.5)
                cv.create_line(sx(x1),sy(y0+m*(x1-x0)),sx(x2),sy(y0+m*(x2-x0)),fill='#dc2626',width=3)
                cv.create_oval(sx(x0)-5,sy(y0)-5,sx(x0)+5,sy(y0)+5,fill='#059669',outline='')
                values.set(f'x₀={x0:.3f}\nf(x₀)={y0:.3f}\nf′(x₀)=slope={m:.3f}\nTangent: y−{y0:.3f}={m:.3f}(x−{x0:.3f})')

        def animate():
            if state['running']:
                cancel_anim();return
            state['running']=True;animbtn.configure(text='⏸ Stop')
            def tick():
                if not state['running']:return
                state['phase']+=.07
                name=lesson.get();p=state['phase']
                if name.startswith('1'):
                    state['scales']['a'].set(1.5*math.sin(p))
                    state['scales']['b'].set(3*math.sin(p*.7))
                elif name.startswith('2'):
                    state['scales']['r'].set(2.75+2*math.sin(p)*.8)
                    state['scales']['h'].set(2*math.sin(p*.55))
                elif name.startswith('3'):
                    state['scales']['vx'].set(4*math.cos(p));state['scales']['vy'].set(4*math.sin(p))
                elif name.startswith('4'):
                    state['scales']['a'].set(math.cos(p));state['scales']['b'].set(-math.sin(p))
                    state['scales']['c'].set(math.sin(p));state['scales']['d'].set(math.cos(p))
                else:
                    state['scales']['x0'].set(3.5*math.sin(p*.65))
                state['after']=self.after(70,tick)
            tick()

        def reset():
            setup()

        lesson.trace_add('write',setup)
        animbtn.configure(command=animate);resetbtn.configure(command=reset)
        cv.bind('<Configure>',lambda e:draw())
        setup()

        flow=self.card(b,'ลำดับการเรียนของ v5',
            '① Parabola: coefficients และ discriminant → ② Circle: center/radius/distance → '
            '③ Vector: magnitude/direction → ④ Matrix: linear transformation/determinant → '
            '⑤ Derivative: tangent/slope → จากนั้นเชื่อมไป Regression, Computer Vision, Robotics, Neural Networks และ Gradient Descent')
        tk.Label(flow,text='Math moves → Student observes → Formula explains → AI applies',
                 bg='white',fg=BLUE,font=('Segoe UI Semibold',11)).pack(anchor='w',padx=18,pady=(0,14))

    # ==================== v5.1 TC SOURCE -> LIVE MATH ====================
    def _v51_detect_live_kind(self, name, source, recs):
        hay=(name+' '+source[:100000]).lower()
        scores={'Parabola':0,'Circle':0,'Trigonometry':0,'Vector':0,'Matrix':0,'Derivative':0,'Statistics':0}
        rules={
            'Parabola':[('parab',6),('quadratic',5),('x*x',3),('sqr(x)',3)],
            'Circle':[('circle',6),('radius',4),('sqrt',1),('distance',2)],
            'Trigonometry':[('sin(',5),('cos(',5),('tan(',4),('angle',2)],
            'Vector':[('vector',6),('dot',4),('cross',4),('magnitude',3)],
            'Matrix':[('matrix',7),('determin',4),('inverse',4),('matmul',5)],
            'Derivative':[('deriv',7),('gradient',5),('diff',3),('newton',3),('integral',2)],
            'Statistics':[('mean',5),('variance',6),('std',5),('sigma',4),('average',4)]
        }
        for kind,items in rules.items():
            for token,w in items:
                scores[kind]+=hay.count(token)*w
        # Parsed expressions add mathematical evidence.
        if sp is not None:
            for r in recs:
                ex=r.get('expr')
                if ex is None: continue
                try:
                    if any(ex.has(f) for f in (sp.sin,sp.cos,sp.tan)): scores['Trigonometry']+=8
                    syms=sorted(ex.free_symbols,key=lambda s:s.name)
                    if len(syms)==1:
                        try:
                            deg=sp.Poly(ex,syms[0]).degree()
                            if deg==2:scores['Parabola']+=7
                        except Exception:pass
                    if len(syms)>=2:scores['Vector']+=1
                except Exception:pass
        best=max(scores,key=scores.get)
        return (best,scores[best],scores) if scores[best]>0 else ('General',0,scores)

    def _v51_relevant_lines(self, source, kind, recs):
        patterns={
            'Parabola':r'parab|quadratic|x\s*\*\s*x|sqr\s*\(\s*x',
            'Circle':r'circle|radius|distance|sqrt|sqr\s*\(',
            'Trigonometry':r'\bsin\s*\(|\bcos\s*\(|\btan\s*\(|angle',
            'Vector':r'vector|\bdot\b|\bcross\b|magnitude|distance',
            'Matrix':r'matrix|determin|inverse|matmul',
            'Derivative':r'deriv|gradient|\bdiff\b|newton|integral',
            'Statistics':r'mean|average|variance|\bstd\b|sigma',
        }
        pat=patterns.get(kind,r'$^')
        lines=source.splitlines()
        hits=[]
        for i,line in enumerate(lines,1):
            if re.search(pat,line,re.I):
                hits.append(i)
        # Also highlight lines containing extracted assignment raw text / lhs.
        for r in recs[:100]:
            raw=r.get('raw','').strip()
            lhs=r.get('lhs','').strip()
            for i,line in enumerate(lines,1):
                if raw and raw in line:
                    hits.append(i)
                elif lhs and re.search(r'\b'+re.escape(lhs)+r'\b\s*(?::=|=)',line):
                    hits.append(i)
        return sorted(set(hits))[:300]

    def _v51_draw_source_math(self, cv, kind, params, phase=0.0):
        cv.delete('all')
        w=max(650,cv.winfo_width()); h=max(430,cv.winfo_height())
        L,R,T,B=55,w-24,34,h-44
        cv.create_rectangle(0,0,w,h,fill='#fbfdff',outline='')
        xmin,xmax,ymin,ymax=-6,6,-6,6
        def sx(x):return L+(x-xmin)/(xmax-xmin)*(R-L)
        def sy(y):return B-(y-ymin)/(ymax-ymin)*(B-T)
        for k in range(13):
            x=xmin+k; px=sx(x); cv.create_line(px,T,px,B,fill='#e8edf3')
            if k%2==0:cv.create_text(px,B+14,text=f'{x:g}',fill=MUTED,font=('Segoe UI',8))
            y=ymin+k; py=sy(y); cv.create_line(L,py,R,py,fill='#e8edf3')
            if k%2==0:cv.create_text(L-6,py,text=f'{y:g}',anchor='e',fill=MUTED,font=('Segoe UI',8))
        cv.create_line(sx(0),T,sx(0),B,fill='#64748b',width=2)
        cv.create_line(L,sy(0),R,sy(0),fill='#64748b',width=2)
        def line(points,color='#2563eb',width=3):
            coords=[]
            for x,y in points:
                if xmin<=x<=xmax and ymin<=y<=ymax:coords += [sx(x),sy(y)]
            if len(coords)>=4:cv.create_line(*coords,fill=color,width=width,smooth=True)
        def arrow(x1,y1,x2,y2,color='#2563eb'):
            cv.create_line(sx(x1),sy(y1),sx(x2),sy(y2),fill=color,width=4,arrow='last',arrowshape=(12,14,5))
        if kind=='Parabola':
            a=params.get('a',1);bb=params.get('b',0);c=params.get('c',0)
            pts=[] 
            for i in range(481):
                x=-6+i*.025;y=a*x*x+bb*x+c
                if -6<=y<=6:pts.append((x,y))
            line(pts)
            cv.create_text(L,18,text=f'y = {a:.2f}x² + {bb:.2f}x + {c:.2f}',anchor='w',fill=TEXT,font=('Cambria Math',12))
        elif kind=='Circle':
            hh=params.get('h',0);kk=params.get('k',0);r=max(.2,params.get('r',3))
            pts=[(hh+r*math.cos(i*2*math.pi/240),kk+r*math.sin(i*2*math.pi/240)) for i in range(241)]
            line(pts);cv.create_oval(sx(hh)-4,sy(kk)-4,sx(hh)+4,sy(kk)+4,fill='#dc2626',outline='')
            arrow(hh,kk,hh+r,kk,'#059669')
            cv.create_text(L,18,text=f'(x−{hh:.2f})² + (y−{kk:.2f})² = {r:.2f}²',anchor='w',fill=TEXT,font=('Cambria Math',12))
        elif kind=='Trigonometry':
            amp=params.get('amp',2.5);freq=params.get('freq',1)
            pts=[(x,amp*math.sin(freq*x+phase)) for x in [-6+i*.025 for i in range(481)]]
            line(pts);cv.create_text(L,18,text=f'y = {amp:.2f} sin({freq:.2f}x + phase)',anchor='w',fill=TEXT,font=('Cambria Math',12))
        elif kind=='Vector':
            vx=params.get('vx',3);vy=params.get('vy',2);arrow(0,0,vx,vy)
            cv.create_text(L,18,text=f'v = ({vx:.2f}, {vy:.2f}), |v|={math.hypot(vx,vy):.2f}',anchor='w',fill=TEXT,font=('Cambria Math',12))
        elif kind=='Matrix':
            a=params.get('a',1);bb=params.get('b',0);c=params.get('c',0);d=params.get('d',1)
            def tr(x,y):return a*x+bb*y,c*x+d*y
            for q in range(-4,5):
                line([(q,-4),(q,4)],'#cbd5e1',1);line([(-4,q),(4,q)],'#cbd5e1',1)
                line([tr(q,-4),tr(q,4)],'#60a5fa',2);line([tr(-4,q),tr(4,q)],'#60a5fa',2)
            arrow(0,0,*tr(1,0),'#dc2626');arrow(0,0,*tr(0,1),'#059669')
            cv.create_text(L,18,text=f'M=[[{a:.2f},{bb:.2f}],[{c:.2f},{d:.2f}]], det={a*d-bb*c:.2f}',anchor='w',fill=TEXT,font=('Cambria Math',12))
        elif kind=='Derivative':
            x0=params.get('x0',1);f=lambda x:x*x/2
            line([(x,f(x)) for x in [-5+i*.025 for i in range(401)] if -6<=f(x)<=6])
            y0=f(x0);m=x0
            x1=max(-5,x0-2);x2=min(5,x0+2)
            cv.create_line(sx(x1),sy(y0+m*(x1-x0)),sx(x2),sy(y0+m*(x2-x0)),fill='#dc2626',width=3)
            cv.create_oval(sx(x0)-5,sy(y0)-5,sx(x0)+5,sy(y0)+5,fill='#059669',outline='')
            cv.create_text(L,18,text=f"f(x)=x²/2, f′({x0:.2f})={m:.2f}",anchor='w',fill=TEXT,font=('Cambria Math',12))
        elif kind=='Statistics':
            vals=[-4,-2.8,-2,-1.5,-.7,0,.4,.9,1.3,2,2.5,3.5]
            mu=sum(vals)/len(vals);sd=math.sqrt(sum((v-mu)**2 for v in vals)/len(vals))
            for x in vals:cv.create_oval(sx(x)-5,sy(0)-5,sx(x)+5,sy(0)+5,fill='#2563eb',outline='')
            cv.create_line(sx(mu),T,sx(mu),B,fill='#dc2626',width=3)
            cv.create_line(sx(mu-sd),T,sx(mu-sd),B,fill='#059669',width=2,dash=(5,3))
            cv.create_line(sx(mu+sd),T,sx(mu+sd),B,fill='#059669',width=2,dash=(5,3))
            cv.create_text(L,18,text=f'μ={mu:.2f}, σ={sd:.2f}, z=(x−μ)/σ',anchor='w',fill=TEXT,font=('Cambria Math',12))
        else:
            cv.create_text(w/2,h/2,text='General source: เลือกสมการที่ตรวจพบด้านซ้ายเพื่อดู symbolic information',fill=MUTED,font=('Segoe UI',11))

    def tc_live_math_lab(self):
        self.clear()
        self.header('🔗 • v5.1 TC Source → Live Math',
                    'เปิด Pascal/C → ตรวจคณิตศาสตร์อัตโนมัติ → Highlight บรรทัดสำคัญ → เลือก Animation → เชื่อม AI')
        b=self.scrollbody()
        intro=self.card(b,'Source-aware Mathematics',
            'v5.1 ทำให้ source code เป็นจุดเริ่มต้นของบทเรียน: ระบบอ่านข้อความ ไม่ execute code ที่นำเข้า '
            'แล้วใช้ pattern + symbolic equations เพื่อเลือก Visual Math ที่เหมาะสม พร้อม highlight บรรทัดที่สัมพันธ์กับแนวคิด')
        top=tk.Frame(intro,bg='white');top.pack(fill='x',padx=18,pady=(0,14))
        ttk.Button(top,text='Open .PAS / .C',style='Primary.TButton').pack(side='left')
        openbtn=top.winfo_children()[-1]
        ttk.Button(top,text='Choose from TC ZIP').pack(side='left',padx=6)
        zipbtn=top.winfo_children()[-1]
        filev=tk.StringVar(value='ยังไม่ได้เลือก source')
        tk.Label(top,textvariable=filev,bg='white',fg=MUTED,font=('Segoe UI',9)).pack(side='left',padx=10)

        body=tk.PanedWindow(b,orient='horizontal',sashwidth=5,bg=BG);body.pack(fill='both',expand=True,padx=28,pady=8)
        left=tk.Frame(body,bg='white',highlightbackground=BORDER,highlightthickness=1)
        right=tk.Frame(body,bg='white',highlightbackground=BORDER,highlightthickness=1)
        body.add(left,minsize=520);body.add(right,minsize=700)

        detected=tk.StringVar(value='Detected Math: —')
        tk.Label(left,textvariable=detected,bg='white',fg=BLUE,font=('Segoe UI Semibold',11)).pack(anchor='w',padx=12,pady=(10,4))
        srcbox=tk.Text(left,height=25,font=('Consolas',8),wrap='none')
        srcbox.pack(fill='both',expand=True,padx=12,pady=4)
        srcbox.tag_configure('mathhit',background='#fef3c7',foreground='#92400e')
        srcbox.tag_configure('current',background='#dbeafe',foreground='#1e3a8a')
        eqv=tk.StringVar(value='Detected equations: —')
        tk.Label(left,textvariable=eqv,bg='white',fg=MUTED,font=('Segoe UI',9),wraplength=500,justify='left').pack(anchor='w',padx=12,pady=(4,10))

        tk.Label(right,text='Live Mathematical Visualization',bg='white',fg=TEXT,font=('Segoe UI Semibold',13)).pack(anchor='w',padx=12,pady=(10,3))
        kindv=tk.StringVar(value='General')
        kindbox=ttk.Combobox(right,textvariable=kindv,state='readonly',
            values=['Parabola','Circle','Trigonometry','Vector','Matrix','Derivative','Statistics','General'])
        kindbox.pack(anchor='w',padx=12,pady=4)
        ctl=tk.Frame(right,bg='white');ctl.pack(fill='x',padx=12,pady=4)
        cv=tk.Canvas(right,height=440,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1)
        cv.pack(fill='both',expand=True,padx=12,pady=6)
        explain=tk.StringVar(value='เลือก source เพื่อเริ่มวิเคราะห์')
        tk.Label(right,textvariable=explain,bg='white',fg=MUTED,font=('Segoe UI',9),wraplength=680,justify='left').pack(anchor='w',padx=12,pady=(0,10))

        state={'source':'','recs':[],'params':{},'running':False,'after':None,'phase':0}

        def stop():
            state['running']=False
            if state.get('after'):
                try:self.after_cancel(state['after'])
                except Exception:pass
                state['after']=None

        def make_controls():
            stop()
            for w in ctl.winfo_children():w.destroy()
            state['params']={}
            specs={
                'Parabola':[('a',-3,3,1),('b',-5,5,0),('c',-5,5,0)],
                'Circle':[('h',-4,4,0),('k',-4,4,0),('r',.3,5,3)],
                'Trigonometry':[('amp',.2,5,2.5),('freq',.2,3,1)],
                'Vector':[('vx',-5,5,3),('vy',-5,5,2)],
                'Matrix':[('a',-2,2,1),('b',-2,2,0),('c',-2,2,0),('d',-2,2,1)],
                'Derivative':[('x0',-4,4,1)],
                'Statistics':[]
            }.get(kindv.get(),[])
            for key,lo,hi,val in specs:
                frame=tk.Frame(ctl,bg='white');frame.pack(side='left',padx=3)
                tk.Label(frame,text=key,bg='white',font=('Segoe UI',8)).pack()
                v=tk.DoubleVar(value=val);state['params'][key]=v
                ttk.Scale(frame,from_=lo,to=hi,variable=v,length=95,command=lambda _=None:draw()).pack()
            ttk.Button(ctl,text='▶ Animate',command=animate).pack(side='left',padx=8)
            draw()

        def params():
            return {k:v.get() for k,v in state['params'].items()}

        def draw():
            self._v51_draw_source_math(cv,kindv.get(),params(),state['phase'])

        def animate():
            if state['running']:
                stop();return
            state['running']=True
            def tick():
                if not state['running']:return
                state['phase']+=.08
                k=kindv.get();p=state['phase']
                try:
                    if k=='Parabola':
                        state['params']['a'].set(1.5*math.sin(p));state['params']['b'].set(2.5*math.cos(p*.7))
                    elif k=='Circle':
                        state['params']['r'].set(2.7+1.4*math.sin(p));state['params']['h'].set(1.5*math.cos(p*.6))
                    elif k=='Vector':
                        state['params']['vx'].set(4*math.cos(p));state['params']['vy'].set(4*math.sin(p))
                    elif k=='Matrix':
                        state['params']['a'].set(math.cos(p));state['params']['b'].set(-math.sin(p));state['params']['c'].set(math.sin(p));state['params']['d'].set(math.cos(p))
                    elif k=='Derivative':state['params']['x0'].set(3.5*math.sin(p*.6))
                    elif k=='Trigonometry':pass
                    draw()
                except Exception:pass
                state['after']=self.after(70,tick)
            tick()

        def analyze(name,source):
            stop();state['source']=source
            recs=self._extract_equations_auto(source);state['recs']=recs
            kind,score,scores=self._v51_detect_live_kind(name,source,recs)
            filev.set(name);kindv.set(kind)
            srcbox.configure(state='normal');srcbox.delete('1.0','end');srcbox.insert('1.0',source[:150000])
            srcbox.tag_remove('mathhit','1.0','end')
            hits=self._v51_relevant_lines(source,kind,recs)
            for ln in hits:
                srcbox.tag_add('mathhit',f'{ln}.0',f'{ln}.end')
            if hits:srcbox.see(f'{hits[0]}.0')
            srcbox.configure(state='disabled')
            detected.set(f'Detected Math: {kind}  • confidence evidence score={score}  • highlighted lines={len(hits)}')
            eqs=[]
            for r in recs[:6]:
                eqs.append(f"{r['lhs']} = {r.get('expr') if r.get('expr') is not None else r['raw']}")
            eqv.set('Detected equations: '+(' | '.join(eqs) if eqs else 'ไม่พบ assignment ที่ parse ได้'))
            connections={
                'Parabola':'Quadratic → regression / loss / trajectory',
                'Circle':'Distance geometry → k-NN / tracking / collision zone',
                'Trigonometry':'sin/cos → rotation / periodic sensor / robot pose',
                'Vector':'magnitude + direction → vision / robot movement / embeddings',
                'Matrix':'linear transform → neural network / image transform',
                'Derivative':'slope → gradient descent / optimization',
                'Statistics':'mean/SD/Z-score → normalization / anomaly detection',
                'General':'อ่าน source และสมการที่ตรวจพบ โดยไม่เดาคณิตศาสตร์เกินหลักฐาน'
            }
            explain.set(f'Auto-selected: {kind}. AI connection: {connections[kind]}. สามารถเปลี่ยนชนิด visualization จาก combobox เพื่อเปรียบเทียบได้')
            make_controls()

        def open_file():
            p=filedialog.askopenfilename(title='Open Pascal/C',filetypes=[('Pascal/C','*.pas *.pp *.c *.h *.cpp *.cc *.cxx *.hpp'),('All','*.*')])
            if not p:return
            data=Path(p).read_bytes();source,_=self._v43_decode(data);analyze(Path(p).name,source)

        def choose_zip():
            zp=filedialog.askopenfilename(title='Choose TC ZIP',filetypes=[('ZIP','*.zip')])
            if not zp:return
            try:
                with zipfile.ZipFile(zp) as z:names=[n for n in z.namelist() if n.lower().endswith(('.pas','.pp','.c','.h','.cpp','.cc','.cxx','.hpp'))]
                win=tk.Toplevel(self);win.title('Choose TC source');win.geometry('820x600')
                q=tk.StringVar();ent=ttk.Entry(win,textvariable=q);ent.pack(fill='x',padx=10,pady=8)
                lb=tk.Listbox(win,font=('Consolas',9));lb.pack(fill='both',expand=True,padx=10,pady=4)
                def fill(*_):
                    term=q.get().lower();lb.delete(0,'end')
                    for n in [n for n in names if term in n.lower()][:1000]:lb.insert('end',n)
                def pick(*_):
                    if not lb.curselection():return
                    n=lb.get(lb.curselection()[0])
                    with zipfile.ZipFile(zp) as z:data=z.read(n)
                    source,_=self._v43_decode(data);win.destroy();analyze(n,source)
                q.trace_add('write',fill);lb.bind('<Double-Button-1>',pick);ent.bind('<Return>',pick)
                ttk.Button(win,text='Open selected',command=pick).pack(pady=7);fill();ent.focus_set()
            except Exception as e:messagebox.showerror('TC ZIP',str(e))

        openbtn.configure(command=open_file);zipbtn.configure(command=choose_zip)
        kindbox.bind('<<ComboboxSelected>>',lambda e:make_controls())
        cv.bind('<Configure>',lambda e:draw())

        note=self.card(b,'v5.1 Learning Flow',
            'TC Source → Auto Detection → Highlight Relevant Code → Extract Equation → Select Live Animation → '
            'Change Parameters → Observe Mathematics → Connect to AI. '
            'Source ที่นำเข้าจะถูกอ่านข้อความเท่านั้น ไม่ compile/execute โดยอัตโนมัติ')
        tk.Label(note,text='จาก “อ่านโค้ด” → “เห็นสมการ” → “เห็นกราฟเคลื่อนไหว” → “เข้าใจว่า AI ใช้คณิตศาสตร์ตรงไหน”',
                 bg='white',fg=BLUE,font=('Segoe UI Semibold',10)).pack(anchor='w',padx=18,pady=(0,14))

    # ==================== v5.2 FOUR-PANEL LEARNING ====================
    def _v52_line_equation(self, line):
        """Parse one selected Pascal/C assignment conservatively."""
        clean=self._strip_legacy_comments(line).strip()
        m=re.search(r'^\s*([A-Za-z_]\w*)\s*(?::=|(?<![<>=!])=(?!=))\s*([^;]+)',clean)
        if not m:return None
        lhs,rhs=m.group(1),m.group(2).strip()
        rec={'lhs':lhs,'raw':rhs,'norm':self._legacy_expr_to_math(rhs),'expr':None,'latex':'','status':'text'}
        if sp is not None and parse_expr is not None:
            try:
                names=set(re.findall(r'\b[A-Za-z_]\w*\b',rec['norm']))
                funcs={'sqrt':sp.sqrt,'sin':sp.sin,'cos':sp.cos,'tan':sp.tan,
                       'exp':sp.exp,'log':sp.log,'Abs':sp.Abs,'pi':sp.pi}
                local=dict(funcs)
                for n in names:
                    if n not in local and n not in {'and','or'}:local[n]=sp.Symbol(n,real=True)
                tr=standard_transformations+(implicit_multiplication_application,convert_xor)
                ex=parse_expr(rec['norm'],local_dict=local,transformations=tr,evaluate=True)
                rec['expr']=ex;rec['latex']=sp.latex(sp.Eq(sp.Symbol(lhs),ex));rec['status']='parsed'
            except Exception:pass
        return rec

    def _v52_python_line(self, rec):
        if not rec:return "# บรรทัดนี้ไม่ใช่ assignment ทางคณิตศาสตร์"
        rhs=rec['norm'].replace('^','**')
        # Python math functions for a readable modern equivalent.
        for fn in ('sqrt','sin','cos','tan','exp','log'):
            rhs=re.sub(r'\b'+fn+r'\s*\(', 'math.'+fn+'(', rhs)
        rhs=rhs.replace('Abs(','abs(').replace('pi','math.pi')
        return f"{rec['lhs']} = {rhs}"

    def _v52_explain(self, rec, kind):
        if not rec:
            return ("บรรทัดนี้อาจเป็น control flow, I/O, declaration หรือคำสั่งกราฟิก "
                    "จึงไม่ควรบังคับแปลงเป็นสมการ")
        typ=self._v43_equation_kind(rec)
        ai={
            'Parabola':'ใช้เชื่อมกับ regression, quadratic loss และ trajectory',
            'Circle':'ใช้กับ Euclidean distance, target zone, tracking และ k-NN',
            'Trigonometry':'ใช้กับมุม การหมุน สัญญาณ และ robot pose',
            'Vector':'ใช้กับพิกัดภาพ ทิศทางหุ่นยนต์ และ embeddings',
            'Matrix':'ใช้กับ linear transformation และ neural-network layers',
            'Derivative':'ใช้กับ gradient และ optimization',
            'Statistics':'ใช้กับ normalization และ anomaly detection',
            'General':'ใช้เป็นพื้นฐาน computational mathematics'
        }.get(kind,'ใช้เป็นพื้นฐาน computational mathematics')
        return f"ชนิดสมการ: {typ}\nNormalized: {rec['lhs']} = {rec['norm']}\nความเชื่อมโยง AI: {ai}"

    def four_panel_learning_lab(self):
        self.clear()
        self.header('🧩 • v5.2 Four-Panel Learning',
                    'เลือกทีละบรรทัด: Original Code | Mathematical Formula | Animated Graph | Modern Python')
        b=self.scrollbody()
        intro=self.card(b,'Interactive Math Textbook',
            'นักเรียนเปิด Pascal/C แล้วคลิกบรรทัดใดก็ได้ โปรแกรมจะวิเคราะห์เฉพาะบรรทัดนั้น '
            'พร้อมแสดง 4 มุมมองในหน้าจอเดียว เพื่อเชื่อมจาก syntax ของโปรแกรมไปสู่สมการ ภาพ และ Python สมัยใหม่')
        bar=tk.Frame(intro,bg='white');bar.pack(fill='x',padx=18,pady=(0,14))
        ttk.Button(bar,text='Open .PAS / .C',style='Primary.TButton').pack(side='left')
        openbtn=bar.winfo_children()[-1]
        ttk.Button(bar,text='Choose from TC ZIP').pack(side='left',padx=6)
        zipbtn=bar.winfo_children()[-1]
        filev=tk.StringVar(value='ยังไม่ได้เลือก source')
        tk.Label(bar,textvariable=filev,bg='white',fg=MUTED,font=('Segoe UI',9)).pack(side='left',padx=10)

        # Source browser / line selector
        source_card=self.card(b,'เลือกบรรทัด Source Code',
            'คลิกบรรทัดเพื่อเปิดรายละเอียด หรือใช้ปุ่ม Previous / Next เพื่อเรียนตามลำดับ')
        nav=tk.Frame(source_card,bg='white');nav.pack(fill='x',padx=18,pady=(0,5))
        linev=tk.StringVar(value='Line —')
        ttk.Button(nav,text='◀ Previous').pack(side='left');prevbtn=nav.winfo_children()[-1]
        ttk.Button(nav,text='Next ▶').pack(side='left',padx=5);nextbtn=nav.winfo_children()[-1]
        tk.Label(nav,textvariable=linev,bg='white',fg=BLUE,font=('Segoe UI Semibold',10)).pack(side='left',padx=10)
        src=tk.Text(source_card,height=13,font=('Consolas',9),wrap='none',cursor='hand2')
        src.pack(fill='x',padx=18,pady=(0,14))
        src.tag_configure('selectedline',background='#dbeafe',foreground='#1e3a8a')
        src.tag_configure('mathline',background='#fef3c7')

        # Four simultaneous panels.
        grid=tk.Frame(b,bg=BG);grid.pack(fill='both',expand=True,padx=28,pady=8)
        grid.grid_columnconfigure(0,weight=1);grid.grid_columnconfigure(1,weight=1)
        grid.grid_rowconfigure(0,weight=1);grid.grid_rowconfigure(1,weight=1)

        def panel(row,col,title):
            f=tk.Frame(grid,bg='white',highlightbackground=BORDER,highlightthickness=1)
            f.grid(row=row,column=col,sticky='nsew',padx=5,pady=5)
            tk.Label(f,text=title,bg='white',fg=TEXT,font=('Segoe UI Semibold',12)).pack(anchor='w',padx=12,pady=(10,4))
            return f
        pcode=panel(0,0,'1 • Original Code')
        pmath=panel(0,1,'2 • Mathematical Formula')
        pgraph=panel(1,0,'3 • Animated Graph')
        ppython=panel(1,1,'4 • Modern Python')

        codev=tk.StringVar(value='เลือกบรรทัดจาก Source Code ด้านบน')
        tk.Label(pcode,textvariable=codev,bg='white',fg=TEXT,font=('Consolas',10),
                 justify='left',wraplength=500).pack(anchor='w',fill='x',padx=12,pady=8)
        contextv=tk.StringVar(value='—')
        tk.Label(pcode,textvariable=contextv,bg='white',fg=MUTED,font=('Segoe UI',9),
                 justify='left',wraplength=500).pack(anchor='w',fill='x',padx=12,pady=(0,12))

        formulav=tk.StringVar(value='—')
        tk.Label(pmath,textvariable=formulav,bg='white',fg=BLUE,font=('Cambria Math',15),
                 justify='left',wraplength=500).pack(anchor='w',fill='x',padx=12,pady=8)
        explainv=tk.StringVar(value='—')
        tk.Label(pmath,textvariable=explainv,bg='white',fg=TEXT,font=('Segoe UI',9),
                 justify='left',wraplength=500).pack(anchor='w',fill='x',padx=12,pady=(0,12))

        cv=tk.Canvas(pgraph,height=310,bg='#fbfdff',highlightthickness=0)
        cv.pack(fill='both',expand=True,padx=10,pady=6)
        graphv=tk.StringVar(value='เลือกบรรทัดเพื่อสร้าง visualization')
        tk.Label(pgraph,textvariable=graphv,bg='white',fg=MUTED,font=('Segoe UI',9),
                 wraplength=500,justify='left').pack(anchor='w',padx=12,pady=(0,10))

        pybox=tk.Text(ppython,height=11,font=('Consolas',10),wrap='word')
        pybox.pack(fill='both',expand=True,padx=12,pady=6)
        pybox.insert('1.0','# Modern Python equivalent จะปรากฏที่นี่');pybox.configure(state='disabled')
        runout=tk.StringVar(value='Experiment: —')
        tk.Label(ppython,textvariable=runout,bg='white',fg=MUTED,font=('Segoe UI',9),
                 justify='left',wraplength=500).pack(anchor='w',padx=12,pady=4)
        ttk.Button(ppython,text='▶ Run Safe Python Experiment',style='Primary.TButton').pack(anchor='w',padx=12,pady=(2,12))
        runbtn=ppython.winfo_children()[-1]

        state={'source':'','lines':[],'line':1,'rec':None,'kind':'General','phase':0,'running':False,'after':None}

        def stop_anim():
            state['running']=False
            if state.get('after'):
                try:self.after_cancel(state['after'])
                except Exception:pass
                state['after']=None

        def choose_kind(rec,line):
            if not rec:return 'General'
            fake=[rec]
            kind,score,_=self._v51_detect_live_kind('',line,fake)
            # Additional expression-level hints.
            if kind=='General' and sp is not None and rec.get('expr') is not None:
                ex=rec['expr']
                try:
                    if any(ex.has(f) for f in (sp.sin,sp.cos,sp.tan)):return 'Trigonometry'
                    syms=sorted(ex.free_symbols,key=lambda s:s.name)
                    if len(syms)==1:
                        try:
                            if sp.Poly(ex,syms[0]).degree()==2:return 'Parabola'
                        except Exception:pass
                except Exception:pass
            return kind

        def graph_params(kind,rec):
            # Default pedagogical parameters. We do not pretend unknown source variables have known values.
            if kind=='Parabola':return {'a':1,'b':0,'c':0}
            if kind=='Circle':return {'h':0,'k':0,'r':3}
            if kind=='Trigonometry':return {'amp':2.5,'freq':1}
            if kind=='Vector':return {'vx':3,'vy':2}
            if kind=='Matrix':return {'a':1,'b':0,'c':0,'d':1}
            if kind=='Derivative':return {'x0':1}
            return {}

        def select_line(n):
            if not state['lines']:return
            n=max(1,min(len(state['lines']),n));state['line']=n
            stop_anim()
            src.configure(state='normal')
            src.tag_remove('selectedline','1.0','end')
            src.tag_add('selectedline',f'{n}.0',f'{n}.end')
            src.see(f'{n}.0');src.configure(state='disabled')
            line=state['lines'][n-1]
            rec=self._v52_line_equation(line);state['rec']=rec
            kind=choose_kind(rec,line);state['kind']=kind
            linev.set(f'Line {n} / {len(state["lines"])}')
            codev.set(line if line.strip() else '(blank line)')
            before=state['lines'][n-2].strip() if n>1 else '—'
            after=state['lines'][n].strip() if n<len(state['lines']) else '—'
            contextv.set(f'Previous: {before[:150]}\nNext: {after[:150]}')
            if rec:
                pretty=f"{rec['lhs']} = {rec.get('expr') if rec.get('expr') is not None else rec['norm']}"
                formulav.set(pretty)
                explainv.set(self._v52_explain(rec,kind))
                py=self._v52_python_line(rec)
            else:
                formulav.set('ไม่ใช่ mathematical assignment')
                explainv.set(self._v52_explain(None,kind))
                py='# No mathematical assignment on this line\n# Read the control/programming role instead.'
            pybox.configure(state='normal');pybox.delete('1.0','end');pybox.insert('1.0',py);pybox.configure(state='disabled')
            graphv.set(f'Visualization: {kind} • ค่าพารามิเตอร์ที่ source ไม่ระบุ ใช้ค่า demo เพื่อการเรียนรู้')
            self._v51_draw_source_math(cv,kind,graph_params(kind,rec),state['phase'])
            runout.set('Experiment: พร้อมทดลอง' if rec and rec.get('expr') is not None else 'Experiment: ไม่มี symbolic expression ที่ปลอดภัยสำหรับทดลอง')

        def click_line(event):
            idx=src.index(f'@{event.x},{event.y}')
            select_line(int(idx.split('.')[0]))

        def safe_experiment():
            rec=state['rec']
            if sp is None or not rec or rec.get('expr') is None:
                runout.set('Experiment: ไม่พบ symbolic expression');return
            ex=rec['expr'];syms=sorted(ex.free_symbols,key=lambda s:s.name)
            if len(syms)>6:
                runout.set('Experiment: ตัวแปรมากเกินไปสำหรับ demo');return
            # Safe symbolic substitution only; no exec/eval of imported source.
            subs={s:(i+1) for i,s in enumerate(syms)}
            try:
                val=sp.N(ex.subs(subs),8)
                assignment=', '.join(f'{s}={v}' for s,v in subs.items()) or 'no variables'
                runout.set(f'Experiment: {assignment}  →  {rec["lhs"]} = {val}')
            except Exception as e:
                runout.set('Experiment: symbolic evaluation ไม่สำเร็จ')

        def load_source(name,source):
            stop_anim();state['source']=source;state['lines']=source.splitlines() or [''];filev.set(name)
            src.configure(state='normal');src.delete('1.0','end');src.insert('1.0',source[:180000])
            # Mark all likely mathematical assignment lines.
            for i,line in enumerate(state['lines'],1):
                if self._v52_line_equation(line):src.tag_add('mathline',f'{i}.0',f'{i}.end')
            src.configure(state='disabled')
            select_line(1)

        def open_file():
            p=filedialog.askopenfilename(title='Open Pascal/C',filetypes=[('Pascal/C','*.pas *.pp *.c *.h *.cpp *.cc *.cxx *.hpp'),('All','*.*')])
            if not p:return
            data=Path(p).read_bytes();source,_=self._v43_decode(data);load_source(Path(p).name,source)

        def choose_zip():
            zp=filedialog.askopenfilename(title='Choose TC ZIP',filetypes=[('ZIP','*.zip')])
            if not zp:return
            try:
                with zipfile.ZipFile(zp) as z:names=[n for n in z.namelist() if n.lower().endswith(('.pas','.pp','.c','.h','.cpp','.cc','.cxx','.hpp'))]
                win=tk.Toplevel(self);win.title('Choose TC source');win.geometry('820x600')
                q=tk.StringVar();ent=ttk.Entry(win,textvariable=q);ent.pack(fill='x',padx=10,pady=8)
                lb=tk.Listbox(win,font=('Consolas',9));lb.pack(fill='both',expand=True,padx=10,pady=4)
                def fill(*_):
                    term=q.get().lower();lb.delete(0,'end')
                    for n in [n for n in names if term in n.lower()][:1000]:lb.insert('end',n)
                def pick(*_):
                    if not lb.curselection():return
                    n=lb.get(lb.curselection()[0])
                    with zipfile.ZipFile(zp) as z:data=z.read(n)
                    source,_=self._v43_decode(data);win.destroy();load_source(n,source)
                q.trace_add('write',fill);lb.bind('<Double-Button-1>',pick);ent.bind('<Return>',pick)
                ttk.Button(win,text='Open selected',command=pick).pack(pady=7);fill();ent.focus_set()
            except Exception as e:messagebox.showerror('TC ZIP',str(e))

        openbtn.configure(command=open_file);zipbtn.configure(command=choose_zip)
        prevbtn.configure(command=lambda:select_line(state['line']-1))
        nextbtn.configure(command=lambda:select_line(state['line']+1))
        runbtn.configure(command=safe_experiment)
        src.bind('<Button-1>',click_line)
        cv.bind('<Configure>',lambda e:self._v51_draw_source_math(cv,state['kind'],graph_params(state['kind'],state['rec']),state['phase']))

        guide=self.card(b,'สำหรับนักเรียน',
            'บรรทัดสีเหลืองคือบรรทัดที่ระบบพบรูปแบบ mathematical assignment • คลิกทีละบรรทัดเพื่ออ่านรายละเอียด • '
            'ช่อง 1 เก็บ syntax เดิม • ช่อง 2 อธิบายสมการ • ช่อง 3 แสดงภาพทางคณิตศาสตร์ • ช่อง 4 แสดง Python equivalent. '
            'ปุ่ม Run Safe Python Experiment ใช้ SymPy substitution เท่านั้น ไม่ execute source Pascal/C และไม่ใช้ Python eval/exec กับโค้ดที่นำเข้า')
        tk.Label(guide,text='READ → FORMULA → SEE → PYTHON → EXPERIMENT → AI',
                 bg='white',fg=BLUE,font=('Segoe UI Semibold',11)).pack(anchor='w',padx=18,pady=(0,14))

    # ==================== v5.3 STUDENT EXERCISES + TEACHER MODE ====================
    def _v53_bank(self):
        return [
          {'topic':'Parabola','level':'Foundation','q':'เมื่อ y = ax²+bx+c และ a > 0 กราฟมีลักษณะอย่างไร?',
           'choices':['เปิดขึ้น','เปิดลง','เป็นเส้นตรง','เป็นวงกลม'],'ans':0,
           'why':'สัมประสิทธิ์ a กำหนดทิศการเปิดของพาราโบลา; a>0 เปิดขึ้น','skill':'Graph'},
          {'topic':'Parabola','level':'Application','q':'สำหรับ y=x²-4x+3 จุดยอดมีค่า x เท่าใด?',
           'choices':['-2','1','2','4'],'ans':2,
           'why':'x ของ vertex = -b/(2a) = 4/2 = 2','skill':'Math'},
          {'topic':'Parabola','level':'Application','q':'ถ้า Δ=b²-4ac > 0 สมการกำลังสองมีรากจริงกี่ค่า?',
           'choices':['0','1','2','บอกไม่ได้'],'ans':2,
           'why':'Discriminant มากกว่า 0 หมายถึงกราฟตัดแกน x สองจุด','skill':'Math'},
          {'topic':'Circle','level':'Foundation','q':'ใน (x-h)²+(y-k)²=r² ค่า (h,k) หมายถึงอะไร?',
           'choices':['จุดศูนย์กลาง','รัศมี','พื้นที่','ความชัน'],'ans':0,
           'why':'(h,k) คือ center และ r คือ radius','skill':'Math'},
          {'topic':'Circle','level':'Application','q':'ถ้ารัศมีเพิ่มจาก 2 เป็น 4 พื้นที่จะเปลี่ยนอย่างไร?',
           'choices':['2 เท่า','4 เท่า','6 เท่า','8 เท่า'],'ans':1,
           'why':'พื้นที่ πr²; เมื่อ r เพิ่ม 2 เท่า พื้นที่เพิ่ม 4 เท่า','skill':'Graph'},
          {'topic':'Vector','level':'Foundation','q':'เวกเตอร์ (3,4) มีขนาดเท่าใด?',
           'choices':['5','7','12','25'],'ans':0,
           'why':'√(3²+4²)=5','skill':'Math'},
          {'topic':'Vector','level':'AI Connection','q':'แนวคิดใดใช้เปรียบเทียบทิศทางของ embedding vectors ได้ดี?',
           'choices':['Cosine similarity','Area of circle','Discriminant','Bubble swap'],'ans':0,
           'why':'Cosine similarity เปรียบเทียบมุม/ทิศทางระหว่างเวกเตอร์','skill':'AI'},
          {'topic':'Matrix','level':'Foundation','q':'เมทริกซ์เอกลักษณ์ 2×2 ทำอะไรกับเวกเตอร์?',
           'choices':['คงค่าเดิม','หมุน 90°','ทำให้เป็นศูนย์','สลับแกนเสมอ'],'ans':0,
           'why':'Identity matrix เป็น transformation ที่ไม่เปลี่ยนเวกเตอร์','skill':'Math'},
          {'topic':'Matrix','level':'Application','q':'|det(M)| ใน linear transformation สื่อถึงอะไร?',
           'choices':['ตัวคูณพื้นที่','จำนวนราก','ค่าเฉลี่ย','ความยาวเส้นรอบวง'],'ans':0,
           'why':'ค่าสัมบูรณ์ determinant คือ area scale factor ใน 2D','skill':'Graph'},
          {'topic':'Derivative','level':'Foundation','q':'Derivative ณ จุดหนึ่งสื่อถึงอะไรบนกราฟ?',
           'choices':['ความชันของเส้นสัมผัส','พื้นที่ใต้กราฟ','จุดศูนย์กลาง','ความน่าจะเป็น'],'ans':0,
           'why':'อนุพันธ์คืออัตราการเปลี่ยนแปลงและ slope ของ tangent','skill':'Math'},
          {'topic':'Derivative','level':'AI Connection','q':'Gradient ถูกใช้โดยตรงในขั้นตอนใดของการฝึกโมเดล?',
           'choices':['Optimization','File decoding','Serial port pairing','Image display'],'ans':0,
           'why':'Gradient descent ใช้ gradient เพื่อปรับ parameters ให้ loss ลดลง','skill':'AI'},
          {'topic':'Statistics','level':'Foundation','q':'Z-score = 0 หมายความว่า x อยู่ตำแหน่งใด?',
           'choices':['เท่ากับค่าเฉลี่ย','สูงกว่าเฉลี่ย 1 SD','ต่ำกว่าเฉลี่ย 1 SD','เป็นค่าสูงสุด'],'ans':0,
           'why':'z=(x-μ)/σ; z=0 เมื่อ x=μ','skill':'Math'},
          {'topic':'Code','level':'Code Reading','q':'Pascal ใช้ operator ใดสำหรับ assignment โดยทั่วไป?',
           'choices':[':=','==','=>','**'],'ans':0,
           'why':':= คือ assignment operator ของ Pascal','skill':'Code'},
          {'topic':'Code','level':'Code Reading','q':'Python ใช้ ** เพื่อหมายถึงอะไร?',
           'choices':['ยกกำลัง','หาร','เปรียบเทียบ','comment'],'ans':0,
           'why':'เช่น x**2 คือ x ยกกำลัง 2','skill':'Code'},
        ]

    def _v53_score_path(self):
        return Path.home()/'.ai_learning_studio_v53_scores.json'

    def _v53_load_scores(self):
        import json
        p=self._v53_score_path()
        if not p.exists():return []
        try:return json.loads(p.read_text(encoding='utf-8'))
        except Exception:return []

    def _v53_save_scores(self, rows):
        import json
        p=self._v53_score_path()
        try:p.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
        except Exception as e:messagebox.showerror('Save score',str(e))

    def student_exercise_lab(self):
        self.clear()
        self.header('📝 • v5.3 Student Exercises',
                    'ทำแบบฝึกหัดก่อนดูเฉลย → ทำนาย → ตอบ → Feedback → คะแนน → ส่งผลให้ Teacher Mode')
        b=self.scrollbody()
        intro=self.card(b,'Student Learning Mode',
            'แบบฝึกหัดเรียงจาก Foundation → Application → AI Connection และแยกทักษะ Code / Math / Graph / AI '
            'ระบบไม่แสดงเฉลยจนกว่านักเรียนจะตอบ เพื่อฝึกการทำนายและอธิบายเหตุผลก่อนดูผลจริง')
        row=tk.Frame(intro,bg='white');row.pack(fill='x',padx=18,pady=(0,14))
        tk.Label(row,text='Student:',bg='white',fg=TEXT).pack(side='left')
        student=tk.StringVar(value='Student 01')
        ttk.Entry(row,textvariable=student,width=20).pack(side='left',padx=5)
        topic=tk.StringVar(value='All Topics')
        ttk.Combobox(row,textvariable=topic,state='readonly',width=18,
                     values=['All Topics','Parabola','Circle','Vector','Matrix','Derivative','Statistics','Code']).pack(side='left',padx=6)
        ttk.Button(row,text='Start / Restart',style='Primary.TButton').pack(side='left',padx=5)
        startbtn=row.winfo_children()[-1]

        card=self.card(b,'Question','เลือกคำตอบก่อน แล้วกด Check Answer')
        progress=tk.StringVar(value='ยังไม่ได้เริ่ม')
        tk.Label(card,textvariable=progress,bg='white',fg=MUTED,font=('Segoe UI',9)).pack(anchor='w',padx=18,pady=(0,4))
        qv=tk.StringVar(value='กด Start / Restart เพื่อเริ่มแบบฝึกหัด')
        tk.Label(card,textvariable=qv,bg='white',fg=TEXT,font=('Segoe UI Semibold',13),
                 wraplength=900,justify='left').pack(anchor='w',padx=18,pady=8)
        choice=tk.IntVar(value=-1)
        choices_frame=tk.Frame(card,bg='white');choices_frame.pack(fill='x',padx=18)
        radios=[]
        for i in range(4):
            rb=ttk.Radiobutton(choices_frame,text='',variable=choice,value=i)
            rb.pack(anchor='w',pady=3);radios.append(rb)
        predict=tk.StringVar()
        tk.Label(card,text='เหตุผล/การทำนายของฉัน (optional):',bg='white',fg=TEXT,font=('Segoe UI',9)).pack(anchor='w',padx=18,pady=(8,2))
        ttk.Entry(card,textvariable=predict).pack(fill='x',padx=18)
        buttons=tk.Frame(card,bg='white');buttons.pack(fill='x',padx=18,pady=12)
        ttk.Button(buttons,text='✓ Check Answer',style='Primary.TButton').pack(side='left')
        checkbtn=buttons.winfo_children()[-1]
        ttk.Button(buttons,text='Next Question ▶').pack(side='left',padx=6)
        nextbtn=buttons.winfo_children()[-1]
        feedback=tk.StringVar(value='')
        tk.Label(card,textvariable=feedback,bg='white',fg=BLUE,font=('Segoe UI',10),
                 wraplength=900,justify='left').pack(anchor='w',padx=18,pady=(0,14))

        summary=self.card(b,'My Progress','คะแนนจะแยกตามทักษะ เพื่อให้นักเรียนรู้ว่าควรทบทวนด้านใด')
        scorev=tk.StringVar(value='Code — | Math — | Graph — | AI — | Total —')
        tk.Label(summary,textvariable=scorev,bg='white',fg=TEXT,font=('Segoe UI Semibold',12)).pack(anchor='w',padx=18,pady=(0,14))

        state={'bank':[],'i':0,'answered':False,'correct':0,'skill_total':{},'skill_ok':{},'answers':[]}

        def update_score():
            parts=[]
            for sk in ['Code','Math','Graph','AI']:
                t=state['skill_total'].get(sk,0);ok=state['skill_ok'].get(sk,0)
                parts.append(f'{sk} {ok}/{t}' if t else f'{sk} —')
            total=len(state['answers']);parts.append(f'Total {state["correct"]}/{total}' if total else 'Total —')
            scorev.set(' | '.join(parts))

        def show():
            if not state['bank']:
                return
            q=state['bank'][state['i']]
            progress.set(f'Question {state["i"]+1}/{len(state["bank"])} • {q["topic"]} • {q["level"]} • Skill: {q["skill"]}')
            qv.set(q['q']);choice.set(-1);predict.set('');feedback.set('');state['answered']=False
            for i,rb in enumerate(radios):rb.configure(text=q['choices'][i])

        def start():
            bank=self._v53_bank()
            if topic.get()!='All Topics':bank=[q for q in bank if q['topic']==topic.get()]
            state.update(bank=bank,i=0,answered=False,correct=0,skill_total={},skill_ok={},answers=[])
            update_score();show()

        def check():
            if not state['bank'] or state['answered']:return
            if choice.get()<0:
                feedback.set('กรุณาเลือกคำตอบก่อนดูเฉลย');return
            q=state['bank'][state['i']];state['answered']=True
            ok=choice.get()==q['ans'];sk=q['skill']
            state['skill_total'][sk]=state['skill_total'].get(sk,0)+1
            if ok:
                state['correct']+=1;state['skill_ok'][sk]=state['skill_ok'].get(sk,0)+1
                feedback.set('✓ ถูกต้อง — '+q['why'])
            else:
                feedback.set(f'✗ คำตอบที่ถูกคือ “{q["choices"][q["ans"]]}” — {q["why"]}')
            state['answers'].append({'topic':q['topic'],'skill':sk,'ok':ok,'prediction':predict.get().strip()})
            update_score()

        def finish_save():
            if not state['answers']:return
            import datetime
            rows=self._v53_load_scores()
            total=len(state['answers']);pct=round(100*state['correct']/total,1) if total else 0
            skills={}
            for sk,t in state['skill_total'].items():
                ok=state['skill_ok'].get(sk,0);skills[sk]={'correct':ok,'total':t,'percent':round(100*ok/t,1)}
            rows.append({'student':student.get().strip() or 'Student','date':datetime.datetime.now().isoformat(timespec='seconds'),
                         'topic':topic.get(),'correct':state['correct'],'total':total,'percent':pct,'skills':skills,'answers':state['answers']})
            self._v53_save_scores(rows);feedback.set(f'บันทึกผลแล้ว: {pct:.1f}% — Teacher Mode สามารถเปิดดูได้')

        def nxt():
            if not state['bank']:return
            if not state['answered']:
                feedback.set('ตอบและกด Check Answer ก่อนเข้าสู่ข้อถัดไป');return
            if state['i']<len(state['bank'])-1:
                state['i']+=1;show()
            else:
                finish_save()
                progress.set('Completed ✓')
                qv.set('ทำแบบฝึกหัดครบแล้ว ผลถูกบันทึกสำหรับ Teacher Mode')

        startbtn.configure(command=start);checkbtn.configure(command=check);nextbtn.configure(command=nxt)

        note=self.card(b,'Learning sequence',
            'นักเรียนต้องตอบก่อนเห็นเฉลย → ได้ immediate feedback → คะแนนถูกแยกเป็น Code / Math / Graph / AI → '
            'เมื่อทำครบ ผลจะถูกเก็บในเครื่องสำหรับ Teacher Mode')
        tk.Label(note,text='PREDICT → ANSWER → EXPLAIN → CHECK → LEARN → SCORE',
                 bg='white',fg=BLUE,font=('Segoe UI Semibold',11)).pack(anchor='w',padx=18,pady=(0,14))

    def teacher_v53_lab(self):
        self.clear()
        self.header('👩‍🏫 • v5.3 Teacher Mode',
                    'ดูผลหลังนักเรียนทำแบบฝึกหัด: ภาพรวม → รายคน → Code / Math / Graph / AI → จุดที่ควรทบทวน')
        b=self.scrollbody()
        intro=self.card(b,'Teacher Dashboard',
            'ข้อมูลมาจาก Student Exercises บนเครื่องนี้ ครูสามารถดูคะแนนรายครั้งและแยกตามทักษะ '
            'เพื่อใช้ประกอบการสอน ไม่ใช่การวินิจฉัยความสามารถถาวรของนักเรียน')
        bar=tk.Frame(intro,bg='white');bar.pack(fill='x',padx=18,pady=(0,14))
        ttk.Button(bar,text='↻ Refresh',style='Primary.TButton').pack(side='left')
        refreshbtn=bar.winfo_children()[-1]
        ttk.Button(bar,text='Clear Local Scores').pack(side='left',padx=6)
        clearbtn=bar.winfo_children()[-1]
        statv=tk.StringVar(value='ยังไม่มีข้อมูล')
        tk.Label(bar,textvariable=statv,bg='white',fg=MUTED,font=('Segoe UI',9)).pack(side='left',padx=10)

        tablecard=self.card(b,'Student Results','เลือกแถวเพื่อดูรายละเอียด')
        cols=('student','date','topic','score','code','math','graph','ai')
        tree=ttk.Treeview(tablecard,columns=cols,show='headings',height=12)
        labels=[('student','Student',130),('date','Date',155),('topic','Topic',110),('score','Total',80),
                ('code','Code',75),('math','Math',75),('graph','Graph',75),('ai','AI',75)]
        for c,t,w in labels:tree.heading(c,text=t);tree.column(c,width=w,anchor='center' if c not in ('student','date') else 'w')
        tree.pack(fill='x',padx=18,pady=(0,14))

        detail=self.card(b,'Learning Analysis','เลือกผลการทำแบบฝึกหัดด้านบน')
        detailv=tk.StringVar(value='—')
        tk.Label(detail,textvariable=detailv,bg='white',fg=TEXT,font=('Segoe UI',10),
                 justify='left',wraplength=950).pack(anchor='w',padx=18,pady=(0,14))
        cv=tk.Canvas(detail,height=270,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1)
        cv.pack(fill='x',padx=18,pady=(0,14))
        state={'rows':[]}

        def skilltxt(r,sk):
            d=r.get('skills',{}).get(sk)
            return f"{d['percent']:.0f}%" if d else '—'

        def refresh():
            rows=self._v53_load_scores();state['rows']=rows
            tree.delete(*tree.get_children())
            for i,r in enumerate(rows):
                tree.insert('','end',iid=str(i),values=(r.get('student',''),r.get('date',''),r.get('topic',''),
                    f"{r.get('percent',0):.0f}%",skilltxt(r,'Code'),skilltxt(r,'Math'),skilltxt(r,'Graph'),skilltxt(r,'AI')))
            if rows:
                avg=sum(r.get('percent',0) for r in rows)/len(rows)
                students=len(set(r.get('student','') for r in rows))
                statv.set(f'{len(rows)} attempts • {students} students • class/attempt average {avg:.1f}%')
            else:statv.set('ยังไม่มีผลแบบฝึกหัด')

        def select(*_):
            sel=tree.selection()
            if not sel:return
            r=state['rows'][int(sel[0])]
            skills=r.get('skills',{})
            lines=[f"Student: {r.get('student')}   Topic: {r.get('topic')}   Total: {r.get('correct')}/{r.get('total')} ({r.get('percent')}%)"]
            review=[]
            for sk in ['Code','Math','Graph','AI']:
                d=skills.get(sk)
                if d:
                    lines.append(f"{sk}: {d['correct']}/{d['total']} = {d['percent']:.1f}%")
                    if d['percent']<70:review.append(sk)
            lines.append('Suggested review areas: '+(', '.join(review) if review else 'ไม่มีทักษะที่ต่ำกว่าเกณฑ์ตัวอย่าง 70% ในครั้งนี้'))
            detailv.set('\n'.join(lines))
            # skill bar chart
            cv.delete('all');w=max(700,cv.winfo_width());h=max(250,cv.winfo_height())
            cv.create_rectangle(0,0,w,h,fill='#fbfdff',outline='')
            names=['Code','Math','Graph','AI'];L=90;R=w-40;T=30;gap=48
            for i,sk in enumerate(names):
                y=T+i*gap; pct=skills.get(sk,{}).get('percent',0)
                cv.create_text(L-10,y+10,text=sk,anchor='e',fill=TEXT,font=('Segoe UI',9))
                cv.create_rectangle(L,y,R,y+20,fill='#e5e7eb',outline='')
                cv.create_rectangle(L,y,L+(R-L)*pct/100,y+20,fill='#60a5fa',outline='')
                cv.create_text(R+5,y+10,text=f'{pct:.0f}%',anchor='w',fill=TEXT,font=('Segoe UI',9))
            cv.create_text(L,h-20,text='0%',anchor='w',fill=MUTED,font=('Segoe UI',8))
            cv.create_text(R,h-20,text='100%',anchor='e',fill=MUTED,font=('Segoe UI',8))

        def clear():
            if messagebox.askyesno('Clear scores','ลบผลแบบฝึกหัดที่บันทึกไว้ในเครื่องทั้งหมดหรือไม่?'):
                self._v53_save_scores([]);refresh();detailv.set('—');cv.delete('all')

        refreshbtn.configure(command=refresh);clearbtn.configure(command=clear);tree.bind('<<TreeviewSelect>>',select)
        cv.bind('<Configure>',select);refresh()

        guide=self.card(b,'การใช้คะแนน',
            'คะแนนเป็น formative assessment เพื่อดูว่าควรสอนซ้ำตรงไหน ควรพิจารณาร่วมกับคำอธิบายของนักเรียน '
            'การทดลองใน Four-Panel Learning และผลงาน Project ไม่ควรใช้เปอร์เซ็นต์ครั้งเดียวเป็นข้อสรุปความสามารถทั้งหมด')
        tk.Label(guide,text='Student Exercise → Evidence → Skill Breakdown → Teaching Adjustment',
                 bg='white',fg=BLUE,font=('Segoe UI Semibold',11)).pack(anchor='w',padx=18,pady=(0,14))

    # ==================== v5.4 AUTO TC EXERCISE GENERATOR ====================
    def _v54_distractors(self, correct, kind):
        pools={
          'type':['Linear','Quadratic / Parabola','Circle / Distance','Trigonometric','Vector','Matrix','Derivative','Statistics'],
          'ai':['Regression / trajectory','k-NN / tracking','Robot pose / periodic signal','Embeddings / direction',
                'Neural network / transformation','Gradient descent / optimization','Normalization / anomaly detection'],
          'python':[':= is Python assignment','^ is always Python exponent','** is Python exponent','sqrt needs no function']
        }
        vals=[x for x in pools.get(kind,[]) if x!=correct]
        return vals[:3]

    def _v54_make_questions(self, filename, source):
        recs=self._extract_equations_auto(source)
        questions=[]
        lines=source.splitlines()
        # Build questions from actual parsed assignments.
        for rec in recs[:80]:
            raw=rec.get('raw',''); lhs=rec.get('lhs','')
            line_no=next((i for i,l in enumerate(lines,1) if lhs and re.search(r'\b'+re.escape(lhs)+r'\b\s*(?::=|=)',l)),None)
            snippet=lines[line_no-1].strip() if line_no else f"{lhs} = {raw}"
            kind,_,_=self._v51_detect_live_kind(filename,snippet,[rec])
            eqkind=self._v43_equation_kind(rec)
            # Q1: code -> normalized equation
            norm=f"{lhs} = {rec.get('expr') if rec.get('expr') is not None else rec.get('norm')}"
            choices=[norm,
                     f"{lhs} = {rec.get('norm','').replace('^','+')}",
                     f"{lhs} = 0",
                     f"{lhs} = {lhs}"]
            questions.append({'topic':kind,'skill':'Code','level':'Source Reading','line':line_no,'snippet':snippet,
                'q':'ข้อใดแทนความหมายทางคณิตศาสตร์ของบรรทัด source นี้ได้ใกล้เคียงที่สุด?',
                'choices':choices,'ans':0,'why':f'ระบบ normalize assignment เป็น {norm}'})
            # Q2: classify
            options=[eqkind]+self._v54_distractors(eqkind,'type')
            while len(options)<4: options.append('General arithmetic')
            questions.append({'topic':kind,'skill':'Math','level':'Classification','line':line_no,'snippet':snippet,
                'q':'สมการ/นิพจน์ในบรรทัดนี้จัดอยู่ในลักษณะใดมากที่สุด?',
                'choices':options[:4],'ans':0,'why':f'Symbolic analyzer จัดเป็น {eqkind}'})
            # Q3: Python equivalent
            py=self._v52_python_line(rec)
            pyopts=[py,py.replace('**','^'),py.replace(' = ',' == '),f"print('{lhs}')"]
            questions.append({'topic':kind,'skill':'Code','level':'Modern Python','line':line_no,'snippet':snippet,
                'q':'Python equivalent ที่เหมาะสมที่สุดคือข้อใด?',
                'choices':pyopts,'ans':0,'why':f'Python ใช้รูปแบบ {py}'})
            # Q4: AI connection only where classification has evidence
            amap={'Parabola':'Regression / trajectory','Circle':'k-NN / tracking',
                  'Trigonometry':'Robot pose / periodic signal','Vector':'Embeddings / direction',
                  'Matrix':'Neural network / transformation','Derivative':'Gradient descent / optimization',
                  'Statistics':'Normalization / anomaly detection'}
            if kind in amap:
                correct=amap[kind]
                opts=[correct]+[x for x in self._v54_distractors(correct,'ai') if x!=correct]
                questions.append({'topic':kind,'skill':'AI','level':'AI Connection','line':line_no,'snippet':snippet,
                    'q':'แนวคิดจาก source นี้เชื่อมกับงาน AI/Robot ข้อใดได้โดยตรงที่สุดในบทเรียนนี้?',
                    'choices':opts[:4],'ans':0,'why':f'{kind} เชื่อมในหลักสูตรกับ {correct}'})
        # If extraction is sparse, add source-literacy questions from real code lines.
        assigns=[(i,l.strip()) for i,l in enumerate(lines,1) if re.search(r'(?::=|(?<![<>=!])=(?!=))',l)]
        for ln,snip in assigns[:20]:
            if len(questions)>=12:break
            questions.append({'topic':'Code','skill':'Code','level':'Source Reading','line':ln,'snippet':snip,
                'q':'บรรทัดนี้มีลักษณะเป็น assignment หรือไม่?',
                'choices':['ใช่','ไม่ใช่','เป็น comment เท่านั้น','เป็นชื่อไฟล์'],'ans':0,
                'why':'พบบริบท assignment operator ใน source; นักเรียนควรตรวจ syntax ของภาษาร่วมด้วย'})
        return questions

    def auto_tc_exercise_lab(self):
        self.clear()
        self.header('🧠 • v5.4 Auto TC Exercise Generator',
                    'เลือกไฟล์ Pascal/C จริง → สร้างแบบฝึกหัดจาก source → ตอบก่อนดูเฉลย → บันทึกเข้า Teacher Mode')
        b=self.scrollbody()
        intro=self.card(b,'Generate exercises from real TC code',
            'ระบบสร้างคำถามจาก assignment/symbolic expressions ที่ตรวจพบในไฟล์จริง เช่น Code Reading, '
            'Math Classification, Modern Python และ AI Connection โดยไม่ execute source ที่นำเข้า')
        bar=tk.Frame(intro,bg='white');bar.pack(fill='x',padx=18,pady=(0,14))
        ttk.Button(bar,text='Open .PAS / .C',style='Primary.TButton').pack(side='left');openbtn=bar.winfo_children()[-1]
        ttk.Button(bar,text='Choose from TC ZIP').pack(side='left',padx=6);zipbtn=bar.winfo_children()[-1]
        student=tk.StringVar(value='Student 01')
        tk.Label(bar,text='Student:',bg='white').pack(side='left',padx=(15,3))
        ttk.Entry(bar,textvariable=student,width=18).pack(side='left')
        status=tk.StringVar(value='เลือก source เพื่อสร้างแบบฝึกหัด')
        tk.Label(intro,textvariable=status,bg='white',fg=MUTED,font=('Segoe UI',9)).pack(anchor='w',padx=18,pady=(0,10))

        sourcecard=self.card(b,'Source Evidence','คำถามทุกข้อจะแสดงบรรทัด source ที่เป็นหลักฐาน')
        snippet=tk.StringVar(value='—')
        tk.Label(sourcecard,textvariable=snippet,bg='#f8fafc',fg=TEXT,font=('Consolas',10),
                 justify='left',wraplength=950).pack(fill='x',padx=18,pady=(0,14))

        qcard=self.card(b,'Generated Question','นักเรียนต้องตอบก่อนจึงเห็นเฉลย')
        progress=tk.StringVar(value='—');qv=tk.StringVar(value='—')
        tk.Label(qcard,textvariable=progress,bg='white',fg=MUTED,font=('Segoe UI',9)).pack(anchor='w',padx=18)
        tk.Label(qcard,textvariable=qv,bg='white',fg=TEXT,font=('Segoe UI Semibold',13),
                 wraplength=950,justify='left').pack(anchor='w',padx=18,pady=8)
        ans=tk.IntVar(value=-1);rbs=[]
        rf=tk.Frame(qcard,bg='white');rf.pack(fill='x',padx=18)
        for i in range(4):
            rb=ttk.Radiobutton(rf,text='',variable=ans,value=i);rb.pack(anchor='w',pady=3);rbs.append(rb)
        reason=tk.StringVar()
        tk.Label(qcard,text='อธิบายเหตุผลก่อนตรวจคำตอบ:',bg='white',fg=TEXT).pack(anchor='w',padx=18,pady=(8,2))
        ttk.Entry(qcard,textvariable=reason).pack(fill='x',padx=18)
        br=tk.Frame(qcard,bg='white');br.pack(fill='x',padx=18,pady=10)
        ttk.Button(br,text='✓ Check Answer',style='Primary.TButton').pack(side='left');checkbtn=br.winfo_children()[-1]
        ttk.Button(br,text='Next ▶').pack(side='left',padx=6);nextbtn=br.winfo_children()[-1]
        feedback=tk.StringVar()
        tk.Label(qcard,textvariable=feedback,bg='white',fg=BLUE,font=('Segoe UI',10),
                 wraplength=950,justify='left').pack(anchor='w',padx=18,pady=(0,12))

        scorecard=self.card(b,'Generated Exercise Score','แยกผลตาม Code / Math / Graph / AI')
        scorev=tk.StringVar(value='ยังไม่มีคะแนน')
        tk.Label(scorecard,textvariable=scorev,bg='white',fg=TEXT,font=('Segoe UI Semibold',11)).pack(anchor='w',padx=18,pady=(0,14))

        state={'file':'','qs':[],'i':0,'answered':False,'correct':0,'skill_total':{},'skill_ok':{},'answers':[]}

        def score():
            p=[]
            for sk in ['Code','Math','Graph','AI']:
                t=state['skill_total'].get(sk,0);o=state['skill_ok'].get(sk,0)
                p.append(f'{sk} {o}/{t}' if t else f'{sk} —')
            p.append(f'Total {state["correct"]}/{len(state["answers"])}')
            scorev.set(' | '.join(p))

        def show():
            if not state['qs']:return
            q=state['qs'][state['i']]
            progress.set(f'Question {state["i"]+1}/{len(state["qs"])} • {q["level"]} • Skill: {q["skill"]}')
            snippet.set(f'File: {state["file"]}  •  Line: {q.get("line") or "?"}\n{q["snippet"]}')
            qv.set(q['q']);ans.set(-1);reason.set('');feedback.set('');state['answered']=False
            opts=list(q['choices'])[:4]
            while len(opts)<4:opts.append('None of the above')
            # Deterministic rotation by question index prevents answer always appearing first.
            shift=state['i']%4; rotated=opts[shift:]+opts[:shift]
            correct_text=opts[q['ans']]
            q['_shown']=rotated;q['_shown_ans']=rotated.index(correct_text)
            for i,rb in enumerate(rbs):rb.configure(text=rotated[i])

        def load(name,source):
            qs=self._v54_make_questions(name,source)
            state.update(file=name,qs=qs,i=0,answered=False,correct=0,skill_total={},skill_ok={},answers=[])
            status.set(f'{name} → สร้างได้ {len(qs)} questions จาก source จริง')
            score()
            if qs:show()
            else:
                qv.set('ไม่พบ assignment ที่เหมาะสมสำหรับสร้างแบบฝึกหัดอัตโนมัติในไฟล์นี้')
                snippet.set('ลองเลือกไฟล์คณิตศาสตร์ เช่น CIRCLE.PAS, PARAX.PAS, PARAY.PAS หรือ source ที่มีสมการ')

        def check():
            if not state['qs'] or state['answered']:return
            if ans.get()<0:feedback.set('กรุณาเลือกคำตอบก่อน');return
            q=state['qs'][state['i']];state['answered']=True
            ok=ans.get()==q['_shown_ans'];sk=q['skill']
            state['skill_total'][sk]=state['skill_total'].get(sk,0)+1
            if ok:state['correct']+=1;state['skill_ok'][sk]=state['skill_ok'].get(sk,0)+1
            feedback.set(('✓ ถูกต้อง — ' if ok else f'✗ คำตอบที่เหมาะสมคือ “{q["_shown"][q["_shown_ans"]]}” — ')+q['why'])
            state['answers'].append({'topic':q['topic'],'skill':sk,'ok':ok,'prediction':reason.get().strip(),
                                     'file':state['file'],'line':q.get('line')})
            score()

        def save_result():
            import datetime
            rows=self._v53_load_scores();total=len(state['answers'])
            pct=round(100*state['correct']/total,1) if total else 0
            skills={}
            for sk,t in state['skill_total'].items():
                o=state['skill_ok'].get(sk,0);skills[sk]={'correct':o,'total':t,'percent':round(100*o/t,1)}
            rows.append({'student':student.get().strip() or 'Student','date':datetime.datetime.now().isoformat(timespec='seconds'),
                         'topic':'AUTO: '+state['file'],'correct':state['correct'],'total':total,'percent':pct,
                         'skills':skills,'answers':state['answers'],'source_file':state['file'],'generator':'v5.4'})
            self._v53_save_scores(rows)
            feedback.set(f'Completed ✓ บันทึก {pct:.1f}% ไปยัง Teacher Mode แล้ว')

        def nxt():
            if not state['qs']:return
            if not state['answered']:feedback.set('ตอบและ Check Answer ก่อนเข้าสู่ข้อถัดไป');return
            if state['i']<len(state['qs'])-1:state['i']+=1;show()
            else:save_result();progress.set('Completed ✓')

        def open_file():
            p=filedialog.askopenfilename(title='Open Pascal/C',filetypes=[('Pascal/C','*.pas *.pp *.c *.h *.cpp *.cc *.cxx *.hpp'),('All','*.*')])
            if not p:return
            data=Path(p).read_bytes();source,_=self._v43_decode(data);load(Path(p).name,source)

        def choose_zip():
            zp=filedialog.askopenfilename(title='Choose TC ZIP',filetypes=[('ZIP','*.zip')])
            if not zp:return
            try:
                with zipfile.ZipFile(zp) as z:names=[n for n in z.namelist() if n.lower().endswith(('.pas','.pp','.c','.h','.cpp','.cc','.cxx','.hpp'))]
                win=tk.Toplevel(self);win.title('Choose TC source for exercises');win.geometry('840x610')
                q=tk.StringVar();ttk.Entry(win,textvariable=q).pack(fill='x',padx=10,pady=8)
                lb=tk.Listbox(win,font=('Consolas',9));lb.pack(fill='both',expand=True,padx=10,pady=4)
                def fill(*_):
                    term=q.get().lower();lb.delete(0,'end')
                    for n in [n for n in names if term in n.lower()][:1200]:lb.insert('end',n)
                def pick(*_):
                    if not lb.curselection():return
                    n=lb.get(lb.curselection()[0])
                    with zipfile.ZipFile(zp) as z:data=z.read(n)
                    source,_=self._v43_decode(data);win.destroy();load(n,source)
                q.trace_add('write',fill);lb.bind('<Double-Button-1>',pick)
                ttk.Button(win,text='Generate from selected file',command=pick).pack(pady=7);fill()
            except Exception as e:messagebox.showerror('TC ZIP',str(e))

        openbtn.configure(command=open_file);zipbtn.configure(command=choose_zip)
        checkbtn.configure(command=check);nextbtn.configure(command=nxt)

        guide=self.card(b,'v5.4 Learning Loop',
            '1) เลือก TC source จริง → 2) ระบบ extract assignment/equation → 3) สร้างคำถามจากหลักฐานในไฟล์ → '
            '4) นักเรียนอธิบายและตอบ → 5) แสดงเฉลยพร้อมเหตุผล → 6) บันทึก Code/Math/AI score → 7) ครูดูผลใน Teacher Mode')
        tk.Label(guide,text='REAL SOURCE → GENERATED QUESTION → REASON → ANSWER → FEEDBACK → TEACHER',
                 bg='white',fg=BLUE,font=('Segoe UI Semibold',11)).pack(anchor='w',padx=18,pady=(0,14))

    # ==================== v5.5 ADAPTIVE AI MATH TUTOR ====================
    def _v55_questions(self):
        # Curated concept checks used by the adaptive engine.
        return [
          {'topic':'Parabola','skill':'Graph','difficulty':1,'q':'ถ้า y=ax² และ a เปลี่ยนจาก 1 เป็น 2 กราฟจะเป็นอย่างไร?',
           'choices':['แคบขึ้นและยังเปิดขึ้น','กว้างขึ้นและเปิดลง','กลายเป็นวงกลม','เลื่อนไปขวาเท่านั้น'],'ans':0,
           'hint':'ดูขนาด |a|: ยิ่งมาก พาราโบลายิ่งแคบ','why':'เมื่อ |a| เพิ่มจาก 1 เป็น 2 ค่า y โตเร็วขึ้น จึงดูแคบขึ้น'},
          {'topic':'Parabola','skill':'Math','difficulty':2,'q':'จุดยอดของ y=x²-6x+5 มี x-coordinate เท่าใด?',
           'choices':['3','-3','5','6'],'ans':0,'hint':'ใช้ x=-b/(2a)','why':'a=1,b=-6 ดังนั้น x=6/2=3'},
          {'topic':'Circle','skill':'Math','difficulty':1,'q':'วงกลมศูนย์กลาง (0,0) รัศมี 5 มีสมการใด?',
           'choices':['x²+y²=25','x+y=5','x²-y²=5','y=5x'],'ans':0,'hint':'ใช้ x²+y²=r²','why':'r²=25'},
          {'topic':'Circle','skill':'AI','difficulty':2,'q':'ระยะ Euclidean จาก (0,0) ถึง (3,4) เท่ากับเท่าใด?',
           'choices':['5','7','12','25'],'ans':0,'hint':'ใช้ √(Δx²+Δy²)','why':'√(3²+4²)=5 ซึ่งเป็น distance ที่ใช้ใน k-NN ได้'},
          {'topic':'Vector','skill':'Math','difficulty':1,'q':'ขนาดของ vector (6,8) คือเท่าใด?',
           'choices':['10','14','48','100'],'ans':0,'hint':'ใช้ √(vx²+vy²)','why':'√(36+64)=10'},
          {'topic':'Vector','skill':'AI','difficulty':2,'q':'Cosine similarity สนใจคุณสมบัติใดเด่นที่สุด?',
           'choices':['มุม/ทิศทางระหว่างเวกเตอร์','พื้นที่วงกลม','รากสมการกำลังสอง','ค่า determinant เท่านั้น'],'ans':0,
           'hint':'cosine เกี่ยวข้องกับ cos ของมุม','why':'ใช้วัดความคล้ายด้านทิศทางของ vectors/embeddings'},
          {'topic':'Matrix','skill':'Math','difficulty':1,'q':'det([[2,0],[0,3]]) เท่ากับเท่าใด?',
           'choices':['6','5','1','0'],'ans':0,'hint':'สำหรับ 2×2: det=ad-bc','why':'2×3-0×0=6'},
          {'topic':'Matrix','skill':'Graph','difficulty':2,'q':'ถ้า |det(M)|=2 พื้นที่หลัง linear transform เป็นอย่างไร?',
           'choices':['เป็น 2 เท่าของเดิม','ครึ่งหนึ่ง','เท่าเดิมเสมอ','เป็นศูนย์'],'ans':0,'hint':'|det| คือ area scale factor','why':'พื้นที่ถูก scale ด้วย |det|'},
          {'topic':'Derivative','skill':'Math','difficulty':1,'q':'ถ้า f(x)=x² แล้ว f′(x) คือข้อใด?',
           'choices':['2x','x','x²','2'],'ans':0,'hint':'power rule: d(xⁿ)/dx = n xⁿ⁻¹','why':'d(x²)/dx=2x'},
          {'topic':'Derivative','skill':'AI','difficulty':2,'q':'ถ้า gradient ของ loss เป็นบวก ใน gradient descent เราปรับ parameter ทิศใด?',
           'choices':['ทิศตรงข้าม gradient','ทิศเดียวกับ gradient เสมอ','ไม่ปรับ','สุ่มเท่านั้น'],'ans':0,
           'hint':'gradient descent ใช้ θ ← θ-η∇L','why':'ลบ gradient เพื่อเคลื่อนไปทางที่ loss ลดลง'},
          {'topic':'Statistics','skill':'Math','difficulty':1,'q':'ถ้า x เท่ากับ mean ค่า z-score เท่าใด?',
           'choices':['0','1','-1','ขึ้นกับจำนวนข้อมูล'],'ans':0,'hint':'z=(x-μ)/σ','why':'x-μ=0 จึง z=0'},
          {'topic':'Statistics','skill':'AI','difficulty':2,'q':'Z-score normalization ช่วยอะไรในการเตรียม feature?',
           'choices':['ทำให้สเกลสัมพันธ์กับ mean และ SD','ทำให้ทุกค่าเป็น 0','ลบทุก outlier','เปลี่ยน classification เป็น regression'],'ans':0,
           'hint':'คิดถึง center=mean และ scale=standard deviation','why':'standardization ทำให้ feature อยู่ในหน่วยของ SD จาก mean'}
        ]

    def _v55_visual(self, cv, topic, phase=0.0):
        params={}
        if topic=='Parabola':params={'a':1.0+0.55*math.sin(phase),'b':0,'c':0}
        elif topic=='Circle':params={'h':0,'k':0,'r':3+0.5*math.sin(phase)}
        elif topic=='Vector':params={'vx':3.5*math.cos(phase),'vy':3.5*math.sin(phase)}
        elif topic=='Matrix':
            params={'a':math.cos(phase),'b':-math.sin(phase),'c':math.sin(phase),'d':math.cos(phase)}
        elif topic=='Derivative':params={'x0':3*math.sin(phase)}
        elif topic=='Statistics':params={}
        self._v51_draw_source_math(cv,topic,params,phase)

    def adaptive_tutor_lab(self):
        self.clear()
        self.header('🤖 • v5.5 Adaptive AI Math Tutor',
                    'ตอบผิด → Hint → Visual Explanation → Retry → ปรับระดับ → Mastery → Teacher Mode')
        b=self.scrollbody()
        intro=self.card(b,'Adaptive Learning Cycle',
            'Tutor ใช้ผลคำตอบใน session เพื่อปรับความยากแบบ rule-based ที่ตรวจสอบได้: '
            'ตอบถูกต่อเนื่องจะขยับไป Application/AI; ตอบผิดจะให้ hint + visualization แล้วสร้างโอกาส retry ก่อนเดินต่อ')
        top=tk.Frame(intro,bg='white');top.pack(fill='x',padx=18,pady=(0,14))
        student=tk.StringVar(value='Student 01')
        tk.Label(top,text='Student:',bg='white').pack(side='left');ttk.Entry(top,textvariable=student,width=18).pack(side='left',padx=5)
        topic=tk.StringVar(value='Parabola')
        ttk.Combobox(top,textvariable=topic,state='readonly',width=16,
                     values=['Parabola','Circle','Vector','Matrix','Derivative','Statistics']).pack(side='left',padx=5)
        ttk.Button(top,text='Start Tutor',style='Primary.TButton').pack(side='left',padx=6);startbtn=top.winfo_children()[-1]

        main=tk.PanedWindow(b,orient='horizontal',sashwidth=5,bg=BG);main.pack(fill='both',expand=True,padx=28,pady=8)
        left=tk.Frame(main,bg='white',highlightbackground=BORDER,highlightthickness=1)
        right=tk.Frame(main,bg='white',highlightbackground=BORDER,highlightthickness=1)
        main.add(left,minsize=500);main.add(right,minsize=650)

        levelv=tk.StringVar(value='Level —')
        tk.Label(left,textvariable=levelv,bg='white',fg=BLUE,font=('Segoe UI Semibold',11)).pack(anchor='w',padx=14,pady=(12,3))
        qv=tk.StringVar(value='กด Start Tutor')
        tk.Label(left,textvariable=qv,bg='white',fg=TEXT,font=('Segoe UI Semibold',13),wraplength=470,justify='left').pack(anchor='w',padx=14,pady=8)
        choice=tk.IntVar(value=-1);rbs=[]
        for i in range(4):
            rb=ttk.Radiobutton(left,text='',variable=choice,value=i);rb.pack(anchor='w',padx=14,pady=3);rbs.append(rb)
        reason=tk.StringVar()
        tk.Label(left,text='ฉันคิดว่า... เพราะ...',bg='white',fg=TEXT).pack(anchor='w',padx=14,pady=(10,2))
        ttk.Entry(left,textvariable=reason).pack(fill='x',padx=14)
        br=tk.Frame(left,bg='white');br.pack(fill='x',padx=14,pady=10)
        ttk.Button(br,text='Check',style='Primary.TButton').pack(side='left');checkbtn=br.winfo_children()[-1]
        ttk.Button(br,text='Show Hint').pack(side='left',padx=5);hintbtn=br.winfo_children()[-1]
        ttk.Button(br,text='Next').pack(side='left');nextbtn=br.winfo_children()[-1]
        feedback=tk.StringVar()
        tk.Label(left,textvariable=feedback,bg='white',fg=BLUE,font=('Segoe UI',10),wraplength=470,justify='left').pack(anchor='w',padx=14,pady=6)
        mastery=tk.StringVar(value='Mastery: —')
        tk.Label(left,textvariable=mastery,bg='#f8fafc',fg=TEXT,font=('Segoe UI Semibold',10),wraplength=470,justify='left').pack(fill='x',padx=14,pady=10)

        tk.Label(right,text='Visual Remediation',bg='white',fg=TEXT,font=('Segoe UI Semibold',13)).pack(anchor='w',padx=12,pady=(10,3))
        cv=tk.Canvas(right,height=440,bg='#fbfdff',highlightthickness=0);cv.pack(fill='both',expand=True,padx=10,pady=6)
        visualmsg=tk.StringVar(value='เมื่อเริ่มบทเรียน ภาพคณิตศาสตร์จะสัมพันธ์กับหัวข้อที่เลือก')
        tk.Label(right,textvariable=visualmsg,bg='white',fg=MUTED,font=('Segoe UI',9),wraplength=620,justify='left').pack(anchor='w',padx=12,pady=(0,10))

        state={'qs':[],'current':None,'level':1,'streak':0,'attempts':0,'correct':0,'answered':False,
               'retry':False,'history':[],'phase':0.0,'after':None,'shown':[],'shown_ans':0}

        def animate():
            state['phase']+=.06
            if state['current']:self._v55_visual(cv,state['current']['topic'],state['phase'])
            state['after']=self.after(90,animate)

        def pick_question():
            qs=[q for q in self._v55_questions() if q['topic']==topic.get()]
            target=state['level']
            cand=[q for q in qs if q['difficulty']==target] or qs
            # Alternate deterministically based on attempt count.
            return cand[state['attempts']%len(cand)] if cand else None

        def show_question(q):
            state['current']=q;state['answered']=False;state['retry']=False;choice.set(-1);reason.set('')
            qv.set(q['q']);levelv.set(f'Adaptive Level {state["level"]} • {q["topic"]} • {q["skill"]}')
            opts=list(q['choices']);shift=state['attempts']%4;shown=opts[shift:]+opts[:shift]
            state['shown']=shown;state['shown_ans']=shown.index(opts[q['ans']])
            for i,rb in enumerate(rbs):rb.configure(text=shown[i])
            feedback.set('ตอบก่อนดูเฉลย หรือกด Show Hint หากต้องการตัวช่วย')
            visualmsg.set('ลองทำนายคำตอบจากสมการก่อน แล้วใช้ภาพด้านขวาตรวจสอบแนวคิด')
            self._v55_visual(cv,q['topic'],state['phase'])

        def update_mastery():
            n=state['attempts'];pct=(100*state['correct']/n) if n else 0
            mastery.set(f'Mastery evidence in this session: {state["correct"]}/{n} = {pct:.1f}%  •  '
                        f'current level={state["level"]}  •  correct streak={state["streak"]}')

        def start():
            state.update(level=1,streak=0,attempts=0,correct=0,answered=False,retry=False,history=[])
            q=pick_question();show_question(q);update_mastery()

        def hint():
            q=state['current']
            if not q:return
            feedback.set('Hint: '+q['hint'])
            visualmsg.set('ใช้ Hint ร่วมกับภาพ: เปลี่ยนจากการเดาคำตอบเป็นการเชื่อม formula → geometry/graph → answer')

        def check():
            q=state['current']
            if not q or state['answered']:return
            if choice.get()<0:feedback.set('เลือกคำตอบก่อน');return
            ok=choice.get()==state['shown_ans'];state['attempts']+=1
            state['history'].append({'topic':q['topic'],'skill':q['skill'],'difficulty':q['difficulty'],
                                     'ok':ok,'reason':reason.get().strip(),'retry':state['retry']})
            if ok:
                state['correct']+=1;state['streak']+=1;state['answered']=True
                feedback.set('✓ ถูกต้อง — '+q['why'])
                visualmsg.set('เชื่อมคำตอบกับภาพด้านขวา แล้วกด Next เพื่อให้ Tutor ปรับบทเรียน')
                if state['streak']>=2:state['level']=2
            else:
                state['streak']=0;state['level']=1;state['retry']=True
                feedback.set('ยังไม่ถูก — '+q['hint']+'  ลองดูภาพด้านขวาแล้วตอบใหม่อีกครั้ง')
                visualmsg.set('Remediation: ภาพกำลังแสดง concept เดิม ให้สังเกตตัวแปร/รูปทรง/ความชัน แล้ว Retry')
                # allow another attempt, without revealing answer
                choice.set(-1);state['answered']=False
            update_mastery()

        def save():
            import datetime
            if not state['history']:return
            rows=self._v53_load_scores()
            n=state['attempts'];pct=round(100*state['correct']/n,1) if n else 0
            skills={}
            for sk in set(h['skill'] for h in state['history']):
                hs=[h for h in state['history'] if h['skill']==sk];ok=sum(1 for h in hs if h['ok'])
                skills[sk]={'correct':ok,'total':len(hs),'percent':round(100*ok/len(hs),1)}
            rows.append({'student':student.get().strip() or 'Student','date':datetime.datetime.now().isoformat(timespec='seconds'),
                         'topic':'TUTOR: '+topic.get(),'correct':state['correct'],'total':n,'percent':pct,
                         'skills':skills,'answers':state['history'],'generator':'v5.5-adaptive',
                         'adaptive_level':state['level']})
            self._v53_save_scores(rows)
            feedback.set(f'บันทึก session ไป Teacher Mode แล้ว • {pct:.1f}%')

        def nxt():
            if not state['current']:return
            if not state['answered']:
                feedback.set('ตอบให้ถูกก่อนเข้าสู่คำถามถัดไป เพื่อให้ remediation loop สมบูรณ์');return
            if state['attempts']>=6:
                save();qv.set('Session complete ✓');levelv.set('ส่งผลไป Teacher Mode แล้ว');return
            show_question(pick_question())

        startbtn.configure(command=start);hintbtn.configure(command=hint);checkbtn.configure(command=check);nextbtn.configure(command=nxt)
        cv.bind('<Configure>',lambda e:self._v55_visual(cv,state['current']['topic'],state['phase']) if state['current'] else None)
        animate()

        flow=self.card(b,'Adaptive rule used in v5.5',
            'เริ่ม Level 1 → ตอบถูกต่อเนื่อง 2 ครั้งจึงไป Level 2 → ถ้าตอบผิดกลับมาทบทวน Foundation '
            'พร้อม Hint + Animated Visual และต้อง Retry concept เดิมก่อนเดินต่อ การปรับระดับนี้เป็นกฎที่ครูตรวจสอบได้ '
            'ไม่ใช่การประเมินความสามารถถาวรของนักเรียน')
        tk.Label(flow,text='DIAGNOSE → HINT → VISUALIZE → RETRY → ADVANCE → MASTERY EVIDENCE',
                 bg='white',fg=BLUE,font=('Segoe UI Semibold',11)).pack(anchor='w',padx=18,pady=(0,14))

    # ==================== v5.6 SELECT LINE -> AUTO LESSON -> TC MENU ====================
    def _v56_lesson_for_line(self, filename, line):
        rec=self._v52_line_equation(line)
        if rec:
            kind,score,_=self._v51_detect_live_kind(filename,line,[rec])
            formula=f"{rec['lhs']} = {rec.get('expr') if rec.get('expr') is not None else rec['norm']}"
            py=self._v52_python_line(rec)
            typ=self._v43_equation_kind(rec)
        else:
            kind,score='General',0
            formula='ไม่พบ mathematical assignment ในบรรทัดนี้'
            py='# Programming/control line — study its role in the algorithm'
            typ='Programming / algorithm statement'
        concepts={
          'Parabola':('Quadratic / Parabola','สังเกต a,b,c และผลต่อรูปร่าง/จุดยอดของกราฟ',
                      'Regression, quadratic loss และ trajectory'),
          'Circle':('Circle / Distance','เชื่อม center, radius และ Euclidean distance',
                    'k-NN, target zone, collision และ tracking'),
          'Trigonometry':('Trigonometry','เชื่อม sin/cos กับมุม การหมุน และคาบ',
                          'robot pose, periodic sensor และ signal features'),
          'Vector':('Vector','แยก magnitude และ direction ของเวกเตอร์',
                    'vision coordinates, robot direction และ embeddings'),
          'Matrix':('Matrix Transformation','ดูว่า matrix เปลี่ยน basis/vector อย่างไร',
                    'linear layer, image transform และ robotics'),
          'Derivative':('Derivative / Gradient','ดู slope ณ จุดและการเปลี่ยนแปลงของฟังก์ชัน',
                        'gradient descent และ optimization'),
          'Statistics':('Statistics','เชื่อม mean, SD และ standardized value',
                        'normalization และ anomaly detection'),
          'General':('Code Reading','อ่านหน้าที่ของบรรทัดใน algorithm ก่อนพยายามแปลงเป็นสมการ',
                     'algorithmic thinking / program flow')
        }
        title,goal,ai=concepts.get(kind,concepts['General'])
        return {'rec':rec,'kind':kind,'score':score,'formula':formula,'python':py,'type':typ,
                'title':title,'goal':goal,'ai':ai}

    def _v56_question(self, lesson):
        k=lesson['kind']
        bank={
          'Parabola':('ถ้า |a| ใน y=ax²+bx+c เพิ่มขึ้น โดยเครื่องหมาย a ไม่เปลี่ยน รูปร่างหลักจะเป็นอย่างไร?',
                      ['พาราโบลาแคบขึ้น','กลายเป็นวงกลม','เป็นเส้นตรงเสมอ','ไม่มีผล'],0,
                      '|a| มากขึ้นทำให้ค่า y เปลี่ยนเร็วขึ้นเมื่อห่างจากแกนสมมาตร'),
          'Circle':('ในสมการวงกลม (x-h)²+(y-k)²=r² ตัวแปร r ควบคุมอะไร?',
                    ['รัศมี','ความชัน','ค่าเฉลี่ย','จำนวนมิติ'],0,'r คือระยะจาก center ถึงเส้นรอบวง'),
          'Trigonometry':('sin และ cos มีประโยชน์เด่นกับแนวคิดใด?',
                            ['มุมและการหมุน','การเรียงลำดับอย่างเดียว','พื้นที่วงกลมอย่างเดียว','ชื่อไฟล์'],0,
                            'sin/cos เชื่อมพิกัดกับมุมและการเคลื่อนที่แบบคาบ'),
          'Vector':('ขนาดของ vector (3,4) เท่ากับเท่าใด?',
                    ['5','7','12','25'],0,'√(3²+4²)=5'),
          'Matrix':('determinant ใน 2D เชื่อมกับอะไร?',
                    ['ตัวคูณพื้นที่','ค่าเฉลี่ย','จำนวนราก','sample rate'],0,'|det| คือ area scale factor'),
          'Derivative':('Derivative ณ จุดหนึ่งหมายถึงอะไรบนกราฟ?',
                        ['ความชันของ tangent','พื้นที่วงกลม','ค่าเฉลี่ย','จำนวน class'],0,
                        'Derivative คือ instantaneous rate of change / tangent slope'),
          'Statistics':('ถ้า x=mean แล้ว z-score เท่าใด?',
                        ['0','1','-1','2'],0,'z=(x-μ)/σ จึงเป็น 0 เมื่อ x=μ'),
          'General':('ขั้นแรกเมื่อบรรทัดไม่ใช่สมการควรทำอะไร?',
                     ['อ่านบทบาทของมันใน algorithm/context','บังคับสร้างสมการ','ลบบรรทัด','ถือว่าเป็น AI model'],0,
                     'ไม่ควรสร้างคณิตศาสตร์ที่ไม่มีหลักฐานจาก source')
        }
        q,choices,ans,why=bank.get(k,bank['General'])
        return {'q':q,'choices':choices,'ans':ans,'why':why}

    def line_lesson_tc_lab(self):
        self.clear()
        self.header('📖 • v5.6 Select Line → Auto Lesson → TC Menu',
                    'เลือกบรรทัดก่อน → ระบบสร้างบทเรียน → ทำแบบฝึกหัด → ผ่านบทเรียน → เลือกหัวข้อ/ไฟล์ถัดไปจาก TC')
        b=self.scrollbody()
        intro=self.card(b,'Step 1 • Select a source line',
            'เปิดไฟล์ Pascal/C หรือเลือกจาก TC ZIP แล้วคลิกบรรทัดที่ต้องการเรียน ระบบจะสร้าง mini lesson '
            'จากหลักฐานของบรรทัดนั้น โดยไม่ execute source code')
        top=tk.Frame(intro,bg='white');top.pack(fill='x',padx=18,pady=(0,12))
        ttk.Button(top,text='Open .PAS / .C',style='Primary.TButton').pack(side='left');openbtn=top.winfo_children()[-1]
        ttk.Button(top,text='Browse TC ZIP').pack(side='left',padx=6);zipbtn=top.winfo_children()[-1]
        filev=tk.StringVar(value='ยังไม่ได้เลือก source')
        tk.Label(top,textvariable=filev,bg='white',fg=MUTED,font=('Segoe UI',9)).pack(side='left',padx=10)
        src=tk.Text(intro,height=13,font=('Consolas',9),wrap='none',cursor='hand2')
        src.pack(fill='x',padx=18,pady=(0,12))
        src.tag_configure('sel',background='#dbeafe',foreground='#1e3a8a')
        src.tag_configure('math',background='#fef3c7')

        lesson_card=self.card(b,'Step 2 • Auto Lesson','คลิกบรรทัดด้านบนเพื่อสร้างบทเรียน')
        titlev=tk.StringVar(value='Lesson: —');formulav=tk.StringVar(value='Formula: —')
        goalv=tk.StringVar(value='Learning goal: —');aiv=tk.StringVar(value='AI connection: —')
        tk.Label(lesson_card,textvariable=titlev,bg='white',fg=BLUE,font=('Segoe UI Semibold',13)).pack(anchor='w',padx=18)
        tk.Label(lesson_card,textvariable=formulav,bg='white',fg=TEXT,font=('Cambria Math',13),wraplength=920,justify='left').pack(anchor='w',padx=18,pady=4)
        tk.Label(lesson_card,textvariable=goalv,bg='white',fg=TEXT,font=('Segoe UI',10),wraplength=920,justify='left').pack(anchor='w',padx=18,pady=2)
        tk.Label(lesson_card,textvariable=aiv,bg='white',fg=MUTED,font=('Segoe UI',9),wraplength=920,justify='left').pack(anchor='w',padx=18,pady=(2,10))

        panes=tk.PanedWindow(lesson_card,orient='horizontal',sashwidth=5,bg='white');panes.pack(fill='both',expand=True,padx=18,pady=(0,12))
        visual=tk.Frame(panes,bg='#fbfdff');modern=tk.Frame(panes,bg='#f8fafc')
        panes.add(visual,minsize=520);panes.add(modern,minsize=420)
        cv=tk.Canvas(visual,height=330,bg='#fbfdff',highlightthickness=0);cv.pack(fill='both',expand=True)
        tk.Label(modern,text='Modern Python',bg='#f8fafc',fg=TEXT,font=('Segoe UI Semibold',11)).pack(anchor='w',padx=10,pady=(10,3))
        pybox=tk.Text(modern,height=8,font=('Consolas',9),wrap='word');pybox.pack(fill='x',padx=10)
        pybox.configure(state='disabled')
        explain=tk.StringVar(value='เลือกบรรทัดเพื่อเริ่ม')
        tk.Label(modern,textvariable=explain,bg='#f8fafc',fg=TEXT,font=('Segoe UI',9),wraplength=390,justify='left').pack(anchor='w',padx=10,pady=10)

        practice=self.card(b,'Step 3 • Practice before continuing',
            'ตอบคำถามจาก concept ของบรรทัดนี้ให้ถูกก่อน ระบบจึงเปิดขั้นเลือก TC menu ถัดไป')
        qv=tk.StringVar(value='—');tk.Label(practice,textvariable=qv,bg='white',fg=TEXT,font=('Segoe UI Semibold',12),
                                            wraplength=920,justify='left').pack(anchor='w',padx=18,pady=5)
        ans=tk.IntVar(value=-1);rbs=[]
        for i in range(4):
            rb=ttk.Radiobutton(practice,text='',variable=ans,value=i);rb.pack(anchor='w',padx=18,pady=2);rbs.append(rb)
        feedback=tk.StringVar(value='')
        br=tk.Frame(practice,bg='white');br.pack(fill='x',padx=18,pady=10)
        ttk.Button(br,text='✓ Check Lesson',style='Primary.TButton').pack(side='left');checkbtn=br.winfo_children()[-1]
        ttk.Button(br,text='Show Hint / Visual').pack(side='left',padx=6);hintbtn=br.winfo_children()[-1]
        tk.Label(practice,textvariable=feedback,bg='white',fg=BLUE,font=('Segoe UI',10),wraplength=900,justify='left').pack(anchor='w',padx=18,pady=(0,12))

        nextcard=self.card(b,'Step 4 • Choose next TC lesson',
            'เมื่อทำบทเรียนผ่านแล้ว เลือก “บรรทัดถัดไป” หรือกลับไปเลือกไฟล์/หัวข้อจาก TC')
        nr=tk.Frame(nextcard,bg='white');nr.pack(fill='x',padx=18,pady=(0,14))
        ttk.Button(nr,text='Next Source Line ▶',state='disabled').pack(side='left');nextline=nr.winfo_children()[-1]
        ttk.Button(nr,text='📚 Choose another TC file',state='disabled').pack(side='left',padx=6);nexttc=nr.winfo_children()[-1]
        ttk.Button(nr,text='🧭 Open TC Math Gallery',state='disabled').pack(side='left');gallery=nr.winfo_children()[-1]

        state={'name':'','source':'','lines':[],'line':0,'lesson':None,'question':None,'phase':0.0,'after':None}

        def draw():
            if state['lesson']:self._v55_visual(cv,state['lesson']['kind'],state['phase'])

        def animate():
            state['phase']+=.055;draw();state['after']=self.after(100,animate)

        def select_line(n):
            if not state['lines']:return
            n=max(1,min(len(state['lines']),n));state['line']=n
            src.configure(state='normal');src.tag_remove('sel','1.0','end');src.tag_add('sel',f'{n}.0',f'{n}.end');src.see(f'{n}.0');src.configure(state='disabled')
            line=state['lines'][n-1]
            lesson=self._v56_lesson_for_line(state['name'],line);state['lesson']=lesson
            q=self._v56_question(lesson);state['question']=q
            titlev.set(f'Line {n} • {lesson["title"]} • detected={lesson["kind"]}')
            formulav.set('Formula / meaning: '+lesson['formula'])
            goalv.set('Learning goal: '+lesson['goal']);aiv.set('AI connection: '+lesson['ai'])
            pybox.configure(state='normal');pybox.delete('1.0','end');pybox.insert('1.0',lesson['python']);pybox.configure(state='disabled')
            explain.set(f'Classification: {lesson["type"]}\nDetection evidence score: {lesson["score"]}\n'
                        'ภาพเป็น visual model ของ concept ที่ตรวจพบ; ถ้า source ไม่ระบุ parameter จะใช้ค่า demo เพื่อการเรียนรู้')
            qv.set(q['q']);ans.set(-1);feedback.set('')
            for i,rb in enumerate(rbs):rb.configure(text=q['choices'][i])
            nextline.configure(state='disabled');nexttc.configure(state='disabled');gallery.configure(state='disabled')
            draw()

        def click(event):
            idx=src.index(f'@{event.x},{event.y}');select_line(int(idx.split('.')[0]))

        def check():
            q=state['question']
            if not q:return
            if ans.get()<0:feedback.set('กรุณาเลือกคำตอบก่อน');return
            if ans.get()==q['ans']:
                feedback.set('✓ ผ่านบทเรียน — '+q['why']+'  ตอนนี้เลือกบรรทัดถัดไปหรือเลือก TC lesson ใหม่ได้')
                nextline.configure(state='normal');nexttc.configure(state='normal');gallery.configure(state='normal')
            else:
                feedback.set('ยังไม่ผ่าน — ทบทวน Formula และ Animation แล้วลองใหม่: '+q['why'])
                ans.set(-1)

        def hint():
            lesson=state['lesson']
            if not lesson:return
            feedback.set('Hint: '+lesson['goal']+' • ดูการเปลี่ยนแปลงในภาพแล้วกลับมาตอบอีกครั้ง')

        def load(name,source):
            state.update(name=name,source=source,lines=source.splitlines() or [''],line=0,lesson=None,question=None)
            filev.set(name);src.configure(state='normal');src.delete('1.0','end');src.insert('1.0',source[:180000])
            for i,line in enumerate(state['lines'],1):
                if self._v52_line_equation(line):src.tag_add('math',f'{i}.0',f'{i}.end')
            src.configure(state='disabled')
            titlev.set('Lesson: เลือกบรรทัดที่ต้องการเรียน');formulav.set('Formula: —');goalv.set('Learning goal: —');aiv.set('AI connection: —')
            qv.set('หลังเลือกบรรทัด ระบบจะสร้างคำถามสำหรับ mini lesson นั้น')
            cv.delete('all')

        def open_file():
            p=filedialog.askopenfilename(title='Open Pascal/C',filetypes=[('Pascal/C','*.pas *.pp *.c *.h *.cpp *.cc *.cxx *.hpp'),('All','*.*')])
            if not p:return
            data=Path(p).read_bytes();source,_=self._v43_decode(data);load(Path(p).name,source)

        def choose_zip():
            zp=filedialog.askopenfilename(title='Choose TC ZIP',filetypes=[('ZIP','*.zip')])
            if not zp:return
            try:
                with zipfile.ZipFile(zp) as z:
                    names=[n for n in z.namelist() if n.lower().endswith(('.pas','.pp','.c','.h','.cpp','.cc','.cxx','.hpp'))]
                win=tk.Toplevel(self);win.title('TC Lesson Menu');win.geometry('900x640')
                tk.Label(win,text='TC Source Menu — เลือกไฟล์เพื่อสร้างบทเรียนจากบรรทัด',font=('Segoe UI Semibold',13)).pack(anchor='w',padx=12,pady=(10,3))
                q=tk.StringVar();ttk.Entry(win,textvariable=q).pack(fill='x',padx=12,pady=6)
                lb=tk.Listbox(win,font=('Consolas',9));lb.pack(fill='both',expand=True,padx=12,pady=4)
                def fill(*_):
                    term=q.get().lower();lb.delete(0,'end')
                    preferred=sorted(names,key=lambda n:(0 if any(k in n.lower() for k in ('circle','para','ellipse','stat','matrix','vector','sort','tree')) else 1,n.lower()))
                    for n in [x for x in preferred if term in x.lower()][:1500]:lb.insert('end',n)
                def pick(*_):
                    if not lb.curselection():return
                    n=lb.get(lb.curselection()[0])
                    with zipfile.ZipFile(zp) as z:data=z.read(n)
                    source,_=self._v43_decode(data);win.destroy();load(n,source)
                q.trace_add('write',fill);lb.bind('<Double-Button-1>',pick)
                ttk.Button(win,text='Open selected TC lesson',command=pick).pack(pady=8);fill()
            except Exception as e:messagebox.showerror('TC ZIP',str(e))

        def next_line():
            if state['lines']:select_line(min(len(state['lines']),state['line']+1))

        openbtn.configure(command=open_file);zipbtn.configure(command=choose_zip)
        src.bind('<Button-1>',click);checkbtn.configure(command=check);hintbtn.configure(command=hint)
        nextline.configure(command=next_line);nexttc.configure(command=choose_zip);gallery.configure(command=self.math_gallery_lab)
        cv.bind('<Configure>',lambda e:draw());animate()

        flow=self.card(b,'v5.6 Learning Architecture',
            'SELECT LINE → AUTO LESSON → FORMULA + VISUAL + PYTHON → PRACTICE → PASS → NEXT LINE / TC MENU. '
            'บรรทัดสีเหลืองคือ assignment ที่ตรวจพบ นักเรียนยังเลือกบรรทัดอื่นได้เพื่อศึกษาบทบาทของ algorithm โดยระบบจะไม่บังคับสร้างสมการปลอม')
        tk.Label(flow,text='SOURCE LINE → UNDERSTAND → SEE → PRACTICE → COMPLETE → CHOOSE NEXT TC',
                 bg='white',fg=BLUE,font=('Segoe UI Semibold',11)).pack(anchor='w',padx=18,pady=(0,14))

    # ==================== v5.7 AI -> ROBOT SIMULATOR -> HARDWARE ====================
    def _v57_ports(self):
        try:
            import serial.tools.list_ports
            return [(p.device,p.description) for p in serial.tools.list_ports.comports()]
        except Exception:return []

    def _v57_robot_draw(self,cv,x,y,heading,trail,cmd='STOP'):
        cv.delete('all');w=max(650,cv.winfo_width());h=max(430,cv.winfo_height())
        cv.create_rectangle(0,0,w,h,fill='#f8fafc',outline='')
        # arena
        m=35;cv.create_rectangle(m,m,w-m,h-m,outline='#94a3b8',width=2)
        for gx in range(m,w-m,50):cv.create_line(gx,m,gx,h-m,fill='#e5e7eb')
        for gy in range(m,h-m,50):cv.create_line(m,gy,w-m,gy,fill='#e5e7eb')
        if len(trail)>1:
            pts=[]
            for px,py in trail[-300:]:pts.extend([px,py])
            cv.create_line(*pts,fill='#93c5fd',width=2)
        r=18
        import math
        # robot body triangle
        a=heading
        pts=[]
        for ang,rad in [(a,26),(a+2.5,r),(a-2.5,r)]:
            pts.extend([x+math.cos(ang)*rad,y-math.sin(ang)*rad])
        cv.create_polygon(*pts,fill='#2563eb',outline='#1e3a8a',width=2)
        cv.create_oval(x-7,y-7,x+7,y+7,fill='white',outline='')
        cv.create_text(m+8,m+8,anchor='nw',text=f'Robot Command: {cmd}',fill=TEXT,font=('Segoe UI Semibold',11))
        cv.create_text(m+8,m+28,anchor='nw',text=f'Position ({x:.0f},{y:.0f}) • heading {math.degrees(heading)%360:.0f}°',fill=MUTED,font=('Segoe UI',9))

    def ai_robot_control_lab(self):
        self.clear()
        self.header('🤖 • v5.7 AI → Robot Control Laboratory',
                    'แยก AI/Webcam outputs ออกจากบทเรียน → Mapping เป็นคำสั่ง → จำลองหุ่นยนต์ในคอม → ตรวจ Hardware → จึงอนุญาต Real Robot')
        b=self.scrollbody()
        intro=self.card(b,'Safety-first control pipeline',
            'โรงเรียนที่ไม่มีหุ่นยนต์สามารถใช้ Simulator ได้เต็มบทเรียน ส่วน Real Hardware ถูกแยกออกและล็อกไว้ '
            'จนกว่าจะผ่าน Hardware Check และครู/ผู้ใช้เปิด Enable Real Robot เอง')
        # Input/output command mapper
        mapper=self.card(b,'1 • AI / Webcam Output → Robot Command Mapper',
            'จำลองผลลัพธ์จาก Image AI หรือ Webcam ก่อน แล้วกำหนดว่าผลแต่ละ class จะสั่งหุ่นยนต์อย่างไร')
        mr=tk.Frame(mapper,bg='white');mr.pack(fill='x',padx=18,pady=(0,8))
        sourcev=tk.StringVar(value='Manual / AI Demo')
        ttk.Combobox(mr,textvariable=sourcev,state='readonly',width=20,
                     values=['Manual / AI Demo','Image AI Result','Webcam Position']).pack(side='left')
        outputv=tk.StringVar(value='CENTER')
        ttk.Combobox(mr,textvariable=outputv,state='readonly',width=16,
                     values=['LEFT','CENTER','RIGHT','NEAR','FAR','CLASS_A','CLASS_B','NO_OBJECT']).pack(side='left',padx=6)
        conf=tk.DoubleVar(value=.90)
        tk.Label(mr,text='Confidence',bg='white').pack(side='left',padx=(10,3))
        ttk.Scale(mr,from_=0,to=1,variable=conf,length=140).pack(side='left')
        threshold=tk.DoubleVar(value=.60)
        tk.Label(mr,text='Threshold',bg='white').pack(side='left',padx=(10,3))
        ttk.Scale(mr,from_=0,to=1,variable=threshold,length=140).pack(side='left')
        mapping={'LEFT':'TURN_LEFT','CENTER':'FORWARD','RIGHT':'TURN_RIGHT','NEAR':'STOP',
                 'FAR':'FORWARD','CLASS_A':'TURN_LEFT','CLASS_B':'TURN_RIGHT','NO_OBJECT':'STOP'}
        mapv=tk.StringVar(value='')
        tk.Label(mapper,textvariable=mapv,bg='white',fg=BLUE,font=('Segoe UI Semibold',10)).pack(anchor='w',padx=18,pady=(0,10))

        sim=self.card(b,'2 • Robot Simulator — works without hardware',
            'หุ่นยนต์เสมือนเดินในสนามบนคอมพิวเตอร์ด้วยคำสั่งเดียวกับที่เตรียมส่งให้ฮาร์ดแวร์จริง')
        controls=tk.Frame(sim,bg='white');controls.pack(fill='x',padx=18,pady=(0,6))
        for label,cmd in [('↑ Forward','FORWARD'),('← Left','TURN_LEFT'),('Stop','STOP'),('Right →','TURN_RIGHT'),('↓ Back','BACKWARD')]:
            ttk.Button(controls,text=label).pack(side='left',padx=3)
            controls.winfo_children()[-1].configure(command=lambda c=cmd:manual(c))
        ttk.Button(controls,text='▶ Auto from AI Output',style='Primary.TButton').pack(side='left',padx=10);autobtn=controls.winfo_children()[-1]
        cv=tk.Canvas(sim,height=440,bg='#f8fafc',highlightbackground=BORDER,highlightthickness=1);cv.pack(fill='both',expand=True,padx=18,pady=(0,14))

        hw=self.card(b,'3 • Real Robot Gate',
            'Real Robot จะยังไม่ทำงานจากหน้านี้จนกว่าจะผ่าน Hardware Check และเปิด Enable Real Robot')
        hwr=tk.Frame(hw,bg='white');hwr.pack(fill='x',padx=18,pady=(0,12))
        hwstatus=tk.StringVar(value='Hardware status: NOT CHECKED')
        tk.Label(hwr,textvariable=hwstatus,bg='white',fg='#b45309',font=('Segoe UI Semibold',10)).pack(side='left')
        ttk.Button(hwr,text='Open Hardware Check',command=self.hardware_check_lab).pack(side='left',padx=12)
        realenable=tk.BooleanVar(value=False)
        ttk.Checkbutton(hwr,text='Enable Real Robot (after check)',variable=realenable).pack(side='left')
        ttk.Button(hwr,text='Send current command',state='disabled').pack(side='left',padx=8);sendbtn=hwr.winfo_children()[-1]

        state={'x':420.,'y':240.,'heading':0.,'trail':[(420.,240.)],'cmd':'STOP','auto':False,'after':None}

        def command_from_ai():
            if conf.get()<threshold.get():return 'STOP'
            return mapping.get(outputv.get(),'STOP')

        def update_map(*_):
            cmd=command_from_ai()
            mapv.set(f'AI Output={outputv.get()} • confidence={conf.get():.2f} → command={cmd}'
                     + (' (below threshold → STOP)' if conf.get()<threshold.get() else ''))
        outputv.trace_add('write',update_map);conf.trace_add('write',update_map);threshold.trace_add('write',update_map)

        def step(cmd):
            import math
            state['cmd']=cmd
            if cmd=='TURN_LEFT':state['heading']+=.18
            elif cmd=='TURN_RIGHT':state['heading']-=.18
            elif cmd in ('FORWARD','BACKWARD'):
                d=8 if cmd=='FORWARD' else -6
                state['x']+=math.cos(state['heading'])*d;state['y']-=math.sin(state['heading'])*d
                w=max(650,cv.winfo_width());h=max(430,cv.winfo_height())
                state['x']=max(55,min(w-55,state['x']));state['y']=max(55,min(h-55,state['y']))
                state['trail'].append((state['x'],state['y']))
            self._v57_robot_draw(cv,state['x'],state['y'],state['heading'],state['trail'],cmd)

        def manual(cmd):
            state['auto']=False;step(cmd)

        def auto():
            state['auto']=not state['auto']
            autobtn.configure(text='■ Stop Auto' if state['auto'] else '▶ Auto from AI Output')
            def tick():
                if not state['auto']:return
                step(command_from_ai());state['after']=self.after(120,tick)
            if state['auto']:tick()

        def gate(*_):
            # v5.7 intentionally requires check in dedicated screen each run; no silent connection.
            sendbtn.configure(state='disabled')
            if realenable.get():
                hwstatus.set('Hardware status: run Hardware Check first; real send remains locked in Simulator')
        realenable.trace_add('write',gate)
        autobtn.configure(command=auto)
        cv.bind('<Configure>',lambda e:self._v57_robot_draw(cv,state['x'],state['y'],state['heading'],state['trail'],state['cmd']))
        update_map();self._v57_robot_draw(cv,state['x'],state['y'],state['heading'],state['trail'],'STOP')

        flow=self.card(b,'Control architecture',
            'Image AI/Webcam Output → Confidence Gate → Command Mapper → Robot Simulator → Hardware Check → Real Robot. '
            'ดังนั้นกิจกรรมเดียวกันใช้ได้ทั้งโรงเรียนที่มีและไม่มีอุปกรณ์จริง')
        tk.Label(flow,text='AI OUTPUT → SAFE COMMAND → SIMULATE FIRST → VERIFY HARDWARE → REAL WORLD',
                 bg='white',fg=BLUE,font=('Segoe UI Semibold',11)).pack(anchor='w',padx=18,pady=(0,14))

    def hardware_check_lab(self):
        self.clear()
        self.header('🧪 • v5.7 Hardware Check',
                    'ตรวจ Python modules → Webcam → Serial/COM → Connection test ก่อนนำคำสั่งไปใช้กับหุ่นยนต์จริง')
        b=self.scrollbody()
        intro=self.card(b,'Pre-flight Hardware Inspection',
            'หน้านี้แยกจาก Simulator โดยตั้งใจ เพื่อให้โรงเรียนที่ไม่มี hardware ใช้โปรแกรมได้ตามปกติ '
            'และผู้ที่มีอุปกรณ์ตรวจทีละส่วนก่อนเชื่อมต่อจริง')
        result=self.card(b,'System Checks','กด Run All Checks')
        status=tk.Text(result,height=15,font=('Consolas',9),wrap='word');status.pack(fill='x',padx=18,pady=(0,10))
        br=tk.Frame(result,bg='white');br.pack(fill='x',padx=18,pady=(0,14))
        ttk.Button(br,text='Run All Checks',style='Primary.TButton').pack(side='left');runbtn=br.winfo_children()[-1]
        ttk.Button(br,text='Test Webcam').pack(side='left',padx=5);cambtn=br.winfo_children()[-1]
        ttk.Button(br,text='Refresh COM Ports').pack(side='left');portbtn=br.winfo_children()[-1]

        conn=self.card(b,'Serial / Robot Connection','เลือกพอร์ตหลังตรวจพบ แล้วทดสอบเปิด-ปิด connection โดยยังไม่ส่งคำสั่งเคลื่อนที่')
        rr=tk.Frame(conn,bg='white');rr.pack(fill='x',padx=18,pady=(0,10))
        portv=tk.StringVar();portbox=ttk.Combobox(rr,textvariable=portv,state='readonly',width=38);portbox.pack(side='left')
        baud=tk.StringVar(value='9600');ttk.Combobox(rr,textvariable=baud,state='readonly',width=10,values=['9600','19200','38400','57600','115200']).pack(side='left',padx=6)
        ttk.Button(rr,text='Test Connection').pack(side='left');testbtn=rr.winfo_children()[-1]
        connv=tk.StringVar(value='Not connected')
        tk.Label(conn,textvariable=connv,bg='white',fg=MUTED,font=('Segoe UI Semibold',10)).pack(anchor='w',padx=18,pady=(0,14))

        checklist=self.card(b,'Recommended physical safety check',
            'ก่อนใช้งานจริง: ยกล้อหุ่นยนต์ให้พ้นพื้นในการทดสอบครั้งแรก • ตรวจ polarity/แรงดัน • '
            'มีปุ่ม/วิธีหยุดฉุกเฉิน • จำกัดความเร็วเริ่มต้น • ให้ครูดูแลเมื่อเชื่อมมอเตอร์')
        tk.Label(checklist,text='Simulator PASS ≠ Hardware PASS — ต้องตรวจฮาร์ดแวร์จริงแยกต่างหาก',
                 bg='white',fg='#b45309',font=('Segoe UI Semibold',10)).pack(anchor='w',padx=18,pady=(0,14))

        def log(s):
            status.insert('end',s+'\n');status.see('end')

        def ports():
            ps=self._v57_ports();portbox['values']=[p[0] for p in ps]
            if ps and not portv.get():portv.set(ps[0][0])
            log(f'[SERIAL] {len(ps)} port(s): '+(', '.join(f'{a} ({d})' for a,d in ps) if ps else 'none'))
            return ps

        def camera():
            try:
                import cv2
                cap=cv2.VideoCapture(0)
                ok,frame=cap.read();cap.release()
                log('[WEBCAM] PASS — frame received' if ok and frame is not None else '[WEBCAM] FAIL — camera not available/busy')
                return bool(ok and frame is not None)
            except Exception as e:
                log('[WEBCAM] FAIL — '+str(e));return False

        def allchecks():
            status.delete('1.0','end')
            for mod in ['tkinter','sympy','cv2','serial','PIL']:
                try:
                    __import__(mod);log(f'[MODULE] {mod}: PASS')
                except Exception as e:log(f'[MODULE] {mod}: MISSING ({e})')
            camera();ports()
            log('[INFO] No motor command was sent during these checks.')

        def test_connection():
            if not portv.get():connv.set('FAIL: no COM/serial port selected');return
            try:
                import serial
                ser=serial.Serial(portv.get(),int(baud.get()),timeout=1)
                ser.close()
                connv.set(f'PASS: {portv.get()} opened and closed successfully — no motion command sent')
                log('[CONNECTION] PASS — port open/close only')
            except Exception as e:
                connv.set('FAIL: '+str(e));log('[CONNECTION] FAIL — '+str(e))

        runbtn.configure(command=allchecks);cambtn.configure(command=camera);portbtn.configure(command=ports);testbtn.configure(command=test_connection)
        ports()

    # ==================== v5.8 ROBOT COMMAND CENTER ====================
    def robot_command_center_lab(self):
        self.clear()
        self.header('🎛 • v5.8 Robot Command Center',
                    'รวม Math / Image AI / Webcam / Adaptive AI / Manual → Decision → Command → Simulator หรือ Real Hardware → Feedback')
        b=self.scrollbody()
        intro=self.card(b,'Unified Robot Architecture',
            'ทุก input ถูกแปลงเป็น command มาตรฐานที่จุดเดียวก่อนส่งออก นักเรียนจึงเห็นชัดว่า AI ไม่ได้ควบคุมมอเตอร์โดยตรง '
            'แต่ผ่าน Decision + Safety Gate + Command Router ก่อนเสมอ')

        # Pipeline animation
        pipe=self.card(b,'1 • Live AI-Robot Pipeline','INPUT → AI → DECISION → COMMAND → ROBOT → FEEDBACK')
        pcv=tk.Canvas(pipe,height=145,bg='#fbfdff',highlightthickness=0)
        pcv.pack(fill='x',padx=18,pady=(0,12))

        setup=self.card(b,'2 • Input & Decision Center',
            'เลือกแหล่งข้อมูลและจำลอง output ของแต่ละระบบ จากนั้น Command Center จะสร้างคำสั่งกลาง')
        r=tk.Frame(setup,bg='white');r.pack(fill='x',padx=18,pady=(0,8))
        source=tk.StringVar(value='Manual')
        ttk.Combobox(r,textvariable=source,state='readonly',width=18,
                     values=['Manual','Math Result','Image AI','Webcam','Adaptive AI']).pack(side='left')
        value=tk.StringVar(value='CENTER')
        valuebox=ttk.Combobox(r,textvariable=value,state='readonly',width=18,
            values=['LEFT','CENTER','RIGHT','NEAR','FAR','CLASS_A','CLASS_B','NO_OBJECT','POSITIVE','NEGATIVE','CORRECT','RETRY'])
        valuebox.pack(side='left',padx=6)
        conf=tk.DoubleVar(value=.90);th=tk.DoubleVar(value=.60)
        tk.Label(r,text='Confidence',bg='white').pack(side='left',padx=(12,3))
        ttk.Scale(r,from_=0,to=1,variable=conf,length=130).pack(side='left')
        tk.Label(r,text='Safety threshold',bg='white').pack(side='left',padx=(12,3))
        ttk.Scale(r,from_=0,to=1,variable=th,length=130).pack(side='left')

        commandv=tk.StringVar(value='STOP');decisionv=tk.StringVar(value='Waiting')
        info=tk.Frame(setup,bg='#f8fafc');info.pack(fill='x',padx=18,pady=(2,12))
        tk.Label(info,textvariable=decisionv,bg='#f8fafc',fg=TEXT,font=('Segoe UI',10)).pack(anchor='w',padx=10,pady=(8,2))
        tk.Label(info,textvariable=commandv,bg='#f8fafc',fg=BLUE,font=('Segoe UI Semibold',14)).pack(anchor='w',padx=10,pady=(2,8))

        route=self.card(b,'3 • Output Router',
            'SIMULATOR เป็นค่าเริ่มต้นและใช้ได้โดยไม่มีอุปกรณ์จริง ส่วน REAL HARDWARE ต้องผ่านการตรวจและเปิดใช้งานอย่างชัดเจน')
        rr=tk.Frame(route,bg='white');rr.pack(fill='x',padx=18,pady=(0,10))
        target=tk.StringVar(value='SIMULATOR')
        ttk.Radiobutton(rr,text='Computer Simulator',variable=target,value='SIMULATOR').pack(side='left')
        ttk.Radiobutton(rr,text='Real Hardware',variable=target,value='HARDWARE').pack(side='left',padx=14)
        hardware_ok=tk.BooleanVar(value=False)
        ttk.Checkbutton(rr,text='Hardware Check PASS (confirm after testing)',variable=hardware_ok).pack(side='left',padx=10)
        ttk.Button(rr,text='Open Hardware Check',command=self.hardware_check_lab).pack(side='left')
        gatev=tk.StringVar(value='Route: SIMULATOR')
        tk.Label(route,textvariable=gatev,bg='white',fg='#b45309',font=('Segoe UI Semibold',10)).pack(anchor='w',padx=18,pady=(0,12))

        sim=self.card(b,'4 • Robot Digital Twin / Simulator',
            'คำสั่งเดียวกับ Command Center ถูกแสดงเป็นการเคลื่อนที่ในคอมพิวเตอร์ก่อนนำไปใช้จริง')
        sr=tk.Frame(sim,bg='white');sr.pack(fill='x',padx=18,pady=(0,6))
        ttk.Button(sr,text='▶ Run one command',style='Primary.TButton').pack(side='left');runbtn=sr.winfo_children()[-1]
        ttk.Button(sr,text='▶ Auto Run').pack(side='left',padx=5);autobtn=sr.winfo_children()[-1]
        ttk.Button(sr,text='■ Emergency STOP').pack(side='left');stopbtn=sr.winfo_children()[-1]
        ttk.Button(sr,text='Reset Simulator').pack(side='left',padx=5);resetbtn=sr.winfo_children()[-1]
        cv=tk.Canvas(sim,height=430,bg='#f8fafc',highlightbackground=BORDER,highlightthickness=1)
        cv.pack(fill='both',expand=True,padx=18,pady=(0,12))

        logcard=self.card(b,'5 • Feedback / Event Log',
            'แสดง Input, Decision, Command, Route และผลการจำลอง เพื่อใช้สอนเรื่อง feedback loop')
        log=tk.Text(logcard,height=9,font=('Consolas',9),wrap='word');log.pack(fill='x',padx=18,pady=(0,12))

        mapping={
          'LEFT':'TURN_LEFT','CENTER':'FORWARD','RIGHT':'TURN_RIGHT','NEAR':'STOP','FAR':'FORWARD',
          'CLASS_A':'TURN_LEFT','CLASS_B':'TURN_RIGHT','NO_OBJECT':'STOP',
          'POSITIVE':'FORWARD','NEGATIVE':'BACKWARD','CORRECT':'FORWARD','RETRY':'STOP'
        }
        state={'x':420.,'y':230.,'heading':0.,'trail':[(420.,230.)],'cmd':'STOP',
               'auto':False,'phase':0,'after':None,'pipeline_step':0}

        def decide(*_):
            if source.get()=='Manual':
                cmd=mapping.get(value.get(),'STOP');reason='Manual mapping'
            elif conf.get()<th.get():
                cmd='STOP';reason=f'Confidence {conf.get():.2f} < threshold {th.get():.2f} → safety STOP'
            else:
                cmd=mapping.get(value.get(),'STOP');reason=f'{source.get()} output {value.get()} accepted at {conf.get():.2f}'
            commandv.set('COMMAND: '+cmd);decisionv.set('DECISION: '+reason);state['cmd']=cmd
            if target.get()=='HARDWARE':
                gatev.set('Route: HARDWARE LOCKED — confirm Hardware Check PASS' if not hardware_ok.get()
                          else 'Route: HARDWARE ARMED — simulation preview still recommended')
            else:gatev.set('Route: SIMULATOR — no physical hardware required')
            draw_pipeline()

        def draw_pipeline():
            pcv.delete('all');w=max(850,pcv.winfo_width())
            labels=['INPUT','AI','DECISION','COMMAND','ROBOT','FEEDBACK']
            xs=[55+i*(w-110)/5 for i in range(6)]
            active=state['pipeline_step']%6
            for i,(x,lab) in enumerate(zip(xs,labels)):
                fill='#2563eb' if i==active else '#e2e8f0'
                fg='white' if i==active else '#334155'
                pcv.create_oval(x-34,38,x+34,106,fill=fill,outline='#94a3b8')
                pcv.create_text(x,72,text=lab,fill=fg,font=('Segoe UI Semibold',8))
                if i<5:
                    pcv.create_line(x+36,72,xs[i+1]-36,72,arrow='last',fill='#64748b',width=2)
            pcv.create_text(15,126,anchor='w',text=f'{source.get()}:{value.get()} → {state["cmd"]} → {target.get()}',
                            fill=MUTED,font=('Segoe UI',9))

        def logit(msg):
            import datetime
            log.insert('end',datetime.datetime.now().strftime('%H:%M:%S')+'  '+msg+'\n');log.see('end')

        def simulate(cmd):
            import math
            state['cmd']=cmd
            if cmd=='TURN_LEFT':state['heading']+=.20
            elif cmd=='TURN_RIGHT':state['heading']-=.20
            elif cmd in ('FORWARD','BACKWARD'):
                d=9 if cmd=='FORWARD' else -7
                state['x']+=math.cos(state['heading'])*d;state['y']-=math.sin(state['heading'])*d
                w=max(650,cv.winfo_width());h=max(420,cv.winfo_height())
                state['x']=max(55,min(w-55,state['x']));state['y']=max(55,min(h-55,state['y']))
                state['trail'].append((state['x'],state['y']))
            self._v57_robot_draw(cv,state['x'],state['y'],state['heading'],state['trail'],cmd)
            logit(f'INPUT={source.get()}:{value.get()}  DECISION={decisionv.get()[10:]}  COMMAND={cmd}  ROUTE=SIMULATOR  FEEDBACK=position({state["x"]:.0f},{state["y"]:.0f})')

        def execute():
            decide();cmd=state['cmd']
            # v5.8 deliberately never sends motor bytes from this screen.
            if target.get()=='HARDWARE':
                if not hardware_ok.get():
                    logit('HARDWARE BLOCKED: Hardware Check not confirmed');gatev.set('BLOCKED — run Hardware Check first')
                    return
                logit(f'HARDWARE PREVIEW ONLY: {cmd}. Use dedicated tested hardware protocol before real motor output.')
                gatev.set('Hardware PASS confirmed • command previewed • direct motor transmission disabled in v5.8')
                return
            simulate(cmd)

        def auto():
            state['auto']=not state['auto'];autobtn.configure(text='■ Stop Auto' if state['auto'] else '▶ Auto Run')
            def tick():
                if not state['auto']:return
                execute();state['pipeline_step']=(state['pipeline_step']+1)%6;draw_pipeline()
                state['after']=self.after(180,tick)
            if state['auto']:tick()

        def emergency():
            state['auto']=False;state['cmd']='STOP';commandv.set('COMMAND: STOP');autobtn.configure(text='▶ Auto Run')
            self._v57_robot_draw(cv,state['x'],state['y'],state['heading'],state['trail'],'STOP')
            logit('EMERGENCY STOP');gatev.set('STOPPED')

        def reset():
            emergency();state.update(x=420.,y=230.,heading=0.,trail=[(420.,230.)],pipeline_step=0)
            self._v57_robot_draw(cv,state['x'],state['y'],state['heading'],state['trail'],'STOP');draw_pipeline()

        for v in (source,value):v.trace_add('write',decide)
        conf.trace_add('write',decide);th.trace_add('write',decide);target.trace_add('write',decide);hardware_ok.trace_add('write',decide)
        runbtn.configure(command=execute);autobtn.configure(command=auto);stopbtn.configure(command=emergency);resetbtn.configure(command=reset)
        cv.bind('<Configure>',lambda e:self._v57_robot_draw(cv,state['x'],state['y'],state['heading'],state['trail'],state['cmd']))
        pcv.bind('<Configure>',lambda e:draw_pipeline())
        decide();reset()

        architecture=self.card(b,'v5.8 Teaching Architecture',
            'Math Result / Image AI / Webcam / Adaptive AI / Manual → unified Decision Center → Confidence/Safety Gate → '
            'standard robot command → Computer Simulator or gated Hardware route → Feedback. '
            'โรงเรียนไม่มีอุปกรณ์สามารถเรียนและทดลองถึง Simulator + Feedback ได้ครบ')
        tk.Label(architecture,text='INPUT → AI → DECISION → SAFETY → COMMAND → ROBOT → FEEDBACK → NEXT DECISION',
                 bg='white',fg=BLUE,font=('Segoe UI Semibold',11)).pack(anchor='w',padx=18,pady=(0,14))

if __name__=='__main__': Studio().mainloop()
