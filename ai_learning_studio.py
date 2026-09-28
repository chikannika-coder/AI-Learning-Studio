import json
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

APP='AI Learning Studio — V4.7 Mathematical Knowledge Map'
BG='#f4f7fb'; NAV='#15243b'; BLUE='#20a4d8'; TEXT='#14213d'; MUTED='#66758a'; BORDER='#dce5ef'; GREEN='#15803d'; ORANGE='#c2410c'

class Studio(tk.Tk):
    def __init__(self):
        super().__init__(); self.title(APP); self.geometry('1420x880'); self.minsize(1100,720); self.configure(bg=BG)
        self.class_data={'A':[],'B':[]}; self.features={'A':[],'B':[]}; self.model=None; self.last_metrics={}; self.progress={str(i):0 for i in range(1,9)}
        self.robot=(260,180); self.robot_serial=None; self.sim=True; self.lesson_score=0; self.scores={str(i):0 for i in range(1,9)}; self.student_name='Student'; self.tc_zip=self._find_tc_zip(); self.webcam_cap=None; self.museum_scores={k:0 for k in ['Circle','Parabola','Ellipse','Sorting','Statistics','Probability','Decision Tree']}; self.mcs_progress={str(i):0 for i in range(1,9)}; self.mcs_robot_rule={'logic':True,'graph_path':['A','B','D','F'],'probability_threshold':0.55,'last_probability':0.0}
        self._style(); self._layout(); self.home()
    def _style(self):
        s=ttk.Style(self)
        try:s.theme_use('clam')
        except:pass
        s.configure('Primary.TButton',font=('Segoe UI Semibold',10),padding=(12,8)); s.configure('TButton',font=('Segoe UI',10),padding=(9,7)); s.configure('TNotebook.Tab',font=('Segoe UI Semibold',10),padding=(12,8))
    def _layout(self):
        self.side=tk.Frame(self,bg=NAV,width=230); self.side.pack(side='left',fill='y'); self.side.pack_propagate(False)
        tk.Label(self.side,text='AI',font=('Segoe UI Black',30),fg='#68d7ff',bg=NAV).pack(anchor='w',padx=22,pady=(20,0)); tk.Label(self.side,text='LEARNING STUDIO',font=('Segoe UI Semibold',12),fg='white',bg=NAV).pack(anchor='w',padx=22,pady=(0,18))
        items=[('⌂  Home',self.home),('01  Coding & Algorithm',self.lesson1),('02  Dataset Lab',self.lesson2),('03  Image AI',self.lesson3),('04  Sound AI',self.lesson4),('05  Live AI + Math',self.lesson5),('06  Robot AI',self.lesson6),('07  AI Agent',self.lesson7),('08  Project Studio',self.lesson8),('🏛  TC Math Museum',self.tc_math_museum),('📘  MCS Math for CS',self.mcs_center),('▶  MCS Animation → Robot',self.mcs_animation_lab),('∫  AI Equation → Animation',self.ai_equation_animation_lab),('↔  Equation Experiment Lab',self.equation_experiment_lab),('∿  Trig + Calculus Animation',self.trig_calculus_animation_lab),('▦  Matrix + Probability Lab',self.matrix_probability_animation_lab),('🎲  Random Walk + Bayes',self.random_walk_bayes_lab),('📊  MCS Statistics Lab',self.mcs_statistics_lab),('📈  Random Variable + PMF/CDF',self.random_variable_distribution_lab),('⚖  Binomial Theory vs Experiment',self.binomial_compare_lab),('🔗  Indicator + Covariance Lab',self.indicator_covariance_lab),('💾  C Program Math Archive',self.cprog_math_archive_lab),('📐  Markov vs Chebyshev',self.markov_chebyshev_compare_lab),('🧮  C Source → Math Concepts',self.c_source_math_concepts_lab),('🧠  V4 Auto C → Mathematics',self.v40_auto_c_math_lab),('∑  V4.1 Math Model → Source',self.v41_math_model_source_lab),('ƒ  V4.2 Source → Expression → Equation',self.v42_source_expression_model_lab),('🕸  V4.3 Dependency + Recurrence',self.v43_dependency_recurrence_lab),('∴  V4.4 Symbolic Proof → Simulation',self.v44_symbolic_proof_simulation_lab),('🔬  V4.5 Source → Proof Pipeline',self.v45_source_to_proof_lab),('🧭  V4.6 Math Model Classifier',self.v46_math_model_classifier_lab),('🗺  V4.7 Math Knowledge Map',self.v47_math_knowledge_map_lab),('📷  v4 Vision → Robot Lab',self.lesson6),('🎛  v5.8 Robot Command Center',self.robot_command_center_lab),('🤖  v5.7 AI → Robot Control',self.ai_robot_control_lab),('🧪  v5.7 Hardware Check',self.hardware_check_lab),('📖  v5.6 Line → Lesson → TC Menu',self.line_lesson_tc_lab),('🤖  v5.5 Adaptive AI Tutor',self.adaptive_tutor_lab),('🧠  v5.4 Auto TC Exercises',self.auto_tc_exercise_lab),('📝  v5.3 Student Exercises',self.student_exercise_lab),('👩‍🏫  v5.3 Teacher Mode',self.teacher_v53_lab),('🧩  v5.2 Four-Panel Learning',self.four_panel_learning_lab),('🔗  v5.1 TC Source → Live Math',self.tc_live_math_lab),('🎞  v5 Math Animation Lab',self.math_animation_lab),('🖼  TC Math Gallery',self.math_gallery_lab),('🧭  Equation Atlas (All Files)',self.equation_atlas_lab),('∫  Auto Equation Lab',self.auto_equation_lab),('∑  Math Comparison',self.math_lab),('⌘  TC Code Lab',self.tc_code_lab),('▣  Teacher Mode',self.teacher_mode),('▤  Worksheets',self.worksheets)]
        # V4.6: scrollable sidebar so all accumulated lessons remain reachable.
        # Keep the original menu list intact; only the rendering container changes.
        _menu_host = getattr(self, 'sidebar', None)
        if not isinstance(_menu_host, tk.Widget):
            _menu_host = getattr(self, 'side', None)
        if not isinstance(_menu_host, tk.Widget):
            _menu_host = getattr(self, 'left', None)
        if not isinstance(_menu_host, tk.Widget):
            # Fallback: discover a visible frame on the left; existing buttons still use self.nav_button below.
            _menu_host = self.root if hasattr(self, 'root') else self

        _nav_wrap = tk.Frame(_menu_host, bg=NAV)
        _nav_wrap.pack(fill='both', expand=True)
        _nav_canvas = tk.Canvas(_nav_wrap, bg=NAV, highlightthickness=0, bd=0, width=265)
        _nav_scroll = ttk.Scrollbar(_nav_wrap, orient='vertical', command=_nav_canvas.yview)
        _nav_inner = tk.Frame(_nav_canvas, bg=NAV)
        _nav_win = _nav_canvas.create_window((0,0), window=_nav_inner, anchor='nw')
        _nav_canvas.configure(yscrollcommand=_nav_scroll.set)
        _nav_canvas.pack(side='left', fill='both', expand=True)
        _nav_scroll.pack(side='right', fill='y')
        _nav_inner.bind('<Configure>', lambda e: _nav_canvas.configure(scrollregion=_nav_canvas.bbox('all')))
        _nav_canvas.bind('<Configure>', lambda e: _nav_canvas.itemconfigure(_nav_win, width=e.width))
        def _wheel(e):
            if getattr(e, 'delta', 0):
                _nav_canvas.yview_scroll(int(-1*(e.delta/120)), 'units')
        _nav_canvas.bind('<Enter>', lambda e: _nav_canvas.bind_all('<MouseWheel>', _wheel))
        _nav_canvas.bind('<Leave>', lambda e: _nav_canvas.unbind_all('<MouseWheel>'))

        for t,c in items:
            tk.Button(_nav_inner,text=t,command=c,bg=NAV,fg='#e8eef8',
                      activebackground='#223957',activeforeground='white',bd=0,
                      font=('Segoe UI',10),anchor='w',padx=20,pady=7,
                      cursor='hand2').pack(fill='x')
        tk.Label(self.side,text='v5.8 MASTER + MCS • V4.6 • Scroll Menu',
                 font=('Segoe UI',8),fg='#8293ab',bg=NAV).pack(side='bottom',pady=6)
        self.main=tk.Frame(self,bg=BG)
        self.main.pack(side='left',fill='both',expand=True)
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
        mcshero=self.card(b,'MCS INTEGRATION V2 — Mathematics → AI → Robot',
            'เพิ่ม Mathematics for Computer Science ลงบนฐาน v5.8 โดยไม่ลบเมนูเดิม: Logic/Truth → Sets/Relations → State Machine → Graph → Counting → Probability → Recurrence → AI Decision → Robot Simulation')
        ttk.Button(mcshero,text='เปิด MCS Animation → Robot',style='Primary.TButton',command=self.mcs_animation_lab).pack(anchor='w',padx=18,pady=(0,14))
        eqhero=self.card(b,'V3 • AI EQUATION → ANIMATION',
            'นักเรียนพิมพ์สมการ/สูตรเอง → Symbolic Math → Step-by-Step → Graph Animation → Experiment → เชื่อม MCS/Robot')
        ttk.Button(eqhero,text='เปิด AI Equation → Animation',style='Primary.TButton',command=self.ai_equation_animation_lab).pack(anchor='w',padx=18,pady=(0,14))
        exhero=self.card(b,'V3.1 • EQUATION EXPERIMENT LAB',
            'เปลี่ยนค่า a, b, c แบบ Slider → ดูสมการ/กราฟ/ราก/อนุพันธ์เปลี่ยนทันที → Animate Parameter → ส่งผลไป Robot Simulation')
        ttk.Button(exhero,text='เปิด Equation Experiment Lab',style='Primary.TButton',command=self.equation_experiment_lab).pack(anchor='w',padx=18,pady=(0,14))
        calchero=self.card(b,'V3.2 • TRIGONOMETRY + CALCULUS ANIMATION',
            'ทดลอง y = A sin(Bx + C) แบบ Slider และดู Derivative/Tangent/Integral Area เคลื่อนไหวบนกราฟ')
        ttk.Button(calchero,text='เปิด Trig + Calculus Animation',style='Primary.TButton',command=self.trig_calculus_animation_lab).pack(anchor='w',padx=18,pady=(0,14))
        v33hero=self.card(b,'V3.3 • VECTOR / MATRIX + PROBABILITY ANIMATION',
            'ทดลอง Linear Transformation ของ Vector/Shape และ Probability Distribution แบบ Animation → ส่งค่าที่ได้เข้าสู่ AI Decision / Robot Simulation')
        ttk.Button(v33hero,text='เปิด Matrix + Probability Lab',style='Primary.TButton',command=self.matrix_probability_animation_lab).pack(anchor='w',padx=18,pady=(0,14))
        v34hero=self.card(b,'V3.4 • RANDOM WALK → ROBOT PATH → CONDITIONAL / BAYES',
            'Random Walk บน Graph → เปรียบเทียบกับ BFS shortest path → Robot Mission Animation → Conditional Probability → Bayes Update')
        ttk.Button(v34hero,text='เปิด Random Walk + Bayes Lab',style='Primary.TButton',command=self.random_walk_bayes_lab).pack(anchor='w',padx=18,pady=(0,14))
        v35hero=self.card(b,'V3.5 • MATHEMATICAL STATISTICS LAB',
            'เก็บข้อมูลจาก Random Walk หลายรอบ → Frequency / Relative Frequency → Mean / Variance / SD → Empirical Probability → Convergence')
        ttk.Button(v35hero,text='เปิด MCS Statistics Lab',style='Primary.TButton',command=self.mcs_statistics_lab).pack(anchor='w',padx=18,pady=(0,14))
        v36hero=self.card(b,'V3.6 • RANDOM VARIABLE → HISTOGRAM → PMF → CDF → E[X] / Var(X)',
            'สร้าง distribution จาก Random Walk จริง เปรียบเทียบ Empirical กับ Theoretical first-passage distribution และดูการก่อตัวแบบ Animation')
        ttk.Button(v36hero,text='เปิด Random Variable + PMF/CDF',style='Primary.TButton',command=self.random_variable_distribution_lab).pack(anchor='w',padx=18,pady=(0,14))
        v37hero=self.card(b,'V3.7 • BINOMIAL: THEORY vs EXPERIMENT',
            'Bernoulli trials → Binomial PMF → Monte Carlo experiment → เปรียบเทียบความคลาดเคลื่อน → E[X], Var(X), SD → Convergence')
        ttk.Button(v37hero,text='เปิด Binomial Theory vs Experiment',style='Primary.TButton',command=self.binomial_compare_lab).pack(anchor='w',padx=18,pady=(0,14))
        v38hero=self.card(b,'V3.8 • INDICATOR → EXPECTATION → COVARIANCE / CORRELATION',
            'เปรียบเทียบ Theory vs Experiment ของตัวแปรสุ่มคู่ พร้อมเชื่อมตัวอย่างจากคลัง C Programming เดิมที่มี random, loop, array, struct และ graphics')
        ttk.Button(v38hero,text='เปิด Indicator + Covariance Lab',style='Primary.TButton',command=self.indicator_covariance_lab).pack(anchor='w',padx=18,pady=(0,6))
        ttk.Button(v38hero,text='เปิด C Program Math Archive',command=self.cprog_math_archive_lab).pack(anchor='w',padx=18,pady=(0,14))
        v39hero=self.card(b,'V3.9 • MARKOV vs CHEBYSHEV → C SOURCE → MATHEMATICS',
            'เปรียบเทียบ probability bounds ด้วย Theory vs Simulation ก่อน แล้วเชื่อม source C เดิมกับ Randomness, Iteration, Data, Geometry และ State')
        ttk.Button(v39hero,text='เปิด Markov vs Chebyshev',style='Primary.TButton',command=self.markov_chebyshev_compare_lab).pack(anchor='w',padx=18,pady=(0,6))
        ttk.Button(v39hero,text='เปิด C Source → Math Concepts',command=self.c_source_math_concepts_lab).pack(anchor='w',padx=18,pady=(0,14))
        v40hero=self.card(b,'V4.0 • MATH-FIRST AUTO SOURCE SELECTION',
            'วิเคราะห์ caimath.zip + tc.zip อัตโนมัติ → จัดอันดับ source ตามหลักฐานทางคณิตศาสตร์ → เลือก source → Math Model → Formula → Experiment → Visualization')
        ttk.Button(v40hero,text='เปิด V4 Auto C → Mathematics',style='Primary.TButton',command=self.v40_auto_c_math_lab).pack(anchor='w',padx=18,pady=(0,14))
        v41hero=self.card(b,'V4.1 • MATHEMATICAL MODEL → SOURCE EVIDENCE',
            'เริ่มจากเลือก Mathematical Model ก่อน → สมการ/ตัวแปร/กราฟ/การทดลอง → แล้วให้ระบบค้น source C/Pascal ที่มีหลักฐานสอดคล้อง')
        ttk.Button(v41hero,text='เปิด V4.1 Math Model → Source',style='Primary.TButton',command=self.v41_math_model_source_lab).pack(anchor='w',padx=18,pady=(0,14))
        v42hero=self.card(b,'V4.2 • SOURCE → VARIABLES / EXPRESSIONS → MATHEMATICAL MODEL',
            'แยกตัวแปรและ assignment expressions จาก C/Pascal จริงก่อน → normalize เป็นสมการ → จับคู่กับ Mathematical Model → Graph/Experiment')
        ttk.Button(v42hero,text='เปิด V4.2 Source → Expression → Equation',style='Primary.TButton',command=self.v42_source_expression_model_lab).pack(anchor='w',padx=18,pady=(0,14))
        v43hero=self.card(b,'V4.3 • MATHEMATICAL DEPENDENCY + RECURRENCE',
            'สร้าง dependency graph จากนิพจน์จริง และแยก algebraic assignment ออกจาก recurrence candidate อย่างระมัดระวัง')
        ttk.Button(v43hero,text='เปิด V4.3 Dependency + Recurrence',style='Primary.TButton',command=self.v43_dependency_recurrence_lab).pack(anchor='w',padx=18,pady=(0,14))
        v44hero=self.card(b,'V4.4 • SYMBOLIC PROOF → SIMULATION',
            'พิสูจน์ recurrence xₙ₊₁=axₙ+b เชิงสัญลักษณ์ก่อน: fixed point → closed form → induction → convergence แล้วจึงตรวจด้วย numerical simulation')
        ttk.Button(v44hero,text='เปิด V4.4 Symbolic Proof → Simulation',style='Primary.TButton',command=self.v44_symbolic_proof_simulation_lab).pack(anchor='w',padx=18,pady=(0,14))
        v45hero=self.card(b,'V4.5 • SOURCE → VERIFIED RECURRENCE → PROOF',
            'Source → self-dependency → loop/update evidence → affine recurrence → symbolic proof → simulation')
        ttk.Button(v45hero,text='เปิด V4.5 Source → Proof Pipeline',style='Primary.TButton',command=self.v45_source_to_proof_lab).pack(anchor='w',padx=18,pady=(0,14))
        v46hero=self.card(b,'V4.6 • MATHEMATICAL MODEL CLASSIFIER',
            'จัดกลุ่ม source ตามหลักฐานเป็น Algebra / Geometry / Trigonometry / Probability / Statistics / Sequence-Recurrence และเลือก derivation ที่เหมาะกับแต่ละประเภท')
        ttk.Button(v46hero,text='เปิด V4.6 Math Model Classifier',style='Primary.TButton',command=self.v46_math_model_classifier_lab).pack(anchor='w',padx=18,pady=(0,14))
        v47hero=self.card(b,'V4.7 • MATHEMATICAL KNOWLEDGE MAP',
            'แผนที่คณิตศาสตร์: Concept → Definition → Formula → Prerequisite → Source Evidence → Proof/Derivation → Simulation')
        ttk.Button(v47hero,text='เปิด V4.7 Math Knowledge Map',style='Primary.TButton',command=self.v47_math_knowledge_map_lab).pack(anchor='w',padx=18,pady=(0,14))



















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
    # ==================== v3.0 MCS: MATHEMATICS FOR COMPUTER SCIENCE ====================
    def mcs_center(self):
        self.clear(); self.header('MCS • Mathematics for Computer Science',
            'v3.0 • Proof & Logic → Sets/Relations → Induction → State Machines → Graphs/Number Theory → Counting → Probability → Recurrences')
        b=self.scrollbody()
        self.card(b,'SOURCE & PURPOSE',
            'โมดูลนี้จัดโครงสร้างจาก Mathematics for Computer Science (2018): ใช้แบบจำลองและวิธีทางคณิตศาสตร์เพื่อวิเคราะห์ปัญหาใน Computer Science '
            'และเชื่อมแนวคิดเข้ากับ Algorithm, AI, Robot และ TC Code Lab เดิมของโปรแกรม')
        topics=[
            ('01 Proof & Logic','Propositions • Predicates • Implication • Contradiction • Logical formulas • SAT',self.mcs_logic),
            ('02 Sets & Relations','Sets • Sequences • Functions • Binary Relations • Finite Cardinality',self.mcs_sets),
            ('03 Induction','Ordinary Induction • Strong Induction • Well Ordering',self.mcs_induction),
            ('04 State Machines','States • Transitions • Invariants • Correctness & Termination',self.mcs_state_machine),
            ('05 Graphs & Number Theory','Graph/network reasoning • GCD • modular arithmetic • CS connections',self.mcs_graph_number),
            ('06 Counting','Counting rules • combinations • inclusion-exclusion • generating-function connection',self.mcs_counting),
            ('07 Probability','Events • conditional probability • random variables • expectation • variance • random walks',self.mcs_probability),
            ('08 Recurrences','Towers of Hanoi • Merge Sort • linear and divide-and-conquer recurrences',self.mcs_recurrence)
        ]
        launch=self.card(b,'v3.1 • MCS ANIMATION → ROBOT PIPELINE',
            'Logic/Truth Table → Graph → Probability → State/Decision → Robot Simulation  •  เนื้อหา MCS ถูกเปลี่ยนจากสูตรเป็นภาพเคลื่อนไหวและการตัดสินใจของหุ่นยนต์')
        ttk.Button(launch,text='▶ เปิด MCS Animation & Robot Lab',style='Primary.TButton',command=self.mcs_animation_lab).pack(anchor='w',padx=18,pady=(0,14))
        for i,(title,desc,cmd) in enumerate(topics):
            c=self.card(b,title,desc)
            tk.Label(c,text=f'Progress {self.mcs_progress[str(i+1)]}%',bg='white',fg=MUTED).pack(anchor='w',padx=18)
            ttk.Button(c,text='เปิด Interactive Lab →',command=cmd).pack(anchor='e',padx=18,pady=(0,12))

    def _mcs_done(self,n):
        self.mcs_progress[str(n)]=100

    def _mcs_shell(self,title,sub,learn):
        self.clear(); self.header(title,sub); b=self.scrollbody(); self.card(b,'LEARN',learn); return b

    def mcs_logic(self):
        b=self._mcs_shell('MCS 01 • Proof & Logic','Propositions → Logical Formulas → Computer Programs',
            'Proposition คือข้อความที่มีค่าความจริง True/False การสร้างสูตรตรรกะใช้ NOT, AND, OR และ implication; '
            'แนวคิดนี้เชื่อมโดยตรงกับเงื่อนไข IF/ELSE และการตรวจความถูกต้องของโปรแกรม')
        c=self.card(b,'INTERACTIVE • Truth Table','กำหนด P และ Q แล้วดู NOT P, P AND Q, P OR Q และ P → Q')
        p=tk.BooleanVar(value=True); q=tk.BooleanVar(value=False); out=tk.StringVar()
        row=tk.Frame(c,bg='white'); row.pack(anchor='w',padx=18,pady=8)
        ttk.Checkbutton(row,text='P',variable=p).pack(side='left',padx=8); ttk.Checkbutton(row,text='Q',variable=q).pack(side='left',padx=8)
        def calc():
            P,Q=p.get(),q.get(); out.set(f'P={P}  Q={Q}\nNOT P={not P}\nP AND Q={P and Q}\nP OR Q={P or Q}\nP → Q={(not P) or Q}'); self._mcs_done(1)
        tk.Label(c,textvariable=out,bg='white',fg=BLUE,font=('Consolas',12),justify='left').pack(anchor='w',padx=18,pady=8)
        ttk.Button(c,text='Evaluate Logic',command=calc).pack(anchor='w',padx=18,pady=(0,12)); calc()
        self.card(b,'CONNECT TO AI / ROBOT','Sensor condition → Boolean proposition → IF/ELSE decision → Robot action. ใช้หลักเดียวกับ threshold ในบท Coding & Algorithm')

    def mcs_sets(self):
        b=self._mcs_shell('MCS 02 • Sets & Relations','Mathematical Data Types for Computer Science',
            'Sets, sequences, functions และ binary relations เป็นโครงสร้างพื้นฐานที่ใช้แทนข้อมูล ความสัมพันธ์ และ mapping ในระบบคอมพิวเตอร์')
        c=self.card(b,'INTERACTIVE • Set Operations','ใส่สมาชิกเป็นตัวเลขหรือคำ คั่นด้วย comma')
        ea=ttk.Entry(c); eb=ttk.Entry(c); ea.insert(0,'1,2,3,4'); eb.insert(0,'3,4,5'); ea.pack(fill='x',padx=18,pady=4); eb.pack(fill='x',padx=18,pady=4)
        out=tk.StringVar(); tk.Label(c,textvariable=out,bg='white',fg=TEXT,font=('Consolas',11),justify='left').pack(anchor='w',padx=18,pady=8)
        def calc():
            A={x.strip() for x in ea.get().split(',') if x.strip()}; B={x.strip() for x in eb.get().split(',') if x.strip()}
            out.set(f'A ∪ B = {sorted(A|B)}\nA ∩ B = {sorted(A&B)}\nA - B = {sorted(A-B)}\nA ⊆ B = {A<=B}'); self._mcs_done(2)
        ttk.Button(c,text='Calculate Sets',command=calc).pack(anchor='w',padx=18,pady=12); calc()
        self.card(b,'CS CONNECTION','Set ใช้แทนกลุ่มข้อมูล; relation ใช้แทนความสัมพันธ์ระหว่างสมาชิก เช่น user→permission, node→edge และข้อมูลเชิงสัมพันธ์')

    def mcs_induction(self):
        b=self._mcs_shell('MCS 03 • Induction','Ordinary / Strong Induction / Well Ordering',
            'Induction ใช้พิสูจน์ข้อความที่เกี่ยวกับจำนวนเต็มและโครงสร้างแบบ recursive: base case → induction hypothesis → induction step')
        c=self.card(b,'INTERACTIVE • Sum 1..n','ตรวจตัวอย่างสูตร 1+2+...+n = n(n+1)/2')
        n=tk.IntVar(value=8); ttk.Spinbox(c,from_=1,to=100,textvariable=n,width=8).pack(anchor='w',padx=18,pady=8); out=tk.StringVar()
        def calc():
            N=n.get(); direct=sum(range(1,N+1)); formula=N*(N+1)//2; out.set(f'n={N} | direct={direct} | formula={formula} | match={direct==formula}'); self._mcs_done(3)
        tk.Label(c,textvariable=out,bg='white',fg=BLUE,font=('Consolas',11)).pack(anchor='w',padx=18); ttk.Button(c,text='Verify Example',command=calc).pack(anchor='w',padx=18,pady=12); calc()
        self.card(b,'PROOF MAP','Base case: n=1 • Assume true for n=k • Show true for n=k+1. โปรแกรมใช้ตัวอย่างนี้เพื่อช่วยมองโครงสร้าง proof ไม่ใช่แทนการพิสูจน์ทั่วไป')

    def mcs_state_machine(self):
        b=self._mcs_shell('MCS 04 • State Machines','States → Transitions → Invariant → Correctness',
            'State machine อธิบายระบบด้วยสถานะและ transition ซึ่งเชื่อมโดยตรงกับ Robot/Agent: Sense → state → rule → next state/action')
        c=self.card(b,'INTERACTIVE • Robot State Machine','ปรับ sensor แล้วให้ state machine เปลี่ยน SAFE / CAUTION / DANGER')
        v=tk.IntVar(value=30); out=tk.StringVar()
        ttk.Scale(c,from_=0,to=100,variable=v).pack(fill='x',padx=18,pady=8)
        def run():
            x=v.get(); state='DANGER' if x>=70 else ('CAUTION' if x>=45 else 'SAFE'); action={'SAFE':'FORWARD','CAUTION':'SLOW','DANGER':'STOP'}[state]
            out.set(f'sensor={x} → state={state} → action={action}'); self._mcs_done(4)
        tk.Label(c,textvariable=out,bg='white',fg=BLUE,font=('Consolas',12)).pack(anchor='w',padx=18); ttk.Button(c,text='Run Transition',command=run).pack(anchor='w',padx=18,pady=12); run()
        self.card(b,'INVARIANT IDEA','Invariant คือคุณสมบัติที่ต้องคงจริงระหว่าง transitions ใช้ช่วยให้เหตุผลเกี่ยวกับ correctness ของระบบ')

    def mcs_graph_number(self):
        b=self._mcs_shell('MCS 05 • Graphs & Number Theory','Networks + arithmetic structure for computing',
            'Graph ใช้แทน vertices/nodes และ edges/connections; number theory สนใจ divisibility, primes, GCD และ modular arithmetic ซึ่งมีบทบาทใน algorithms และ cryptography')
        c=self.card(b,'INTERACTIVE • GCD / Modular Arithmetic')
        row=tk.Frame(c,bg='white'); row.pack(anchor='w',padx=18,pady=8); a=tk.IntVar(value=84); d=tk.IntVar(value=30)
        ttk.Entry(row,textvariable=a,width=10).pack(side='left',padx=4); ttk.Entry(row,textvariable=d,width=10).pack(side='left',padx=4); out=tk.StringVar()
        def calc():
            A,D=a.get(),d.get(); out.set(f'gcd({A},{D}) = {math.gcd(A,D)}   |   {A} mod {D} = {A%D if D else "undefined"}'); self._mcs_done(5)
        tk.Label(c,textvariable=out,bg='white',fg=BLUE,font=('Consolas',11)).pack(anchor='w',padx=18); ttk.Button(c,text='Calculate',command=calc).pack(anchor='w',padx=18,pady=12); calc()
        self.card(b,'GRAPH CONNECTION','Network, search tree, robot path และ random walk สามารถอธิบายด้วย node + edge และนำไปต่อยอดเป็น graph algorithms')

    def mcs_counting(self):
        b=self._mcs_shell('MCS 06 • Counting','Counting rules → combinations → inclusion-exclusion',
            'Combinatorics ใช้นับจำนวนความเป็นไปได้อย่างเป็นระบบ และเป็นพื้นฐานของการวิเคราะห์ algorithms และ probability')
        c=self.card(b,'INTERACTIVE • Permutation / Combination')
        row=tk.Frame(c,bg='white'); row.pack(anchor='w',padx=18,pady=8); n=tk.IntVar(value=8); r=tk.IntVar(value=3)
        ttk.Spinbox(row,from_=0,to=50,textvariable=n,width=7).pack(side='left',padx=4); ttk.Spinbox(row,from_=0,to=50,textvariable=r,width=7).pack(side='left',padx=4); out=tk.StringVar()
        def calc():
            N,R=n.get(),r.get()
            if 0<=R<=N:
                perm=math.factorial(N)//math.factorial(N-R); comb=math.comb(N,R); out.set(f'P({N},{R})={perm}   C({N},{R})={comb}'); self._mcs_done(6)
            else: out.set('ต้องมี 0 ≤ r ≤ n')
        tk.Label(c,textvariable=out,bg='white',fg=BLUE,font=('Consolas',11)).pack(anchor='w',padx=18); ttk.Button(c,text='Count',command=calc).pack(anchor='w',padx=18,pady=12); calc()

    def mcs_probability(self):
        b=self._mcs_shell('MCS 07 • Probability','Events → Conditional Probability → Random Variables → Expectation/Variance',
            'Probability space อธิบายเหตุการณ์และความไม่แน่นอน; conditional probability, expectation และ variance เชื่อมกับการประเมินข้อมูลและ AI')
        c=self.card(b,'INTERACTIVE • Dice Experiment','จำลองการทอยลูกเต๋าและเปรียบเทียบ empirical probability กับแนวคิด probability')
        trials=tk.IntVar(value=1000); out=tk.StringVar()
        ttk.Spinbox(c,from_=10,to=100000,increment=10,textvariable=trials,width=12).pack(anchor='w',padx=18,pady=8)
        def run():
            N=trials.get(); vals=[random.randint(1,6) for _ in range(N)]; six=sum(x==6 for x in vals); mu=statistics.mean(vals); var=statistics.pvariance(vals)
            out.set(f'P̂(6)={six/N:.4f} | mean={mu:.4f} | variance={var:.4f} | trials={N}'); self._mcs_done(7)
        tk.Label(c,textvariable=out,bg='white',fg=BLUE,font=('Consolas',11)).pack(anchor='w',padx=18); ttk.Button(c,text='Run Simulation',command=run).pack(anchor='w',padx=18,pady=12); run()
        self.card(b,'AI CONNECTION','Probability ช่วยอธิบาย uncertainty; expectation/variance เชื่อมกับ data analysis และ model evaluation โดยต้องแยก probability จาก confidence ให้ชัดเจน')

    def mcs_recurrence(self):
        b=self._mcs_shell('MCS 08 • Recurrences','Towers of Hanoi → Merge Sort → Divide-and-Conquer',
            'Recurrence นิยามค่าปัจจุบันจากค่าก่อนหน้า และใช้วิเคราะห์ recursive algorithms เช่น Towers of Hanoi และ Merge Sort')
        c=self.card(b,'INTERACTIVE • Towers of Hanoi','จำนวน move ขั้นต่ำเป็น recurrence T(n)=2T(n-1)+1')
        n=tk.IntVar(value=5); out=tk.StringVar(); ttk.Spinbox(c,from_=1,to=20,textvariable=n,width=8).pack(anchor='w',padx=18,pady=8)
        def calc():
            N=n.get(); moves=2**N-1; out.set(f'T({N}) = 2^{N} - 1 = {moves} moves'); self._mcs_done(8)
        tk.Label(c,textvariable=out,bg='white',fg=BLUE,font=('Consolas',11)).pack(anchor='w',padx=18); ttk.Button(c,text='Calculate Recurrence',command=calc).pack(anchor='w',padx=18,pady=12); calc()
        self.card(b,'ALGORITHM CONNECTION','Merge Sort ใช้ divide-and-conquer recurrence; ใช้เชื่อมกลับไปยัง TC sorting code และการวิเคราะห์ขั้นตอนวิธี')


    # ==================== v3.1 MCS ANIMATION + ROBOT INTEGRATION ====================
    def mcs_animation_lab(self):
        self.clear()
        self.header('▶ MCS Animation & Robot Lab',
            'mcs.pdf → Logic / Truth → Graph → Probability → Decision → Simulated Robot')
        body=self.scrollbody()
        self.card(body,'MCS → COMPUTATION → ROBOT',
            'ห้องทดลองนี้เชื่อม Mathematics for Computer Science เข้ากับ AI Learning Studio โดยให้ผู้เรียนเห็น “เหตุผล” ก่อน “การกระทำ”: '
            'Boolean logic สร้างเงื่อนไข, graph สร้างเส้นทาง, probability แทนความไม่แน่นอน และ state/decision rule เปลี่ยนผลคำนวณเป็นการเคลื่อนที่ของหุ่นยนต์จำลอง')

        nb=ttk.Notebook(body); nb.pack(fill='both',expand=True,padx=28,pady=12)
        f1=tk.Frame(nb,bg='white'); f2=tk.Frame(nb,bg='white'); f3=tk.Frame(nb,bg='white'); f4=tk.Frame(nb,bg='white')
        nb.add(f1,text='1 Logic / Truth'); nb.add(f2,text='2 Graph'); nb.add(f3,text='3 Probability'); nb.add(f4,text='4 Robot Integration')
        self._anim_logic_tab(f1)
        self._anim_graph_tab(f2)
        self._anim_probability_tab(f3)
        self._anim_robot_tab(f4)

    def _anim_logic_tab(self,parent):
        tk.Label(parent,text='PROPOSITION → TRUTH TABLE → LOGIC GATE → DECISION',
                 bg='white',fg=TEXT,font=('Segoe UI Semibold',13)).pack(anchor='w',padx=18,pady=(16,4))
        tk.Label(parent,text='MCS: logical formulas and implication. เปลี่ยน P,Q เป็นสัญญาณที่ไหลผ่าน AND / OR / NOT / implication',
                 bg='white',fg=MUTED).pack(anchor='w',padx=18)
        top=tk.Frame(parent,bg='white'); top.pack(fill='x',padx=18,pady=8)
        p=tk.BooleanVar(value=True); q=tk.BooleanVar(value=False); gate=tk.StringVar(value='AND')
        ttk.Checkbutton(top,text='P',variable=p).pack(side='left',padx=5)
        ttk.Checkbutton(top,text='Q',variable=q).pack(side='left',padx=5)
        ttk.Combobox(top,textvariable=gate,values=['AND','OR','XOR','IMPLIES'],state='readonly',width=12).pack(side='left',padx=8)
        cv=tk.Canvas(parent,height=330,bg='#f7fbfd',highlightthickness=1,highlightbackground=BORDER); cv.pack(fill='x',padx=18,pady=8)
        status=tk.StringVar(); tk.Label(parent,textvariable=status,bg='white',fg=BLUE,font=('Consolas',11)).pack(anchor='w',padx=18)
        def result():
            P,Q=p.get(),q.get(); g=gate.get()
            return (P and Q) if g=='AND' else ((P or Q) if g=='OR' else ((P != Q) if g=='XOR' else ((not P) or Q)))
        def draw(stage=0):
            cv.delete('all'); P,Q=p.get(),q.get(); R=result()
            cv.create_text(20,20,anchor='w',text=f'P={P}     Q={Q}     Gate={gate.get()}',font=('Segoe UI Semibold',12),fill=TEXT)
            cv.create_oval(60,95,100,135,fill='#8bd3f7' if P else '#d7dee7',outline=''); cv.create_text(80,115,text='P')
            cv.create_oval(60,205,100,245,fill='#8bd3f7' if Q else '#d7dee7',outline=''); cv.create_text(80,225,text='Q')
            cv.create_line(100,115,250,150,width=4,fill='#20a4d8' if stage>=1 else '#cbd5e1')
            cv.create_line(100,225,250,180,width=4,fill='#20a4d8' if stage>=2 else '#cbd5e1')
            cv.create_rectangle(250,125,385,205,fill='#ffffff',outline='#20a4d8',width=2)
            cv.create_text(317,165,text=gate.get(),font=('Segoe UI Black',18),fill=TEXT)
            cv.create_line(385,165,500,165,width=5,fill=GREEN if stage>=3 and R else (ORANGE if stage>=3 else '#cbd5e1'))
            cv.create_oval(500,140,550,190,fill=GREEN if R else ORANGE,outline='')
            cv.create_text(525,165,text='TRUE' if R else 'FALSE',fill='white',font=('Segoe UI Bold',9))
            rows=[(False,False),(False,True),(True,False),(True,True)]
            y=270
            table='   P      Q      RESULT\n' + '\n'.join(f'{str(a):5}  {str(b):5}  {str(((a and b) if gate.get()=="AND" else ((a or b) if gate.get()=="OR" else ((a!=b) if gate.get()=="XOR" else ((not a) or b))))):5}' for a,b in rows)
            cv.create_text(610,y,anchor='center',text=table,font=('Consolas',10),fill=TEXT)
            status.set(f'Logic result = {R} → Robot permission = {"MOVE" if R else "STOP"}')
            self.mcs_robot_rule['logic']=R
        def animate():
            for i,delay in enumerate((0,350,700,1050)):
                self.after(delay,lambda k=i: draw(k))
            self._mcs_done(1)
        ttk.Button(parent,text='▶ Animate Truth / Logic',style='Primary.TButton',command=animate).pack(anchor='w',padx=18,pady=10)
        gate.trace_add('write',lambda *_:draw(0)); p.trace_add('write',lambda *_:draw(0)); q.trace_add('write',lambda *_:draw(0)); draw()

    def _anim_graph_tab(self,parent):
        tk.Label(parent,text='GRAPH → PATH → ROBOT ROUTE',bg='white',fg=TEXT,font=('Segoe UI Semibold',13)).pack(anchor='w',padx=18,pady=(16,4))
        tk.Label(parent,text='MCS graph concepts: vertices, edges, walks/paths and connectivity. จุดแต่ละจุดคือ vertex และเส้นคือ edge',
                 bg='white',fg=MUTED).pack(anchor='w',padx=18)
        cv=tk.Canvas(parent,height=420,bg='#f7fbfd',highlightthickness=1,highlightbackground=BORDER); cv.pack(fill='x',padx=18,pady=8)
        nodes={'A':(100,210),'B':(250,90),'C':(250,330),'D':(430,110),'E':(430,310),'F':(620,210)}
        edges=[('A','B'),('A','C'),('B','D'),('B','E'),('C','E'),('D','F'),('E','F')]
        path=['A','B','D','F']; token=[None]
        def base(high=-1):
            cv.delete('all')
            for i,(u,v) in enumerate(edges):
                x1,y1=nodes[u]; x2,y2=nodes[v]
                on=i<=high and (u,v) in list(zip(path,path[1:]))
                cv.create_line(x1,y1,x2,y2,width=5 if on else 2,fill=GREEN if on else '#a9b8c8')
            for n,(x,y) in nodes.items():
                cv.create_oval(x-24,y-24,x+24,y+24,fill='#20a4d8',outline='')
                cv.create_text(x,y,text=n,fill='white',font=('Segoe UI Bold',12))
            cv.create_text(20,25,anchor='w',text='Path A → B → D → F',font=('Segoe UI Semibold',12),fill=TEXT)
        def animate():
            base(-1)
            for i in range(len(path)):
                def step(k=i):
                    base(k-1)
                    x,y=nodes[path[k]]
                    cv.create_oval(x-12,y-12,x+12,y+12,fill=ORANGE,outline='',tags='robot')
                    cv.create_text(x,y-40,text=f'Robot @ {path[k]}',fill=ORANGE,font=('Segoe UI Bold',9))
                self.after(i*650,step)
            self.mcs_robot_rule['graph_path']=path[:]; self._mcs_done(5)
        ttk.Button(parent,text='▶ Animate Graph Path',style='Primary.TButton',command=animate).pack(anchor='w',padx=18,pady=10)
        base()

    def _anim_probability_tab(self,parent):
        tk.Label(parent,text='PROBABILITY → RANDOM EXPERIMENT → RISK DECISION',bg='white',fg=TEXT,font=('Segoe UI Semibold',13)).pack(anchor='w',padx=18,pady=(16,4))
        tk.Label(parent,text='MCS probability: sample space, events, random variables, expectation/variance and random walks. '
                             'ตัวอย่างนี้ให้ความถี่สะสมเคลื่อนไหวเข้าใกล้ probability ของเหตุการณ์',
                 bg='white',fg=MUTED,wraplength=1000,justify='left').pack(anchor='w',padx=18)
        ctl=tk.Frame(parent,bg='white'); ctl.pack(fill='x',padx=18,pady=8)
        trials=tk.IntVar(value=120); threshold=tk.DoubleVar(value=.55)
        ttk.Label(ctl,text='Trials').pack(side='left'); ttk.Spinbox(ctl,from_=20,to=1000,increment=20,textvariable=trials,width=8).pack(side='left',padx=6)
        ttk.Label(ctl,text='Robot risk threshold').pack(side='left',padx=(20,2)); ttk.Entry(ctl,textvariable=threshold,width=8).pack(side='left')
        cv=tk.Canvas(parent,height=360,bg='#f7fbfd',highlightthickness=1,highlightbackground=BORDER); cv.pack(fill='x',padx=18,pady=8)
        status=tk.StringVar(); tk.Label(parent,textvariable=status,bg='white',fg=BLUE,font=('Consolas',11)).pack(anchor='w',padx=18)
        state={'i':0,'hit':0}
        def axes():
            cv.delete('all'); cv.create_line(55,300,760,300,fill='#64748b'); cv.create_line(55,40,55,300,fill='#64748b')
            cv.create_line(55,170,760,170,fill='#cbd5e1',dash=(4,4)); cv.create_text(765,170,text='0.5',anchor='w',fill=MUTED)
            cv.create_text(60,25,text='Empirical P(die ≥ 4)',anchor='w',fill=TEXT,font=('Segoe UI Semibold',11))
        def run():
            axes(); state['i']=0; state['hit']=0; pts=[]
            N=max(20,int(trials.get()))
            def tick():
                batch=max(1,N//80)
                for _ in range(batch):
                    if state['i']>=N: break
                    state['i']+=1
                    if random.randint(1,6)>=4: state['hit']+=1
                    prob=state['hit']/state['i']
                    x=55+705*state['i']/N; y=300-250*prob
                    pts.append((x,y))
                    if len(pts)>1: cv.create_line(*pts[-2],*pts[-1],fill=BLUE,width=2)
                prob=state['hit']/state['i']; th=float(threshold.get())
                action='STOP / REPLAN' if prob>=th else 'MOVE'
                status.set(f'trial={state["i"]}/{N}   P̂(event)={prob:.3f}   threshold={th:.2f}   → Robot {action}')
                self.mcs_robot_rule['last_probability']=prob; self.mcs_robot_rule['probability_threshold']=th
                if state['i']<N: self.after(35,tick)
                else: self._mcs_done(7)
            tick()
        ttk.Button(parent,text='▶ Run Probability Animation',style='Primary.TButton',command=run).pack(anchor='w',padx=18,pady=10)
        axes()

    def _anim_robot_tab(self,parent):
        tk.Label(parent,text='INTEGRATED ROBOT: LOGIC + GRAPH + PROBABILITY',bg='white',fg=TEXT,font=('Segoe UI Semibold',13)).pack(anchor='w',padx=18,pady=(16,4))
        tk.Label(parent,text='Robot จะเดินตาม graph path เมื่อ Logic=True และ probability risk ต่ำกว่า threshold; ถ้าเงื่อนไขไม่ผ่านจะหยุด/วางแผนใหม่',
                 bg='white',fg=MUTED).pack(anchor='w',padx=18)
        cv=tk.Canvas(parent,height=430,bg='#eef5f8',highlightthickness=1,highlightbackground=BORDER); cv.pack(fill='x',padx=18,pady=8)
        log=tk.Text(parent,height=7,font=('Consolas',10)); log.pack(fill='x',padx=18,pady=5)
        nodes={'A':(100,215),'B':(270,90),'D':(470,110),'F':(680,215)}
        def world(robot_node='A',msg='READY'):
            cv.delete('all')
            seq=['A','B','D','F']
            for u,v in zip(seq,seq[1:]):
                cv.create_line(*nodes[u],*nodes[v],fill='#9fb3c8',width=5)
            for n,(x,y) in nodes.items():
                cv.create_oval(x-22,y-22,x+22,y+22,fill='#dbeafe',outline=BLUE,width=2); cv.create_text(x,y,text=n,fill=TEXT)
            x,y=nodes[robot_node]
            cv.create_rectangle(x-25,y-18,x+25,y+18,fill=BLUE,outline='')
            cv.create_oval(x-22,y+14,x-10,y+26,fill=TEXT,outline=''); cv.create_oval(x+10,y+14,x+22,y+26,fill=TEXT,outline='')
            cv.create_text(25,30,anchor='w',text=msg,font=('Segoe UI Semibold',12),fill=ORANGE if 'STOP' in msg else GREEN)
        def run():
            log.delete('1.0','end')
            logic=bool(self.mcs_robot_rule.get('logic',True))
            prob=float(self.mcs_robot_rule.get('last_probability',0.0))
            th=float(self.mcs_robot_rule.get('probability_threshold',.55))
            path=self.mcs_robot_rule.get('graph_path',['A','B','D','F'])
            log.insert('end',f'LOGIC      permission={logic}\nGRAPH      path={" → ".join(path)}\nPROBABILITY risk={prob:.3f}, threshold={th:.3f}\n')
            if not logic:
                world(path[0],'STOP: LOGIC FALSE'); log.insert('end','DECISION   STOP because Boolean condition is false\n'); return
            if prob>=th:
                world(path[0],'STOP / REPLAN: RISK HIGH'); log.insert('end','DECISION   STOP/REPLAN because estimated risk reached threshold\n'); return
            log.insert('end','DECISION   MOVE: logic true and risk below threshold\n')
            for i,n in enumerate(path):
                def step(k=i,node=n):
                    world(node,f'MOVE {k+1}/{len(path)} • {node}')
                    log.insert('end',f'ACT        robot moved to {node}\n'); log.see('end')
                self.after(i*700,step)
            self.done(6,100)
        ttk.Button(parent,text='▶ RUN MCS → ROBOT',style='Primary.TButton',command=run).pack(anchor='w',padx=18,pady=10)
        world()



    # ==================== V3: STUDENT EQUATION -> SYMBOLIC MATH -> ANIMATION ====================
    def _safe_student_expr(self, text):
        """Restricted math parser for student-entered expressions; no Python builtins."""
        if sp is None:
            raise ValueError('ต้องติดตั้ง SymPy')
        text=(text or '').strip().replace('^','**').replace('×','*').replace('÷','/')
        if len(text)>240:
            raise ValueError('สมการยาวเกินไป')
        if not re.fullmatch(r"[0-9A-Za-z_+\-*/().,= <>\s]*", text):
            raise ValueError('พบอักขระที่ไม่รองรับ')
        bad={'__','import','exec','eval','open','os','sys','subprocess','lambda','globals','locals','class'}
        low=text.lower()
        if any(x in low for x in bad):
            raise ValueError('รูปแบบนี้ไม่อนุญาต')
        allowed_names={'x','y','z','t','a','b','c','n','pi','e','sin','cos','tan','sqrt','exp','log','abs'}
        words=set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", text))
        unknown=words-allowed_names
        if unknown:
            raise ValueError('ตัวแปร/ฟังก์ชันที่ยังไม่รองรับ: '+', '.join(sorted(unknown)))
        local={k:sp.Symbol(k, real=True) for k in ['x','y','z','t','a','b','c','n']}
        local.update({'pi':sp.pi,'e':sp.E,'sin':sp.sin,'cos':sp.cos,'tan':sp.tan,
                      'sqrt':sp.sqrt,'exp':sp.exp,'log':sp.log,'abs':sp.Abs})
        trans=standard_transformations+(implicit_multiplication_application,convert_xor)
        def one(part):
            return parse_expr(part.strip(),local_dict=local,global_dict={
                'Integer':sp.Integer,'Float':sp.Float,'Rational':sp.Rational,
                'Symbol':sp.Symbol,'Function':sp.Function
            },transformations=trans,evaluate=True)
        if '=' in text:
            if text.count('=')!=1: raise ValueError('รองรับเครื่องหมาย = หนึ่งตำแหน่ง')
            l,r=text.split('=',1); return sp.Eq(one(l),one(r)),local
        return one(text),local

    def ai_equation_animation_lab(self):
        self.clear()
        self.header('∫ AI Equation → Animation Lab',
            'นักเรียนพิมพ์สูตร/สมการเอง → Symbolic Math → Explain → Solve/Transform → Graph → Animation → Experiment')
        b=self.scrollbody()
        self.card(b,'แนวคิด V3',
            'เริ่มจาก Algebra + Function Graph ก่อน เพราะเป็นฐานของ Calculus, Probability, MCS และ Robot ต่อไป '
            'ระบบใช้ SymPy เป็น symbolic engine สำหรับคำนวณ/ตรวจผล ส่วนคำอธิบาย AI ในรุ่นนี้สร้างจากโครงสร้างคณิตศาสตร์ที่ตรวจได้ ไม่เดาคำตอบจากข้อความอย่างเดียว')

        c=self.card(b,'1 • ENTER EQUATION / FORMULA',
            'ตัวอย่าง: x^2 - 5*x + 6 = 0   |   y = sin(x)   |   x^3 - 4*x   |   sqrt(x^2+4)')
        row=tk.Frame(c,bg='white'); row.pack(fill='x',padx=18,pady=8)
        eq=tk.StringVar(value='x^2 - 5*x + 6 = 0')
        ttk.Entry(row,textvariable=eq,font=('Consolas',12)).pack(side='left',fill='x',expand=True)
        mode=tk.StringVar(value='Auto')
        ttk.Combobox(row,textvariable=mode,values=['Auto','Solve','Factor','Expand','Simplify','Differentiate','Integrate'],
                     state='readonly',width=15).pack(side='left',padx=8)
        var=tk.StringVar(value='x')
        ttk.Combobox(row,textvariable=var,values=['x','y','z','t'],state='readonly',width=5).pack(side='left')

        quick=tk.Frame(c,bg='white'); quick.pack(fill='x',padx=18,pady=(0,8))
        examples=['x^2 - 5*x + 6 = 0','y = sin(x)','x^3 - 4*x','(x+2)^2','exp(-x^2)','x^2 + y^2 = 25']
        for ex in examples:
            ttk.Button(quick,text=ex,command=lambda q=ex:eq.set(q)).pack(side='left',padx=3,pady=3)

        pane=tk.PanedWindow(b,orient='horizontal',sashwidth=5,bg=BG); pane.pack(fill='both',expand=True,padx=28,pady=8)
        left=tk.Frame(pane,bg='white',highlightbackground=BORDER,highlightthickness=1)
        right=tk.Frame(pane,bg='white',highlightbackground=BORDER,highlightthickness=1)
        pane.add(left,minsize=470); pane.add(right,minsize=620)

        tk.Label(left,text='2 • AI / SYMBOLIC EXPLANATION',bg='white',fg=TEXT,font=('Segoe UI Semibold',12)).pack(anchor='w',padx=14,pady=(14,5))
        explanation=tk.Text(left,height=21,font=('Consolas',10),wrap='word'); explanation.pack(fill='both',expand=True,padx=14,pady=6)
        stepvar=tk.IntVar(value=0)
        controls=tk.Frame(left,bg='white'); controls.pack(fill='x',padx=14,pady=8)
        prevb=ttk.Button(controls,text='◀ Previous'); prevb.pack(side='left')
        nextb=ttk.Button(controls,text='Next Step ▶',style='Primary.TButton'); nextb.pack(side='left',padx=6)
        playb=ttk.Button(controls,text='▶ Auto Animate'); playb.pack(side='left')
        resetb=ttk.Button(controls,text='↺ Reset'); resetb.pack(side='left',padx=6)

        tk.Label(right,text='3 • MATHEMATICAL ANIMATION',bg='white',fg=TEXT,font=('Segoe UI Semibold',12)).pack(anchor='w',padx=14,pady=(14,5))
        cv=tk.Canvas(right,height=500,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1)
        cv.pack(fill='both',expand=True,padx=14,pady=6)
        status=tk.StringVar(value='กด Analyze Equation เพื่อเริ่ม')
        tk.Label(right,textvariable=status,bg='white',fg=MUTED,font=('Segoe UI',9),wraplength=680,justify='left').pack(anchor='w',padx=14,pady=(0,10))

        state={'obj':None,'expr':None,'symbol':None,'steps':[],'index':0,'timer':None}

        def choose_expr(obj,sym):
            if isinstance(obj,sp.Equality):
                # y=f(x) graphs f(x); otherwise graph lhs-rhs and roots at y=0.
                if obj.lhs==sp.Symbol('y') and sym==sp.Symbol('x'): return obj.rhs
                if obj.rhs==sp.Symbol('y') and sym==sp.Symbol('x'): return obj.lhs
                return sp.simplify(obj.lhs-obj.rhs)
            return obj

        def build_steps(obj,sym,op):
            expr=choose_expr(obj,sym)
            steps=[('Original',obj,'อ่านโครงสร้างสมการ/นิพจน์ที่นักเรียนป้อน')]
            if isinstance(obj,sp.Equality):
                norm=sp.simplify(obj.lhs-obj.rhs)
                steps.append(('Normalize',sp.Eq(norm,0),'ย้ายทุกพจน์ให้อยู่ด้านเดียวเพื่อวิเคราะห์'))
            else:
                norm=expr
            target=op
            if op=='Auto':
                target='Solve' if isinstance(obj,sp.Equality) else 'Simplify'
            try:
                if target=='Solve':
                    ans=sp.solve(obj if isinstance(obj,sp.Equality) else sp.Eq(expr,0),sym)
                    fac=sp.factor(norm if isinstance(obj,sp.Equality) else expr)
                    if fac != (norm if isinstance(obj,sp.Equality) else expr):
                        steps.append(('Factor',fac,'แยกตัวประกอบเพื่อมองโครงสร้างและรากได้ง่ายขึ้น'))
                    steps.append(('Solve',ans,'หาค่าของตัวแปรที่ทำให้สมการเป็นจริง'))
                elif target=='Factor':
                    steps.append(('Factor',sp.factor(expr),'แยกตัวประกอบของนิพจน์'))
                elif target=='Expand':
                    steps.append(('Expand',sp.expand(expr),'กระจายวงเล็บและรวมโครงสร้างพหุนาม'))
                elif target=='Simplify':
                    steps.append(('Simplify',sp.simplify(expr),'ลดรูปโดยคงความหมายทางคณิตศาสตร์'))
                elif target=='Differentiate':
                    steps.append(('Differentiate',sp.diff(expr,sym),f'หาอนุพันธ์เทียบกับ {sym}'))
                elif target=='Integrate':
                    steps.append(('Integrate',sp.integrate(expr,sym),f'หาปริพันธ์ไม่จำกัดเขตเทียบกับ {sym}'))
            except Exception as e:
                steps.append(('Result','ไม่สามารถหาผลแบบปิดได้',str(e)))
            return expr,steps

        def draw_axes():
            cv.delete('all'); w=max(cv.winfo_width(),620); h=max(cv.winfo_height(),460)
            pad=48; cv.create_line(pad,h/2,w-pad,h/2,fill='#94a3b8'); cv.create_line(w/2,pad,w/2,h-pad,fill='#94a3b8')
            for i in range(-5,6):
                x=w/2+i*(w-2*pad)/10; y=h/2-i*(h-2*pad)/10
                cv.create_line(x,h/2-4,x,h/2+4,fill='#94a3b8'); cv.create_text(x,h/2+14,text=str(i*2),fill=MUTED,font=('Segoe UI',8))
                cv.create_line(w/2-4,y,w/2+4,y,fill='#94a3b8'); 
                if i: cv.create_text(w/2-15,y,text=str(i*2),fill=MUTED,font=('Segoe UI',8))
            return w,h,pad

        def draw_graph(expr,progress=1.0):
            w,h,pad=draw_axes()
            sym=state['symbol']
            if sym is None or sym not in getattr(expr,'free_symbols',set()): return
            others=list(expr.free_symbols-{sym})
            subs={q:1 for q in others}
            try: fun=sp.lambdify(sym,expr.subs(subs),'math')
            except Exception:return
            pts=[]; N=320; upto=max(2,int(N*progress))
            for i in range(upto):
                xv=-10+20*i/(N-1)
                try:
                    yv=float(fun(xv))
                    if not math.isfinite(yv) or abs(yv)>20: 
                        if len(pts)>=4: cv.create_line(*pts,fill=BLUE,width=3,smooth=True)
                        pts=[]; continue
                    px=pad+(xv+10)/20*(w-2*pad); py=h-pad-(yv+10)/20*(h-2*pad)
                    pts += [px,py]
                except Exception:
                    pass
            if len(pts)>=4: cv.create_line(*pts,fill=BLUE,width=3,smooth=True)
            cv.create_text(pad,22,anchor='w',text=f'f({sym}) = {str(expr)[:70]}',fill=TEXT,font=('Segoe UI Semibold',11))

        def render_step(i,animate=False):
            if not state['steps']: return
            i=max(0,min(i,len(state['steps'])-1)); state['index']=i
            title,val,why=state['steps'][i]
            explanation.delete('1.0','end')
            explanation.insert('end',f'STEP {i+1}/{len(state["steps"])} — {title}\n\n')
            explanation.insert('end',f'{sp.pretty(val,use_unicode=True) if sp is not None else val}\n\n')
            explanation.insert('end',f'อธิบาย: {why}\n\n')
            explanation.insert('end','หลักการ: ผล symbolic ใช้สำหรับคำนวณ/ตรวจคำตอบ ส่วน animation ช่วยให้เห็นโครงสร้าง ไม่ใช้แทนการพิสูจน์เมื่อโจทย์ต้องการ proof')
            status.set(f'{title} • {why}')
            expr=state['expr']
            if animate and expr is not None:
                frames=24
                def frame(k=0):
                    if k>frames:return
                    draw_graph(expr,k/frames)
                    state['timer']=self.after(30,lambda:frame(k+1))
                frame()
            else:
                draw_graph(expr,1.0)

        def analyze():
            if sp is None:
                messagebox.showerror('SymPy','ต้องติดตั้ง SymPy ก่อน'); return
            try:
                obj,loc=self._safe_student_expr(eq.get())
                sym=loc[var.get()]
                expr,steps=build_steps(obj,sym,mode.get())
                state.update(obj=obj,expr=expr,symbol=sym,steps=steps,index=0)
                render_step(0,True)
            except Exception as e:
                explanation.delete('1.0','end'); explanation.insert('end','INPUT ERROR\n\n'+str(e))
                status.set('กรุณาตรวจรูปสมการ')

        def next_step():
            if state['steps']: render_step(min(state['index']+1,len(state['steps'])-1),True)
        def prev_step():
            if state['steps']: render_step(max(state['index']-1,0),False)
        def reset():
            if state.get('timer'):
                try:self.after_cancel(state['timer'])
                except Exception:pass
            state.update(steps=[],index=0,timer=None); explanation.delete('1.0','end'); draw_axes(); status.set('Reset แล้ว')
        def autoplay():
            if not state['steps']: analyze()
            def go(i=0):
                if i>=len(state['steps']): return
                render_step(i,True); self.after(950,lambda:go(i+1))
            go()

        action=self.card(b,'4 • EXPERIMENT & NEXT CONNECTION',
            'V3 เริ่มจากสมการ/ฟังก์ชันที่นักเรียนป้อนเอง จากนั้นรุ่นถัดไปจะต่อ Parameter Slider, Calculus, Probability Distribution, Matrix/Vector และ Equation → Robot Control')
        ttk.Button(action,text='Analyze Equation',style='Primary.TButton',command=analyze).pack(side='left',padx=18,pady=12)
        ttk.Button(action,text='Send concept → MCS Animation / Robot',command=self.mcs_animation_lab).pack(side='left',padx=4,pady=12)

        nextb.configure(command=next_step); prevb.configure(command=prev_step); playb.configure(command=autoplay); resetb.configure(command=reset)
        draw_axes()


    # ==================== V3.1: PARAMETER EXPERIMENT -> GRAPH -> CALCULUS -> ROBOT ====================
    def equation_experiment_lab(self):
        self.clear()
        self.header('↔ Equation Experiment Lab • V3.1',
            'Parameter Slider → Dynamic Graph → Roots / Derivative → Animation → Robot Mapping')
        b=self.scrollbody()
        self.card(b,'WHY THIS COMES NEXT',
            'หลังจาก V3 ให้นักเรียนพิมพ์สมการเอง รุ่น V3.1 ทำให้ “ทดลอง” ได้จริง: '
            'เปลี่ยนพารามิเตอร์แล้วเห็นกราฟ ราก จุดยอด ความชัน และคำสั่งหุ่นยนต์เปลี่ยนพร้อมกัน '
            'เริ่มจาก quadratic y = ax² + bx + c เพราะเชื่อม Algebra, Graph และ Calculus ได้ชัดเจน')

        c=self.card(b,'1 • LIVE EQUATION:  y = ax² + bx + c')
        vals={'a':tk.DoubleVar(value=1.0),'b':tk.DoubleVar(value=-2.0),'c':tk.DoubleVar(value=-3.0)}
        labels={}
        for name,lo,hi in [('a',-5,5),('b',-10,10),('c',-10,10)]:
            r=tk.Frame(c,bg='white'); r.pack(fill='x',padx=18,pady=4)
            tk.Label(r,text=name,width=3,bg='white',fg=TEXT,font=('Segoe UI Semibold',11)).pack(side='left')
            sc=ttk.Scale(r,from_=lo,to=hi,variable=vals[name]); sc.pack(side='left',fill='x',expand=True,padx=8)
            labels[name]=tk.Label(r,width=8,bg='white',fg=BLUE,font=('Consolas',10)); labels[name].pack(side='left')
        eqtext=tk.StringVar()
        tk.Label(c,textvariable=eqtext,bg='white',fg=TEXT,font=('Consolas',13)).pack(anchor='w',padx=18,pady=8)

        pane=tk.PanedWindow(b,orient='horizontal',sashwidth=5,bg=BG); pane.pack(fill='both',expand=True,padx=28,pady=8)
        left=tk.Frame(pane,bg='white',highlightbackground=BORDER,highlightthickness=1)
        right=tk.Frame(pane,bg='white',highlightbackground=BORDER,highlightthickness=1)
        pane.add(left,minsize=690); pane.add(right,minsize=390)
        cv=tk.Canvas(left,height=510,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1)
        cv.pack(fill='both',expand=True,padx=12,pady=12)

        tk.Label(right,text='LIVE MATHEMATICAL ANALYSIS',bg='white',fg=TEXT,font=('Segoe UI Semibold',12)).pack(anchor='w',padx=14,pady=(14,4))
        info=tk.Text(right,height=18,font=('Consolas',10),wrap='word'); info.pack(fill='both',expand=True,padx=14,pady=6)
        robot=tk.StringVar()
        tk.Label(right,text='ROBOT MAPPING',bg='white',fg=TEXT,font=('Segoe UI Semibold',11)).pack(anchor='w',padx=14,pady=(8,2))
        tk.Label(right,textvariable=robot,bg='white',fg=BLUE,font=('Consolas',10),justify='left',wraplength=360).pack(anchor='w',padx=14,pady=(0,8))

        controls=tk.Frame(right,bg='white'); controls.pack(fill='x',padx=14,pady=8)
        running={'job':None,'phase':0}

        def values():
            return vals['a'].get(),vals['b'].get(),vals['c'].get()

        def graph():
            a,bv,cc=values()
            for k,v in vals.items(): labels[k].config(text=f'{v.get():.2f}')
            eqtext.set(f'y = ({a:.2f})x² + ({bv:.2f})x + ({cc:.2f})')
            cv.delete('all'); w=max(cv.winfo_width(),650); h=max(cv.winfo_height(),480); pad=48
            x0=w/2; y0=h/2
            cv.create_line(pad,y0,w-pad,y0,fill='#94a3b8'); cv.create_line(x0,pad,x0,h-pad,fill='#94a3b8')
            for i in range(-5,6):
                px=x0+i*(w-2*pad)/10; py=y0-i*(h-2*pad)/10
                cv.create_line(px,y0-4,px,y0+4,fill='#94a3b8'); cv.create_line(x0-4,py,x0+4,py,fill='#94a3b8')
                if i: cv.create_text(px,y0+14,text=str(i*2),fill=MUTED,font=('Segoe UI',8))
            pts=[]
            for i in range(361):
                x=-10+20*i/360; y=a*x*x+bv*x+cc
                if abs(y)<=10:
                    px=pad+(x+10)/20*(w-2*pad); py=h-pad-(y+10)/20*(h-2*pad)
                    pts += [px,py]
                else:
                    if len(pts)>=4: cv.create_line(*pts,fill=BLUE,width=3,smooth=True)
                    pts=[]
            if len(pts)>=4: cv.create_line(*pts,fill=BLUE,width=3,smooth=True)

            disc=bv*bv-4*a*cc if abs(a)>1e-9 else None
            roots=[]
            vertex=None
            if abs(a)>1e-9:
                vx=-bv/(2*a); vy=a*vx*vx+bv*vx+cc; vertex=(vx,vy)
                if -10<=vx<=10 and -10<=vy<=10:
                    px=pad+(vx+10)/20*(w-2*pad); py=h-pad-(vy+10)/20*(h-2*pad)
                    cv.create_oval(px-6,py-6,px+6,py+6,fill=ORANGE,outline='')
                    cv.create_text(px+8,py-12,anchor='w',text=f'V({vx:.2f},{vy:.2f})',fill=ORANGE,font=('Segoe UI',9))
                if disc is not None and disc>=0:
                    r1=(-bv+math.sqrt(disc))/(2*a); r2=(-bv-math.sqrt(disc))/(2*a); roots=[r1,r2]
                    for rr in roots:
                        if -10<=rr<=10:
                            px=pad+(rr+10)/20*(w-2*pad)
                            cv.create_oval(px-5,y0-5,px+5,y0+5,fill=GREEN,outline='')
            derivative=f"y' = {2*a:.2f}x + {bv:.2f}"
            info.delete('1.0','end')
            info.insert('end',f'EQUATION\n  y = {a:.3f}x² + {bv:.3f}x + {cc:.3f}\n\n')
            if abs(a)>1e-9:
                info.insert('end',f'DISCRIMINANT\n  Δ = b² - 4ac = {disc:.4f}\n\n')
                info.insert('end',f'ROOTS\n  {", ".join(f"{r:.4f}" for r in roots) if roots else "ไม่มีรากจริง"}\n\n')
                info.insert('end',f'VERTEX\n  ({vertex[0]:.4f}, {vertex[1]:.4f})\n\n')
            else:
                info.insert('end','LINEAR CASE\n  a ≈ 0 จึงเปลี่ยนจาก quadratic เป็นเส้นตรง\n\n')
            info.insert('end',f'DERIVATIVE\n  {derivative}\n\n')
            slope=bv
            action='TURN RIGHT' if slope>1 else ('TURN LEFT' if slope<-1 else 'FORWARD')
            risk=min(1.0,abs(cc)/10)
            if risk>=0.75: action='STOP'
            robot.set(f'feature: slope at x=0 = {slope:.2f}\nrisk proxy = |c|/10 = {risk:.2f}\n→ simulated robot: {action}')
            self.mcs_robot_rule['last_probability']=risk
            return action

        def animate_parameter():
            if running['job']:
                try:self.after_cancel(running['job'])
                except Exception:pass
            running['phase']=0
            def tick():
                k=running['phase']; vals['b'].set(-8+16*(k%80)/79)
                graph(); running['phase']+=1
                if running['phase']<160: running['job']=self.after(55,tick)
                else: running['job']=None
            tick()

        def stop():
            if running['job']:
                try:self.after_cancel(running['job'])
                except Exception:pass
            running['job']=None

        def send_robot():
            action=graph()
            messagebox.showinfo('Equation → Robot',
                f'ส่งผลการทดลองเข้าสู่แนวคิด Robot Simulation แล้ว\n\nAction = {action}\n'
                'เปิด MCS Animation → Robot เพื่อทดลอง Logic/Graph/Probability ต่อได้')

        ttk.Button(controls,text='▶ Animate b',style='Primary.TButton',command=animate_parameter).pack(side='left')
        ttk.Button(controls,text='■ Stop',command=stop).pack(side='left',padx=5)
        ttk.Button(controls,text='Robot Mapping',command=send_robot).pack(side='left',padx=5)
        ttk.Button(right,text='เปิด MCS Animation → Robot',command=self.mcs_animation_lab).pack(anchor='w',padx=14,pady=8)

        for v in vals.values(): v.trace_add('write',lambda *_:graph())
        self.after(100,graph)

        c2=self.card(b,'2 • NEXT MATHEMATICAL LAYERS',
            'ลำดับต่อจาก V3.1: Trigonometry Parameter Lab → Calculus Tangent/Area Animation → Vector & Matrix Transform → '
            'Probability Distribution → Logic/Equation to Robot Control. ทุกส่วนจะเพิ่มบนฐานเดิมโดยไม่ลบเมนูที่มีอยู่')


    # ==================== V3.2: TRIGONOMETRY + CALCULUS VISUAL LAB ====================
    def trig_calculus_animation_lab(self):
        self.clear()
        self.header('∿ Trigonometry + Calculus Animation • V3.2',
            'Wave Parameters → Dynamic Graph → Derivative/Tangent → Integral Area → Animated Exploration')
        b=self.scrollbody()
        self.card(b,'LEARNING BRIDGE',
            'V3.2 ต่อจาก Algebra/Quadratic ไปสู่ Trigonometry และ Calculus: นักเรียนเปลี่ยน amplitude, frequency, phase '
            'แล้วเห็นกราฟและอนุพันธ์เปลี่ยนทันที จากนั้นเลื่อนจุด x₀ เพื่อดูเส้นสัมผัส และช่วง [L,R] เพื่อดูพื้นที่ปริพันธ์')

        c=self.card(b,'1 • TRIGONOMETRY EXPERIMENT  y = A sin(Bx + C)')
        A=tk.DoubleVar(value=2.0); B=tk.DoubleVar(value=1.0); C=tk.DoubleVar(value=0.0)
        x0=tk.DoubleVar(value=0.5); L=tk.DoubleVar(value=-2.0); R=tk.DoubleVar(value=2.0)
        vars_=[('A amplitude',A,0.2,5.0),('B frequency',B,0.2,4.0),('C phase',C,-3.14,3.14),
               ('x₀ tangent',x0,-6.0,6.0),('L integral',L,-6.0,6.0),('R integral',R,-6.0,6.0)]
        val_labels=[]
        for title,varr,lo,hi in vars_:
            row=tk.Frame(c,bg='white'); row.pack(fill='x',padx=18,pady=3)
            tk.Label(row,text=title,width=14,anchor='w',bg='white',fg=TEXT,font=('Segoe UI',10)).pack(side='left')
            ttk.Scale(row,from_=lo,to=hi,variable=varr).pack(side='left',fill='x',expand=True,padx=8)
            lab=tk.Label(row,width=8,bg='white',fg=BLUE,font=('Consolas',9)); lab.pack(side='left')
            val_labels.append((varr,lab))

        pane=tk.PanedWindow(b,orient='horizontal',sashwidth=5,bg=BG); pane.pack(fill='both',expand=True,padx=28,pady=8)
        left=tk.Frame(pane,bg='white',highlightbackground=BORDER,highlightthickness=1)
        right=tk.Frame(pane,bg='white',highlightbackground=BORDER,highlightthickness=1)
        pane.add(left,minsize=700); pane.add(right,minsize=390)
        cv=tk.Canvas(left,height=520,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1)
        cv.pack(fill='both',expand=True,padx=12,pady=12)
        info=tk.Text(right,height=22,font=('Consolas',10),wrap='word'); info.pack(fill='both',expand=True,padx=14,pady=14)
        status=tk.StringVar(value='พร้อมทดลอง')
        tk.Label(right,textvariable=status,bg='white',fg=MUTED,font=('Segoe UI',9),wraplength=360,justify='left').pack(anchor='w',padx=14,pady=(0,8))
        run={'job':None,'k':0}

        def calc():
            aa,bb,cc=A.get(),B.get(),C.get()
            xx=x0.get(); ll,rr=sorted((L.get(),R.get()))
            y=aa*math.sin(bb*xx+cc)
            slope=aa*bb*math.cos(bb*xx+cc)
            area=(-aa/bb*math.cos(bb*rr+cc))-(-aa/bb*math.cos(bb*ll+cc)) if abs(bb)>1e-9 else 0.0
            return aa,bb,cc,xx,ll,rr,y,slope,area

        def redraw():
            for vv,llab in val_labels: llab.config(text=f'{vv.get():.2f}')
            aa,bb,cc,xx,ll,rr,y,slope,area=calc()
            cv.delete('all'); w=max(cv.winfo_width(),660); h=max(cv.winfo_height(),490); pad=48
            xmin,xmax=-2*math.pi,2*math.pi; ymin,ymax=-6,6
            def P(x,yv):
                return (pad+(x-xmin)/(xmax-xmin)*(w-2*pad),
                        h-pad-(yv-ymin)/(ymax-ymin)*(h-2*pad))
            xaxis=P(0,0)[1]; yaxis=P(0,0)[0]
            cv.create_line(pad,xaxis,w-pad,xaxis,fill='#94a3b8'); cv.create_line(yaxis,pad,yaxis,h-pad,fill='#94a3b8')
            # Integral area polygon between L/R and x-axis.
            poly=[]
            n=120
            for i in range(n+1):
                q=ll+(rr-ll)*i/n; py=aa*math.sin(bb*q+cc); poly += list(P(q,py))
            poly += list(P(rr,0)); poly += list(P(ll,0))
            if len(poly)>=6: cv.create_polygon(*poly,fill='#dbeafe',outline='')
            # Function
            pts=[]
            for i in range(420):
                q=xmin+(xmax-xmin)*i/419; yy=aa*math.sin(bb*q+cc); pts += list(P(q,yy))
            cv.create_line(*pts,fill=BLUE,width=3,smooth=True)
            # Derivative
            dpts=[]
            for i in range(420):
                q=xmin+(xmax-xmin)*i/419; yy=aa*bb*math.cos(bb*q+cc)
                if ymin<=yy<=ymax: dpts += list(P(q,yy))
            if len(dpts)>=4: cv.create_line(*dpts,fill=GREEN,width=2,smooth=True)
            # Tangent at x0
            span=2.0; x1=max(xmin,xx-span); x2=min(xmax,xx+span)
            t1=y+slope*(x1-xx); t2=y+slope*(x2-xx)
            cv.create_line(*P(x1,t1),*P(x2,t2),fill=ORANGE,width=2)
            px,py=P(xx,y); cv.create_oval(px-6,py-6,px+6,py+6,fill=ORANGE,outline='')
            cv.create_text(pad,20,anchor='w',text='function  |  derivative  |  tangent  |  integral area',
                           fill=TEXT,font=('Segoe UI Semibold',10))
            info.delete('1.0','end')
            info.insert('end',f'FUNCTION\n y = {aa:.3f} sin({bb:.3f}x + {cc:.3f})\n\n')
            info.insert('end',f'DERIVATIVE\n y′ = {aa*bb:.3f} cos({bb:.3f}x + {cc:.3f})\n\n')
            info.insert('end',f'AT x₀ = {xx:.3f}\n y(x₀) = {y:.4f}\n slope = y′(x₀) = {slope:.4f}\n\n')
            info.insert('end',f'DEFINITE INTEGRAL\n ∫[{ll:.3f},{rr:.3f}] y dx = {area:.5f}\n\n')
            info.insert('end','INTERPRETATION\n• A เปลี่ยนความสูงของคลื่น\n• B เปลี่ยนความถี่และขนาดอนุพันธ์\n'
                              '• C เลื่อนเฟส\n• เส้นสัมผัสแสดงความชันเฉพาะจุด\n• พื้นที่ระบายแสดง signed area ของ definite integral')
            status.set(f'x₀={xx:.2f}  slope={slope:.3f}  integral={area:.3f}')

        def animate_x0():
            stop()
            run['k']=0
            def tick():
                k=run['k']; x0.set(-2*math.pi+4*math.pi*(k%160)/159)
                redraw(); run['k']+=1
                if run['k']<160: run['job']=self.after(45,tick)
                else: run['job']=None
            tick()

        def animate_phase():
            stop(); run['k']=0
            def tick():
                k=run['k']; C.set(-math.pi+2*math.pi*(k%140)/139)
                redraw(); run['k']+=1
                if run['k']<140: run['job']=self.after(50,tick)
                else: run['job']=None
            tick()

        def stop():
            if run['job']:
                try:self.after_cancel(run['job'])
                except Exception:pass
            run['job']=None

        ctrl=tk.Frame(right,bg='white'); ctrl.pack(fill='x',padx=14,pady=8)
        ttk.Button(ctrl,text='▶ Tangent Motion',style='Primary.TButton',command=animate_x0).pack(side='left')
        ttk.Button(ctrl,text='▶ Phase',command=animate_phase).pack(side='left',padx=4)
        ttk.Button(ctrl,text='■ Stop',command=stop).pack(side='left')
        ttk.Button(right,text='กลับ AI Equation → Animation',command=self.ai_equation_animation_lab).pack(anchor='w',padx=14,pady=4)
        ttk.Button(right,text='ต่อ MCS Animation → Robot',command=self.mcs_animation_lab).pack(anchor='w',padx=14,pady=4)

        for vv,_ in val_labels: vv.trace_add('write',lambda *_:redraw())
        self.after(120,redraw())

        self.card(b,'NEXT → V3.3',
            'ขั้นถัดไปจะเพิ่ม Vector/Matrix Transformation Animation และ Probability Distribution Animation '
            'ก่อนเชื่อมค่าทางคณิตศาสตร์เข้าสู่ AI Decision และ Robot Control อย่างเป็นระบบ')


    # ==================== V3.3: VECTOR/MATRIX + PROBABILITY -> AI/ROBOT ====================
    def matrix_probability_animation_lab(self):
        self.clear()
        self.header('▦ Vector / Matrix + Probability Animation • V3.3',
            'Linear Transformation → Probability Distribution → AI Decision → Robot Simulation')
        b=self.scrollbody()
        self.card(b,'V3.3 LEARNING GOAL',
            'เชื่อมคณิตศาสตร์ที่มองเห็นได้กับการตัดสินใจของ AI: Matrix เปลี่ยนตำแหน่ง/รูปร่างของ vector '
            'ส่วน Probability แสดง uncertainty ของข้อมูล แล้วนำผลทั้งสองไปสร้างคำสั่งจำลองให้ Robot')

        nb=ttk.Notebook(b); nb.pack(fill='both',expand=True,padx=28,pady=10)
        mt=tk.Frame(nb,bg='white'); pt=tk.Frame(nb,bg='white'); rt=tk.Frame(nb,bg='white')
        nb.add(mt,text='Vector / Matrix')
        nb.add(pt,text='Probability Distribution')
        nb.add(rt,text='AI → Robot')

        # ---------- MATRIX ----------
        tk.Label(mt,text='2×2 LINEAR TRANSFORMATION',bg='white',fg=TEXT,
                 font=('Segoe UI Semibold',12)).pack(anchor='w',padx=16,pady=(14,4))
        matrix_vars=[tk.DoubleVar(value=1),tk.DoubleVar(value=0),
                     tk.DoubleVar(value=0),tk.DoubleVar(value=1)]
        vector_vars=[tk.DoubleVar(value=2),tk.DoubleVar(value=1)]
        top=tk.Frame(mt,bg='white'); top.pack(fill='x',padx=16,pady=6)
        mf=tk.Frame(top,bg='white'); mf.pack(side='left')
        for i,v in enumerate(matrix_vars):
            ttk.Entry(mf,textvariable=v,width=7).grid(row=i//2,column=i%2,padx=3,pady=3)
        tk.Label(top,text=' × ',bg='white',font=('Segoe UI',14)).pack(side='left',padx=8)
        vf=tk.Frame(top,bg='white'); vf.pack(side='left')
        for i,v in enumerate(vector_vars): ttk.Entry(vf,textvariable=v,width=7).grid(row=i,column=0,padx=3,pady=3)
        presets=tk.Frame(top,bg='white'); presets.pack(side='left',padx=16)
        matrix_status=tk.StringVar(value='')
        matrix_state={'tx':2.0,'ty':1.0,'det':1.0,'scale':1.0,'job':None}

        mcv=tk.Canvas(mt,height=430,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1)
        mcv.pack(fill='both',expand=True,padx=16,pady=8)
        tk.Label(mt,textvariable=matrix_status,bg='white',fg=MUTED,font=('Consolas',9),
                 justify='left').pack(anchor='w',padx=16,pady=(0,8))

        def setmat(a,bv,c,d):
            for vv,x in zip(matrix_vars,[a,bv,c,d]): vv.set(x)
            draw_matrix()

        for textv,mat in [('Identity',(1,0,0,1)),('Rotate 45°',(0.707,-0.707,0.707,0.707)),
                          ('Scale',(1.6,0,0,0.7)),('Shear',(1,0.8,0,1)),('Reflect X',(1,0,0,-1))]:
            ttk.Button(presets,text=textv,command=lambda q=mat:setmat(*q)).pack(side='left',padx=2)

        def draw_matrix(progress=1.0):
            try:
                a,bv,c,d=[v.get() for v in matrix_vars]; x,y=[v.get() for v in vector_vars]
            except Exception:return
            tx=a*x+bv*y; ty=c*x+d*y; det=a*d-bv*c
            matrix_state.update(tx=tx,ty=ty,det=det,scale=math.sqrt(tx*tx+ty*ty))
            mcv.delete('all'); w=max(mcv.winfo_width(),700); h=max(mcv.winfo_height(),400)
            cx,cy=w/2,h/2; scale=min((w-90)/14,(h-70)/10)
            def P(px,py): return cx+px*scale,cy-py*scale
            mcv.create_line(35,cy,w-35,cy,fill='#94a3b8'); mcv.create_line(cx,25,cx,h-25,fill='#94a3b8')
            # Original square/grid basis
            sq=[(-1,-1),(1,-1),(1,1),(-1,1)]
            orig=[]
            for px,py in sq: orig += list(P(px,py))
            mcv.create_polygon(*orig,outline='#94a3b8',fill='',width=2)
            # transformed shape interpolated for animation
            trans=[]
            for px,py in sq:
                qx=a*px+bv*py; qy=c*px+d*py
                ix=px+(qx-px)*progress; iy=py+(qy-py)*progress
                trans += list(P(ix,iy))
            mcv.create_polygon(*trans,outline=BLUE,fill='#dbeafe',width=3)
            # vector original and transformed
            ox,oy=P(x,y); mcv.create_line(cx,cy,ox,oy,fill=GREEN,width=3,arrow='last')
            ix=x+(tx-x)*progress; iy=y+(ty-y)*progress; qx,qy=P(ix,iy)
            mcv.create_line(cx,cy,qx,qy,fill=ORANGE,width=4,arrow='last')
            mcv.create_text(20,18,anchor='w',text='original vector / transformed vector / transformed unit square',
                            fill=TEXT,font=('Segoe UI Semibold',10))
            matrix_status.set(
                f'M = [[{a:.2f}, {bv:.2f}], [{c:.2f}, {d:.2f}]]   v = ({x:.2f},{y:.2f})\n'
                f'Mv = ({tx:.3f},{ty:.3f})   det(M) = {det:.3f}   |Mv| = {matrix_state["scale"]:.3f}')
            update_robot_summary()

        def animate_matrix():
            if matrix_state.get('job'):
                try:self.after_cancel(matrix_state['job'])
                except Exception:pass
            def frame(k=0):
                draw_matrix(k/30)
                if k<30: matrix_state['job']=self.after(35,lambda:frame(k+1))
                else: matrix_state['job']=None
            frame()
        ttk.Button(mt,text='▶ Animate Transformation',style='Primary.TButton',
                   command=animate_matrix).pack(anchor='w',padx=16,pady=(0,12))

        # ---------- PROBABILITY ----------
        tk.Label(pt,text='PROBABILITY DISTRIBUTION — NORMAL MODEL',bg='white',fg=TEXT,
                 font=('Segoe UI Semibold',12)).pack(anchor='w',padx=16,pady=(14,4))
        mu=tk.DoubleVar(value=0.0); sigma=tk.DoubleVar(value=1.0); threshold=tk.DoubleVar(value=1.0)
        prob_state={'risk':0.1587,'job':None}
        plabs=[]
        for title,v,lo,hi in [('μ mean',mu,-3,3),('σ std.dev.',sigma,0.2,3),('risk threshold',threshold,-3,3)]:
            r=tk.Frame(pt,bg='white'); r.pack(fill='x',padx=16,pady=3)
            tk.Label(r,text=title,width=14,anchor='w',bg='white').pack(side='left')
            ttk.Scale(r,from_=lo,to=hi,variable=v).pack(side='left',fill='x',expand=True,padx=8)
            ll=tk.Label(r,width=8,bg='white',fg=BLUE,font=('Consolas',9)); ll.pack(side='left'); plabs.append((v,ll))
        pcv=tk.Canvas(pt,height=420,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1)
        pcv.pack(fill='both',expand=True,padx=16,pady=8)
        pstatus=tk.StringVar()
        tk.Label(pt,textvariable=pstatus,bg='white',fg=MUTED,font=('Consolas',9),justify='left').pack(anchor='w',padx=16,pady=(0,8))

        def normal_cdf(z):
            return 0.5*(1.0+math.erf(z/math.sqrt(2.0)))

        def draw_prob():
            mm=mu.get(); ss=max(0.05,sigma.get()); th=threshold.get()
            for vv,ll in plabs: ll.config(text=f'{vv.get():.2f}')
            risk=1-normal_cdf((th-mm)/ss); prob_state['risk']=risk
            self.mcs_robot_rule['last_probability']=risk
            pcv.delete('all'); w=max(pcv.winfo_width(),700); h=max(pcv.winfo_height(),390); pad=48
            xmin,xmax=-6,6; ymax=1/(ss*math.sqrt(2*math.pi))*1.18
            def P(x,y): return pad+(x-xmin)/(xmax-xmin)*(w-2*pad),h-pad-y/ymax*(h-2*pad)
            base=P(0,0)[1]; pcv.create_line(pad,base,w-pad,base,fill='#94a3b8')
            pts=[]
            for i in range(400):
                x=xmin+(xmax-xmin)*i/399
                y=math.exp(-0.5*((x-mm)/ss)**2)/(ss*math.sqrt(2*math.pi))
                pts += list(P(x,y))
            pcv.create_line(*pts,fill=BLUE,width=3,smooth=True)
            # Shade tail x >= threshold
            start=max(th,xmin); poly=list(P(start,0))
            for i in range(180):
                x=start+(xmax-start)*i/179
                y=math.exp(-0.5*((x-mm)/ss)**2)/(ss*math.sqrt(2*math.pi))
                poly += list(P(x,y))
            poly += list(P(xmax,0))
            if len(poly)>=6: pcv.create_polygon(*poly,fill='#fde68a',outline='')
            tx,_=P(th,0); pcv.create_line(tx,25,tx,base,fill=ORANGE,width=2,dash=(5,3))
            pcv.create_text(tx+5,30,anchor='nw',text='threshold',fill=ORANGE,font=('Segoe UI',9))
            pcv.create_text(pad,18,anchor='w',text='Normal PDF and right-tail probability P(X ≥ threshold)',
                            fill=TEXT,font=('Segoe UI Semibold',10))
            decision='STOP / REPLAN' if risk>=self.mcs_robot_rule.get('probability_threshold',0.55) else 'MOVE'
            pstatus.set(f'μ={mm:.3f}  σ={ss:.3f}  threshold={th:.3f}\n'
                        f'P(X ≥ threshold) = {risk:.4f}  → Robot probability decision: {decision}')
            update_robot_summary()

        def animate_threshold():
            if prob_state.get('job'):
                try:self.after_cancel(prob_state['job'])
                except Exception:pass
            def tick(k=0):
                threshold.set(-3+6*(k%120)/119); draw_prob()
                if k<119: prob_state['job']=self.after(45,lambda:tick(k+1))
                else: prob_state['job']=None
            tick()
        ttk.Button(pt,text='▶ Animate Threshold',style='Primary.TButton',
                   command=animate_threshold).pack(anchor='w',padx=16,pady=(0,12))

        # ---------- AI / ROBOT ----------
        tk.Label(rt,text='MATHEMATICS → AI DECISION → ROBOT',bg='white',fg=TEXT,
                 font=('Segoe UI Semibold',13)).pack(anchor='w',padx=18,pady=(18,6))
        summary=tk.Text(rt,height=18,font=('Consolas',10),wrap='word'); summary.pack(fill='both',expand=True,padx=18,pady=8)
        robot_canvas=tk.Canvas(rt,height=250,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1)
        robot_canvas.pack(fill='x',padx=18,pady=8)
        robot_anim={'job':None}

        def robot_decision():
            risk=prob_state['risk']; tx=matrix_state['tx']; det=matrix_state['det']
            pth=self.mcs_robot_rule.get('probability_threshold',0.55)
            if risk>=pth: return 'STOP / REPLAN'
            if det<0: return 'TURN LEFT'
            if tx>0.5: return 'TURN RIGHT'
            if tx<-0.5: return 'TURN LEFT'
            return 'FORWARD'

        def update_robot_summary():
            if 'summary' not in locals(): return
            try:
                decision=robot_decision()
                summary.delete('1.0','end')
                summary.insert('end','INPUT 1 — MATRIX TRANSFORMATION\n')
                summary.insert('end',f'  transformed vector = ({matrix_state["tx"]:.3f}, {matrix_state["ty"]:.3f})\n')
                summary.insert('end',f'  determinant = {matrix_state["det"]:.3f}\n\n')
                summary.insert('end','INPUT 2 — PROBABILITY / UNCERTAINTY\n')
                summary.insert('end',f'  right-tail probability = {prob_state["risk"]:.4f}\n')
                summary.insert('end',f'  decision threshold = {self.mcs_robot_rule.get("probability_threshold",0.55):.2f}\n\n')
                summary.insert('end','CONTROL RULE\n')
                summary.insert('end','  High probability risk → STOP/REPLAN\n')
                summary.insert('end','  Otherwise matrix direction/determinant influences TURN/FORWARD\n\n')
                summary.insert('end',f'ROBOT DECISION → {decision}\n\n')
                summary.insert('end','นี่เป็น educational mapping เพื่อให้เห็นการเชื่อม Math → Decision → Action ไม่ใช่ autonomous safety controller.')
            except Exception: pass

        def run_robot():
            decision=robot_decision(); robot_canvas.delete('all')
            w=max(robot_canvas.winfo_width(),700); h=230
            robot_canvas.create_line(45,h/2,w-45,h/2,fill='#94a3b8',width=3)
            robot_canvas.create_text(45,30,anchor='w',text=f'DECISION: {decision}',fill=TEXT,font=('Segoe UI Semibold',12))
            if 'STOP' in decision:
                x=w/2; robot_canvas.create_rectangle(x-25,h/2-18,x+25,h/2+18,fill=ORANGE,outline='')
                robot_canvas.create_text(x,h/2+38,text='STOP',fill=ORANGE,font=('Segoe UI Semibold',10)); return
            start=70; end=w-70 if 'RIGHT' in decision or decision=='FORWARD' else 120
            def frame(k=0):
                robot_canvas.delete('bot')
                x=start+(end-start)*k/35
                robot_canvas.create_rectangle(x-22,h/2-16,x+22,h/2+16,fill=BLUE,outline='',tags='bot')
                robot_canvas.create_oval(x-17,h/2+12,x-7,h/2+22,fill=TEXT,outline='',tags='bot')
                robot_canvas.create_oval(x+7,h/2+12,x+17,h/2+22,fill=TEXT,outline='',tags='bot')
                if k<35: robot_anim['job']=self.after(45,lambda:frame(k+1))
                else: robot_anim['job']=None
            frame()

        buttons=tk.Frame(rt,bg='white'); buttons.pack(fill='x',padx=18,pady=8)
        ttk.Button(buttons,text='▶ RUN AI → ROBOT',style='Primary.TButton',command=run_robot).pack(side='left')
        ttk.Button(buttons,text='เปิด MCS Animation → Robot',command=self.mcs_animation_lab).pack(side='left',padx=6)
        ttk.Button(buttons,text='Robot Command Center',command=self.robot_command_center_lab).pack(side='left')

        for vv in matrix_vars+vector_vars: vv.trace_add('write',lambda *_:draw_matrix())
        for vv,_ in plabs: vv.trace_add('write',lambda *_:draw_prob())
        self.after(150,lambda:(draw_matrix(),draw_prob(),update_robot_summary()))

        self.card(b,'NEXT → V3.4',
            'ขั้นต่อไป: Vector Field / Matrix Composition → Binomial & Discrete Probability → Conditional Probability / Bayes → '
            'Random Walk on Graph → รวมเป็น Math Mission Pipeline ที่ส่งผลไป Robot Simulation')


    # ==================== V3.4: RANDOM WALK -> PATH PLANNING -> CONDITIONAL/BAYES ====================
    def random_walk_bayes_lab(self):
        self.clear()
        self.header('🎲 Random Walk → Robot Path → Conditional Probability / Bayes • V3.4',
            'สุ่มเดินบนกราฟ → BFS วางเส้นทาง → Robot Mission → Evidence → Bayesian Update')
        b=self.scrollbody()
        self.card(b,'MCS CONNECTION',
            'Random walk on graphs ใช้แสดง stochastic movement ส่วน graph search ใช้หาเส้นทางอย่างมีระบบ '
            'จากนั้น Conditional Probability และ Bayes ใช้อัปเดตความเชื่อเมื่อ robot ได้ evidence จาก sensor')

        nb=ttk.Notebook(b); nb.pack(fill='both',expand=True,padx=28,pady=10)
        rw=tk.Frame(nb,bg='white'); mission=tk.Frame(nb,bg='white'); bay=tk.Frame(nb,bg='white')
        nb.add(rw,text='1 Random Walk + BFS')
        nb.add(mission,text='2 Robot Mission')
        nb.add(bay,text='3 Conditional + Bayes')

        nodes={'A':(90,220),'B':(230,80),'C':(230,350),'D':(410,90),'E':(410,345),'F':(600,215),'G':(760,215)}
        edges=[('A','B'),('A','C'),('B','D'),('B','E'),('C','E'),('D','F'),('E','F'),('F','G')]
        adj={k:[] for k in nodes}
        for u,v in edges: adj[u].append(v); adj[v].append(u)
        state={'random_path':[],'bfs_path':[],'mission_path':[],'job':None,'risk':0.0}

        # ---------- Random Walk + BFS ----------
        top=tk.Frame(rw,bg='white'); top.pack(fill='x',padx=16,pady=10)
        start=tk.StringVar(value='A'); goal=tk.StringVar(value='G'); steps=tk.IntVar(value=12)
        for textv,var,vals in [('Start',start,list(nodes)),('Goal',goal,list(nodes))]:
            tk.Label(top,text=textv,bg='white').pack(side='left',padx=(0,3))
            ttk.Combobox(top,textvariable=var,values=vals,state='readonly',width=5).pack(side='left',padx=(0,10))
        tk.Label(top,text='Random steps',bg='white').pack(side='left')
        ttk.Spinbox(top,from_=1,to=50,textvariable=steps,width=5).pack(side='left',padx=5)
        gcv=tk.Canvas(rw,height=470,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1)
        gcv.pack(fill='both',expand=True,padx=16,pady=6)
        rwstatus=tk.StringVar(value='Random Walk = stochastic exploration | BFS = systematic shortest path (unweighted graph)')
        tk.Label(rw,textvariable=rwstatus,bg='white',fg=MUTED,font=('Consolas',9),justify='left',wraplength=950).pack(anchor='w',padx=16,pady=(0,8))

        def draw_graph(path=None,robot_at=None,visited=None):
            gcv.delete('all')
            for u,v in edges:
                x1,y1=nodes[u]; x2,y2=nodes[v]
                active=path and any((path[i]==u and path[i+1]==v) or (path[i]==v and path[i+1]==u) for i in range(len(path)-1))
                gcv.create_line(x1,y1,x2,y2,fill=ORANGE if active else '#cbd5e1',width=4 if active else 2)
            for n,(x,y) in nodes.items():
                fill='#dbeafe' if not visited or n not in visited else '#dcfce7'
                gcv.create_oval(x-23,y-23,x+23,y+23,fill=fill,outline=BLUE,width=2)
                gcv.create_text(x,y,text=n,fill=TEXT,font=('Segoe UI Semibold',11))
            if robot_at in nodes:
                x,y=nodes[robot_at]; gcv.create_rectangle(x-15,y-38,x+15,y-26,fill=ORANGE,outline='',tags='robot')
            gcv.create_text(20,18,anchor='w',text='Graph: random exploration vs BFS route',fill=TEXT,font=('Segoe UI Semibold',10))

        def bfs_path(s0,g0):
            if s0==g0:return [s0],[s0]
            q=[s0]; parent={s0:None}; order=[]
            while q:
                u=q.pop(0); order.append(u)
                if u==g0:break
                for v in adj[u]:
                    if v not in parent: parent[v]=u; q.append(v)
            if g0 not in parent:return [],order
            p=[]; u=g0
            while u is not None:p.append(u); u=parent[u]
            return p[::-1],order

        def random_walk():
            stop_jobs(); cur=start.get(); p=[cur]; n=max(1,min(50,steps.get()))
            for _ in range(n):
                if cur==goal.get():break
                cur=random.choice(adj[cur]); p.append(cur)
            state['random_path']=p
            def frame(i=0):
                draw_graph(p[:i+1],p[i],set(p[:i+1]))
                rwstatus.set(f'RANDOM WALK step {i}/{len(p)-1}: {" → ".join(p[:i+1])}\n'
                             f'Goal reached: {p[-1]==goal.get()}')
                if i<len(p)-1: state['job']=self.after(420,lambda:frame(i+1))
            frame()

        def run_bfs():
            stop_jobs(); p,order=bfs_path(start.get(),goal.get()); state['bfs_path']=p; state['mission_path']=p
            def frame(i=0):
                shown=set(order[:min(i+1,len(order))]); upto=min(i+1,len(p))
                draw_graph(p[:upto],p[min(i,len(p)-1)] if p else None,shown)
                rwstatus.set(f'BFS visited: {" → ".join(order[:min(i+1,len(order))])}\n'
                             f'Shortest path: {" → ".join(p) if p else "not found"}')
                if i<max(len(order),len(p))-1: state['job']=self.after(420,lambda:frame(i+1))
            frame()

        def stop_jobs():
            if state.get('job'):
                try:self.after_cancel(state['job'])
                except Exception:pass
            state['job']=None

        buttons=tk.Frame(rw,bg='white'); buttons.pack(fill='x',padx=16,pady=8)
        ttk.Button(buttons,text='🎲 Animate Random Walk',style='Primary.TButton',command=random_walk).pack(side='left')
        ttk.Button(buttons,text='🔎 Animate BFS Path',command=run_bfs).pack(side='left',padx=5)
        ttk.Button(buttons,text='■ Stop',command=stop_jobs).pack(side='left')
        draw_graph()

        # ---------- Robot Mission ----------
        tk.Label(mission,text='ROBOT MISSION — FOLLOW THE PLANNED GRAPH PATH',bg='white',fg=TEXT,
                 font=('Segoe UI Semibold',12)).pack(anchor='w',padx=16,pady=(14,4))
        mcv=tk.Canvas(mission,height=450,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1)
        mcv.pack(fill='both',expand=True,padx=16,pady=8)
        mstatus=tk.StringVar(value='กด PLAN BFS แล้ว RUN ROBOT')
        tk.Label(mission,textvariable=mstatus,bg='white',fg=MUTED,font=('Consolas',9)).pack(anchor='w',padx=16,pady=(0,8))

        def draw_mission(path=None,idx=0):
            mcv.delete('all')
            for u,v in edges:
                x1,y1=nodes[u]; x2,y2=nodes[v]
                active=path and any((path[i]==u and path[i+1]==v) or (path[i]==v and path[i+1]==u) for i in range(len(path)-1))
                mcv.create_line(x1,y1,x2,y2,fill=GREEN if active else '#cbd5e1',width=4 if active else 2)
            for n,(x,y) in nodes.items():
                mcv.create_oval(x-22,y-22,x+22,y+22,fill='#f8fafc',outline=BLUE,width=2)
                mcv.create_text(x,y,text=n,fill=TEXT,font=('Segoe UI Semibold',10))
            if path:
                n=path[min(idx,len(path)-1)]; x,y=nodes[n]
                mcv.create_rectangle(x-18,y-38,x+18,y-27,fill=ORANGE,outline='')
                mcv.create_text(20,18,anchor='w',text='Planned route: '+' → '.join(path),fill=TEXT,font=('Segoe UI Semibold',10))

        def plan_mission():
            p,order=bfs_path(start.get(),goal.get()); state['mission_path']=p; draw_mission(p,0)
            self.mcs_robot_rule['graph_path']=p
            mstatus.set('BFS PLAN: '+' → '.join(p))

        def run_mission():
            stop_jobs()
            if not state['mission_path']: plan_mission()
            p=state['mission_path']
            def frame(i=0):
                draw_mission(p,i); mstatus.set(f'ROBOT at {p[i]} • step {i+1}/{len(p)}')
                if i<len(p)-1: state['job']=self.after(650,lambda:frame(i+1))
                else: mstatus.set('MISSION COMPLETE • '+' → '.join(p))
            if p: frame()
        mb=tk.Frame(mission,bg='white'); mb.pack(fill='x',padx=16,pady=8)
        ttk.Button(mb,text='1 PLAN BFS',command=plan_mission).pack(side='left')
        ttk.Button(mb,text='2 ▶ RUN ROBOT',style='Primary.TButton',command=run_mission).pack(side='left',padx=6)
        ttk.Button(mb,text='Robot Command Center',command=self.robot_command_center_lab).pack(side='left')
        draw_mission()

        # ---------- Conditional Probability / Bayes ----------
        tk.Label(bay,text='CONDITIONAL PROBABILITY + BAYES SENSOR UPDATE',bg='white',fg=TEXT,
                 font=('Segoe UI Semibold',12)).pack(anchor='w',padx=16,pady=(14,4))
        self.card(bay,'SCENARIO',
            'Robot ต้องประเมินว่า “มี obstacle จริง” (H) หลัง sensor แจ้ง positive (+). '
            'ปรับ Prior P(H), Sensitivity P(+|H), False-positive P(+|¬H) แล้วดู Posterior P(H|+) เปลี่ยนแบบ real-time')
        prior=tk.DoubleVar(value=.20); sens=tk.DoubleVar(value=.90); fpr=tk.DoubleVar(value=.10)
        blabs=[]
        for title,v in [('Prior P(H)',prior),('Sensitivity P(+|H)',sens),('False positive P(+|¬H)',fpr)]:
            r=tk.Frame(bay,bg='white'); r.pack(fill='x',padx=18,pady=4)
            tk.Label(r,text=title,width=24,anchor='w',bg='white').pack(side='left')
            ttk.Scale(r,from_=0.01,to=.99,variable=v).pack(side='left',fill='x',expand=True,padx=8)
            ll=tk.Label(r,width=8,bg='white',fg=BLUE,font=('Consolas',9)); ll.pack(side='left'); blabs.append((v,ll))
        bcv=tk.Canvas(bay,height=360,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1)
        bcv.pack(fill='both',expand=True,padx=18,pady=8)
        bstatus=tk.StringVar()
        tk.Label(bay,textvariable=bstatus,bg='white',fg=MUTED,font=('Consolas',9),justify='left').pack(anchor='w',padx=18,pady=(0,8))

        def draw_bayes():
            p=prior.get(); se=sens.get(); fp=fpr.get()
            for vv,ll in blabs: ll.config(text=f'{vv.get():.3f}')
            ppos=se*p+fp*(1-p)
            post=(se*p/ppos) if ppos>0 else 0
            state['risk']=post; self.mcs_robot_rule['last_probability']=post
            bcv.delete('all'); w=max(bcv.winfo_width(),800); h=330
            # probability tree
            x0,y0=80,h/2; x1=300; x2=560
            bcv.create_oval(x0-20,y0-20,x0+20,y0+20,fill='#dbeafe',outline=BLUE)
            bcv.create_text(x0,y0,text='Start')
            branches=[('H',p,y0-90),('¬H',1-p,y0+90)]
            for name,pr,yy in branches:
                bcv.create_line(x0+20,y0,x1-20,yy,fill='#94a3b8',width=2)
                bcv.create_oval(x1-20,yy-20,x1+20,yy+20,fill='#f8fafc',outline=BLUE)
                bcv.create_text(x1,yy,text=name)
                bcv.create_text((x0+x1)/2, (y0+yy)/2-8,text=f'{pr:.2f}',fill=MUTED)
                cond=se if name=='H' else fp
                bcv.create_line(x1+20,yy,x2-20,yy,fill=ORANGE,width=3)
                bcv.create_oval(x2-20,yy-20,x2+20,yy+20,fill='#fef3c7',outline=ORANGE)
                bcv.create_text(x2,yy,text='+')
                bcv.create_text((x1+x2)/2,yy-10,text=f'P(+|{name})={cond:.2f}',fill=MUTED)
            bx=690; bw=70; maxh=180
            bcv.create_rectangle(bx,h-45-maxh,bx+bw,h-45,outline='#cbd5e1')
            bh=maxh*post
            bcv.create_rectangle(bx,h-45-bh,bx+bw,h-45,fill=GREEN,outline='')
            bcv.create_text(bx+bw/2,h-25,text='P(H|+)',fill=TEXT)
            bcv.create_text(bx+bw/2,h-55-bh,text=f'{post:.3f}',fill=GREEN,font=('Segoe UI Semibold',11))
            decision='STOP / REPLAN' if post>=self.mcs_robot_rule.get('probability_threshold',.55) else 'CONTINUE'
            bstatus.set(f'P(+) = P(+|H)P(H) + P(+|¬H)P(¬H) = {ppos:.4f}\n'
                        f'Bayes: P(H|+) = P(+|H)P(H) / P(+) = {post:.4f}\n'
                        f'Robot decision using threshold {self.mcs_robot_rule.get("probability_threshold",.55):.2f}: {decision}')

        def animate_prior():
            stop_jobs()
            def tick(k=0):
                prior.set(.02+.96*(k%100)/99); draw_bayes()
                if k<99: state['job']=self.after(45,lambda:tick(k+1))
            tick()
        bb=tk.Frame(bay,bg='white'); bb.pack(fill='x',padx=18,pady=8)
        ttk.Button(bb,text='▶ Animate Prior → Posterior',style='Primary.TButton',command=animate_prior).pack(side='left')
        ttk.Button(bb,text='Open Robot Mission',command=lambda:nb.select(mission)).pack(side='left',padx=6)
        for vv,_ in blabs: vv.trace_add('write',lambda *_:draw_bayes())
        self.after(120,draw_bayes)

        self.card(b,'NEXT → V3.5',
            'ต่อไปจะรวม Random Walk statistics + Conditional/Bayes evidence เข้ากับ Graph Mission โดยให้ sensor evidence '
            'เปลี่ยน route/STOP/REPLAN ระหว่างที่ robot กำลังเดิน และเพิ่ม visit-frequency / empirical probability dashboard')


    # ==================== V3.5: MATHEMATICAL STATISTICS FROM RANDOM WALK ====================
    def mcs_statistics_lab(self):
        self.clear()
        self.header('📊 MCS Mathematical Statistics Lab • V3.5',
            'Random Walk Data → Frequency → Relative Frequency → Mean / Variance / SD → Empirical Probability → Convergence')
        b=self.scrollbody()
        self.card(b,'MATHEMATICS FIRST',
            'V3.5 เน้น “ข้อมูล → สถิติ → ความน่าจะเป็นเชิงทดลอง” ก่อนนำไป AI/Robot: '
            'ระบบทำ Random Walk ซ้ำหลาย trials แล้วเก็บจำนวนครั้งที่แต่ละ node ถูกเยี่ยมชม, จำนวนก้าวถึงเป้าหมาย, '
            'success rate และ running estimate เพื่อให้นักเรียนเห็น Law of Large Numbers ในเชิงทดลอง')

        nodes={'A':(90,210),'B':(230,75),'C':(230,340),'D':(410,85),'E':(410,335),'F':(590,210),'G':(750,210)}
        edges=[('A','B'),('A','C'),('B','D'),('B','E'),('C','E'),('D','F'),('E','F'),('F','G')]
        adj={k:[] for k in nodes}
        for u,v in edges: adj[u].append(v); adj[v].append(u)

        ctl=self.card(b,'1 • DATA COLLECTION')
        row=tk.Frame(ctl,bg='white'); row.pack(fill='x',padx=18,pady=8)
        start=tk.StringVar(value='A'); goal=tk.StringVar(value='G')
        trials=tk.IntVar(value=500); maxsteps=tk.IntVar(value=20)
        for title,var,vals in [('Start',start,list(nodes)),('Goal',goal,list(nodes))]:
            tk.Label(row,text=title,bg='white').pack(side='left',padx=(0,3))
            ttk.Combobox(row,textvariable=var,values=vals,state='readonly',width=5).pack(side='left',padx=(0,10))
        tk.Label(row,text='Trials',bg='white').pack(side='left')
        ttk.Spinbox(row,from_=10,to=10000,increment=10,textvariable=trials,width=8).pack(side='left',padx=5)
        tk.Label(row,text='Max steps',bg='white').pack(side='left')
        ttk.Spinbox(row,from_=1,to=200,textvariable=maxsteps,width=6).pack(side='left',padx=5)

        nb=ttk.Notebook(b); nb.pack(fill='both',expand=True,padx=28,pady=10)
        freq=tk.Frame(nb,bg='white'); desc=tk.Frame(nb,bg='white'); conv=tk.Frame(nb,bg='white')
        nb.add(freq,text='Frequency Distribution')
        nb.add(desc,text='Descriptive Statistics')
        nb.add(conv,text='Empirical Probability')

        fcv=tk.Canvas(freq,height=450,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1)
        fcv.pack(fill='both',expand=True,padx=14,pady=10)
        dtext=tk.Text(desc,height=24,font=('Consolas',10),wrap='word')
        dtext.pack(fill='both',expand=True,padx=14,pady=10)
        ccv=tk.Canvas(conv,height=450,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1)
        ccv.pack(fill='both',expand=True,padx=14,pady=10)

        status=tk.StringVar(value='ยังไม่มีข้อมูล — กด RUN STATISTICAL EXPERIMENT')
        tk.Label(b,textvariable=status,bg=BG,fg=MUTED,font=('Consolas',9),justify='left',
                 wraplength=1100).pack(anchor='w',padx=30,pady=(0,8))
        state={'counts':{n:0 for n in nodes},'step_samples':[],'successes':0,
               'running':[],'total_visits':0,'N':0,'job':None}

        def sample_stats(xs):
            n=len(xs)
            if not n:return 0,0,0,0,0
            mean=sum(xs)/n
            var=sum((x-mean)**2 for x in xs)/n
            svar=sum((x-mean)**2 for x in xs)/(n-1) if n>1 else 0
            return mean,var,math.sqrt(var),svar,math.sqrt(svar)

        def simulate_once(s0,g0,limit):
            cur=s0; path=[cur]
            for _ in range(limit):
                if cur==g0: break
                cur=random.choice(adj[cur]); path.append(cur)
            return path,cur==g0

        def collect():
            try:
                N=max(10,min(10000,int(trials.get())))
                lim=max(1,min(200,int(maxsteps.get())))
            except Exception:
                messagebox.showerror('Input','กรุณาใส่ Trials / Max steps เป็นจำนวนเต็ม'); return
            counts={n:0 for n in nodes}; samples=[]; successes=0; running=[]; total=0
            s0,g0=start.get(),goal.get()
            for i in range(1,N+1):
                path,ok=simulate_once(s0,g0,lim)
                for n in path: counts[n]+=1; total+=1
                if ok: successes+=1; samples.append(len(path)-1)
                running.append(successes/i)
            state.update(counts=counts,step_samples=samples,successes=successes,running=running,
                         total_visits=total,N=N)
            render_all()
            status.set(f'Collected {N} random walks • success={successes} • '
                       f'empirical P(reach {g0} within {lim} steps)={successes/N:.4f}')

        def render_frequency():
            fcv.delete('all'); w=max(fcv.winfo_width(),760); h=max(fcv.winfo_height(),420)
            pad=55; names=list(nodes); vals=[state['counts'][n] for n in names]
            vmax=max(vals+[1]); bw=(w-2*pad)/len(names)*.65
            fcv.create_line(pad,h-pad,w-pad,h-pad,fill='#94a3b8')
            for i,(n,v) in enumerate(zip(names,vals)):
                cx=pad+(i+.5)*(w-2*pad)/len(names); bh=(h-2*pad)*v/vmax
                fcv.create_rectangle(cx-bw/2,h-pad-bh,cx+bw/2,h-pad,fill='#dbeafe',outline=BLUE,width=2)
                fcv.create_text(cx,h-pad+15,text=n,fill=TEXT)
                fcv.create_text(cx,h-pad-bh-10,text=str(v),fill=TEXT,font=('Consolas',8))
            fcv.create_text(pad,20,anchor='w',text='Node visit frequency (all visits across all trials)',
                            fill=TEXT,font=('Segoe UI Semibold',10))

        def render_desc():
            xs=state['step_samples']; mean,var,sd,svar,ssd=sample_stats(xs)
            N=state['N']; succ=state['successes']; p=succ/N if N else 0
            rel={n:(state['counts'][n]/state['total_visits'] if state['total_visits'] else 0) for n in nodes}
            dtext.delete('1.0','end')
            dtext.insert('end','DESCRIPTIVE STATISTICS — SUCCESSFUL WALKS\n\n')
            dtext.insert('end',f'N trials                 = {N}\nSuccessful walks         = {succ}\n')
            dtext.insert('end',f'Empirical success P-hat  = {p:.6f}\n\n')
            dtext.insert('end',f'Mean steps               = {mean:.6f}\n')
            dtext.insert('end',f'Population variance       = {var:.6f}\nPopulation SD             = {sd:.6f}\n')
            dtext.insert('end',f'Sample variance (n-1)     = {svar:.6f}\nSample SD                 = {ssd:.6f}\n\n')
            dtext.insert('end','NODE RELATIVE FREQUENCY\n')
            for n in nodes:
                dtext.insert('end',f'  {n}: {state["counts"][n]:6d} visits   relative={rel[n]:.6f}\n')
            if N:
                se=math.sqrt(p*(1-p)/N)
                dtext.insert('end',f'\nSTANDARD ERROR OF P-HAT\n  sqrt(p-hat(1-p-hat)/N) = {se:.6f}\n')
                lo=max(0,p-1.96*se); hi=min(1,p+1.96*se)
                dtext.insert('end',f'\nApprox. 95% interval (normal approximation)\n  [{lo:.6f}, {hi:.6f}]\n')
            dtext.insert('end','\nหมายเหตุ: interval นี้เป็นการประมาณเชิงการศึกษา ไม่ใช่ exact binomial interval.')

        def render_convergence(progress=1.0):
            ccv.delete('all'); data=state['running']; w=max(ccv.winfo_width(),760); h=max(ccv.winfo_height(),420); pad=55
            ccv.create_line(pad,h-pad,w-pad,h-pad,fill='#94a3b8'); ccv.create_line(pad,25,pad,h-pad,fill='#94a3b8')
            ccv.create_text(pad,18,anchor='w',text='Running empirical probability: successes / trials so far',
                            fill=TEXT,font=('Segoe UI Semibold',10))
            if not data:return
            upto=max(2,min(len(data),int(len(data)*progress)))
            pts=[]
            for i,p in enumerate(data[:upto]):
                x=pad+(w-2*pad)*(i/max(1,len(data)-1)); y=h-pad-p*(h-2*pad)
                pts += [x,y]
            if len(pts)>=4: ccv.create_line(*pts,fill=BLUE,width=2)
            final=data[-1]; fy=h-pad-final*(h-2*pad)
            ccv.create_line(pad,fy,w-pad,fy,fill=ORANGE,dash=(5,4))
            ccv.create_text(w-pad,fy-10,anchor='e',text=f'final P-hat={final:.4f}',fill=ORANGE,font=('Consolas',9))
            for q in [0,.25,.5,.75,1]:
                y=h-pad-q*(h-2*pad); ccv.create_text(pad-8,y,text=f'{q:.2f}',anchor='e',fill=MUTED,font=('Segoe UI',8))

        def render_all():
            render_frequency(); render_desc(); render_convergence()

        def animate_convergence():
            if not state['running']: collect()
            if state.get('job'):
                try:self.after_cancel(state['job'])
                except Exception:pass
            k={'v':1}
            def tick():
                k['v']+=2
                render_convergence(min(1,k['v']/100))
                if k['v']<100: state['job']=self.after(35,tick)
                else: state['job']=None
            render_convergence(.01); tick()

        def export_csv():
            if not state['N']:
                messagebox.showinfo('Statistics','กรุณารันการทดลองก่อน'); return
            path=Path('mcs_random_walk_statistics.csv')
            with path.open('w',newline='',encoding='utf-8-sig') as f:
                wr=csv.writer(f); wr.writerow(['node','visit_count','relative_frequency'])
                for n in nodes:
                    wr.writerow([n,state['counts'][n],state['counts'][n]/state['total_visits'] if state['total_visits'] else 0])
            messagebox.showinfo('Export',f'บันทึกแล้ว: {path.resolve()}')

        actions=tk.Frame(ctl,bg='white'); actions.pack(fill='x',padx=18,pady=(0,12))
        ttk.Button(actions,text='▶ RUN STATISTICAL EXPERIMENT',style='Primary.TButton',command=collect).pack(side='left')
        ttk.Button(actions,text='▶ Animate Convergence',command=animate_convergence).pack(side='left',padx=5)
        ttk.Button(actions,text='Export CSV',command=export_csv).pack(side='left')
        ttk.Button(actions,text='Random Walk + Bayes V3.4',command=self.random_walk_bayes_lab).pack(side='left',padx=5)

        self.card(b,'MATHEMATICAL IDEAS IN V3.5',
            'Frequency และ relative frequency สรุปข้อมูลจากการทดลอง; mean/variance/standard deviation อธิบายจำนวนก้าว; '
            'P-hat = successes/N เป็น empirical probability; running P-hat แสดงการเปลี่ยนของค่าประมาณเมื่อจำนวน trials เพิ่มขึ้น. '
            'ขั้นต่อไป V3.6 จะเพิ่ม histogram ของ step distribution, PMF/CDF, expectation, variance ของ random variable '
            'และเปรียบเทียบ empirical distribution กับแบบจำลองทางคณิตศาสตร์')


    # ==================== V3.6: RANDOM VARIABLE / PMF / CDF / EXPECTATION ====================
    def random_variable_distribution_lab(self):
        self.clear()
        self.header('📈 Random Variable → Histogram → PMF → CDF • V3.6',
            'Random Walk First-Passage Time X → Empirical Distribution → Exact Finite-Horizon Distribution → E[X] / Var(X)')
        b=self.scrollbody()
        self.card(b,'RANDOM VARIABLE',
            'กำหนด X = จำนวนก้าวที่ Random Walk ใช้ “ครั้งแรก” เพื่อไปถึง Goal ภายใน Max steps. '
            'แต่ละ trial ให้ observation ของ X เมื่อสำเร็จ; trial ที่ยังไม่ถึงเป้าหมายภายใน horizon จะถูกบันทึกเป็น censored/failure '
            'และแสดง probability mass ที่เหลือแยกต่างหาก')

        nodes=['A','B','C','D','E','F','G']
        edges=[('A','B'),('A','C'),('B','D'),('B','E'),('C','E'),('D','F'),('E','F'),('F','G')]
        adj={k:[] for k in nodes}
        for u,v in edges: adj[u].append(v); adj[v].append(u)

        ctl=self.card(b,'1 • EXPERIMENT SETTINGS')
        r=tk.Frame(ctl,bg='white'); r.pack(fill='x',padx=18,pady=8)
        start=tk.StringVar(value='A'); goal=tk.StringVar(value='G'); trials=tk.IntVar(value=2000); horizon=tk.IntVar(value=30)
        for title,var,vals in [('Start',start,nodes),('Goal',goal,nodes)]:
            tk.Label(r,text=title,bg='white').pack(side='left',padx=(0,3))
            ttk.Combobox(r,textvariable=var,values=vals,state='readonly',width=5).pack(side='left',padx=(0,10))
        tk.Label(r,text='Trials',bg='white').pack(side='left')
        ttk.Spinbox(r,from_=50,to=20000,increment=50,textvariable=trials,width=8).pack(side='left',padx=5)
        tk.Label(r,text='Max steps',bg='white').pack(side='left')
        ttk.Spinbox(r,from_=2,to=100,textvariable=horizon,width=6).pack(side='left',padx=5)

        nb=ttk.Notebook(b); nb.pack(fill='both',expand=True,padx=28,pady=10)
        htab=tk.Frame(nb,bg='white'); ptab=tk.Frame(nb,bg='white'); ctab=tk.Frame(nb,bg='white'); mtab=tk.Frame(nb,bg='white')
        nb.add(htab,text='Histogram')
        nb.add(ptab,text='PMF: Empirical vs Exact')
        nb.add(ctab,text='CDF')
        nb.add(mtab,text='E[X] + Variance')

        hcv=tk.Canvas(htab,height=430,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1); hcv.pack(fill='both',expand=True,padx=12,pady=10)
        pcv=tk.Canvas(ptab,height=430,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1); pcv.pack(fill='both',expand=True,padx=12,pady=10)
        ccv=tk.Canvas(ctab,height=430,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1); ccv.pack(fill='both',expand=True,padx=12,pady=10)
        txt=tk.Text(mtab,height=25,font=('Consolas',10),wrap='word'); txt.pack(fill='both',expand=True,padx=12,pady=10)
        status=tk.StringVar(value='กด RUN DISTRIBUTION EXPERIMENT')
        tk.Label(b,textvariable=status,bg=BG,fg=MUTED,font=('Consolas',9),wraplength=1100,justify='left').pack(anchor='w',padx=30,pady=(0,8))

        st={'N':0,'samples':[],'fail':0,'emp':{},'exact':{},'survive':0.0,'job':None}

        def one_walk(s0,g0,H):
            cur=s0
            if cur==g0:return 0
            for k in range(1,H+1):
                cur=random.choice(adj[cur])
                if cur==g0:return k
            return None

        def exact_first_passage(s0,g0,H):
            # Dynamic programming on probability mass that has not yet hit goal.
            if s0==g0:return {0:1.0},0.0
            alive={s0:1.0}; hit={}
            for k in range(1,H+1):
                nxt={}
                for u,p in alive.items():
                    deg=len(adj[u])
                    for v in adj[u]:
                        q=p/deg
                        if v==g0: hit[k]=hit.get(k,0.0)+q
                        else: nxt[v]=nxt.get(v,0.0)+q
                alive=nxt
            return hit,sum(alive.values())

        def moments(dist):
            mass=sum(dist.values())
            if mass<=0:return 0,0,0,mass
            # Conditional moments among arrivals within finite horizon.
            mean=sum(x*p for x,p in dist.items())/mass
            var=sum(((x-mean)**2)*p for x,p in dist.items())/mass
            return mean,var,math.sqrt(var),mass

        def run():
            try:N=max(50,min(20000,int(trials.get()))); H=max(2,min(100,int(horizon.get())))
            except Exception:
                messagebox.showerror('Input','Trials / Max steps ต้องเป็นจำนวนเต็ม'); return
            sam=[]; fail=0
            for _ in range(N):
                x=one_walk(start.get(),goal.get(),H)
                if x is None: fail+=1
                else:sam.append(x)
            counts={}
            for x in sam:counts[x]=counts.get(x,0)+1
            emp={x:c/N for x,c in counts.items()} # unconditional finite-horizon mass
            exact,surv=exact_first_passage(start.get(),goal.get(),H)
            st.update(N=N,samples=sam,fail=fail,emp=emp,exact=exact,survive=surv)
            render()
            status.set(f'N={N} • observed arrivals={len(sam)} • censored/failure={fail} • '
                       f'empirical P(hit by {H})={len(sam)/N:.5f} • exact={sum(exact.values()):.5f}')

        def axes(cv,title,ymax=1.0):
            cv.delete('all'); w=max(cv.winfo_width(),760); h=max(cv.winfo_height(),400); pad=55
            cv.create_line(pad,h-pad,w-pad,h-pad,fill='#94a3b8'); cv.create_line(pad,25,pad,h-pad,fill='#94a3b8')
            cv.create_text(pad,18,anchor='w',text=title,fill=TEXT,font=('Segoe UI Semibold',10))
            return w,h,pad,max(ymax,1e-9)

        def render_hist():
            H=horizon.get(); counts={}
            for x in st['samples']:counts[x]=counts.get(x,0)+1
            xs=list(range(0,H+1)); vmax=max(list(counts.values())+[1])
            w,h,pad,_=axes(hcv,'Histogram of first-passage step X (successful arrivals)',vmax)
            bw=(w-2*pad)/max(1,len(xs))*.78
            for i,x in enumerate(xs):
                v=counts.get(x,0); cx=pad+(i+.5)*(w-2*pad)/len(xs); bh=(h-2*pad)*v/vmax
                if v:hcv.create_rectangle(cx-bw/2,h-pad-bh,cx+bw/2,h-pad,fill='#dbeafe',outline=BLUE)
                if len(xs)<=35 or x%5==0:hcv.create_text(cx,h-pad+14,text=str(x),fill=MUTED,font=('Segoe UI',7))
            hcv.create_text(w-pad,18,anchor='e',text=f'censored={st["fail"]}',fill=ORANGE,font=('Consolas',9))

        def render_pmf(progress=1.0):
            H=horizon.get(); ymax=max(list(st['exact'].values())+list(st['emp'].values())+[.01])*1.15
            w,h,pad,_=axes(pcv,'PMF: empirical first-passage mass vs exact finite-horizon mass',ymax)
            upto=max(1,int(H*progress))
            for x in range(0,upto+1):
                ex=st['exact'].get(x,0); em=st['emp'].get(x,0)
                cx=pad+(x+.5)*(w-2*pad)/(H+1); bw=(w-2*pad)/(H+1)*.32
                if ex: pcv.create_rectangle(cx-bw,h-pad-ex/ymax*(h-2*pad),cx,h-pad,fill='#dcfce7',outline=GREEN)
                if em: pcv.create_rectangle(cx,h-pad-em/ymax*(h-2*pad),cx+bw,h-pad,fill='#dbeafe',outline=BLUE)
                if H<=35 or x%5==0:pcv.create_text(cx,h-pad+14,text=str(x),fill=MUTED,font=('Segoe UI',7))
            pcv.create_text(w-pad,18,anchor='e',text='exact | empirical',fill=TEXT,font=('Segoe UI',9))

        def render_cdf():
            H=horizon.get(); w,h,pad,_=axes(ccv,'CDF F(k)=P(X≤k): empirical vs exact',1)
            eacc=0; tacc=0; ep=[]; tp=[]
            for x in range(H+1):
                eacc+=st['emp'].get(x,0); tacc+=st['exact'].get(x,0)
                px=pad+(x/H)*(w-2*pad)
                ep += [px,h-pad-eacc*(h-2*pad)]; tp += [px,h-pad-tacc*(h-2*pad)]
            if len(ep)>=4:ccv.create_line(*ep,fill=BLUE,width=3)
            if len(tp)>=4:ccv.create_line(*tp,fill=GREEN,width=2)
            ccv.create_text(w-pad,18,anchor='e',text=f'F_exact({H})={tacc:.5f}  F_emp({H})={eacc:.5f}',fill=TEXT,font=('Consolas',9))

        def render_moments():
            emean,evar,esd,emass=moments(st['emp']); tmean,tvar,tsd,tmass=moments(st['exact'])
            txt.delete('1.0','end')
            txt.insert('end','RANDOM VARIABLE X = FIRST-PASSAGE STEP\n\n')
            txt.insert('end','FINITE-HORIZON PROBABILITY MASS\n')
            txt.insert('end',f'  Empirical P(hit by H) = {emass:.8f}\n  Exact P(hit by H)     = {tmass:.8f}\n')
            txt.insert('end',f'  Exact survival/failure mass after H = {st["survive"]:.8f}\n\n')
            txt.insert('end','CONDITIONAL MOMENTS GIVEN X ≤ H (arrival within horizon)\n')
            txt.insert('end',f'  Empirical E[X | hit]   = {emean:.8f}\n  Exact E[X | hit]       = {tmean:.8f}\n')
            txt.insert('end',f'  Empirical Var(X | hit) = {evar:.8f}\n  Exact Var(X | hit)     = {tvar:.8f}\n')
            txt.insert('end',f'  Empirical SD            = {esd:.8f}\n  Exact SD                = {tsd:.8f}\n\n')
            txt.insert('end','DEFINITIONS\n')
            txt.insert('end','  PMF: p(k)=P(X=k)\n  CDF: F(k)=P(X≤k)=Σ p(j), j≤k\n')
            txt.insert('end','  E[X]=Σ k p(k)\n  Var(X)=E[(X-E[X])²]\n\n')
            txt.insert('end','IMPORTANT\n')
            txt.insert('end','  เพราะการทดลองกำหนด Max steps ค่า moment ด้านบนเป็น conditional moments ของการถึงเป้าหมายภายใน horizon.\n')
            txt.insert('end','  failure/survival mass ถูกแยกไว้ ไม่ได้นำมาปลอมเป็นค่าของ X.')

        def render():
            render_hist(); render_pmf(); render_cdf(); render_moments()

        def animate():
            if not st['N']:run()
            if st.get('job'):
                try:self.after_cancel(st['job'])
                except Exception:pass
            k={'v':0}
            nb.select(ptab)
            def tick():
                k['v']+=2; render_pmf(min(1,k['v']/100))
                if k['v']<100:st['job']=self.after(35,tick)
                else:st['job']=None
            tick()

        actions=tk.Frame(ctl,bg='white'); actions.pack(fill='x',padx=18,pady=(0,12))
        ttk.Button(actions,text='▶ RUN DISTRIBUTION EXPERIMENT',style='Primary.TButton',command=run).pack(side='left')
        ttk.Button(actions,text='▶ Animate PMF Formation',command=animate).pack(side='left',padx=5)
        ttk.Button(actions,text='V3.5 Statistics',command=self.mcs_statistics_lab).pack(side='left')

        self.card(b,'MATHEMATICAL PROGRESSION',
            'V3.5: frequency / mean / variance / empirical probability → V3.6: random variable / histogram / PMF / CDF / expectation / variance '
            '/ empirical-vs-exact distribution. ขั้นต่อไป V3.7 เหมาะกับ Bernoulli/Binomial, indicator variables, covariance, '
            'Markov/Chebyshev bounds และ sampling เพื่อขยายจาก distribution หนึ่งตัวไปสู่ probability theory ที่เป็นระบบ')


    # ==================== V3.7: BINOMIAL THEORY VS EXPERIMENT ====================
    def binomial_compare_lab(self):
        self.clear()
        self.header('⚖ Binomial Distribution — Theory vs Experiment • V3.7',
            'Bernoulli Trials → Theoretical PMF → Monte Carlo → Error Analysis → E[X] / Var(X) → Convergence')
        b=self.scrollbody()
        self.card(b,'MATHEMATICAL MODEL',
            'ให้ X = จำนวน Success จาก Bernoulli trials ที่เป็นอิสระจำนวน n ครั้ง โดยแต่ละครั้งมี P(Success)=p. '
            'ทฤษฎีให้ X ~ Binomial(n,p) และ P(X=k)=C(n,k)p^k(1-p)^(n-k). '
            'V3.7 เปรียบเทียบสูตรนี้กับความถี่สัมพัทธ์จากการทดลอง Monte Carlo โดยตรง')

        ctl=self.card(b,'1 • PARAMETERS')
        nvar=tk.IntVar(value=10); pvar=tk.DoubleVar(value=.5); Nvar=tk.IntVar(value=2000)
        rows=[('n trials per experiment',nvar,1,50),('p success probability',pvar,0.01,.99),('Monte Carlo experiments',Nvar,100,20000)]
        labs=[]
        for title,var,lo,hi in rows:
            r=tk.Frame(ctl,bg='white'); r.pack(fill='x',padx=18,pady=4)
            tk.Label(r,text=title,width=25,anchor='w',bg='white').pack(side='left')
            if isinstance(var,tk.IntVar):
                ttk.Spinbox(r,from_=lo,to=hi,textvariable=var,width=10).pack(side='left',padx=8)
            else:
                ttk.Scale(r,from_=lo,to=hi,variable=var).pack(side='left',fill='x',expand=True,padx=8)
            ll=tk.Label(r,width=10,bg='white',fg=BLUE,font=('Consolas',9)); ll.pack(side='left'); labs.append((var,ll))

        nb=ttk.Notebook(b); nb.pack(fill='both',expand=True,padx=28,pady=10)
        cmp=tk.Frame(nb,bg='white'); err=tk.Frame(nb,bg='white'); mom=tk.Frame(nb,bg='white'); con=tk.Frame(nb,bg='white')
        nb.add(cmp,text='PMF Comparison'); nb.add(err,text='Error Analysis')
        nb.add(mom,text='Mean / Variance'); nb.add(con,text='Convergence')

        pcv=tk.Canvas(cmp,height=450,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1); pcv.pack(fill='both',expand=True,padx=12,pady=10)
        ecv=tk.Canvas(err,height=450,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1); ecv.pack(fill='both',expand=True,padx=12,pady=10)
        mtxt=tk.Text(mom,height=25,font=('Consolas',10),wrap='word'); mtxt.pack(fill='both',expand=True,padx=12,pady=10)
        ccv=tk.Canvas(con,height=450,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1); ccv.pack(fill='both',expand=True,padx=12,pady=10)

        status=tk.StringVar(value='กด RUN COMPARISON เพื่อเริ่มการทดลอง')
        tk.Label(b,textvariable=status,bg=BG,fg=MUTED,font=('Consolas',9),wraplength=1100,justify='left').pack(anchor='w',padx=30,pady=(0,8))
        st={'theory':[],'emp':[],'samples':[],'running_mean':[],'running_p0':[],'job':None}

        def choose(n,k): return math.comb(n,k)

        def run():
            try:n=max(1,min(50,int(nvar.get()))); p=min(.99,max(.01,float(pvar.get()))); N=max(100,min(20000,int(Nvar.get())))
            except Exception:
                messagebox.showerror('Input','กรุณาตรวจค่า n, p และจำนวน experiments'); return
            theory=[choose(n,k)*(p**k)*((1-p)**(n-k)) for k in range(n+1)]
            counts=[0]*(n+1); samples=[]; rm=[]; rp=[]; total=0; zero=0
            for i in range(1,N+1):
                x=sum(1 for _ in range(n) if random.random()<p)
                samples.append(x); counts[x]+=1; total+=x
                if x==0:zero+=1
                rm.append(total/i); rp.append(zero/i)
            emp=[c/N for c in counts]
            st.update(theory=theory,emp=emp,samples=samples,running_mean=rm,running_p0=rp)
            render_all()
            mae=sum(abs(emp[k]-theory[k]) for k in range(n+1))/(n+1)
            mx=max(abs(emp[k]-theory[k]) for k in range(n+1))
            status.set(f'n={n}  p={p:.3f}  N={N} • mean absolute PMF error={mae:.6f} • max error={mx:.6f}')

        def base_axes(cv,title):
            cv.delete('all'); w=max(cv.winfo_width(),780); h=max(cv.winfo_height(),420); pad=58
            cv.create_line(pad,h-pad,w-pad,h-pad,fill='#94a3b8'); cv.create_line(pad,25,pad,h-pad,fill='#94a3b8')
            cv.create_text(pad,18,anchor='w',text=title,fill=TEXT,font=('Segoe UI Semibold',10))
            return w,h,pad

        def render_pmf(progress=1.0):
            n=nvar.get(); w,h,pad=base_axes(pcv,'Binomial PMF: theoretical probability vs empirical relative frequency')
            ymax=max(st['theory']+st['emp']+[.01])*1.18 if st['theory'] else 1
            upto=max(0,min(n,int(n*progress)))
            group=(w-2*pad)/(n+1); bw=group*.28
            for k in range(upto+1):
                t=st['theory'][k]; e=st['emp'][k]; cx=pad+(k+.5)*group
                pcv.create_rectangle(cx-bw,h-pad-t/ymax*(h-2*pad),cx,h-pad,fill='#dcfce7',outline=GREEN)
                pcv.create_rectangle(cx,h-pad-e/ymax*(h-2*pad),cx+bw,h-pad,fill='#dbeafe',outline=BLUE)
                if n<=25 or k%5==0:pcv.create_text(cx,h-pad+15,text=str(k),fill=MUTED,font=('Segoe UI',8))
            pcv.create_text(w-pad,18,anchor='e',text='theory | experiment',fill=TEXT,font=('Segoe UI',9))

        def render_error():
            n=nvar.get(); w,h,pad=base_axes(ecv,'Absolute error | empirical PMF − theoretical PMF |')
            errs=[abs(st['emp'][k]-st['theory'][k]) for k in range(n+1)] if st['theory'] else []
            ymax=max(errs+[.001])*1.15; group=(w-2*pad)/(n+1); bw=group*.58
            for k,e in enumerate(errs):
                cx=pad+(k+.5)*group; bh=e/ymax*(h-2*pad)
                ecv.create_rectangle(cx-bw/2,h-pad-bh,cx+bw/2,h-pad,fill='#fef3c7',outline=ORANGE)
                if n<=25 or k%5==0:ecv.create_text(cx,h-pad+15,text=str(k),fill=MUTED,font=('Segoe UI',8))

        def render_moments():
            n=nvar.get(); p=pvar.get(); xs=st['samples']; N=len(xs)
            tmean=n*p; tvar=n*p*(1-p); tsd=math.sqrt(tvar)
            emean=sum(xs)/N if N else 0
            evar=sum((x-emean)**2 for x in xs)/N if N else 0; esd=math.sqrt(evar)
            mtxt.delete('1.0','end')
            mtxt.insert('end','BINOMIAL THEORETICAL MOMENTS\n\n')
            mtxt.insert('end',f'E[X] = np = {n}×{p:.5f} = {tmean:.8f}\n')
            mtxt.insert('end',f'Var(X) = np(1-p) = {tvar:.8f}\nSD(X) = sqrt(Var) = {tsd:.8f}\n\n')
            mtxt.insert('end','MONTE CARLO SAMPLE MOMENTS\n\n')
            mtxt.insert('end',f'Empirical mean     = {emean:.8f}   error={emean-tmean:+.8f}\n')
            mtxt.insert('end',f'Empirical variance = {evar:.8f}   error={evar-tvar:+.8f}\n')
            mtxt.insert('end',f'Empirical SD       = {esd:.8f}   error={esd-tsd:+.8f}\n\n')
            if st['theory']:
                mae=sum(abs(st['emp'][k]-st['theory'][k]) for k in range(n+1))/(n+1)
                rmse=math.sqrt(sum((st['emp'][k]-st['theory'][k])**2 for k in range(n+1))/(n+1))
                mtxt.insert('end',f'PMF MAE  = {mae:.8f}\nPMF RMSE = {rmse:.8f}\n\n')
            mtxt.insert('end','INTERPRETATION\n')
            mtxt.insert('end','เมื่อจำนวน Monte Carlo experiments เพิ่มขึ้น relative frequency โดยทั่วไปจะเข้าใกล้ theoretical probability มากขึ้น '
                              'แต่การทดลองแต่ละครั้งยังมี sampling variation.')

        def render_conv(progress=1.0):
            w,h,pad=base_axes(ccv,'Convergence of sample mean toward theoretical E[X] = np')
            data=st['running_mean']
            if not data:return
            upto=max(2,min(len(data),int(len(data)*progress))); n=nvar.get(); target=n*pvar.get()
            ymax=max(max(data[:upto])+1,target+1,1); pts=[]
            for i,y in enumerate(data[:upto]):
                x=pad+(w-2*pad)*(i/max(1,len(data)-1)); py=h-pad-y/ymax*(h-2*pad); pts += [x,py]
            if len(pts)>=4:ccv.create_line(*pts,fill=BLUE,width=2)
            ty=h-pad-target/ymax*(h-2*pad); ccv.create_line(pad,ty,w-pad,ty,fill=ORANGE,dash=(5,4))
            ccv.create_text(w-pad,ty-10,anchor='e',text=f'theoretical mean={target:.4f}',fill=ORANGE,font=('Consolas',9))

        def render_all():
            for v,ll in labs:
                try:ll.config(text=f'{v.get():.3f}' if isinstance(v,tk.DoubleVar) else str(v.get()))
                except Exception:pass
            render_pmf(); render_error(); render_moments(); render_conv()

        def animate_compare():
            if not st['theory']:run()
            if st.get('job'):
                try:self.after_cancel(st['job'])
                except Exception:pass
            nb.select(cmp); k={'v':0}
            def tick():
                k['v']+=3; render_pmf(min(1,k['v']/100))
                if k['v']<100:st['job']=self.after(40,tick)
                else:st['job']=None
            tick()

        def animate_convergence():
            if not st['theory']:run()
            if st.get('job'):
                try:self.after_cancel(st['job'])
                except Exception:pass
            nb.select(con); k={'v':0}
            def tick():
                k['v']+=2; render_conv(min(1,k['v']/100))
                if k['v']<100:st['job']=self.after(35,tick)
                else:st['job']=None
            tick()

        act=tk.Frame(ctl,bg='white'); act.pack(fill='x',padx=18,pady=(0,12))
        ttk.Button(act,text='▶ RUN COMPARISON',style='Primary.TButton',command=run).pack(side='left')
        ttk.Button(act,text='▶ PMF Compare Animation',command=animate_compare).pack(side='left',padx=5)
        ttk.Button(act,text='▶ Mean Convergence',command=animate_convergence).pack(side='left')
        ttk.Button(act,text='V3.6 PMF/CDF',command=self.random_variable_distribution_lab).pack(side='left',padx=5)

        self.card(b,'NEXT MATHEMATICAL STEP',
            'V3.7 เน้น “Theory vs Experiment” ก่อนตามที่กำหนด. ขั้นต่อไป V3.8 จะใช้ Bernoulli/Indicator Variables เป็นฐาน '
            'เพื่ออธิบาย linearity of expectation, covariance/correlation และ dependence/independence '
            'พร้อมทดลองข้อมูลคู่และเปรียบเทียบค่าทฤษฎีกับค่าจาก simulation')


    # ==================== V3.8: INDICATORS / COVARIANCE + C PROGRAM ARCHIVE ====================
    def indicator_covariance_lab(self):
        self.clear()
        self.header('🔗 Indicator Variables → Covariance / Correlation • V3.8',
            'Theory vs Experiment: Bernoulli indicators, joint variables, independence/dependence and correlation')
        b=self.scrollbody()
        self.card(b,'MATHEMATICAL IDEA',
            'ให้ I และ J เป็น indicator variables (0 หรือ 1). ทดลองเปลี่ยน P(I=1), P(J=1|I=1), P(J=1|I=0). '
            'ระบบคำนวณ joint distribution แบบทฤษฎี แล้วสุ่มข้อมูลเพื่อเปรียบเทียบ E[I], E[J], E[IJ], Cov(I,J) และ Corr(I,J).')

        ctl=self.card(b,'1 • JOINT BERNOULLI MODEL')
        pi=tk.DoubleVar(value=.50); q1=tk.DoubleVar(value=.80); q0=tk.DoubleVar(value=.20); N=tk.IntVar(value=5000)
        labels=[]
        for title,var,lo,hi in [('P(I=1)',pi,.01,.99),('P(J=1 | I=1)',q1,.01,.99),('P(J=1 | I=0)',q0,.01,.99)]:
            r=tk.Frame(ctl,bg='white'); r.pack(fill='x',padx=18,pady=3)
            tk.Label(r,text=title,width=22,anchor='w',bg='white').pack(side='left')
            ttk.Scale(r,from_=lo,to=hi,variable=var).pack(side='left',fill='x',expand=True,padx=8)
            ll=tk.Label(r,width=8,bg='white',fg=BLUE,font=('Consolas',9)); ll.pack(side='left'); labels.append((var,ll))
        r=tk.Frame(ctl,bg='white'); r.pack(fill='x',padx=18,pady=3)
        tk.Label(r,text='Monte Carlo samples',width=22,anchor='w',bg='white').pack(side='left')
        ttk.Spinbox(r,from_=100,to=30000,increment=100,textvariable=N,width=10).pack(side='left',padx=8)

        nb=ttk.Notebook(b); nb.pack(fill='both',expand=True,padx=28,pady=10)
        jt=tk.Frame(nb,bg='white'); ct=tk.Frame(nb,bg='white'); st=tk.Frame(nb,bg='white')
        nb.add(jt,text='Joint Distribution'); nb.add(ct,text='Theory vs Experiment'); nb.add(st,text='Scatter / Dependence')
        jcv=tk.Canvas(jt,height=430,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1); jcv.pack(fill='both',expand=True,padx=12,pady=10)
        txt=tk.Text(ct,height=25,font=('Consolas',10),wrap='word'); txt.pack(fill='both',expand=True,padx=12,pady=10)
        scv=tk.Canvas(st,height=430,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1); scv.pack(fill='both',expand=True,padx=12,pady=10)
        status=tk.StringVar(value='กด RUN THEORY vs EXPERIMENT')
        tk.Label(b,textvariable=status,bg=BG,fg=MUTED,font=('Consolas',9)).pack(anchor='w',padx=30,pady=(0,8))
        state={'pairs':[],'theory':{},'emp':{}}

        def corr_from_moments(ei,ej,eij):
            cov=eij-ei*ej; vi=ei*(1-ei); vj=ej*(1-ej)
            cor=cov/math.sqrt(vi*vj) if vi>0 and vj>0 else 0
            return cov,cor

        def run():
            p=pi.get(); a=q1.get(); z=q0.get(); ns=max(100,min(30000,int(N.get())))
            th={(1,1):p*a,(1,0):p*(1-a),(0,1):(1-p)*z,(0,0):(1-p)*(1-z)}
            counts={k:0 for k in th}; pairs=[]
            for _ in range(ns):
                i=1 if random.random()<p else 0
                pj=a if i else z; j=1 if random.random()<pj else 0
                counts[(i,j)]+=1; pairs.append((i,j))
            emp={k:counts[k]/ns for k in counts}
            state.update(pairs=pairs,theory=th,emp=emp); render()
            tcov,tcor=corr_from_moments(p,th[(1,1)]+th[(0,1)],th[(1,1)])
            status.set(f'N={ns} • theoretical Cov={tcov:.6f} • theoretical Corr={tcor:.6f}')

        def render_joint():
            jcv.delete('all'); w=max(jcv.winfo_width(),760); h=max(jcv.winfo_height(),400)
            cells=[((0,0),120,240),((0,1),360,240),((1,0),120,90),((1,1),360,90)]
            for key,x,y in cells:
                t=state['theory'].get(key,0); e=state['emp'].get(key,0)
                jcv.create_rectangle(x,y,x+180,y+100,fill='#f8fafc',outline=BLUE,width=2)
                jcv.create_text(x+90,y+22,text=f'I={key[0]}, J={key[1]}',fill=TEXT,font=('Segoe UI Semibold',10))
                jcv.create_text(x+90,y+50,text=f'Theory = {t:.5f}',fill=GREEN,font=('Consolas',9))
                jcv.create_text(x+90,y+73,text=f'Experiment = {e:.5f}',fill=BLUE,font=('Consolas',9))
            jcv.create_text(600,80,anchor='w',text='Independence condition:',fill=TEXT,font=('Segoe UI Semibold',10))
            jcv.create_text(600,110,anchor='w',text='P(J=1|I=1) = P(J=1|I=0)',fill=MUTED,font=('Consolas',9))

        def render_text():
            th=state['theory']; em=state['emp']
            if not th:return
            tei=th[(1,0)]+th[(1,1)]; tej=th[(0,1)]+th[(1,1)]; teij=th[(1,1)]
            eei=em[(1,0)]+em[(1,1)]; eej=em[(0,1)]+em[(1,1)]; eeij=em[(1,1)]
            tcov,tcor=corr_from_moments(tei,tej,teij); ecov,ecor=corr_from_moments(eei,eej,eeij)
            txt.delete('1.0','end')
            txt.insert('end','INDICATOR VARIABLES\n  I,J ∈ {0,1} and E[I]=P(I=1)\n\n')
            txt.insert('end',f'THEORY\n  E[I]={tei:.8f}\n  E[J]={tej:.8f}\n  E[IJ]={teij:.8f}\n')
            txt.insert('end',f'  Cov(I,J)=E[IJ]-E[I]E[J] = {tcov:.8f}\n  Corr(I,J) = {tcor:.8f}\n\n')
            txt.insert('end',f'EXPERIMENT\n  mean(I)={eei:.8f}\n  mean(J)={eej:.8f}\n  mean(IJ)={eeij:.8f}\n')
            txt.insert('end',f'  sample-style population Cov={ecov:.8f}\n  Corr={ecor:.8f}\n\n')
            txt.insert('end','LINEARITY OF EXPECTATION\n  E[I+J] = E[I] + E[J] ไม่จำเป็นต้องให้ I,J independent.\n')
            txt.insert('end',f'  Theory: {tei+tej:.8f}    Experiment: {eei+eej:.8f}\n\n')
            txt.insert('end','DEPENDENCE CHECK\n')
            txt.insert('end',f'  P(J=1|I=1)={q1.get():.5f}, P(J=1|I=0)={q0.get():.5f}\n')
            txt.insert('end','  ถ้าสองค่านี้เท่ากันในโมเดลนี้ I และ J เป็น independent; ถ้าต่างกันจะเกิด dependence.')

        def render_scatter():
            scv.delete('all'); w=max(scv.winfo_width(),760); h=max(scv.winfo_height(),400); pad=70
            scv.create_line(pad,h-pad,w-pad,h-pad,fill='#94a3b8'); scv.create_line(pad,30,pad,h-pad,fill='#94a3b8')
            # show counts at four binary coordinate locations; jitter-free so count labels remain mathematical.
            counts={(0,0):0,(0,1):0,(1,0):0,(1,1):0}
            for q in state['pairs']:counts[q]+=1
            for (i,j),c in counts.items():
                x=pad+i*(w-2*pad); y=h-pad-j*(h-2*pad)
                r=min(42,8+math.sqrt(c)*.35)
                scv.create_oval(x-r,y-r,x+r,y+r,fill='#dbeafe',outline=BLUE,width=2)
                scv.create_text(x,y,text=str(c),fill=TEXT,font=('Consolas',9))
            scv.create_text(w/2,h-20,text='I',fill=TEXT); scv.create_text(20,h/2,text='J',fill=TEXT)

        def render():
            for v,ll in labels:ll.config(text=f'{v.get():.3f}')
            render_joint(); render_text(); render_scatter()

        act=tk.Frame(ctl,bg='white'); act.pack(fill='x',padx=18,pady=(0,12))
        ttk.Button(act,text='▶ RUN THEORY vs EXPERIMENT',style='Primary.TButton',command=run).pack(side='left')
        ttk.Button(act,text='V3.7 Binomial Compare',command=self.binomial_compare_lab).pack(side='left',padx=5)
        ttk.Button(act,text='C Program Math Archive',command=self.cprog_math_archive_lab).pack(side='left')
        self.card(b,'NEXT',
            'V3.9 เหมาะกับ Markov inequality → Chebyshev inequality → sampling bounds แล้วเปรียบเทียบ bound ทางทฤษฎีกับ tail probability จาก simulation.')

    def cprog_math_archive_lab(self):
        self.clear()
        self.header('💾 C Program Math Archive • cprog-ok → V3.8',
            'จัดตัวอย่าง C Programming เดิมให้ตรงกับหัวข้อคณิตศาสตร์/Probability/Simulation โดยไม่เปลี่ยนความหมายของ source')
        b=self.scrollbody()
        self.card(b,'SOURCE ARCHIVE SUMMARY',
            'cprog-ok.zip มีไฟล์ C/H และโปรแกรม DOS/graphics หลายชุด (S26–S53). '
            'V3.8 ใช้ source เหล่านี้เป็น “historical programming examples” และจัดเข้าหมวดตามสิ่งที่พบใน code เช่น random(), loops, arrays, structs และ graphics. '
            'ไม่ได้อ้างว่าโปรแกรมเดิมสอน covariance โดยตรง; การเชื่อมกับ MCS เป็นชั้นการเรียนรู้ที่ AI Learning Studio เพิ่มให้')
        data=[('cprog-ok/S26/TETRIS.C', ['random', 'loop', 'struct', 'array', 'graphics']), ('cprog-ok/S27/ATOM.C', ['random', 'loop', 'struct', 'array', 'graphics']), ('cprog-ok/S28/WORM.C', ['random', 'loop', 'struct', 'array', 'graphics']), ('cprog-ok/S29/TREEROAD.C', ['random', 'loop', 'struct', 'array', 'graphics']), ('cprog-ok/S30/BIGTEXT.C', ['random', 'loop', 'struct', 'array', 'graphics']), ('cprog-ok/S32/BLOCKOUT.C', ['random', 'loop', 'array', 'graphics']), ('cprog-ok/S33/BOMBER.C', ['random', 'loop', 'struct', 'array', 'graphics']), ('cprog-ok/S36/TEST24.C', ['random', 'loop', 'struct', 'array', 'graphics']), ('cprog-ok/S37/BALLTRIS.C', ['random', 'loop', 'struct', 'array', 'graphics']), ('cprog-ok/S38/VESA.C', ['random', 'loop', 'array', 'graphics']), ('cprog-ok/S39/DINOSTAR.C', ['random', 'loop', 'struct', 'array', 'graphics']), ('cprog-ok/S40/FIREWORK.C', ['random', 'loop', 'array', 'graphics'])]
        box=self.card(b,'C SOURCE EXAMPLES MATCHED TO V3.8')
        tree=ttk.Treeview(box,columns=('file','math'),show='headings',height=14)
        tree.heading('file',text='C source'); tree.heading('math',text='Detected concepts → learning connection')
        tree.column('file',width=300); tree.column('math',width=620)
        tree.pack(fill='both',expand=True,padx=14,pady=10)
        for fn,tags in data:
            conn=[]
            if 'random' in tags:conn.append('random sampling / Monte Carlo idea')
            if 'loop' in tags:conn.append('repeated trials / iteration')
            if 'array' in tags:conn.append('data collection / frequency table')
            if 'struct' in tags:conn.append('structured state / random-variable record')
            if 'graphics' in tags:conn.append('visualization / animation')
            tree.insert('', 'end', values=(fn.replace('cprog-ok/',''), ', '.join(conn)))
        self.card(b,'HOW IT FITS',
            'ตัวอย่างที่มี random + loop เหมาะสำหรับอธิบายการสุ่มซ้ำและ empirical probability; array เหมาะกับการเก็บ counts/samples; '
            'struct เหมาะกับการอธิบาย state; graphics เหมาะกับการแปลงข้อมูลคณิตศาสตร์เป็น visualization. '
            'เนื้อหา Probability/Covariance ใน V3.8 ยังคำนวณด้วยโมเดลคณิตศาสตร์ของ Studio เพื่อให้ตรวจ Theory vs Experiment ได้ชัดเจน')
        ttk.Button(b,text='เปิด Indicator + Covariance Lab',style='Primary.TButton',command=self.indicator_covariance_lab).pack(anchor='w',padx=30,pady=12)


    # ==================== V3.9: PROBABILITY BOUNDS + C SOURCE TO MATH ====================
    def markov_chebyshev_compare_lab(self):
        self.clear()
        self.header('📐 Markov vs Chebyshev — Theory vs Simulation • V3.9',
            'Probability bounds: observe actual tail probability, then compare with mathematical upper bounds')
        b=self.scrollbody()
        self.card(b,'WHY COMPARE?',
            'Markov ใช้กับตัวแปรสุ่มไม่ติดลบและใช้เพียง E[X]. Chebyshev ใช้ mean และ variance เพื่อ bound '
            'P(|X-μ|≥a). ใน Lab นี้ใช้ Exponential random variable เพื่อให้ X≥0 และมี mean/variance ที่ทราบแน่นอน '
            'จากนั้นเปรียบเทียบ actual/theoretical tail, Monte Carlo estimate และ bounds')

        ctl=self.card(b,'1 • PARAMETERS')
        mu=tk.DoubleVar(value=2.0); ath=tk.DoubleVar(value=4.0); dev=tk.DoubleVar(value=2.0); N=tk.IntVar(value=10000)
        specs=[('Mean μ of Exponential X',mu,.2,6.0),('Markov threshold t',ath,.2,12.0),('Chebyshev deviation a',dev,.2,8.0)]
        labs=[]
        for title,var,lo,hi in specs:
            r=tk.Frame(ctl,bg='white'); r.pack(fill='x',padx=18,pady=3)
            tk.Label(r,text=title,width=28,anchor='w',bg='white').pack(side='left')
            ttk.Scale(r,from_=lo,to=hi,variable=var).pack(side='left',fill='x',expand=True,padx=8)
            ll=tk.Label(r,width=9,bg='white',fg=BLUE,font=('Consolas',9)); ll.pack(side='left'); labs.append((var,ll))
        r=tk.Frame(ctl,bg='white'); r.pack(fill='x',padx=18,pady=3)
        tk.Label(r,text='Monte Carlo samples',width=28,anchor='w',bg='white').pack(side='left')
        ttk.Spinbox(r,from_=500,to=50000,increment=500,textvariable=N,width=10).pack(side='left',padx=8)

        nb=ttk.Notebook(b); nb.pack(fill='both',expand=True,padx=28,pady=10)
        mt=tk.Frame(nb,bg='white'); ct=tk.Frame(nb,bg='white'); et=tk.Frame(nb,bg='white')
        nb.add(mt,text='Markov Comparison'); nb.add(ct,text='Chebyshev Comparison'); nb.add(et,text='Equations + Error')
        mcv=tk.Canvas(mt,height=430,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1); mcv.pack(fill='both',expand=True,padx=12,pady=10)
        ccv=tk.Canvas(ct,height=430,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1); ccv.pack(fill='both',expand=True,padx=12,pady=10)
        txt=tk.Text(et,height=25,font=('Consolas',10),wrap='word'); txt.pack(fill='both',expand=True,padx=12,pady=10)
        status=tk.StringVar(value='กด RUN BOUND COMPARISON')
        tk.Label(b,textvariable=status,bg=BG,fg=MUTED,font=('Consolas',9)).pack(anchor='w',padx=30,pady=(0,8))
        st={}

        def bar_chart(cv,title,items):
            cv.delete('all'); w=max(cv.winfo_width(),760); h=max(cv.winfo_height(),400); pad=60
            cv.create_line(pad,h-pad,w-pad,h-pad,fill='#94a3b8')
            ymax=max([v for _,v in items]+[1e-6])*1.15; group=(w-2*pad)/len(items); bw=group*.55
            cv.create_text(pad,18,anchor='w',text=title,fill=TEXT,font=('Segoe UI Semibold',10))
            for i,(name,v) in enumerate(items):
                cx=pad+(i+.5)*group; bh=v/ymax*(h-2*pad)
                cv.create_rectangle(cx-bw/2,h-pad-bh,cx+bw/2,h-pad,fill='#dbeafe',outline=BLUE,width=2)
                cv.create_text(cx,h-pad+18,text=name,fill=TEXT,font=('Segoe UI',9))
                cv.create_text(cx,h-pad-bh-12,text=f'{v:.5f}',fill=TEXT,font=('Consolas',9))

        def run():
            m=max(.001,mu.get()); t=max(.001,ath.get()); a=max(.001,dev.get()); ns=max(500,min(50000,int(N.get())))
            # inverse-CDF exponential sampling with mean m
            xs=[-m*math.log(max(1e-15,1-random.random())) for _ in range(ns)]
            mark_emp=sum(x>=t for x in xs)/ns
            mark_actual=math.exp(-t/m)
            mark_bound=min(1,m/t)
            # For exponential: Var(X)=m^2. Exact two-sided tail around mean.
            lo=max(0,m-a); hi=m+a
            p_lo=(1-math.exp(-lo/m)) if lo>0 else 0.0
            p_hi=math.exp(-hi/m)
            chev_actual=p_lo+p_hi
            chev_emp=sum(abs(x-m)>=a for x in xs)/ns
            chev_bound=min(1,(m*m)/(a*a))
            st.update(mark_emp=mark_emp,mark_actual=mark_actual,mark_bound=mark_bound,
                      chev_emp=chev_emp,chev_actual=chev_actual,chev_bound=chev_bound,
                      sample_mean=sum(xs)/ns,sample_var=sum((x-sum(xs)/ns)**2 for x in xs)/ns,
                      m=m,t=t,a=a,ns=ns)
            render()
            status.set(f'N={ns} • Markov actual={mark_actual:.5f} ≤ bound={mark_bound:.5f} • '
                       f'Chebyshev actual={chev_actual:.5f} ≤ bound={chev_bound:.5f}')

        def render():
            for v,ll in labs:ll.config(text=f'{v.get():.3f}')
            if not st:return
            bar_chart(mcv,'P(X ≥ t): actual vs simulation vs Markov upper bound',
                      [('Actual',st['mark_actual']),('Simulation',st['mark_emp']),('Markov bound',st['mark_bound'])])
            bar_chart(ccv,'P(|X-μ| ≥ a): actual vs simulation vs Chebyshev upper bound',
                      [('Actual',st['chev_actual']),('Simulation',st['chev_emp']),('Chebyshev bound',st['chev_bound'])])
            txt.delete('1.0','end')
            txt.insert('end','MARKOV INEQUALITY\n  For X ≥ 0: P(X ≥ t) ≤ E[X]/t\n')
            txt.insert('end',f'  E[X]=μ={st["m"]:.6f}, t={st["t"]:.6f}\n')
            txt.insert('end',f'  Exact tail={st["mark_actual"]:.8f}  Simulation={st["mark_emp"]:.8f}  Bound={st["mark_bound"]:.8f}\n\n')
            txt.insert('end','CHEBYSHEV INEQUALITY\n  P(|X-μ| ≥ a) ≤ Var(X)/a²\n')
            txt.insert('end',f'  For exponential Var(X)=μ²={st["m"]**2:.8f}, a={st["a"]:.6f}\n')
            txt.insert('end',f'  Exact tail={st["chev_actual"]:.8f}  Simulation={st["chev_emp"]:.8f}  Bound={st["chev_bound"]:.8f}\n\n')
            txt.insert('end','SAMPLE CHECK\n')
            txt.insert('end',f'  sample mean={st["sample_mean"]:.8f} vs theory μ={st["m"]:.8f}\n')
            txt.insert('end',f'  sample variance={st["sample_var"]:.8f} vs theory μ²={st["m"]**2:.8f}\n\n')
            txt.insert('end','KEY IDEA\n  Bound ไม่จำเป็นต้องเท่ากับ actual probability; หน้าที่คือให้ขอบเขตบนที่รับประกันภายใต้เงื่อนไขของ theorem.')

        act=tk.Frame(ctl,bg='white'); act.pack(fill='x',padx=18,pady=(0,12))
        ttk.Button(act,text='▶ RUN BOUND COMPARISON',style='Primary.TButton',command=run).pack(side='left')
        ttk.Button(act,text='C Source → Math',command=self.c_source_math_concepts_lab).pack(side='left',padx=5)
        ttk.Button(act,text='V3.8 Indicator/Covariance',command=self.indicator_covariance_lab).pack(side='left')
        self.card(b,'MATHEMATICAL SEQUENCE',
            'V3.7 Binomial comparison → V3.8 indicators/covariance → V3.9 Markov/Chebyshev bounds. '
            'ลำดับนี้ทำให้นักเรียนเห็น distribution และ moments ก่อนเรียนว่าค่า moments สามารถควบคุม tail probability ได้อย่างไร')

    def c_source_math_concepts_lab(self):
        self.clear()
        self.header('🧮 C Source → Mathematical Concepts • V3.9',
            'Source evidence → programming structure → mathematical interpretation → modern simulation')
        b=self.scrollbody()
        self.card(b,'GROUNDING RULE',
            'รายการนี้จัดหมวดจากสิ่งที่ตรวจพบใน source cprog-ok จริง เช่น random(), loop, array, struct และ graphics primitives. '
            'คำว่า “Math connection” คือการตีความเพื่อการสอนของ AI Learning Studio ไม่ได้หมายความว่า source C ต้นฉบับประกาศ theorem เหล่านี้ไว้')
        data=[('INTERRUP/INTERRUP.C', ['Iteration / sequences', 'Arrays / indexed data']), ('S26/GRAPH.C', ['Iteration / sequences', 'Arrays / indexed data', 'Structured state', 'Coordinate geometry / visualization']), ('S26/TETRIS.C', ['Random sampling / empirical probability', 'Iteration / sequences', 'Arrays / indexed data', 'Structured state', 'Coordinate geometry / visualization']), ('S27/ATOM.C', ['Random sampling / empirical probability', 'Iteration / sequences', 'Arrays / indexed data', 'Structured state', 'Coordinate geometry / visualization']), ('S28/WORM.C', ['Random sampling / empirical probability', 'Iteration / sequences', 'Arrays / indexed data', 'Structured state', 'Coordinate geometry / visualization']), ('S29/TREEROAD.C', ['Random sampling / empirical probability', 'Iteration / sequences', 'Arrays / indexed data', 'Structured state', 'Coordinate geometry / visualization']), ('S30/BIGTEXT.C', ['Random sampling / empirical probability', 'Iteration / sequences', 'Arrays / indexed data', 'Structured state', 'Coordinate geometry / visualization']), ('S31/CUTSCENE.C', ['Iteration / sequences', 'Arrays / indexed data', 'Structured state']), ('S32/BLOCKOUT.C', ['Random sampling / empirical probability', 'Iteration / sequences', 'Arrays / indexed data', 'Coordinate geometry / visualization']), ('S32/LIBGRAPH.C', ['Iteration / sequences', 'Arrays / indexed data', 'Coordinate geometry / visualization']), ('S33/BOMBER.C', ['Random sampling / empirical probability', 'Iteration / sequences', 'Arrays / indexed data', 'Structured state']), ('S34/IMAGE00.C', ['Arrays / indexed data']), ('S38/LIBVESA.C', ['Iteration / sequences']), ('S38/VESA.C', ['Random sampling / empirical probability', 'Iteration / sequences', 'Arrays / indexed data'])]
        box=self.card(b,'SOURCE → CONCEPT MAP')
        tree=ttk.Treeview(box,columns=('src','evidence','math'),show='headings',height=17)
        tree.heading('src',text='C source'); tree.heading('evidence',text='Detected source structure'); tree.heading('math',text='Mathematical learning connection')
        tree.column('src',width=230); tree.column('evidence',width=320); tree.column('math',width=480)
        tree.pack(fill='both',expand=True,padx=14,pady=10)
        for fn,cs in data:
            ev=[]; mc=[]
            for c in cs:
                if c.startswith('Random'): ev.append('random()'); mc.append('sampling / empirical probability')
                elif c.startswith('Iteration'): ev.append('for/while'); mc.append('sequences / repeated trials')
                elif c.startswith('Arrays'): ev.append('array'); mc.append('vectors, indexed samples, frequency')
                elif c.startswith('Structured'): ev.append('struct'); mc.append('state variables / sample records')
                elif c.startswith('Coordinate'): ev.append('graphics primitives'); mc.append('coordinate geometry / visualization')
            tree.insert('', 'end', values=(fn,', '.join(ev),', '.join(mc)))

        self.card(b,'TEACHING PIPELINE',
            'C Source → identify loop/random/data/geometry/state → formulate a mathematical variable or experiment → '
            'write formula → reproduce with Python simulation → compare theoretical result with empirical result → visualization/animation. '
            'ตัวอย่างเช่น source ที่มี random()+loop สามารถใช้ตั้งคำถามเรื่อง frequency และ probability; '
            'source ที่มี graphics primitives ใช้เชื่อม coordinate geometry และ transformations')
        self.card(b,'IMPORTANT DISTINCTION',
            'Markov และ Chebyshev ใน V3.9 มาจากเส้นทาง MCS/Probability ของ Studio; '
            'source C ใช้เป็นตัวอย่าง programming structure ที่เชื่อมไปสู่การทดลองคณิตศาสตร์ ไม่ได้ใช้เป็นหลักฐานว่าตัวโปรแกรม C เดิมพิสูจน์ inequalities เหล่านี้')
        r=tk.Frame(b,bg=BG); r.pack(fill='x',padx=30,pady=12)
        ttk.Button(r,text='เปิด Markov vs Chebyshev',style='Primary.TButton',command=self.markov_chebyshev_compare_lab).pack(side='left')
        ttk.Button(r,text='C Program Archive V3.8',command=self.cprog_math_archive_lab).pack(side='left',padx=5)


    # ==================== V4.0: MATH-FIRST AUTOMATIC C SOURCE SELECTION ====================
    def v40_auto_c_math_lab(self):
        self.clear()
        self.header('🧠 V4.0 • Auto C Source → Mathematics',
            'caimath.zip + tc.zip → automatic evidence scan → mathematical ranking → model/formula → experiment')
        b=self.scrollbody()
        self.card(b,'MATH FIRST',
            'V4.0 ไม่เลือก source จากชื่อไฟล์อย่างเดียว แต่ให้คะแนนจากโครงสร้างที่พบใน source เช่น sin/cos/tan, sqrt/pow, '
            'random(), graphics coordinates, numeric types, loops และ operators. จากนั้นจึงเสนอ “Math connection” '
            'เพื่อให้นักเรียนเริ่มจากแนวคิดคณิตศาสตร์ก่อน แล้วค่อยย้อนกลับไปอ่าน C/TC code')

        catalog=[('caimath', 'caimath/MAIN.PAS', 15, ['random', 'coordinate geometry', 'arrays'], 755), ('caimath', 'caimath/ELLIPSEX.PAS', 14, ['sqrt/power', 'coordinate geometry', 'arrays'], 618), ('caimath', 'caimath/ELLIPSEY.PAS', 14, ['sqrt/power', 'coordinate geometry', 'arrays'], 610), ('caimath', 'caimath/START.PAS', 14, ['trigonometry', 'coordinate geometry'], 365), ('caimath', 'caimath/CIRCLE.PAS', 10, ['coordinate geometry', 'arrays'], 524), ('caimath', 'caimath/COMPARE.PAS', 10, ['coordinate geometry', 'arrays'], 828), ('caimath', 'caimath/KVGA.PAS', 10, ['coordinate geometry', 'arrays'], 265), ('caimath', 'caimath/PARAX.PAS', 10, ['coordinate geometry', 'arrays'], 663), ('caimath', 'caimath/PARAY.PAS', 10, ['coordinate geometry', 'arrays'], 673), ('caimath', 'caimath/YJJSVGA.PAS', 10, ['coordinate geometry', 'arrays'], 266), ('caimath', 'caimath/YJJVGA.PAS', 10, ['coordinate geometry', 'arrays'], 828), ('caimath', 'caimath/COEY.PAS', 9, ['sqrt/power', 'coordinate geometry'], 141), ('caimath', 'caimath/COPARAX.PAS', 9, ['coordinate geometry'], 164), ('caimath', 'caimath/COPARAY.PAS', 9, ['coordinate geometry'], 129), ('caimath', 'caimath/PREVIEW.PAS', 7, ['coordinate geometry', 'arrays'], 274), ('caimath', 'caimath/KFADE.PAS', 6, ['arrays'], 82), ('caimath', 'caimath/CELLIPSE.PAS', 5, ['coordinate geometry'], 132), ('caimath', 'caimath/COCIRCLE.PAS', 5, ['coordinate geometry'], 91), ('caimath', 'caimath/COEX.PAS', 5, ['coordinate geometry'], 132), ('caimath', 'caimath/HELP.PAS', 0, [], 14), ('tc', 'tc/EXAMPLES/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1401), ('tc', 'tc/Project/Bin/BGI/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1404), ('tc', 'tc/Project/Children/BGI/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1404), ('tc', 'tc/Project/Children/TC3/BGI/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1404), ('tc', 'tc/Project/ClothLine/BGI/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1404), ('tc', 'tc/Project/Roof/BGI/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1404), ('tc', 'tc/Project/Roof/TC/BGI/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1404), ('tc', 'tc/TC/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1401), ('tc', 'tc/TC/c/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1401), ('tc', 'tc/TC/cprog/S26/TETRIS.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 286), ('tc', 'tc/TC/cprog/S27/ATOM.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 257), ('tc', 'tc/TC/EXAMP/Project/BGI/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1404), ('tc', 'tc/TC/port/control2/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1401), ('tc', 'tc/TC/Project/Bin/BGI/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1404), ('tc', 'tc/TC/Project/Children/BGI/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1404), ('tc', 'tc/TC/Project/Children/TC3/BGI/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1404), ('tc', 'tc/TC/Project/ClothLine/BGI/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1404), ('tc', 'tc/TC/Project/Roof/BGI/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1404), ('tc', 'tc/TC/Project/Roof/TC/BGI/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1404), ('tc', 'tc/TC/S26/TETRIS.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 286), ('tc', 'tc/TC/S27/ATOM.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 257), ('tc', 'tc/TC/TC/BGI/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1404), ('tc', 'tc/TC/TC/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1404), ('tc', 'tc/TC/TC/OUTPUT/ClothLine/BGI/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1404), ('tc', 'tc/TC/TC/OUTPUT/RoofAndCurtain/BGI/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1404), ('tc', 'tc/TC/TC/OUTPUT/RoofAndCurtain/TC/BGI/BGIDEMO.C', 24, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 1404), ('tc', 'tc/TC/cprog/S35/JUPITER.C', 23, ['trigonometry', 'sqrt/power', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 379), ('tc', 'tc/TC/S35/JUPITER.C', 23, ['trigonometry', 'sqrt/power', 'coordinate geometry', 'iteration', 'arrays', 'numeric types'], 379), ('tc', 'tc/TC/cprog/S40/FIREWORK.C', 22, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays'], 349), ('tc', 'tc/TC/S40/FIREWORK.C', 22, ['random', 'trigonometry', 'coordinate geometry', 'iteration', 'arrays'], 349)]
        state={'rows':catalog,'selected':None}

        box=self.card(b,'1 • AUTO-RANKED SOURCE CANDIDATES')
        top=tk.Frame(box,bg='white'); top.pack(fill='x',padx=14,pady=(8,2))
        source_filter=tk.StringVar(value='ALL')
        ttk.Combobox(top,textvariable=source_filter,values=['ALL','caimath','tc'],state='readonly',width=12).pack(side='left')
        tk.Label(top,text='  เรียงคะแนน Math evidence จากมาก → น้อย',bg='white',fg=MUTED).pack(side='left')
        tree=ttk.Treeview(box,columns=('archive','file','score','evidence'),show='headings',height=14)
        for c,t,w in [('archive','Archive',90),('file','Source',310),('score','Math score',85),('evidence','Detected evidence',560)]:
            tree.heading(c,text=t); tree.column(c,width=w)
        tree.pack(fill='both',expand=True,padx=14,pady=8)

        detail=self.card(b,'2 • SOURCE → MATHEMATICAL MODEL')
        title=tk.StringVar(value='เลือก source จากตาราง หรือกด AUTO SELECT')
        tk.Label(detail,textvariable=title,bg='white',fg=TEXT,font=('Segoe UI Semibold',11),anchor='w').pack(fill='x',padx=16,pady=(10,4))
        txt=tk.Text(detail,height=18,font=('Consolas',10),wrap='word'); txt.pack(fill='both',expand=True,padx=14,pady=(0,10))

        def math_map(evs):
            concepts=[]; formulas=[]
            if 'trigonometry' in evs:
                concepts+=['Trigonometric functions','periodic motion / coordinates']
                formulas+=['sin²θ + cos²θ = 1','x = r cos θ,  y = r sin θ']
            if 'sqrt/power' in evs:
                concepts+=['powers / roots','Euclidean distance']
                formulas+=['d = √((x₂-x₁)² + (y₂-y₁)²)']
            if 'coordinate geometry' in evs:
                concepts+=['coordinate geometry','transformations / graphical representation']
                formulas+=['Δx = x₂-x₁,  Δy = y₂-y₁']
            if 'random' in evs:
                concepts+=['random experiment','frequency / empirical probability']
                formulas+=['P-hat(A) = count(A) / N']
            if 'iteration' in evs:
                concepts+=['sequences / recurrence / repeated computation']
                formulas+=['xₙ₊₁ = F(xₙ)  (when the loop updates state)']
            if 'arrays' in evs:
                concepts+=['indexed data / vectors / samples']
                formulas+=['mean = (1/n) Σ xᵢ']
            if 'numeric types' in evs:
                concepts+=['real-valued numerical computation']
            return concepts,formulas

        def refresh(*_):
            for x in tree.get_children(): tree.delete(x)
            flt=source_filter.get()
            rows=[r for r in state['rows'] if flt=='ALL' or r[0]==flt]
            rows=sorted(rows,key=lambda r:(-r[2],r[1].lower()))
            for r in rows:
                tree.insert('', 'end', values=(r[0],r[1],r[2],', '.join(r[3])))
        source_filter.trace_add('write',refresh)

        def select_values(vals):
            if not vals:return
            arc,fn,score,evtext=vals
            row=next((r for r in state['rows'] if r[0]==arc and r[1]==fn),None)
            if not row:return
            state['selected']=row; evs=row[3]; concepts,formulas=math_map(evs)
            title.set(f'{arc} → {fn}  |  Math evidence score={score}')
            txt.delete('1.0','end')
            txt.insert('end','DETECTED IN SOURCE\n')
            for e in evs: txt.insert('end',f'  • {e}\n')
            txt.insert('end','\nMATHEMATICAL CONNECTION (Studio interpretation)\n')
            for c in concepts: txt.insert('end',f'  • {c}\n')
            txt.insert('end','\nFORMULAS / MODELS TO STUDY\n')
            for f in formulas: txt.insert('end',f'  {f}\n')
            txt.insert('end','\nLEARNING PIPELINE\n')
            txt.insert('end','  Source evidence → Mathematical variable → Formula/model → numerical experiment → compare → visualization\n')
            txt.insert('end','\nหมายเหตุ: สูตรเป็นเส้นทางการสอนที่ Studio เชื่อมจากโครงสร้าง code; ไม่ได้อ้างว่า source ต้นฉบับพิสูจน์สูตรเหล่านี้ทั้งหมด.')

        def selected(_=None):
            sel=tree.selection()
            if sel: select_values(tree.item(sel[0],'values'))
        tree.bind('<<TreeviewSelect>>',selected)

        def auto_select():
            rows=[r for r in state['rows'] if source_filter.get()=='ALL' or r[0]==source_filter.get()]
            if not rows:return
            best=max(rows,key=lambda r:r[2])
            # select matching tree row
            for iid in tree.get_children():
                v=tree.item(iid,'values')
                if v[0]==best[0] and v[1]==best[1]:
                    tree.selection_set(iid); tree.see(iid); select_values(v); break

        # A math-first experiment independent of legacy compiler availability.
        exp=self.card(b,'3 • MATHEMATICAL EXPERIMENT')
        er=tk.Frame(exp,bg='white'); er.pack(fill='x',padx=16,pady=6)
        N=tk.IntVar(value=2000)
        tk.Label(er,text='Monte Carlo N',bg='white').pack(side='left')
        ttk.Spinbox(er,from_=100,to=20000,increment=100,textvariable=N,width=9).pack(side='left',padx=6)
        result=tk.StringVar(value='เลือก source แล้วทดลองแนวคิด probability/frequency หรือ geometry')
        tk.Label(exp,textvariable=result,bg='white',fg=MUTED,font=('Consolas',9),wraplength=1050,justify='left').pack(anchor='w',padx=16,pady=6)
        cv=tk.Canvas(exp,height=280,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1); cv.pack(fill='x',padx=14,pady=(0,10))

        def experiment():
            if not state['selected']: auto_select()
            if not state['selected']:return
            evs=state['selected'][3]; cv.delete('all'); w=max(cv.winfo_width(),760); h=270
            if 'random' in evs:
                ns=max(100,min(20000,int(N.get())))
                # estimate area of quarter circle: P(x²+y²≤1)=π/4 on unit square
                hit=0; pts=[]
                for i in range(ns):
                    x=random.random(); y=random.random(); inside=x*x+y*y<=1
                    if inside:hit+=1
                    if i<700:pts.append((x,y,inside))
                est=4*hit/ns
                for x,y,inside in pts:
                    px=40+x*(h-70); py=h-30-y*(h-70)
                    cv.create_oval(px-1,py-1,px+1,py+1,outline=GREEN if inside else ORANGE)
                result.set(f'Random sampling experiment: π ≈ 4×hits/N = {est:.6f}; absolute error={abs(est-math.pi):.6f}')
            else:
                # trig/coordinate visualization is a deterministic math experiment.
                pts=[]
                for d in range(361):
                    th=math.radians(d); x=math.cos(th); y=math.sin(th); pts += [w/2+x*105,h/2-y*105]
                cv.create_line(*pts,fill=BLUE,width=2)
                cv.create_line(w/2-130,h/2,w/2+130,h/2,fill='#94a3b8')
                cv.create_line(w/2,h/2-120,w/2,h/2+120,fill='#94a3b8')
                result.set('Coordinate experiment: x=cos θ, y=sin θ → x²+y²=1. ใช้เป็นฐานเชื่อม graphics/trigonometry/geometry.')

        buttons=tk.Frame(box,bg='white'); buttons.pack(fill='x',padx=14,pady=(0,10))
        ttk.Button(buttons,text='🤖 AUTO SELECT BEST MATH SOURCE',style='Primary.TButton',command=auto_select).pack(side='left')
        ttk.Button(buttons,text='▶ RUN MATH EXPERIMENT',command=experiment).pack(side='left',padx=6)
        ttk.Button(buttons,text='V3.9 Bounds',command=self.markov_chebyshev_compare_lab).pack(side='left')

        self.card(b,'V4.0 DESIGN PRINCIPLE',
            'Automatic selection is transparent: score comes from detectable code evidence, not an opaque claim about source intent. '
            'Mathematics remains first; C/TC source is used as the concrete programming context. '
            'Next stage can add source viewer + line-level highlighting + automatic extraction of numeric expressions into a structured Math Model.')
        refresh()

    # ==================== V4.1: MATHEMATICAL MODEL FIRST, SOURCE SECOND ====================
    def v41_math_model_source_lab(self):
        self.clear()
        self.header('∑ V4.1 • Mathematical Model → Source Evidence',
            'เลือกคณิตศาสตร์ก่อน: Model → Variables → Equation → Graph/Experiment → matching C/Pascal source')
        b=self.scrollbody()
        self.card(b,'V4.1 LEARNING ORDER',
            '1) Mathematical Model  2) Variables  3) Equation  4) Visualization/Experiment  '
            '5) Source evidence. Source ใช้ยืนยันว่ามีโครงสร้าง programming ที่สัมพันธ์กับ model; '
            'ไม่ให้ source เป็นตัวกำหนดความหมายทางคณิตศาสตร์โดยอัตโนมัติ')

        models={
          'Circle / Trigonometry': {
             'vars':'θ, r, x, y','eq':['x = r cos θ','y = r sin θ','x² + y² = r²'],
             'need':['trigonometry','coordinate geometry'],
             'note':'Parametric circle and trigonometric identity / coordinate geometry.'},
          'Distance / Pythagorean': {
             'vars':'x₁, y₁, x₂, y₂, d','eq':['Δx=x₂-x₁','Δy=y₂-y₁','d = √(Δx²+Δy²)'],
             'need':['sqrt/power','coordinate geometry'],
             'note':'Euclidean distance from the Pythagorean theorem.'},
          'Monte Carlo Probability': {
             'vars':'N, hit, P-hat','eq':['P-hat(A)=hit/N','π ≈ 4·hit/N  for quarter-circle experiment'],
             'need':['random','iteration'],
             'note':'Repeated random sampling produces empirical relative frequency.'},
          'Sequence / Iteration': {
             'vars':'n, xₙ, xₙ₊₁','eq':['xₙ₊₁ = F(xₙ)','mean=(1/N)Σxᵢ'],
             'need':['iteration','arrays'],
             'note':'A loop can represent repeated computation; arrays can store indexed observations.'}
        }
        source_records=[('tc', 'tc/EXAMPLES/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(87, 'void PutPixelDemo(void);'), (100, 'void StatusLine(char *msg);'), (118, 'PutPixelDemo();'), (314, 'line( h, h, h, vp.bottom-vp.top-h );'), (315, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (322, 'line( h/2, j, h, j );'), (332, 'color = random( MaxColors );'), (334, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/Project/Bin/BGI/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(90, 'void PutPixelDemo(void);'), (103, 'void StatusLine(char *msg);'), (121, 'PutPixelDemo();'), (317, 'line( h, h, h, vp.bottom-vp.top-h );'), (318, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (325, 'line( h/2, j, h, j );'), (335, 'color = random( MaxColors );'), (337, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/Project/Children/BGI/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(90, 'void PutPixelDemo(void);'), (103, 'void StatusLine(char *msg);'), (121, 'PutPixelDemo();'), (317, 'line( h, h, h, vp.bottom-vp.top-h );'), (318, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (325, 'line( h/2, j, h, j );'), (335, 'color = random( MaxColors );'), (337, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/Project/Children/TC3/BGI/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(90, 'void PutPixelDemo(void);'), (103, 'void StatusLine(char *msg);'), (121, 'PutPixelDemo();'), (317, 'line( h, h, h, vp.bottom-vp.top-h );'), (318, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (325, 'line( h/2, j, h, j );'), (335, 'color = random( MaxColors );'), (337, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/Project/ClothLine/BGI/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(90, 'void PutPixelDemo(void);'), (103, 'void StatusLine(char *msg);'), (121, 'PutPixelDemo();'), (317, 'line( h, h, h, vp.bottom-vp.top-h );'), (318, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (325, 'line( h/2, j, h, j );'), (335, 'color = random( MaxColors );'), (337, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/Project/Roof/BGI/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(90, 'void PutPixelDemo(void);'), (103, 'void StatusLine(char *msg);'), (121, 'PutPixelDemo();'), (317, 'line( h, h, h, vp.bottom-vp.top-h );'), (318, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (325, 'line( h/2, j, h, j );'), (335, 'color = random( MaxColors );'), (337, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/Project/Roof/TC/BGI/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(90, 'void PutPixelDemo(void);'), (103, 'void StatusLine(char *msg);'), (121, 'PutPixelDemo();'), (317, 'line( h, h, h, vp.bottom-vp.top-h );'), (318, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (325, 'line( h/2, j, h, j );'), (335, 'color = random( MaxColors );'), (337, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/TC/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(87, 'void PutPixelDemo(void);'), (100, 'void StatusLine(char *msg);'), (118, 'PutPixelDemo();'), (314, 'line( h, h, h, vp.bottom-vp.top-h );'), (315, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (322, 'line( h/2, j, h, j );'), (332, 'color = random( MaxColors );'), (334, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/TC/EXAMP/Project/BGI/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(90, 'void PutPixelDemo(void);'), (103, 'void StatusLine(char *msg);'), (121, 'PutPixelDemo();'), (317, 'line( h, h, h, vp.bottom-vp.top-h );'), (318, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (325, 'line( h/2, j, h, j );'), (335, 'color = random( MaxColors );'), (337, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/TC/Project/Bin/BGI/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(90, 'void PutPixelDemo(void);'), (103, 'void StatusLine(char *msg);'), (121, 'PutPixelDemo();'), (317, 'line( h, h, h, vp.bottom-vp.top-h );'), (318, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (325, 'line( h/2, j, h, j );'), (335, 'color = random( MaxColors );'), (337, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/TC/Project/Children/BGI/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(90, 'void PutPixelDemo(void);'), (103, 'void StatusLine(char *msg);'), (121, 'PutPixelDemo();'), (317, 'line( h, h, h, vp.bottom-vp.top-h );'), (318, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (325, 'line( h/2, j, h, j );'), (335, 'color = random( MaxColors );'), (337, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/TC/Project/Children/TC3/BGI/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(90, 'void PutPixelDemo(void);'), (103, 'void StatusLine(char *msg);'), (121, 'PutPixelDemo();'), (317, 'line( h, h, h, vp.bottom-vp.top-h );'), (318, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (325, 'line( h/2, j, h, j );'), (335, 'color = random( MaxColors );'), (337, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/TC/Project/ClothLine/BGI/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(90, 'void PutPixelDemo(void);'), (103, 'void StatusLine(char *msg);'), (121, 'PutPixelDemo();'), (317, 'line( h, h, h, vp.bottom-vp.top-h );'), (318, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (325, 'line( h/2, j, h, j );'), (335, 'color = random( MaxColors );'), (337, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/TC/Project/Roof/BGI/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(90, 'void PutPixelDemo(void);'), (103, 'void StatusLine(char *msg);'), (121, 'PutPixelDemo();'), (317, 'line( h, h, h, vp.bottom-vp.top-h );'), (318, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (325, 'line( h/2, j, h, j );'), (335, 'color = random( MaxColors );'), (337, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/TC/Project/Roof/TC/BGI/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(90, 'void PutPixelDemo(void);'), (103, 'void StatusLine(char *msg);'), (121, 'PutPixelDemo();'), (317, 'line( h, h, h, vp.bottom-vp.top-h );'), (318, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (325, 'line( h/2, j, h, j );'), (335, 'color = random( MaxColors );'), (337, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/TC/S26/TETRIS.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(59, 'if((*ptr >> i) & 1) PutPixel(x1,y,color);'), (72, 'Vline(x,x + 8,y,color + 3); Vline(x + 1,x + 7,y + 1,color + 1);'), (73, 'Hline(x,y,y + 7,color + 3); Hline(x + 1,y + 1,y + 6,color + 1);'), (74, 'Vline(x,x + 8,y + 7,color - 4); Vline(x + 1,x + 7,y + 6,color - 3);'), (75, 'Hline(x + 8,y,y + 7,color - 5); Hline(x + 7,y + 1,y + 6,color - 3);'), (119, 'pl1 = 48+(sin(k / 30) * 47.0 + 256 * (int)(47 * cos(k / 40)));'), (120, 'pl2 = 48+(sin(k / 14) * 47.0 + 256 * (int)(47 * sin(k / 32))) - pl1;'), (127, 'PutPixel(i + 142,j,color);')]), ('tc', 'tc/TC/S27/ATOM.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(55, 'void PutPixel(int x, int y, BYTE color)'), (141, 'T_cos[i] = (double)(cos((double)i *'), (143, 'T_sin[i] = (double)(sin((double)i *'), (154, 'BALL[i].Color = random(2);'), (225, 'GANX[i] = random(270) + 30;'), (226, 'GANY[i] = random(170) + 30;'), (227, 'PX[i] = random(6) - 3;'), (228, 'PY[i] = random(6) - 3;')]), ('tc', 'tc/TC/S40/FIREWORK.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(123, 'void PutPixel(int i, int j, int color)'), (135, 'PutPixel(i, j, color);'), (138, 'void  gensincos(void)'), (143, 'tcos[0][i] = (int)(cos(M_PI * i / 180) * SIZE);'), (144, 'tsin[0][i] = (int)(sin(M_PI * i / 180) * SIZE);'), (147, 'tcos[1][i] = (int)(tan(M_PI * i / 220) * SIZE);'), (148, 'tsin[1][i] = (int)(sin(M_PI * i / 240) * SIZE);'), (209, 'PutPixel(i, j, color);')]), ('tc', 'tc/TC/TC/BGI/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(90, 'void PutPixelDemo(void);'), (103, 'void StatusLine(char *msg);'), (121, 'PutPixelDemo();'), (317, 'line( h, h, h, vp.bottom-vp.top-h );'), (318, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (325, 'line( h/2, j, h, j );'), (335, 'color = random( MaxColors );'), (337, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/TC/TC/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(90, 'void PutPixelDemo(void);'), (103, 'void StatusLine(char *msg);'), (121, 'PutPixelDemo();'), (317, 'line( h, h, h, vp.bottom-vp.top-h );'), (318, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (325, 'line( h/2, j, h, j );'), (335, 'color = random( MaxColors );'), (337, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/TC/TC/OUTPUT/ClothLine/BGI/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(90, 'void PutPixelDemo(void);'), (103, 'void StatusLine(char *msg);'), (121, 'PutPixelDemo();'), (317, 'line( h, h, h, vp.bottom-vp.top-h );'), (318, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (325, 'line( h/2, j, h, j );'), (335, 'color = random( MaxColors );'), (337, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/TC/TC/OUTPUT/RoofAndCurtain/BGI/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(90, 'void PutPixelDemo(void);'), (103, 'void StatusLine(char *msg);'), (121, 'PutPixelDemo();'), (317, 'line( h, h, h, vp.bottom-vp.top-h );'), (318, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (325, 'line( h/2, j, h, j );'), (335, 'color = random( MaxColors );'), (337, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/TC/TC/OUTPUT/RoofAndCurtain/TC/BGI/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(90, 'void PutPixelDemo(void);'), (103, 'void StatusLine(char *msg);'), (121, 'PutPixelDemo();'), (317, 'line( h, h, h, vp.bottom-vp.top-h );'), (318, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (325, 'line( h/2, j, h, j );'), (335, 'color = random( MaxColors );'), (337, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/TC/c/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(87, 'void PutPixelDemo(void);'), (100, 'void StatusLine(char *msg);'), (118, 'PutPixelDemo();'), (314, 'line( h, h, h, vp.bottom-vp.top-h );'), (315, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (322, 'line( h/2, j, h, j );'), (332, 'color = random( MaxColors );'), (334, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/TC/cprog/S26/TETRIS.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(59, 'if((*ptr >> i) & 1) PutPixel(x1,y,color);'), (72, 'Vline(x,x + 8,y,color + 3); Vline(x + 1,x + 7,y + 1,color + 1);'), (73, 'Hline(x,y,y + 7,color + 3); Hline(x + 1,y + 1,y + 6,color + 1);'), (74, 'Vline(x,x + 8,y + 7,color - 4); Vline(x + 1,x + 7,y + 6,color - 3);'), (75, 'Hline(x + 8,y,y + 7,color - 5); Hline(x + 7,y + 1,y + 6,color - 3);'), (119, 'pl1 = 48+(sin(k / 30) * 47.0 + 256 * (int)(47 * cos(k / 40)));'), (120, 'pl2 = 48+(sin(k / 14) * 47.0 + 256 * (int)(47 * sin(k / 32))) - pl1;'), (127, 'PutPixel(i + 142,j,color);')]), ('tc', 'tc/TC/cprog/S27/ATOM.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(55, 'void PutPixel(int x, int y, BYTE color)'), (141, 'T_cos[i] = (double)(cos((double)i *'), (143, 'T_sin[i] = (double)(sin((double)i *'), (154, 'BALL[i].Color = random(2);'), (225, 'GANX[i] = random(270) + 30;'), (226, 'GANY[i] = random(170) + 30;'), (227, 'PX[i] = random(6) - 3;'), (228, 'PY[i] = random(6) - 3;')]), ('tc', 'tc/TC/cprog/S40/FIREWORK.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(123, 'void PutPixel(int i, int j, int color)'), (135, 'PutPixel(i, j, color);'), (138, 'void  gensincos(void)'), (143, 'tcos[0][i] = (int)(cos(M_PI * i / 180) * SIZE);'), (144, 'tsin[0][i] = (int)(sin(M_PI * i / 180) * SIZE);'), (147, 'tcos[1][i] = (int)(tan(M_PI * i / 220) * SIZE);'), (148, 'tsin[1][i] = (int)(sin(M_PI * i / 240) * SIZE);'), (209, 'PutPixel(i, j, color);')]), ('tc', 'tc/TC/port/control2/BGIDEMO.C', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(87, 'void PutPixelDemo(void);'), (100, 'void StatusLine(char *msg);'), (118, 'PutPixelDemo();'), (314, 'line( h, h, h, vp.bottom-vp.top-h );'), (315, 'line( h, (vp.bottom-vp.top)-h, (vp.right-vp.left)-h, (vp.bottom-vp.top)-h );'), (322, 'line( h/2, j, h, j );'), (332, 'color = random( MaxColors );'), (334, 'line( j, (vp.bottom-vp.top)-h, j, (vp.bottom-vp.top-3)-(h/2) );')]), ('tc', 'tc/TC/tp/EXAMPLES/BGI/BGIDEMO.PAS', 17, ['trigonometry', 'random', 'coordinate geometry', 'iteration', 'arrays'], [(309, 'RandColor := Random(MaxColor)+1;'), (352, 'procedure StatusLine(Msg : string);'), (375, "StatusLine('Esc aborts or press a key...');"), (470, "StatusLine('Esc aborts or press a key');"), (476, 'SetFillStyle(Random(MaxFillStyles), FillColor);'), (477, 'FillEllipse(Random(MaxX), Random(MaxY),'), (478, 'Random(MaxRadius), Random(MaxRadius));'), (493, "StatusLine('Esc aborts or press a key');")]), ('tc', 'tc/TC/S35/JUPITER.C', 16, ['trigonometry', 'sqrt/power', 'coordinate geometry', 'iteration', 'arrays'], [(232, 'PutPixel(x1, y, color);'), (343, 'Rah[j] = sqrt(Radius * Radius - (Radius - j) * (Radius - j));'), (345, 'theta = asin((float) i / (float)Rah[j]);'), (365, 'PutPixel(GanX + i, GanY + j, *(loc + h_offset));'), (366, 'PutPixel(GanX - i, GanY + j, *(loc - h_offset));')]), ('tc', 'tc/TC/cprog/S35/JUPITER.C', 16, ['trigonometry', 'sqrt/power', 'coordinate geometry', 'iteration', 'arrays'], [(232, 'PutPixel(x1, y, color);'), (343, 'Rah[j] = sqrt(Radius * Radius - (Radius - j) * (Radius - j));'), (345, 'theta = asin((float) i / (float)Rah[j]);'), (365, 'PutPixel(GanX + i, GanY + j, *(loc + h_offset));'), (366, 'PutPixel(GanX - i, GanY + j, *(loc - h_offset));')]), ('tc', 'tc/EXAMPLES/MCPARSER.C', 12, ['trigonometry', 'sqrt/power', 'iteration', 'arrays'], [(319, 'curtoken.x.value = pow(token2.x.value, token1.x.value);'), (371, 'curtoken.x.value = acos(curtoken.x.value);'), (373, 'curtoken.x.value = asin(curtoken.x.value);'), (375, 'curtoken.x.value = atan(curtoken.x.value);'), (379, 'curtoken.x.value = cos(curtoken.x.value);'), (393, 'curtoken.x.value = sin(curtoken.x.value);'), (395, 'curtoken.x.value = sqrt(curtoken.x.value);'), (401, 'curtoken.x.value = tan(curtoken.x.value);')]), ('tc', 'tc/Project/Children/TC3/EXAMPLES/TCALC/TCPARSER.C', 12, ['trigonometry', 'sqrt/power', 'iteration', 'arrays'], [(319, 'curtoken.x.value = pow(token2.x.value, token1.x.value);'), (371, 'curtoken.x.value = acos(curtoken.x.value);'), (373, 'curtoken.x.value = asin(curtoken.x.value);'), (375, 'curtoken.x.value = atan(curtoken.x.value);'), (379, 'curtoken.x.value = cos(curtoken.x.value);'), (393, 'curtoken.x.value = sin(curtoken.x.value);'), (395, 'curtoken.x.value = sqrt(curtoken.x.value);'), (401, 'curtoken.x.value = tan(curtoken.x.value);')]), ('tc', 'tc/Project/Roof/TC/BIN/CH24_2.CPP', 12, ['trigonometry', 'coordinate geometry', 'iteration', 'arrays'], [(3, '/*   draw a interesting picture using line()          */'), (19, 'x[i] =  x_center + rad *  cos(36*i*3.14159/180);'), (20, 'y[i] =  y_center + rad *  sin(36*i*3.14159/180);'), (24, 'line(x[i],y[i],x[j],y[j]);')]), ('tc', 'tc/Project/Roof/TC/EXAMPLES/TCALC/TCPARSER.C', 12, ['trigonometry', 'sqrt/power', 'iteration', 'arrays'], [(319, 'curtoken.x.value = pow(token2.x.value, token1.x.value);'), (371, 'curtoken.x.value = acos(curtoken.x.value);'), (373, 'curtoken.x.value = asin(curtoken.x.value);'), (375, 'curtoken.x.value = atan(curtoken.x.value);'), (379, 'curtoken.x.value = cos(curtoken.x.value);'), (393, 'curtoken.x.value = sin(curtoken.x.value);'), (395, 'curtoken.x.value = sqrt(curtoken.x.value);'), (401, 'curtoken.x.value = tan(curtoken.x.value);')]), ('tc', 'tc/Project/Water-Fail/WATER.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(53, 'x = random(260) + 70;'), (54, 'y = random(205) + 90;'), (55, 'r = random(2)+1;'), (57, 'circle(x,y,r);'), (199, 'line(x1,y1,x1,y2);'), (200, 'line(x1,y1,x2,y1);'), (202, 'line(x1+1,y1+1,x1+1,y2);'), (203, 'line(x1+1,y1+1,x2,y1+1);')]), ('tc', 'tc/SORT/TEST2.PAS', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(18, "outtextxy(170,160,'23');  beep(random(2000),100); delay(200);"), (20, "outtextxy(221,160,'17');  beep(random(2000),100); delay(200);"), (22, "outtextxy(272,160,'8');   beep(random(2000),100); delay(200);"), (24, "outtextxy(323,160,'86');  beep(random(2000),100); delay(200);"), (26, "outtextxy(374,160,'91');  beep(random(2000),100); delay(200);"), (28, "outtextxy(425,160,'42');  beep(random(2000),100);"), (38, 'for k := 1 to 5 do beep(random(500),30);'), (41, 'begin   boxyup(125,125,495,290,random(15)+1,0,0,1);')]), ('tc', 'tc/TC/19ANLOG.C', 12, ['trigonometry', 'coordinate geometry', 'iteration', 'arrays'], [(31, 'circle(320,250,100);'), (32, 'circle(320,250,125);'), (33, 'circle(320,250,1);'), (34, 'circle(320,250,7);'), (76, 'xm=320+80*(sin(PI/30*j));'), (77, 'ym=250-80*(cos(PI/30*j));'), (78, 'xh=320+60*sin(PI/6*i+PI/360*j);'), (79, 'yh=250-60*cos(PI/6*i+PI/360*j);')]), ('tc', 'tc/TC/ANLOGC.C', 12, ['trigonometry', 'coordinate geometry', 'iteration', 'arrays'], [(15, 'circle(x,y,210);'), (21, 'outtextxy(x+(r-14)*cos(M_PI/6*i)-10,y-(r-14)*sin(M_PI/6*i)-26,n[i]);'), (23, 'outtextxy(x+(r-14)*cos(M_PI/6*i)-20,y-(r-14)*sin(M_PI/6*i)-26,n[i]);'), (32, 'circle(x,y,10);'), (38, 'line(x,y,x+(r-60)*cos(thetamin*(M_PI/180)),y-(r-60)*sin(thetamin*(M_PI/180'), (40, 'circle(x+(r-80)*cos(thetamin*(M_PI/180)),y-(r-80)*sin(thetamin*(M_PI/180))'), (42, 'line(x,y,x+(r-110)*cos(M_PI/6*h-((m/2)*(M_PI/180))),y-(r-110)*sin(M_PI/6*h'), (44, 'circle(x+(r-130)*cos(M_PI/6*h-((m/2)*(M_PI/180))),y-(r-130)*sin(M_PI/6*h-(')]), ('tc', 'tc/TC/CASE.C', 12, ['trigonometry', 'coordinate geometry', 'iteration', 'arrays'], [(71, 'Cos=cos(Sx);'), (72, 'Sin=sin(Sx);'), (188, 'line(i,0,i,480);'), (192, 'line(0,i,640,i);')]), ('tc', 'tc/TC/MCPARSER.C', 12, ['trigonometry', 'sqrt/power', 'iteration', 'arrays'], [(319, 'curtoken.x.value = pow(token2.x.value, token1.x.value);'), (371, 'curtoken.x.value = acos(curtoken.x.value);'), (373, 'curtoken.x.value = asin(curtoken.x.value);'), (375, 'curtoken.x.value = atan(curtoken.x.value);'), (379, 'curtoken.x.value = cos(curtoken.x.value);'), (393, 'curtoken.x.value = sin(curtoken.x.value);'), (395, 'curtoken.x.value = sqrt(curtoken.x.value);'), (401, 'curtoken.x.value = tan(curtoken.x.value);')]), ('tc', 'tc/TC/Project/Children/TC3/EXAMPLES/TCALC/TCPARSER.C', 12, ['trigonometry', 'sqrt/power', 'iteration', 'arrays'], [(319, 'curtoken.x.value = pow(token2.x.value, token1.x.value);'), (371, 'curtoken.x.value = acos(curtoken.x.value);'), (373, 'curtoken.x.value = asin(curtoken.x.value);'), (375, 'curtoken.x.value = atan(curtoken.x.value);'), (379, 'curtoken.x.value = cos(curtoken.x.value);'), (393, 'curtoken.x.value = sin(curtoken.x.value);'), (395, 'curtoken.x.value = sqrt(curtoken.x.value);'), (401, 'curtoken.x.value = tan(curtoken.x.value);')]), ('tc', 'tc/TC/Project/Roof/TC/BIN/CH24_2.CPP', 12, ['trigonometry', 'coordinate geometry', 'iteration', 'arrays'], [(3, '/*   draw a interesting picture using line()          */'), (19, 'x[i] =  x_center + rad *  cos(36*i*3.14159/180);'), (20, 'y[i] =  y_center + rad *  sin(36*i*3.14159/180);'), (24, 'line(x[i],y[i],x[j],y[j]);')]), ('tc', 'tc/TC/Project/Roof/TC/EXAMPLES/TCALC/TCPARSER.C', 12, ['trigonometry', 'sqrt/power', 'iteration', 'arrays'], [(319, 'curtoken.x.value = pow(token2.x.value, token1.x.value);'), (371, 'curtoken.x.value = acos(curtoken.x.value);'), (373, 'curtoken.x.value = asin(curtoken.x.value);'), (375, 'curtoken.x.value = atan(curtoken.x.value);'), (379, 'curtoken.x.value = cos(curtoken.x.value);'), (393, 'curtoken.x.value = sin(curtoken.x.value);'), (395, 'curtoken.x.value = sqrt(curtoken.x.value);'), (401, 'curtoken.x.value = tan(curtoken.x.value);')]), ('tc', 'tc/TC/Project/Water-Fail/WATER.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(53, 'x = random(260) + 70;'), (54, 'y = random(205) + 90;'), (55, 'r = random(2)+1;'), (57, 'circle(x,y,r);'), (199, 'line(x1,y1,x1,y2);'), (200, 'line(x1,y1,x2,y1);'), (202, 'line(x1+1,y1+1,x1+1,y2);'), (203, 'line(x1+1,y1+1,x2,y1+1);')]), ('tc', 'tc/TC/S28/WORM.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(31, 'void PutPixel(int x, int y, BYTE color)'), (176, 'PutPixel(x0, i, color);'), (177, 'PutPixel(x1, i, color);'), (180, 'PutPixel(i, y0, color);'), (181, 'PutPixel(i, y1, color);'), (209, 'k = random(16);'), (217, 'EgX = random(300) + 10; EgY = random(180) + 10;'), (230, 'k = random(NumW);')]), ('tc', 'tc/TC/S29/TREEROAD.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(33, 'void PutPixel(int x, int y, BYTE color)'), (53, 'PutPixel(i, j, color);'), (335, 'MakePoint(random(80) - 40, 3, -68, &stars[i]);'), (337, 'MakePoint(random(80) - 40, -random(20), -68, &stars[i]);'), (370, 'sound(random(30) * 60 + 400);'), (377, 'PutPixel(p.x + 160, p.y + 110, color + 71);'), (421, 'if((*ptr >> i) & 1) PutPixel(x1, y, color);')]), ('tc', 'tc/TC/S30/BIGTEXT.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(35, 'void PutPixel(int x, int y, BYTE color)'), (55, 'PutPixel(i, j, color);'), (131, 'MakePoint(random(20) - 10, random(20) - 10,'), (132, 'random(50) - 60, &stars[i]);'), (133, 'stars[i].Speed = INT_TO_FIXED(random(2) + 1);'), (147, 'MakePoint(random(20) - 10, random(20) - 10,'), (148, 'random(10) - 65, &stars[i]);'), (151, 'PutPixel(p.x + 160, p.y + 100, FIXED_TO_INT(stars[i].z) + 81);')]), ('tc', 'tc/TC/S32/BLOCKOUT.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(169, 'Vline(x, x + 20, y, color + 2);'), (170, 'Vline(x + 1, x+19, y + 1, color);'), (171, 'Hline(x, y, y + 7, color + 2);'), (172, 'Hline(x + 1, y + 1, y + 6, color);'), (173, 'Vline(x, x + 20, y + 7, color - 5);'), (174, 'Vline(x + 1, x + 19, y + 6, color - 4);'), (175, 'Hline(x + 20, y, y + 7, color - 6);'), (176, 'Hline(x + 19, y + 1, y + 6, color - 4);')]), ('tc', 'tc/TC/S37/BALLTRIS.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(86, 'putpixelrgb(i, y0, r, g, b);'), (87, 'putpixelrgb(i, y1, r, g, b);'), (90, 'putpixelrgb(x0, i, r, g, b);'), (91, 'putpixelrgb(x1, i, r, g, b);'), (99, 'putpixelrgb(i, j, r, g, b);'), (121, 'putpixelrgb(i, j, r/3, g/3, b/3);'), (130, 'nBaray[i] = random(Level);'), (143, 'nBaray[0] = nBaray[1] = nBaray[2] = random(Level);')]), ('tc', 'tc/TC/S39/DINOSTAR.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(185, 'void PutPixel(int i, int j, int color)'), (215, 'PutPixel(i, j, color);'), (230, 'PutPixel(i, j, color);'), (231, 'PutPixel(i + 1,j, color);'), (232, 'PutPixel(i, j + 1, color);'), (233, 'PutPixel(i + 1, j + 1, color);'), (258, 'k = random(4) + 4;'), (260, 'PutPixel(x + 17 + (i / k), y + 38 + i, (color << 5) + 8);')]), ('tc', 'tc/TC/S41/SANTA.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(78, 'HamOGx[i] = HamGx[i] = random(300);'), (79, 'HamOGy[i] = HamGy[i] = -random(100) * 2;'), (80, 'AddHam[i] = random(2) + 1;'), (82, 'AddHam[i] = random(4) + 2;'), (98, 'PutPixel(random(320), random(170), 11);'), (100, 'PutImage(i * 16, 184, Flor[random(3)]);'), (163, 'sound(200 + s * random(30));'), (178, 'sound(400 + s * random(30));')]), ('tc', 'tc/TC/S43/KILLYABA.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(210, 'if(random(LEVEL)==0&& j > Line){'), (211, 'Map[i][j] = random(7);'), (216, 'Color0 = random(7);'), (217, 'Color1 = random(7);'), (218, 'NewCo0 = random(7);'), (219, 'NewCo1 = random(7);'), (250, 'if(random(20)==0)'), (251, 'PutSpriteColor(i*9+10+random(2),j*8+4,')]), ('tc', 'tc/TC/S46/WINLOGO.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(50, 'void PutPixel(int x, int y, BYTE color)'), (94, 'PutPixel(i, j, color);'), (211, 'PutPixel(i, y0, color);'), (212, 'PutPixel(i, y1, color);'), (215, 'PutPixel(x0, i, color);'), (216, 'PutPixel(x1, i, color);'), (357, 'PutSprite(i * 14, j * 23, BALL[random(7)]);'), (363, 'PutSprite(random(24) * 14, random(17) * 23, BALL[random(7)]);')]), ('tc', 'tc/TC/S48/SHADOW.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(38, 'void PutPixel(int x, int y, BYTE color)'), (49, 'PutPixel(i, j, color);'), (327, 'void PutPixelShadow(int x, int y)'), (339, 'PutPixelShadow(i, j);'), (352, 'x0 = random(310); x1 = x0 + random(40);'), (353, 'y0 = random(190); y1 = y0 + random(32);'), (355, 'Bar(x0, y0, x1, y1, random(256));')]), ('tc', 'tc/TC/S51/YIN_CUP.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(35, 'void PutPixel(int x, int y, BYTE color)'), (45, 'PutPixel(i, j, color);'), (52, 'PutPixel(x0, i, color);'), (53, 'PutPixel(x1, i, color);'), (56, 'PutPixel(i, y0, color);'), (57, 'PutPixel(i, y1, color);'), (319, 'NexHCheck[i] = random(4);'), (356, 'NexHCheck[i] = random(4);')]), ('tc', 'tc/TC/S52/YIN_CUP2.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(38, 'void PutPixel(int x, int y, BYTE color)'), (48, 'PutPixel(i, j, color);'), (55, 'PutPixel(x0, i, color);'), (56, 'PutPixel(x1, i, color);'), (59, 'PutPixel(i, y0, color);'), (60, 'PutPixel(i, y1, color);'), (319, 'if((*ptr >> i) & 1) PutPixel(x1, y, color);'), (354, 'NexHCheck[i] = random(5);')]), ('tc', 'tc/TC/S53/WATCOM.TXT', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(104, 'ѧ random() ŢҨеͧ #define ҡ'), (105, '#define random(r) rand() % r'), (113, '#define random(r) rand() % r'), (120, 'void PutPixel(short x,short y,unsigned char color)'), (135, 'PutPixel(random(320),random(200),random(256));'), (160, '#define random(r) (rand()%r)'), (185, 'void PutPixel(int x, int y, BYTE color)'), (199, 'PutPixel(i, j, color);')]), ('tc', 'tc/TC/S53/WGRAPH.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(14, '#define random(r) (rand()%r)'), (39, 'void PutPixel(int x, int y, BYTE color)'), (53, 'PutPixel(i, j, color);'), (60, 'PutPixel(x0, i, color);'), (61, 'PutPixel(x1, i, color);'), (64, 'PutPixel(i, y0, color);'), (65, 'PutPixel(i, y1, color);'), (149, 'PutPixel(x1, y, color);')]), ('tc', 'tc/TC/TC/10.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(31, 'void PutPixel(int x, int y, BYTE color)'), (176, 'PutPixel(x0, i, color);'), (177, 'PutPixel(x1, i, color);'), (180, 'PutPixel(i, y0, color);'), (181, 'PutPixel(i, y1, color);'), (209, 'k=random(16);'), (217, 'EgX = random(300) + 10;EgY = random(180) + 10;'), (230, 'k = random(NumW);')]), ('tc', 'tc/TC/TC/ANLOG.C', 12, ['trigonometry', 'coordinate geometry', 'iteration', 'arrays'], [(31, 'circle(320,250,100);'), (32, 'circle(320,250,125);'), (33, 'circle(320,250,1);'), (34, 'circle(320,250,7);'), (76, 'xm=320+80*(sin(PI/30*j));'), (77, 'ym=250-80*(cos(PI/30*j));'), (78, 'xh=320+60*sin(PI/6*i+PI/360*j);'), (79, 'yh=250-60*cos(PI/6*i+PI/360*j);')]), ('tc', 'tc/TC/TC/DEMO/RELAY/HOME.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(210, 'x1=random(500);'), (211, 'y1=random(70);'), (212, 'c1=random(16);'), (216, 'putpixel(x1+50,y1+110,c1);'), (226, 'line(230,355,242,355);'), (227, 'circle(230,355,12);'), (232, 'line(425,355,437,355);'), (233, 'circle(425,355,12);')]), ('tc', 'tc/TC/TC/DEMO/RELAY/TRAINTC1.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(90, 'line(261,306+y,429,306+y);'), (98, 'line(261,306+y,429,306+y);'), (124, 'line(261,289+y,429,289+y);'), (163, 'x=random(480);'), (164, 'y=random(80);'), (165, 'c=random(16);'), (166, 'putpixel(x+70,y+120,c);'), (170, 'line(51,229,610,229);')]), ('tc', 'tc/TC/TC/EXAMPLES/TCALC/TCPARSER.C', 12, ['trigonometry', 'sqrt/power', 'iteration', 'arrays'], [(319, 'curtoken.x.value = pow(token2.x.value, token1.x.value);'), (371, 'curtoken.x.value = acos(curtoken.x.value);'), (373, 'curtoken.x.value = asin(curtoken.x.value);'), (375, 'curtoken.x.value = atan(curtoken.x.value);'), (379, 'curtoken.x.value = cos(curtoken.x.value);'), (393, 'curtoken.x.value = sin(curtoken.x.value);'), (395, 'curtoken.x.value = sqrt(curtoken.x.value);'), (401, 'curtoken.x.value = tan(curtoken.x.value);')]), ('tc', 'tc/TC/TC/MCPARSER.C', 12, ['trigonometry', 'sqrt/power', 'iteration', 'arrays'], [(319, 'curtoken.x.value = pow(token2.x.value, token1.x.value);'), (371, 'curtoken.x.value = acos(curtoken.x.value);'), (373, 'curtoken.x.value = asin(curtoken.x.value);'), (375, 'curtoken.x.value = atan(curtoken.x.value);'), (379, 'curtoken.x.value = cos(curtoken.x.value);'), (393, 'curtoken.x.value = sin(curtoken.x.value);'), (395, 'curtoken.x.value = sqrt(curtoken.x.value);'), (401, 'curtoken.x.value = tan(curtoken.x.value);')]), ('tc', 'tc/TC/TC/OUTPUT/RoofAndCurtain/TC/BIN/CH24_2.CPP', 12, ['trigonometry', 'coordinate geometry', 'iteration', 'arrays'], [(3, '/*   draw a interesting picture using line()          */'), (19, 'x[i] =  x_center + rad *  cos(36*i*3.14159/180);'), (20, 'y[i] =  y_center + rad *  sin(36*i*3.14159/180);'), (24, 'line(x[i],y[i],x[j],y[j]);')]), ('tc', 'tc/TC/TC/OUTPUT/RoofAndCurtain/TC/EXAMPLES/TCALC/TCPARSER.C', 12, ['trigonometry', 'sqrt/power', 'iteration', 'arrays'], [(319, 'curtoken.x.value = pow(token2.x.value, token1.x.value);'), (371, 'curtoken.x.value = acos(curtoken.x.value);'), (373, 'curtoken.x.value = asin(curtoken.x.value);'), (375, 'curtoken.x.value = atan(curtoken.x.value);'), (379, 'curtoken.x.value = cos(curtoken.x.value);'), (393, 'curtoken.x.value = sin(curtoken.x.value);'), (395, 'curtoken.x.value = sqrt(curtoken.x.value);'), (401, 'curtoken.x.value = tan(curtoken.x.value);')]), ('tc', 'tc/TC/TC/anlogcloc.c', 12, ['trigonometry', 'coordinate geometry', 'iteration', 'arrays'], [(15, 'circle(x,y,210);'), (21, 'outtextxy(x+(r-14)*cos(M_PI/6*i)-10,y-(r-14)*sin(M_PI/6*i)-26,n[i]);'), (23, 'outtextxy(x+(r-14)*cos(M_PI/6*i)-20,y-(r-14)*sin(M_PI/6*i)-26,n[i]);'), (32, 'circle(x,y,10);'), (38, 'line(x,y,x+(r-60)*cos(thetamin*(M_PI/180)),y-(r-60)*sin(thetamin*(M_PI/180'), (40, 'circle(x+(r-80)*cos(thetamin*(M_PI/180)),y-(r-80)*sin(thetamin*(M_PI/180))'), (42, 'line(x,y,x+(r-110)*cos(M_PI/6*h-((m/2)*(M_PI/180))),y-(r-110)*sin(M_PI/6*h'), (44, 'circle(x+(r-130)*cos(M_PI/6*h-((m/2)*(M_PI/180))),y-(r-130)*sin(M_PI/6*h-(')]), ('tc', 'tc/TC/TCPARSER.C', 12, ['trigonometry', 'sqrt/power', 'iteration', 'arrays'], [(319, 'curtoken.x.value = pow(token2.x.value, token1.x.value);'), (371, 'curtoken.x.value = acos(curtoken.x.value);'), (373, 'curtoken.x.value = asin(curtoken.x.value);'), (375, 'curtoken.x.value = atan(curtoken.x.value);'), (379, 'curtoken.x.value = cos(curtoken.x.value);'), (393, 'curtoken.x.value = sin(curtoken.x.value);'), (395, 'curtoken.x.value = sqrt(curtoken.x.value);'), (401, 'curtoken.x.value = tan(curtoken.x.value);')]), ('tc', 'tc/TC/TREEROAD.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(33, 'void PutPixel(int x, int y, BYTE color)'), (53, 'PutPixel(i, j, color);'), (334, 'MakePoint(random(80) - 40, 3, -68, &stars[i]);'), (336, 'MakePoint(random(80) - 40, -random(20), -68, &stars[i]);'), (369, 'sound(random(30) * 60 + 400);'), (376, 'PutPixel(p.x + 160, p.y + 110, color + 71);'), (420, 'if((*ptr >> i) & 1) PutPixel(x1, y, color);')]), ('tc', 'tc/TC/c/10 (2).C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(31, 'void PutPixel(int x, int y, BYTE color)'), (176, 'PutPixel(x0, i, color);'), (177, 'PutPixel(x1, i, color);'), (180, 'PutPixel(i, y0, color);'), (181, 'PutPixel(i, y1, color);'), (209, 'k=random(16);'), (217, 'EgX = random(300) + 10;EgY = random(180) + 10;'), (230, 'k = random(NumW);')]), ('tc', 'tc/TC/c/10.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(31, 'void PutPixel(int x, int y, BYTE color)'), (176, 'PutPixel(x0, i, color);'), (177, 'PutPixel(x1, i, color);'), (180, 'PutPixel(i, y0, color);'), (181, 'PutPixel(i, y1, color);'), (207, 'k = random(16);'), (215, 'EgX = random(300) + 10; EgY = random(180) + 10;'), (228, 'k = random(NumW);')]), ('tc', 'tc/TC/c/19.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(31, 'void PutPixel(int x, int y, BYTE color)'), (176, 'PutPixel(x0, i, color);'), (177, 'PutPixel(x1, i, color);'), (180, 'PutPixel(i, y0, color);'), (181, 'PutPixel(i, y1, color);'), (209, 'k = random(16);'), (217, 'EgX = random(300) + 10; EgY = random(180) + 10;'), (230, 'k = random(NumW);')]), ('tc', 'tc/TC/c/27.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(31, 'void PutPixel(int x,int y,BYTE color)'), (176, 'PutPixel(x0,i,color);'), (177, 'PutPixel(x1,i,color);'), (180, 'PutPixel(i,y0,color);'), (181, 'PutPixel(i,y1,color);'), (209, 'k=random(16);'), (217, 'EgX=random(300)+10;EgY=random(180)+10;'), (230, 'k=random(NumW);')]), ('tc', 'tc/TC/c/32.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(31, 'void PutPixel(int x,int y,BYTE color)'), (176, 'PutPixel(x0,i,color);'), (177, 'PutPixel(x1,i,color);'), (180, 'PutPixel(i,y0,color);'), (181, 'PutPixel(i,y1,color);'), (209, 'k=random(16);'), (217, 'EgX=random(300)+10;EgY=random(180)+10;'), (230, 'k=random(NumW);')]), ('tc', 'tc/TC/c/35.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(31, 'void Putpixel(int x, int y, BYTE color)'), (175, 'PutPixel(x0, i, color);'), (176, 'PutPixel(x1, i, color);'), (179, 'PutPixel(i, y0, color);'), (180, 'PutPixel(i, y1, color);'), (208, 'k = random(16);'), (216, 'EgX = random(300) + 10; EgY = random(180) + 10;'), (229, 'k = random(NumW);')]), ('tc', 'tc/TC/c/4.c', 12, ['trigonometry', 'coordinate geometry', 'iteration', 'arrays'], [(15, 'void st_line(void);'), (243, 'putpixel(i,j,WHITE);'), (264, 'line(0,my/2,mx,my/2);'), (266, 'line(mx/2,0,mx/2,my);'), (270, 'line(i,235,i,245);'), (280, 'line(315,j,325,j);'), (298, 'line(0,my/2,mx,my/2);'), (300, 'line(mx/2,0,mx/2,my);')]), ('tc', 'tc/TC/c/8.C', 12, ['random', 'coordinate geometry', 'iteration', 'arrays'], [(31, 'void PutPixel(int x, int y, BYTE color)'), (175, 'PutPixel(x0, i, color);'), (176, 'PutPixel(x1, i, color);'), (179, 'PutPixel(i, y0, color);'), (180, 'PutPixel(i, y1, color);'), (208, 'k = random(16);'), (216, 'EgX = random(300) + 10; EgY = random(180) + 10;'), (229, 'k = random(NumW);')]), ('tc', 'tc/TC/c_grapic/ANLOG.C', 12, ['trigonometry', 'coordinate geometry', 'iteration', 'arrays'], [(31, 'circle(320,250,100);'), (32, 'circle(320,250,125);'), (33, 'circle(320,250,1);'), (34, 'circle(320,250,7);'), (76, 'xm=320+80*(sin(PI/30*j));'), (77, 'ym=250-80*(cos(PI/30*j));'), (78, 'xh=320+60*sin(PI/6*i+PI/360*j);'), (79, 'yh=250-60*cos(PI/6*i+PI/360*j);')]), ('tc', 'tc/TC/c_grapic/TRANFO.C', 12, ['trigonometry', 'coordinate geometry', 'iteration', 'arrays'], [(83, 'Cos=cos(Sx);'), (84, 'Sin=sin(Sx);'), (217, 'line(i,0,i,480);'), (222, 'line(0,i,640,i);')])]
        model=tk.StringVar(value='Circle / Trigonometry')

        choose=self.card(b,'1 • SELECT MATHEMATICAL MODEL')
        ttk.Combobox(choose,textvariable=model,values=list(models.keys()),state='readonly',width=32).pack(anchor='w',padx=16,pady=10)

        nb=ttk.Notebook(b); nb.pack(fill='both',expand=True,padx=28,pady=10)
        math_tab=tk.Frame(nb,bg='white'); graph_tab=tk.Frame(nb,bg='white'); src_tab=tk.Frame(nb,bg='white')
        nb.add(math_tab,text='Mathematical Model'); nb.add(graph_tab,text='Graph / Experiment'); nb.add(src_tab,text='Source Evidence')

        mtxt=tk.Text(math_tab,height=22,font=('Consolas',10),wrap='word'); mtxt.pack(fill='both',expand=True,padx=12,pady=10)
        cv=tk.Canvas(graph_tab,height=440,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1); cv.pack(fill='both',expand=True,padx=12,pady=10)
        result=tk.StringVar(value='')
        tk.Label(graph_tab,textvariable=result,bg='white',fg=MUTED,font=('Consolas',9),wraplength=1000).pack(anchor='w',padx=12,pady=(0,8))

        tree=ttk.Treeview(src_tab,columns=('archive','file','score','evidence'),show='headings',height=13)
        for c,t,w in [('archive','Archive',90),('file','Matched source',330),('score','Match',70),('evidence','Actual detected evidence',520)]:
            tree.heading(c,text=t); tree.column(c,width=w)
        tree.pack(fill='both',expand=True,padx=12,pady=8)
        snippet=tk.Text(src_tab,height=9,font=('Consolas',9),wrap='none'); snippet.pack(fill='both',expand=True,padx=12,pady=(0,10))
        state={'matches':[]}

        def show_math():
            d=models[model.get()]
            mtxt.delete('1.0','end')
            mtxt.insert('end',f'MODEL: {model.get()}\n\nVARIABLES\n  {d["vars"]}\n\nEQUATIONS\n')
            for q in d['eq']: mtxt.insert('end',f'  {q}\n')
            mtxt.insert('end',f'\nINTERPRETATION\n  {d["note"]}\n\n')
            mtxt.insert('end','SOURCE REQUIREMENTS (searched after mathematics)\n')
            for q in d['need']: mtxt.insert('end',f'  • {q}\n')

        def draw():
            cv.delete('all'); w=max(cv.winfo_width(),780); h=max(cv.winfo_height(),400); name=model.get()
            if name=='Circle / Trigonometry':
                cx,cy=w/2,h/2; r=130; pts=[]
                for deg in range(361):
                    th=math.radians(deg); pts += [cx+r*math.cos(th),cy-r*math.sin(th)]
                cv.create_line(*pts,fill=BLUE,width=3); cv.create_line(cx-r-30,cy,cx+r+30,cy,fill='#94a3b8')
                cv.create_line(cx,cy-r-30,cx,cy+r+30,fill='#94a3b8')
                th=math.radians(40); x=cx+r*math.cos(th); y=cy-r*math.sin(th)
                cv.create_line(cx,cy,x,y,fill=ORANGE,width=3); cv.create_text(x+35,y,text='(r cosθ, r sinθ)',fill=TEXT)
                result.set('Visualization: parametric equation maps angle θ to a point on x²+y²=r².')
            elif name=='Distance / Pythagorean':
                x1,y1=160,310; x2,y2=590,100
                cv.create_line(x1,y1,x2,y1,fill=GREEN,width=2); cv.create_line(x2,y1,x2,y2,fill=GREEN,width=2)
                cv.create_line(x1,y1,x2,y2,fill=BLUE,width=3)
                cv.create_text((x1+x2)/2,y1+18,text='Δx',fill=TEXT); cv.create_text(x2+22,(y1+y2)/2,text='Δy',fill=TEXT)
                cv.create_text((x1+x2)/2-20,(y1+y2)/2-18,text='d',fill=BLUE)
                result.set('Visualization: d² = Δx² + Δy².')
            elif name=='Monte Carlo Probability':
                N=2500; hit=0
                for i in range(N):
                    x=random.random(); y=random.random(); inside=x*x+y*y<=1
                    if inside: hit+=1
                    if i<1000:
                        px=70+x*300; py=350-y*300
                        cv.create_oval(px-1,py-1,px+1,py+1,outline=GREEN if inside else ORANGE)
                est=4*hit/N
                result.set(f'Monte Carlo: N={N}, hit={hit}, π estimate={est:.6f}, error={abs(est-math.pi):.6f}')
            else:
                vals=[1.0]
                for _ in range(35): vals.append(.82*vals[-1]+.18*3.0)
                pts=[]
                for i,v in enumerate(vals): pts += [60+i*(w-120)/(len(vals)-1),350-v/3.2*270]
                cv.create_line(*pts,fill=BLUE,width=3)
                result.set('Example recurrence xₙ₊₁=0.82xₙ+0.18·3 converges toward a fixed point.')

        def match_sources():
            d=models[model.get()]; need=set(d['need']); scored=[]
            for rec in source_records:
                arc,fn,base_score,evs,lines=rec; evset=set(evs)
                overlap=len(need & evset)
                if overlap:
                    score=overlap*10 + len(need & evset)/max(1,len(need))*5
                    scored.append((score,rec))
            scored.sort(key=lambda x:(-x[0],-x[1][2],x[1][1]))
            state['matches']=[r for _,r in scored[:25]]
            for iid in tree.get_children():tree.delete(iid)
            for arc,fn,base_score,evs,lines in state['matches']:
                match=len(need & set(evs))
                tree.insert('', 'end',values=(arc,fn,f'{match}/{len(need)}',', '.join(evs)))
            nb.select(src_tab)
            if state['matches']:
                iid=tree.get_children()[0]; tree.selection_set(iid); tree.see(iid); show_snippet()

        def show_snippet(_=None):
            sel=tree.selection()
            if not sel:return
            vals=tree.item(sel[0],'values'); arc,fn=vals[0],vals[1]
            rec=next((r for r in state['matches'] if r[0]==arc and r[1]==fn),None)
            snippet.delete('1.0','end')
            if not rec:return
            snippet.insert('end',f'{arc} / {fn}\n')
            snippet.insert('end','Detected source lines relevant to mathematical evidence:\n\n')
            if rec[4]:
                for no,line in rec[4]: snippet.insert('end',f'L{no:04d}  {line}\n')
            else: snippet.insert('end','No short evidence line was extracted; match is based on structural tokens in the file.')
            snippet.insert('end','\nThese lines are source evidence only; the mathematical model above is the teaching interpretation.')
        tree.bind('<<TreeviewSelect>>',show_snippet)

        def update(*_):
            show_math(); draw()
            for iid in tree.get_children():tree.delete(iid)
            snippet.delete('1.0','end')
        model.trace_add('write',update)

        buttons=tk.Frame(choose,bg='white'); buttons.pack(fill='x',padx=16,pady=(0,10))
        ttk.Button(buttons,text='1 ▶ SHOW MATHEMATICAL MODEL',style='Primary.TButton',command=lambda:(show_math(),nb.select(math_tab))).pack(side='left')
        ttk.Button(buttons,text='2 ▶ GRAPH / EXPERIMENT',command=lambda:(draw(),nb.select(graph_tab))).pack(side='left',padx=5)
        ttk.Button(buttons,text='3 ▶ FIND MATCHING SOURCE',command=match_sources).pack(side='left')
        ttk.Button(buttons,text='V4.0 Auto Source',command=self.v40_auto_c_math_lab).pack(side='left',padx=5)

        self.card(b,'V4.1 PRINCIPLE',
            'Mathematics controls the lesson sequence. Source search happens only after the model is defined. '
            'Matching is transparent and based on detected tokens/structures in caimath/tc source. '
            'V4.2 can continue with line-level variable/expression extraction and a structured equation parser, without executing legacy source.')
        update()

    # ==================== V4.2: SOURCE VARIABLES/EXPRESSIONS -> MATH MODEL ====================
    def v42_source_expression_model_lab(self):
        self.clear()
        self.header('ƒ V4.2 • Source → Variables → Expressions → Mathematical Equation',
            'อ่าน C/Pascal แบบ static only: extract → normalize → map to math model → visualize; ไม่ execute legacy source')
        b=self.scrollbody()
        self.card(b,'PIPELINE',
            '1) เลือก source ที่ระบบจัดอันดับจาก assignment expressions จริง  2) แยก declared variables '
            '3) แยก assignment expression พร้อมเลขบรรทัด  4) แปลง syntax C/Pascal เป็นรูปสมการอ่านง่าย '
            '5) จับคู่กับ Mathematical Model  6) แสดงกราฟ/diagram เมื่อรูปแบบรองรับ')

        data=[('tc', 'tc/TC/tp/EXAMPLES/TVFM/EQU.PAS', 162, [], [(20, 'cmDosShell', 'cmNewWindow + 1', 'cmDosShell          = cmNewWindow + 1;'), (21, 'cmRun', 'cmDosShell + 1', 'cmRun               = cmDosShell + 1;'), (25, 'cmViewAsHex', 'cmExecute + 1', 'cmViewAsHex         = cmExecute + 1;'), (26, 'cmViewAsText', 'cmViewAsHex + 1', 'cmViewAsText        = cmViewAsHex + 1;'), (27, 'cmViewCustom', 'cmViewAsText + 1', 'cmViewCustom        = cmViewAsText + 1;'), (28, 'cmAssociate', 'cmViewCustom + 1', 'cmAssociate         = cmViewCustom + 1;'), (29, 'cmCopy', 'cmAssociate + 1', 'cmCopy              = cmAssociate + 1;'), (30, 'cmDelete', 'cmCopy + 1', 'cmDelete            = cmCopy + 1;'), (31, 'cmRename', 'cmDelete + 1', 'cmRename            = cmDelete + 1;'), (32, 'cmChangeAttr', 'cmRename + 1', 'cmChangeAttr        = cmRename + 1;')]), ('tc', 'tc/TC/caibinary/PROC.PAS', 119, ['i', 'j', 'Old', 'Now', 'p'], [(24, 'x', 'x1 - size', 'x := x1 - size;'), (161, 'x1', 'x1 - 1', 'x1 := x1 - 1;'), (162, 'y1', 'y1 - 1', 'y1 := y1 - 1;'), (168, 'x1', 'x1 - 1', 'x1 := x1 - 1;'), (169, 'y1', 'y1 + 1', 'y1 := y1 + 1;'), (178, 'x1', 'x1 + 1', 'x1 := x1 + 1; y1 := y1 - 1;'), (184, 'x1', 'x1 + 1', 'x1 := x1 + 1;'), (185, 'y1', 'y1 + 1', 'y1 := y1 + 1;'), (228, 'a', 'a - 1', 'a := a - 1; b := b - 1;'), (237, 'a', 'a - 1', 'a := a - 1; b := b + 1;')]), ('tc', 'tc/TC/caitree/PROC.PAS', 119, ['i', 'j', 'Old', 'Now', 'p'], [(24, 'x', 'x1 - size', 'x := x1 - size;'), (161, 'x1', 'x1 - 1', 'x1 := x1 - 1;'), (162, 'y1', 'y1 - 1', 'y1 := y1 - 1;'), (168, 'x1', 'x1 - 1', 'x1 := x1 - 1;'), (169, 'y1', 'y1 + 1', 'y1 := y1 + 1;'), (178, 'x1', 'x1 + 1', 'x1 := x1 + 1; y1 := y1 - 1;'), (184, 'x1', 'x1 + 1', 'x1 := x1 + 1;'), (185, 'y1', 'y1 + 1', 'y1 := y1 + 1;'), (228, 'a', 'a - 1', 'a := a - 1; b := b - 1;'), (237, 'a', 'a - 1', 'a := a - 1; b := b + 1;')]), ('tc', 'tc/TC/tp/caitree/PROC.PAS', 119, ['i', 'j', 'Old', 'Now', 'p'], [(24, 'x', 'x1 - size', 'x := x1 - size;'), (161, 'x1', 'x1 - 1', 'x1 := x1 - 1;'), (162, 'y1', 'y1 - 1', 'y1 := y1 - 1;'), (168, 'x1', 'x1 - 1', 'x1 := x1 - 1;'), (169, 'y1', 'y1 + 1', 'y1 := y1 + 1;'), (178, 'x1', 'x1 + 1', 'x1 := x1 + 1; y1 := y1 - 1;'), (184, 'x1', 'x1 + 1', 'x1 := x1 + 1;'), (185, 'y1', 'y1 + 1', 'y1 := y1 + 1;'), (228, 'a', 'a - 1', 'a := a - 1; b := b - 1;'), (237, 'a', 'a - 1', 'a := a - 1; b := b + 1;')]), ('tc', 'tc/TC/caibinary/TESTNEW.PAS', 90, ['Choose', 'no', 'Count', 'Ti', 'i', 'j', 'Old', 'Now', 'p'], [(96, 'x2', 'x1 + 20', 'x2 := x1 + 20;'), (97, 'y2', 'y1 + 20', 'y2 := y1 + 20;'), (99, 'x1', 'x1 + 22', 'x1 := x1 + 22;'), (101, 'y1', 'y1+22', 'y1 := y1+22;'), (119, 'x', '(x1-22) + 22*co', 'x  := (x1-22) + 22*co;'), (120, 'y', 'y1 + 22*(no)', 'y  := y1 + 22*(no);'), (121, 'x2', 'x + 20', 'x2 := x + 20;'), (122, 'y2', 'y + 20', 'y2 := y + 20;'), (135, 'Time', 'Timer[i] - sec', 'Time := Timer[i] - sec;'), (178, 'Now', 'Now-1', 'Now := Now-1;')]), ('tc', 'tc/TC/caitree/TESTNEW.PAS', 90, ['Choose', 'no', 'Count', 'Ti', 'i', 'j', 'Old', 'Now', 'p'], [(96, 'x2', 'x1 + 20', 'x2 := x1 + 20;'), (97, 'y2', 'y1 + 20', 'y2 := y1 + 20;'), (99, 'x1', 'x1 + 22', 'x1 := x1 + 22;'), (101, 'y1', 'y1+22', 'y1 := y1+22;'), (119, 'x', '(x1-22) + 22*co', 'x  := (x1-22) + 22*co;'), (120, 'y', 'y1 + 22*(no)', 'y  := y1 + 22*(no);'), (121, 'x2', 'x + 20', 'x2 := x + 20;'), (122, 'y2', 'y + 20', 'y2 := y + 20;'), (135, 'Time', 'Timer[i] - sec', 'Time := Timer[i] - sec;'), (178, 'Now', 'Now-1', 'Now := Now-1;')]), ('tc', 'tc/TC/tp/caitree/TESTNEW.PAS', 90, ['Choose', 'no', 'Count', 'Ti', 'i', 'j', 'Old', 'Now', 'p'], [(96, 'x2', 'x1 + 20', 'x2 := x1 + 20;'), (97, 'y2', 'y1 + 20', 'y2 := y1 + 20;'), (99, 'x1', 'x1 + 22', 'x1 := x1 + 22;'), (101, 'y1', 'y1+22', 'y1 := y1+22;'), (119, 'x', '(x1-22) + 22*co', 'x  := (x1-22) + 22*co;'), (120, 'y', 'y1 + 22*(no)', 'y  := y1 + 22*(no);'), (121, 'x2', 'x + 20', 'x2 := x + 20;'), (122, 'y2', 'y + 20', 'y2 := y + 20;'), (135, 'Time', 'Timer[i] - sec', 'Time := Timer[i] - sec;'), (178, 'Now', 'Now-1', 'Now := Now-1;')]), ('tc', 'tc/TC/tp/EXAMPLES/TVFM/TOOLS.PAS', 76, ['i', 'ParamPos', 'I', 'TotalSize', 'R', 'C', 'L', 'Attr', 'Count', 'Command', 'Result', 'J'], [(245, 'GetExeBaseName', 'D + N', 'GetExeBaseName := D + N;'), (320, 's', "s + TwoDigit(t.Month, False) + '-' + TwoDigit(t.Day, True)", "s := s + TwoDigit(t.Month, False) + '-' + TwoDigit(t.Day, True);"), (321, 's', "s + '-' + Copy(FourDigit(t.Year),3,2)", "s := s + '-' + Copy(FourDigit(t.Year),3,2);"), (370, 'Name', 'Name + E', 'Name := Name + E;'), (392, 'Params', 'Copy(Command, ParamPos + 1, $FF)', 'Params := Copy(Command, ParamPos + 1, $FF);'), (394, 'Params', "Params + ' ' + FileName", "Params := Params + ' ' + FileName;"), (441, 'Params', "'/c ' + FileName + Params", "Params := '/c ' + FileName + Params;"), (527, 'Params', "'/c ' + Viewer + ' ' + FileName", "Params := '/c ' + Viewer + ' ' + FileName;"), (650, 'S', "Drive + ':'", "S := Drive + ':';"), (744, 'S', "Path + '\\' + F^.Name + F^.Ext", "S := Path + '\\' + F^.Name + F^.Ext;")]), ('caimath', 'caimath/PARAY.PAS', 67, ['pyxa', 'pyc', 'pyx', 'pyy', 'pyya', 'bpyxa', 'pyh', 'pyk', 'pydatachoice', 'real_delay', 'real_delay2'], [(14, 'Xdelay', 'round((real_delay2*ms)/5000)', 'Xdelay := round((real_delay2*ms)/5000);'), (188, 'bpyxa', '-50', 'bpyxa := -50;'), (194, 'pyya', 'round((pyxa*pyxa)/(4*pyc))', 'pyya  := round((pyxa*pyxa)/(4*pyc));'), (197, 'pyy', 'round((pyxa*pyxa)/(4*pyc))', 'pyy := round((pyxa*pyxa)/(4*pyc));'), (222, 'bpyxa', '-100', 'bpyxa := -100;'), (228, 'pyya', 'round((pyxa*pyxa)/(4*pyc))', 'pyya  := round((pyxa*pyxa)/(4*pyc));'), (231, 'pyy', 'round((pyxa*pyxa)/(4*pyc))', 'pyy := round((pyxa*pyxa)/(4*pyc));'), (270, 'bpyxa', '-85', 'bpyxa := -85;'), (271, 'pyc', '-10', 'pyc   := -10;'), (276, 'pyya', 'round((pyxa*pyxa)/(4*pyc))', 'pyya  := round((pyxa*pyxa)/(4*pyc));')]), ('tc', 'tc/TC/caimath/PARAY.PAS', 67, ['pyxa', 'pyc', 'pyx', 'pyy', 'pyya', 'bpyxa', 'pyh', 'pyk', 'pydatachoice', 'real_delay', 'real_delay2'], [(14, 'Xdelay', 'round((real_delay2*ms)/5000)', 'Xdelay := round((real_delay2*ms)/5000);'), (188, 'bpyxa', '-50', 'bpyxa := -50;'), (194, 'pyya', 'round((pyxa*pyxa)/(4*pyc))', 'pyya  := round((pyxa*pyxa)/(4*pyc));'), (197, 'pyy', 'round((pyxa*pyxa)/(4*pyc))', 'pyy := round((pyxa*pyxa)/(4*pyc));'), (222, 'bpyxa', '-100', 'bpyxa := -100;'), (228, 'pyya', 'round((pyxa*pyxa)/(4*pyc))', 'pyya  := round((pyxa*pyxa)/(4*pyc));'), (231, 'pyy', 'round((pyxa*pyxa)/(4*pyc))', 'pyy := round((pyxa*pyxa)/(4*pyc));'), (270, 'bpyxa', '-85', 'bpyxa := -85;'), (271, 'pyc', '-10', 'pyc   := -10;'), (276, 'pyya', 'round((pyxa*pyxa)/(4*pyc))', 'pyya  := round((pyxa*pyxa)/(4*pyc));')]), ('caimath', 'caimath/PARAX.PAS', 64, ['pxxa', 'pxc', 'pxx', 'pxy', 'pxya', 'bpxxa', 'pxh', 'pxk', 'pxdatachoice', 'real_delay', 'real_delay2'], [(14, 'Xdelay', 'round((real_delay2*ms)/5000)', 'Xdelay := round((real_delay2*ms)/5000);'), (190, 'bpxya', '-50', 'bpxya := -50;'), (196, 'pxxa', 'round((pxya*pxya)/(4*pxc))', 'pxxa  := round((pxya*pxya)/(4*pxc));'), (199, 'pxx', 'round((pxya*pxya)/(4*pxc))', 'pxx := round((pxya*pxya)/(4*pxc));'), (223, 'bpxya', '-100', 'bpxya := -100;'), (229, 'pxxa', 'round((pxya*pxya)/(4*pxc))', 'pxxa  := round((pxya*pxya)/(4*pxc));'), (232, 'pxx', 'round((pxya*pxya)/(4*pxc))', 'pxx := round((pxya*pxya)/(4*pxc));'), (270, 'bpxya', '-83', 'bpxya := -83;'), (276, 'pxxa', 'round((pxya*pxya)/(4*pxc))', 'pxxa  := round((pxya*pxya)/(4*pxc));'), (279, 'pxx', 'round((pxya*pxya)/(4*pxc))', 'pxx := round((pxya*pxya)/(4*pxc));')]), ('tc', 'tc/TC/caimath/PARAX.PAS', 64, ['pxxa', 'pxc', 'pxx', 'pxy', 'pxya', 'bpxxa', 'pxh', 'pxk', 'pxdatachoice', 'real_delay', 'real_delay2'], [(14, 'Xdelay', 'round((real_delay2*ms)/5000)', 'Xdelay := round((real_delay2*ms)/5000);'), (190, 'bpxya', '-50', 'bpxya := -50;'), (196, 'pxxa', 'round((pxya*pxya)/(4*pxc))', 'pxxa  := round((pxya*pxya)/(4*pxc));'), (199, 'pxx', 'round((pxya*pxya)/(4*pxc))', 'pxx := round((pxya*pxya)/(4*pxc));'), (223, 'bpxya', '-100', 'bpxya := -100;'), (229, 'pxxa', 'round((pxya*pxya)/(4*pxc))', 'pxxa  := round((pxya*pxya)/(4*pxc));'), (232, 'pxx', 'round((pxya*pxya)/(4*pxc))', 'pxx := round((pxya*pxya)/(4*pxc));'), (270, 'bpxya', '-83', 'bpxya := -83;'), (276, 'pxxa', 'round((pxya*pxya)/(4*pxc))', 'pxxa  := round((pxya*pxya)/(4*pxc));'), (279, 'pxx', 'round((pxya*pxya)/(4*pxc))', 'pxx := round((pxya*pxya)/(4*pxc));')]), ('caimath', 'caimath/MAIN.PAS', 58, ['real_delay', 'real_delay2', 'valout', 'x', 'y', 'err', 'a', 'w', 'row', 'col'], [(15, 'Xdelay', 'round((real_delay2*ms)/5000)', 'Xdelay := round((real_delay2*ms)/5000);'), (211, 'Ya', '-74', 'Ya := -74;'), (212, 'Xa', 'round((Ya*Ya)/(4*C))', 'Xa := round((Ya*Ya)/(4*C));'), (213, 'Y', '-74', 'Y := -74;'), (216, 'X', 'round((Y*Y)/(4*C))', 'X := round((Y*Y)/(4*C));'), (244, 'xa', '-64', 'xa := -64;'), (245, 'ya', 'round((xa*xa)/(4*c))', 'ya := round((xa*xa)/(4*c));'), (246, 'X', '-64', 'X := -64;'), (248, 'Y', 'round((X*X)/(4*C))', 'Y := round((X*X)/(4*C));'), (362, 'xa', '-64', 'xa := -64;')]), ('tc', 'tc/TC/caimath/MAIN.PAS', 58, ['real_delay', 'real_delay2', 'valout', 'x', 'y', 'err', 'a', 'w', 'row', 'col'], [(15, 'Xdelay', 'round((real_delay2*ms)/5000)', 'Xdelay := round((real_delay2*ms)/5000);'), (211, 'Ya', '-74', 'Ya := -74;'), (212, 'Xa', 'round((Ya*Ya)/(4*C))', 'Xa := round((Ya*Ya)/(4*C));'), (213, 'Y', '-74', 'Y := -74;'), (216, 'X', 'round((Y*Y)/(4*C))', 'X := round((Y*Y)/(4*C));'), (244, 'xa', '-64', 'xa := -64;'), (245, 'ya', 'round((xa*xa)/(4*c))', 'ya := round((xa*xa)/(4*c));'), (246, 'X', '-64', 'X := -64;'), (248, 'Y', 'round((X*X)/(4*C))', 'Y := round((X*X)/(4*C));'), (362, 'xa', '-64', 'xa := -64;')]), ('tc', 'tc/TC/c_grapic/2D.C', 55, ['a', 'b', 'c', 'd', 'e', 'f', 'curcolor', 'gdriver', 'gmode', 'r', 'sa', 'ea'], [(59, 'a', 'getmaxx() / 2', 'a = getmaxx() / 2;'), (60, 'b', 'getmaxy() / 2', 'b = getmaxy() / 2;'), (79, 'd', 'b-1', 'd=b-1;'), (88, 'd', 'b+1', 'd=b+1;'), (96, 'c', 'a+1', 'c=a+1;'), (105, 'c', 'a-1', 'c=a-1;'), (114, 'c', 'a+1', 'c=a+1;'), (115, 'd', 'b+1', 'd=b+1;'), (123, 'c', 'a-1', 'c=a-1;'), (124, 'd', 'b-1', 'd=b-1;')]), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', 54, [], [(64, 'next', 'p->next', 'next = p->next;'), (211, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (240, 'current', 'current->next', 'current = current->next;'), (257, 'cur', 'cur->next', 'cur = cur->next;'), (271, 'cur', 'cur->next', 'cur = cur->next;'), (285, 'res', '&(cur->data)', 'res = &(cur->data);'), (286, 'cur', 'cur->next', 'cur = cur->next;'), (337, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (359, 'cur', 'list->head.next', 'cur = list->head.next;'), (376, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', 54, [], [(68, 'next', 'p->next', 'next = p->next;'), (201, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (224, 'current', 'current->next', 'current = current->next;'), (241, 'cur', 'cur->next', 'cur = cur->next;'), (255, 'cur', 'cur->next', 'cur = cur->next;'), (269, 'res', '&(cur->data)', 'res = &(cur->data);'), (270, 'cur', 'cur->next', 'cur = cur->next;'), (318, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (339, 'cur', 'list->head.next', 'cur = list->head.next;'), (355, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 54, [], [(64, 'next', 'p->next', 'next = p->next;'), (211, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (240, 'current', 'current->next', 'current = current->next;'), (257, 'cur', 'cur->next', 'cur = cur->next;'), (271, 'cur', 'cur->next', 'cur = cur->next;'), (285, 'res', '&(cur->data)', 'res = &(cur->data);'), (286, 'cur', 'cur->next', 'cur = cur->next;'), (337, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (359, 'cur', 'list->head.next', 'cur = list->head.next;'), (376, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/LISTIMP.H', 54, [], [(68, 'next', 'p->next', 'next = p->next;'), (201, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (224, 'current', 'current->next', 'current = current->next;'), (241, 'cur', 'cur->next', 'cur = cur->next;'), (255, 'cur', 'cur->next', 'cur = cur->next;'), (269, 'res', '&(cur->data)', 'res = &(cur->data);'), (270, 'cur', 'cur->next', 'cur = cur->next;'), (318, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (339, 'cur', 'list->head.next', 'cur = list->head.next;'), (355, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/DLISTIMP.H', 54, [], [(64, 'next', 'p->next', 'next = p->next;'), (211, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (240, 'current', 'current->next', 'current = current->next;'), (257, 'cur', 'cur->next', 'cur = cur->next;'), (271, 'cur', 'cur->next', 'cur = cur->next;'), (285, 'res', '&(cur->data)', 'res = &(cur->data);'), (286, 'cur', 'cur->next', 'cur = cur->next;'), (337, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (359, 'cur', 'list->head.next', 'cur = list->head.next;'), (376, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/LISTIMP.H', 54, [], [(68, 'next', 'p->next', 'next = p->next;'), (201, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (224, 'current', 'current->next', 'current = current->next;'), (241, 'cur', 'cur->next', 'cur = cur->next;'), (255, 'cur', 'cur->next', 'cur = cur->next;'), (269, 'res', '&(cur->data)', 'res = &(cur->data);'), (270, 'cur', 'cur->next', 'cur = cur->next;'), (318, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (339, 'cur', 'list->head.next', 'cur = list->head.next;'), (355, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', 54, [], [(64, 'next', 'p->next', 'next = p->next;'), (211, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (240, 'current', 'current->next', 'current = current->next;'), (257, 'cur', 'cur->next', 'cur = cur->next;'), (271, 'cur', 'cur->next', 'cur = cur->next;'), (285, 'res', '&(cur->data)', 'res = &(cur->data);'), (286, 'cur', 'cur->next', 'cur = cur->next;'), (337, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (359, 'cur', 'list->head.next', 'cur = list->head.next;'), (376, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', 54, [], [(68, 'next', 'p->next', 'next = p->next;'), (201, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (224, 'current', 'current->next', 'current = current->next;'), (241, 'cur', 'cur->next', 'cur = cur->next;'), (255, 'cur', 'cur->next', 'cur = cur->next;'), (269, 'res', '&(cur->data)', 'res = &(cur->data);'), (270, 'cur', 'cur->next', 'cur = cur->next;'), (318, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (339, 'cur', 'list->head.next', 'cur = list->head.next;'), (355, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 54, [], [(64, 'next', 'p->next', 'next = p->next;'), (211, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (240, 'current', 'current->next', 'current = current->next;'), (257, 'cur', 'cur->next', 'cur = cur->next;'), (271, 'cur', 'cur->next', 'cur = cur->next;'), (285, 'res', '&(cur->data)', 'res = &(cur->data);'), (286, 'cur', 'cur->next', 'cur = cur->next;'), (337, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (359, 'cur', 'list->head.next', 'cur = list->head.next;'), (376, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/Project/Roof/TC/CLASSLIB/INCLUDE/LISTIMP.H', 54, [], [(68, 'next', 'p->next', 'next = p->next;'), (201, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (224, 'current', 'current->next', 'current = current->next;'), (241, 'cur', 'cur->next', 'cur = cur->next;'), (255, 'cur', 'cur->next', 'cur = cur->next;'), (269, 'res', '&(cur->data)', 'res = &(cur->data);'), (270, 'cur', 'cur->next', 'cur = cur->next;'), (318, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (339, 'cur', 'list->head.next', 'cur = list->head.next;'), (355, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 54, [], [(64, 'next', 'p->next', 'next = p->next;'), (211, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (240, 'current', 'current->next', 'current = current->next;'), (257, 'cur', 'cur->next', 'cur = cur->next;'), (271, 'cur', 'cur->next', 'cur = cur->next;'), (285, 'res', '&(cur->data)', 'res = &(cur->data);'), (286, 'cur', 'cur->next', 'cur = cur->next;'), (337, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (359, 'cur', 'list->head.next', 'cur = list->head.next;'), (376, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/TC/CLASSLIB/INCLUDE/LISTIMP.H', 54, [], [(68, 'next', 'p->next', 'next = p->next;'), (201, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (224, 'current', 'current->next', 'current = current->next;'), (241, 'cur', 'cur->next', 'cur = cur->next;'), (255, 'cur', 'cur->next', 'cur = cur->next;'), (269, 'res', '&(cur->data)', 'res = &(cur->data);'), (270, 'cur', 'cur->next', 'cur = cur->next;'), (318, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (339, 'cur', 'list->head.next', 'cur = list->head.next;'), (355, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/TC/OUTPUT/RoofAndCurtain/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 54, [], [(64, 'next', 'p->next', 'next = p->next;'), (211, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (240, 'current', 'current->next', 'current = current->next;'), (257, 'cur', 'cur->next', 'cur = cur->next;'), (271, 'cur', 'cur->next', 'cur = cur->next;'), (285, 'res', '&(cur->data)', 'res = &(cur->data);'), (286, 'cur', 'cur->next', 'cur = cur->next;'), (337, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (359, 'cur', 'list->head.next', 'cur = list->head.next;'), (376, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/TC/OUTPUT/RoofAndCurtain/TC/CLASSLIB/INCLUDE/LISTIMP.H', 54, [], [(68, 'next', 'p->next', 'next = p->next;'), (201, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (224, 'current', 'current->next', 'current = current->next;'), (241, 'cur', 'cur->next', 'cur = cur->next;'), (255, 'cur', 'cur->next', 'cur = cur->next;'), (269, 'res', '&(cur->data)', 'res = &(cur->data);'), (270, 'cur', 'cur->next', 'cur = cur->next;'), (318, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (339, 'cur', 'list->head.next', 'cur = list->head.next;'), (355, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/SORT/COVERRED.PAS', 52, ['curx', 'cury', 'tarx', 'tary', 'col', 'stepx', 'stepy', 'totalpixel', 'color', 'colorcount', 'fadecount'], [(11, 'picturexofs', '(639-picturewidth) div 2', 'picturexofs = (639-picturewidth) div 2;'), (12, 'pictureyofs', '(479-pictureheight) div 2', 'pictureyofs = (479-pictureheight) div 2;'), (74, 'curx', 'random(639+1) shl step', 'curx:=random(639+1) shl step;'), (75, 'cury', 'random(479+1) shl step', 'cury:=random(479+1) shl step;'), (76, 'tarx', '(picturexofs+xc-1) shl step', 'tarx:=(picturexofs+xc-1) shl step;'), (77, 'tary', '(pictureyofs+yc-1) shl step', 'tary:=(pictureyofs+yc-1) shl step;'), (78, 'stepx', '(tarx-curx) div 64', 'stepx:=(tarx-curx) div 64;'), (79, 'stepy', '(tary-cury) div 64', 'stepy:=(tary-cury) div 64;'), (174, 'memw[$a000:(((y-1) shl 1)*320+(x shl 1))]', '(c shl 8) + c', 'memw[$a000:(((y-1) shl 1)*320+(x shl 1))] := (c shl 8) + c;'), (175, 'memw[$a000:(((y shl 1)-1)*320+(x shl 1))]', '(c shl 8) + c', 'memw[$a000:(((y shl 1)-1)*320+(x shl 1))] := (c shl 8) + c;')]), ('tc', 'tc/TC/sort/COVERRED.PAS', 52, ['curx', 'cury', 'tarx', 'tary', 'col', 'stepx', 'stepy', 'totalpixel', 'color', 'colorcount', 'fadecount'], [(11, 'picturexofs', '(639-picturewidth) div 2', 'picturexofs = (639-picturewidth) div 2;'), (12, 'pictureyofs', '(479-pictureheight) div 2', 'pictureyofs = (479-pictureheight) div 2;'), (74, 'curx', 'random(639+1) shl step', 'curx:=random(639+1) shl step;'), (75, 'cury', 'random(479+1) shl step', 'cury:=random(479+1) shl step;'), (76, 'tarx', '(picturexofs+xc-1) shl step', 'tarx:=(picturexofs+xc-1) shl step;'), (77, 'tary', '(pictureyofs+yc-1) shl step', 'tary:=(pictureyofs+yc-1) shl step;'), (78, 'stepx', '(tarx-curx) div 64', 'stepx:=(tarx-curx) div 64;'), (79, 'stepy', '(tary-cury) div 64', 'stepy:=(tary-cury) div 64;'), (174, 'memw[$a000:(((y-1) shl 1)*320+(x shl 1))]', '(c shl 8) + c', 'memw[$a000:(((y-1) shl 1)*320+(x shl 1))] := (c shl 8) + c;'), (175, 'memw[$a000:(((y shl 1)-1)*320+(x shl 1))]', '(c shl 8) + c', 'memw[$a000:(((y shl 1)-1)*320+(x shl 1))] := (c shl 8) + c;')]), ('tc', 'tc/TC/sort/sort/COVERRED.PAS', 52, ['curx', 'cury', 'tarx', 'tary', 'col', 'stepx', 'stepy', 'totalpixel', 'color', 'colorcount', 'fadecount'], [(11, 'picturexofs', '(639-picturewidth) div 2', 'picturexofs = (639-picturewidth) div 2;'), (12, 'pictureyofs', '(479-pictureheight) div 2', 'pictureyofs = (479-pictureheight) div 2;'), (74, 'curx', 'random(639+1) shl step', 'curx:=random(639+1) shl step;'), (75, 'cury', 'random(479+1) shl step', 'cury:=random(479+1) shl step;'), (76, 'tarx', '(picturexofs+xc-1) shl step', 'tarx:=(picturexofs+xc-1) shl step;'), (77, 'tary', '(pictureyofs+yc-1) shl step', 'tary:=(pictureyofs+yc-1) shl step;'), (78, 'stepx', '(tarx-curx) div 64', 'stepx:=(tarx-curx) div 64;'), (79, 'stepy', '(tary-cury) div 64', 'stepy:=(tary-cury) div 64;'), (174, 'memw[$a000:(((y-1) shl 1)*320+(x shl 1))]', '(c shl 8) + c', 'memw[$a000:(((y-1) shl 1)*320+(x shl 1))] := (c shl 8) + c;'), (175, 'memw[$a000:(((y shl 1)-1)*320+(x shl 1))]', '(c shl 8) + c', 'memw[$a000:(((y shl 1)-1)*320+(x shl 1))] := (c shl 8) + c;')]), ('tc', 'tc/SORT/ALLSORT.PAS', 47, ['i', 'status'], [(62, 'tmp', 'a[i-1]', 'tmp:=a[i-1];'), (65, 'child', '(i)*2', 'child:=(i)*2;'), (71, 'a[i-1]', 'a[child-1]', 'a[i-1]:=a[child-1];'), (154, 'num', 'abs(right-left)+1', 'num:=abs(right-left)+1;'), (155, 'leftend', 'center-1', 'leftend:=center-1;'), (156, 'tmp', 'left+1', 'tmp:=left+1;'), (183, 'x[right]', 'temp[right+1]', 'x[right]:=temp[right+1];'), (204, 'num', 'abs(right-left)+1', 'num:=abs(right-left)+1;'), (207, 'leftend', 'center-1', 'leftend:=center-1;'), (210, 'tmp', 'left+1', 'tmp:=left+1;')]), ('tc', 'tc/TC/sort/ALLSORT.PAS', 47, ['i', 'status'], [(62, 'tmp', 'a[i-1]', 'tmp:=a[i-1];'), (65, 'child', '(i)*2', 'child:=(i)*2;'), (71, 'a[i-1]', 'a[child-1]', 'a[i-1]:=a[child-1];'), (154, 'num', 'abs(right-left)+1', 'num:=abs(right-left)+1;'), (155, 'leftend', 'center-1', 'leftend:=center-1;'), (156, 'tmp', 'left+1', 'tmp:=left+1;'), (183, 'x[right]', 'temp[right+1]', 'x[right]:=temp[right+1];'), (204, 'num', 'abs(right-left)+1', 'num:=abs(right-left)+1;'), (207, 'leftend', 'center-1', 'leftend:=center-1;'), (210, 'tmp', 'left+1', 'tmp:=left+1;')]), ('tc', 'tc/TC/sort/sort/ALLSORT.PAS', 47, ['i', 'status'], [(62, 'tmp', 'a[i-1]', 'tmp:=a[i-1];'), (65, 'child', '(i)*2', 'child:=(i)*2;'), (71, 'a[i-1]', 'a[child-1]', 'a[i-1]:=a[child-1];'), (154, 'num', 'abs(right-left)+1', 'num:=abs(right-left)+1;'), (155, 'leftend', 'center-1', 'leftend:=center-1;'), (156, 'tmp', 'left+1', 'tmp:=left+1;'), (183, 'x[right]', 'temp[right+1]', 'x[right]:=temp[right+1];'), (204, 'num', 'abs(right-left)+1', 'num:=abs(right-left)+1;'), (207, 'leftend', 'center-1', 'leftend:=center-1;'), (210, 'tmp', 'left+1', 'tmp:=left+1;')]), ('tc', 'tc/EXAMPLES/MCUTIL.C', 46, ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/Project/Children/TC3/EXAMPLES/TCALC/TCUTIL.C', 46, ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/Project/Roof/TC/EXAMPLES/TCALC/TCUTIL.C', 46, ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/TC/MCUTIL.C', 46, ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/TC/Project/Children/TC3/EXAMPLES/TCALC/TCUTIL.C', 46, ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/TC/Project/Roof/TC/EXAMPLES/TCALC/TCUTIL.C', 46, ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/TC/TC/EXAMPLES/TCALC/TCUTIL.C', 46, ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/TC/TC/MCUTIL.C', 46, ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/TC/TC/OUTPUT/RoofAndCurtain/TC/EXAMPLES/TCALC/TCUTIL.C', 46, ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/TC/TCUTIL.C', 46, ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/TC/port/control2/MCUTIL.C', 46, ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/INCLUDE/GRAPHICS.H', 43, ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(45, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page\t*/'), (46, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page\t*/'), (48, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page\t*/'), (50, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page\t*/'), (51, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page\t*/'), (52, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page\t*/'), (53, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page\t*/'), (62, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page\t*/'), (63, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page\t*/'), (64, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page\t*/')]), ('tc', 'tc/Project/Bin/Tc3/INCLUDE/GRAPHICS.H', 43, ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(43, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page   */'), (44, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page   */'), (46, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page   */'), (48, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page   */'), (49, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page   */'), (50, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page   */'), (51, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page   */'), (60, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page   */'), (61, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page   */'), (62, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page   */')]), ('tc', 'tc/Project/Children/TC3/INCLUDE/GRAPHICS.H', 43, ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(43, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page   */'), (44, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page   */'), (46, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page   */'), (48, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page   */'), (49, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page   */'), (50, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page   */'), (51, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page   */'), (60, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page   */'), (61, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page   */'), (62, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page   */')]), ('tc', 'tc/Project/Roof/TC/INCLUDE/GRAPHICS.H', 43, ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(43, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page   */'), (44, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page   */'), (46, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page   */'), (48, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page   */'), (49, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page   */'), (50, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page   */'), (51, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page   */'), (60, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page   */'), (61, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page   */'), (62, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page   */')]), ('tc', 'tc/TC/GRAPHICS.H', 43, ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(45, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page\t*/'), (46, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page\t*/'), (48, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page\t*/'), (50, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page\t*/'), (51, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page\t*/'), (52, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page\t*/'), (53, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page\t*/'), (62, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page\t*/'), (63, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page\t*/'), (64, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page\t*/')]), ('tc', 'tc/TC/INCLUDE/GRAPHICS.H', 43, ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(45, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page\t*/'), (46, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page\t*/'), (48, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page\t*/'), (50, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page\t*/'), (51, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page\t*/'), (52, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page\t*/'), (53, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page\t*/'), (62, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page\t*/'), (63, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page\t*/'), (64, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page\t*/')]), ('tc', 'tc/TC/Project/Bin/Tc3/INCLUDE/GRAPHICS.H', 43, ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(43, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page   */'), (44, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page   */'), (46, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page   */'), (48, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page   */'), (49, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page   */'), (50, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page   */'), (51, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page   */'), (60, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page   */'), (61, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page   */'), (62, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page   */')]), ('tc', 'tc/TC/Project/Children/TC3/INCLUDE/GRAPHICS.H', 43, ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(43, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page   */'), (44, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page   */'), (46, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page   */'), (48, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page   */'), (49, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page   */'), (50, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page   */'), (51, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page   */'), (60, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page   */'), (61, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page   */'), (62, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page   */')]), ('tc', 'tc/TC/Project/Roof/TC/INCLUDE/GRAPHICS.H', 43, ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(43, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page   */'), (44, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page   */'), (46, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page   */'), (48, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page   */'), (49, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page   */'), (50, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page   */'), (51, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page   */'), (60, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page   */'), (61, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page   */'), (62, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page   */')]), ('tc', 'tc/TC/TC/GRAPHICS.H', 43, ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(43, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page   */'), (44, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page   */'), (46, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page   */'), (48, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page   */'), (49, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page   */'), (50, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page   */'), (51, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page   */'), (60, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page   */'), (61, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page   */'), (62, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page   */')]), ('tc', 'tc/TC/TC/INCLUDE/GRAPHICS.H', 43, ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(43, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page   */'), (44, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page   */'), (46, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page   */'), (48, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page   */'), (49, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page   */'), (50, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page   */'), (51, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page   */'), (60, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page   */'), (61, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page   */'), (62, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page   */')]), ('tc', 'tc/TC/TC/OUTPUT/RoofAndCurtain/TC/INCLUDE/GRAPHICS.H', 43, ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(43, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page   */'), (44, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page   */'), (46, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page   */'), (48, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page   */'), (49, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page   */'), (50, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page   */'), (51, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page   */'), (60, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page   */'), (61, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page   */'), (62, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page   */')]), ('tc', 'tc/TC/genetic/GRAPHICS.H', 43, ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(45, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page\t*/'), (46, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page\t*/'), (48, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page\t*/'), (50, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page\t*/'), (51, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page\t*/'), (52, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page\t*/'), (53, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page\t*/'), (62, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page\t*/'), (63, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page\t*/'), (64, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page\t*/')]), ('caimath', 'caimath/START.PAS', 40, ['x', 'y', 'c', 'ya', 'xa', 'i', 'd', 'co', 'l', 'p', 'xx', 'yy'], [(11, 'Ya', '-88', 'Ya := -88;'), (12, 'Xa', 'round((Ya*Ya)/(4*C))', 'Xa := round((Ya*Ya)/(4*C));'), (16, 'X', 'round((Y*Y)/(4*C))', 'X := round((Y*Y)/(4*C));'), (30, 'xa', '-88', 'xa := -88;'), (31, 'ya', 'round((xa*xa)/(4*c))', 'ya := round((xa*xa)/(4*c));'), (34, 'Y', 'round((X*X)/(4*C))', 'Y := round((X*X)/(4*C));'), (47, 'Xa', '-105', 'Xa := -105;'), (48, 'Ya', 'round((Xa*Xa)/(4*C))', 'Ya := round((Xa*Xa)/(4*C));'), (51, 'Y', 'round((X*X)/(4*C))', 'Y := round((X*X)/(4*C));'), (63, 'Xa', '-125', 'Xa := -125;')]), ('tc', 'tc/EXAMPLES/BGIDEMO.C', 40, ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(160, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (166, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (254, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (305, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (316, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (317, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (318, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (332, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (338, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (359, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/EXAMPLES/CBAR.C', 40, ['xdelta', 'ydelta', 'xstep', 'ystep', 'change', 'count', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4', 'wfactor', 'hfactor'], [(31, 'xdelta', 'x2 - x1', 'xdelta = x2 - x1;               /* Calculate the change in x coordinates */'), (32, 'ydelta', 'y2 - y1', 'ydelta = y2 - y1;               /* Calculate the change in y coordinates */'), (35, 'xdelta', '-xdelta', 'xdelta = -xdelta;'), (36, 'xstep', '-1', 'xstep = -1;'), (42, 'ydelta', '-ydelta', 'ydelta = -ydelta;'), (43, 'ystep', '-1', 'ystep = -1;'), (107, 'wfactor', 'width / 5', 'wfactor = width / 5;     /* figure out wfactor and hfactor */'), (108, 'hfactor', 'height / 12', 'hfactor = height / 12;'), (109, 'x2', 'x1 + wfactor', 'x2 = x1 + wfactor;       /* compute the location of the points on the bar */'), (110, 'x3', 'x1 + width', 'x3 = x1 + width;')]), ('tc', 'tc/Project/Bin/BGI/BGIDEMO.C', 40, ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/Project/Children/BGI/BGIDEMO.C', 40, ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/Project/Children/TC3/BGI/BGIDEMO.C', 40, ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/Project/Children/TC3/BIN/HOME.C', 40, ['up', 'down', 'ph', 'pr', 'y', 'use', 'hour', 'min', 't', 'sensor', 'chk_choice', 'int', 'chk_pos_home', 'chk_pos_auto', 'a', 'n', 'press', 'b', 'choice', 'm'], [(376, 'a', 'a-5', 'a=a-5;'), (380, 'a', 'a-10', 'a=a-10;'), (383, 'a', 'a-14', 'a=a-14;'), (406, 'a', 'y-130', 'a=y-130;\ta=a/20;'), (410, 'a', 'y-130', 'a=y-130;\ta=a/20;'), (414, 'a', 'y-260', 'a=y-260;\ta=a/20;'), (418, 'a', 'y-260', 'a=y-260;\ta=a/20;'), (429, 'a', 'y-130', 'a=y-130;\ta=a/20;'), (433, 'a', 'y-130', 'a=y-130;\ta=a/20;'), (867, 'a', 'area->tm_mday', 'a = area->tm_mday;')]), ('tc', 'tc/Project/ClothLine/BGI/BGIDEMO.C', 40, ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/Project/Roof/BGI/BGIDEMO.C', 40, ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/Project/Roof/TC/BGI/BGIDEMO.C', 40, ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/Project/Roof/TC/BIN/ASSIGN1.CPP', 40, ['list', 'any1', 'a', 'b', 'v', 'temp', 'm', 't', 'i', 'j', 'q', 'k', 'min', 'max1', 'any2'], [(33, 'list[b]', 'list[b-1]', 'list[b] = list[b-1];'), (34, 'b', 'b - 1', 'b = b - 1;'), (75, 'm', '(max2-min2+1)/2', 'm = (max2-min2+1)/2;'), (77, 'max2', 'max2-1', 'max2=max2-1;'), (83, 'i', 'min2+1', 'i = min2+1;'), (84, 'j', 'max2-1', 'j = max2-1;'), (89, 'i', 'i+1', 'i=i+1;'), (93, 'j', 'j-1', 'j=j-1;'), (126, 'k', 'rand()', 'k = rand();'), (137, 'i', 'i + 1', 'i = i + 1;')]), ('tc', 'tc/Project/Roof/TC/BIN/SU.CPP', 40, ['objlength', 'start_loc', 'add_length', 'plus_minus', 'csect', 'ascii', 'locctr', 'proglength', 'progstart', 'textstart', 'textaddr', 'textlength', 'textarray', 'pc', 'base', 'current_mod', 'litpool', 'litpool1', 'litpool2', 'linenum'], [(306, 'tempo', 'optab[i+1].opcode', 'tempo = optab[i+1].opcode;'), (397, 'hash', 'hash + (unsigned char)(symbol[i])', 'hash = hash + (unsigned char)(symbol[i]);'), (398, 'hash', 'hash % (SYMTABLIMIT + 1)', 'hash = hash % (SYMTABLIMIT + 1);'), (419, 'ptr', '(ptr + 1) % (SYMTABLIMIT + 1)', 'ptr = (ptr + 1) % (SYMTABLIMIT + 1);'), (450, 'ptr', '(ptr + 1) % (SYMTABLIMIT + 1)', 'ptr = (ptr + 1) % (SYMTABLIMIT + 1);'), (469, 'hash', 'hash + (unsigned char)(literal[i])', 'hash = hash + (unsigned char)(literal[i]);'), (470, 'hash', 'hash % (SYMTABLIMIT + 1)', 'hash = hash % (SYMTABLIMIT + 1);'), (491, 'ptr', '(ptr + 1) % (SYMTABLIMIT + 1)', 'ptr = (ptr + 1) % (SYMTABLIMIT + 1);'), (509, 'textlength', 'textlength + littab[i].length', 'textlength = textlength + littab[i].length;'), (510, 'textaddr', 'locctr + littab[i].length / 2', 'textaddr = locctr + littab[i].length / 2;')]), ('tc', 'tc/SORT/TEST.PAS', 40, ['age', 'oldh', 'oldm', 'olds', 'oldTime', 'Timeuse', 'i', 'Tmp', 'a', 'k', 'b', 'line', 'code', 'g', 'x', 'y', 'oldTm', 'timecomfort', 'maxp'], [(16, 'Stoptopic', "'*'", "Stoptopic = '*';   {for stop each topic}"), (254, 'secondToForm', "s1+':'+s2", "secondToForm := s1+':'+s2;"), (296, 'st', 'secondToform(Round((time-oldtime)/18.2))', 'st := secondToform(Round((time-oldtime)/18.2));'), (432, 'topic[t]', 'random(21)', 'topic[t]:=random(21);'), (434, 'se', 'se+[topic[t]]', 'se := se+[topic[t]];'), (455, 'Timeuse', 'Round((Time-oldTm)/18.2)', 'Timeuse := Round((Time-oldTm)/18.2);'), (499, 'i', 'random(15)+1', 'i := random(15)+1;'), (578, 'countArea', 'CountArea+2', 'countArea := CountArea+2;'), (586, 'upscrollbox', '46+((countp-1)*(310 div maxp))', 'upscrollbox := 46+((countp-1)*(310 div maxp));'), (587, 'downscrollBox', '46+(countp*(310 div maxp))', 'downscrollBox :=46+(countp*(310 div maxp));')]), ('tc', 'tc/SORT/TESTA.PAS', 40, ['attr', 'age', 'oldh', 'oldm', 'olds', 'oldTime', 'Timeuse', 'i', 'Tmp', 'a', 'k', 'b', 'line', 'code', 'g', 'x', 'y', 'oldTm', 'timecomfort', 'maxp'], [(19, 'Stoptopic', "'*'", "Stoptopic = '*';   {for stop each topic}"), (271, 'secondToForm', "s1+':'+s2", "secondToForm := s1+':'+s2;"), (311, 'st', 'secondToform(Round((time-oldtime)/18.2))', 'st := secondToform(Round((time-oldtime)/18.2));'), (445, 'topic[t]', 'random(21)', 'topic[t]:=random(21);'), (447, 'se', 'se+[topic[t]]', 'se := se+[topic[t]];'), (470, 'Timeuse', 'Round((Time-oldTm)/18.2)', 'Timeuse := Round((Time-oldTm)/18.2);'), (512, 'i', 'random(15)+1', 'i := random(15)+1;'), (591, 'countArea', 'CountArea+2', 'countArea := CountArea+2;'), (599, 'upscrollbox', '46+((countp-1)*(310 div maxp))', 'upscrollbox := 46+((countp-1)*(310 div maxp));'), (600, 'downscrollBox', '46+(countp*(310 div maxp))', 'downscrollBox :=46+(countp*(310 div maxp));')]), ('tc', 'tc/TC/BGIDEMO.C', 40, ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(160, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (166, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (254, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (305, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (316, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (317, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (318, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (332, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (338, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (359, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/TC/CBAR.C', 40, ['xdelta', 'ydelta', 'xstep', 'ystep', 'change', 'count', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4', 'wfactor', 'hfactor'], [(31, 'xdelta', 'x2 - x1', 'xdelta = x2 - x1;               /* Calculate the change in x coordinates */'), (32, 'ydelta', 'y2 - y1', 'ydelta = y2 - y1;               /* Calculate the change in y coordinates */'), (35, 'xdelta', '-xdelta', 'xdelta = -xdelta;'), (36, 'xstep', '-1', 'xstep = -1;'), (42, 'ydelta', '-ydelta', 'ydelta = -ydelta;'), (43, 'ystep', '-1', 'ystep = -1;'), (107, 'wfactor', 'width / 5', 'wfactor = width / 5;     /* figure out wfactor and hfactor */'), (108, 'hfactor', 'height / 12', 'hfactor = height / 12;'), (109, 'x2', 'x1 + wfactor', 'x2 = x1 + wfactor;       /* compute the location of the points on the bar */'), (110, 'x3', 'x1 + width', 'x3 = x1 + width;')]), ('tc', 'tc/TC/DOUBLE/DOUBBLE.PAS', 40, ['code', 'Side1', 'A', 'B', 'Side2', 'C', 'D', 'Raduis', 'E', 'F', 'a', 'b', 'c', 'x', 'y', 'Meanweek', 'Maxweek', 'Minweek', 'i', 'j'], [(17, 's', 's+c', 's := s+c;'), (62, 'a', 'side1*side1', 'a := side1*side1;'), (63, 'b', '4*side1', 'b := 4*side1;'), (97, 'c', 'side1*side2', 'c := side1*side2;'), (98, 'd', '2*(side1+side2)', 'd := 2*(side1+side2);'), (130, 'e', 'pi * (raduis * raduis)', 'e := pi * (raduis * raduis);'), (131, 'f', '2 * pi * raduis', 'f := 2 * pi * raduis;'), (208, 'x', 'a*a', 'x := a*a;'), (209, 'y', '(b*b) + (c*c)', 'y := (b*b) + (c*c);'), (274, 'sumt', 'sumt+t[i,j]', 'sumt:=sumt+t[i,j];')]), ('tc', 'tc/TC/EXAMP/Project/BGI/BGIDEMO.C', 40, ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/TC/EXAMP/Project/BLOCK.C', 40, ['id', 'num', 'i', 'j', 'chk', 'a', 'b', 'c', 'd', 'str', 'press', 'x', 'y', 'k', 'l', 'm', 'sum', 'aa', 'w', 'sw'], [(720, 'data[j]', 'data[j+1]', 'data[j]=data[j+1];'), (737, 'data[j]', 'data[j+1]', 'data[j]=data[j+1];'), (3008, 'led_t[i]', 'z->b[i]', 'led_t[i]=z->b[i];'), (3010, 'speed[i]', 'z->c[i]', 'speed[i]=z->c[i];'), (3161, 'c_led[i]', 'z->a[i]', 'c_led[i]=z->a[i];'), (3303, 'i', 'z->i', 'i=z->i;'), (3304, 'j', 'z->j', 'j=z->j;'), (3347, 'j', 'j-6', 'j=j-6;'), (3435, 'i', 'z->i', 'i=z->i;'), (3559, 'sw[j]', 'z->a[j]', 'sw[j]=z->a[j];')]), ('tc', 'tc/TC/FACE.C', 40, ['x', 'y', 'radius', 'mood', 'ch', 'i', 'color', 'r', 'imgsize', 'dif', 'x1', 'x2', 'y1', 'y2'], [(33, 'x', 'face1->position.x=320', 'x=face1->position.x=320;'), (34, 'y', 'face1->position.y=180', 'y=face1->position.y=180;'), (37, 'r', 'face1->radius', 'r=face1->radius;'), (52, 'x', 'face1->position.x', 'x=face1->position.x;'), (53, 'y', 'face1->position.y', 'y=face1->position.y;'), (54, 'r', 'face1->radius', 'r=face1->radius;'), (66, 'r', 'face1->radius', 'r=face1->radius;'), (67, 'x1', 'face1->position.x-r/2', 'x1=face1->position.x-r/2;'), (68, 'y1', 'face1->position.y-r/4', 'y1=face1->position.y-r/4;'), (69, 'x2', 'face1->position.x+r/2', 'x2=face1->position.x+r/2;')]), ('tc', 'tc/TC/LENSCAI/LENSCAI.PAS', 40, ['Row', 'Col', 'MaxColumn', 'Maxmenu', 'CharNo', 'ByteNo', 'Ind', 'Len', 'xx', 'yy', 'x2', 'y2', 'c1', 'c2', 'x', 'y', 'd', 'yinc', 'i', 'f'], [(109, 'x2', 'x1+12*9+8', 'x2:=x1+12*9+8;'), (110, 'y2', 'y1+27', 'y2:=y1+27;'), (211, 'x', 'Random(GetMaxX)', 'x := Random(GetMaxX);'), (212, 'y', 'Random(GetMaxY)', 'y := Random(GetMaxY);'), (213, 'd', 'Random(7)', 'd := Random(7);'), (225, 'x', 'x + 1 * (d + 1)', 'x := x + 1 * (d + 1);'), (228, 'y', 'y + 0  * (d + 1)', 'y := y + 0  * (d + 1);'), (320, 'St', 'St+p', 'St:=St+p;'), (350, 'm', 'I/O', 'm :=I/O;'), (383, 'sdat', '(s*f)/(s-f)', 'sdat :=(s*f)/(s-f);')]), ('tc', 'tc/TC/Project/Bin/BGI/BGIDEMO.C', 40, ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/TC/Project/Children/BGI/BGIDEMO.C', 40, ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/TC/Project/Children/TC3/BGI/BGIDEMO.C', 40, ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/TC/Project/Children/TC3/BIN/HOME.C', 40, ['up', 'down', 'ph', 'pr', 'y', 'use', 'hour', 'min', 't', 'sensor', 'chk_choice', 'int', 'chk_pos_home', 'chk_pos_auto', 'a', 'n', 'press', 'b', 'choice', 'm'], [(376, 'a', 'a-5', 'a=a-5;'), (380, 'a', 'a-10', 'a=a-10;'), (383, 'a', 'a-14', 'a=a-14;'), (406, 'a', 'y-130', 'a=y-130;\ta=a/20;'), (410, 'a', 'y-130', 'a=y-130;\ta=a/20;'), (414, 'a', 'y-260', 'a=y-260;\ta=a/20;'), (418, 'a', 'y-260', 'a=y-260;\ta=a/20;'), (429, 'a', 'y-130', 'a=y-130;\ta=a/20;'), (433, 'a', 'y-130', 'a=y-130;\ta=a/20;'), (867, 'a', 'area->tm_mday', 'a = area->tm_mday;')]), ('tc', 'tc/TC/Project/ClothLine/BGI/BGIDEMO.C', 40, ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/TC/Project/Roof/BGI/BGIDEMO.C', 40, ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/TC/Project/Roof/TC/BGI/BGIDEMO.C', 40, ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/TC/Project/Roof/TC/BIN/ASSIGN1.CPP', 40, ['list', 'any1', 'a', 'b', 'v', 'temp', 'm', 't', 'i', 'j', 'q', 'k', 'min', 'max1', 'any2'], [(33, 'list[b]', 'list[b-1]', 'list[b] = list[b-1];'), (34, 'b', 'b - 1', 'b = b - 1;'), (75, 'm', '(max2-min2+1)/2', 'm = (max2-min2+1)/2;'), (77, 'max2', 'max2-1', 'max2=max2-1;'), (83, 'i', 'min2+1', 'i = min2+1;'), (84, 'j', 'max2-1', 'j = max2-1;'), (89, 'i', 'i+1', 'i=i+1;'), (93, 'j', 'j-1', 'j=j-1;'), (126, 'k', 'rand()', 'k = rand();'), (137, 'i', 'i + 1', 'i = i + 1;')]), ('tc', 'tc/TC/Project/Roof/TC/BIN/SU.CPP', 40, ['objlength', 'start_loc', 'add_length', 'plus_minus', 'csect', 'ascii', 'locctr', 'proglength', 'progstart', 'textstart', 'textaddr', 'textlength', 'textarray', 'pc', 'base', 'current_mod', 'litpool', 'litpool1', 'litpool2', 'linenum'], [(306, 'tempo', 'optab[i+1].opcode', 'tempo = optab[i+1].opcode;'), (397, 'hash', 'hash + (unsigned char)(symbol[i])', 'hash = hash + (unsigned char)(symbol[i]);'), (398, 'hash', 'hash % (SYMTABLIMIT + 1)', 'hash = hash % (SYMTABLIMIT + 1);'), (419, 'ptr', '(ptr + 1) % (SYMTABLIMIT + 1)', 'ptr = (ptr + 1) % (SYMTABLIMIT + 1);'), (450, 'ptr', '(ptr + 1) % (SYMTABLIMIT + 1)', 'ptr = (ptr + 1) % (SYMTABLIMIT + 1);'), (469, 'hash', 'hash + (unsigned char)(literal[i])', 'hash = hash + (unsigned char)(literal[i]);'), (470, 'hash', 'hash % (SYMTABLIMIT + 1)', 'hash = hash % (SYMTABLIMIT + 1);'), (491, 'ptr', '(ptr + 1) % (SYMTABLIMIT + 1)', 'ptr = (ptr + 1) % (SYMTABLIMIT + 1);'), (509, 'textlength', 'textlength + littab[i].length', 'textlength = textlength + littab[i].length;'), (510, 'textaddr', 'locctr + littab[i].length / 2', 'textaddr = locctr + littab[i].length / 2;')]), ('tc', 'tc/TC/S26/TETRIS.C', 40, ['RightArrow', 'LeftArrow', 'UpArrow', 'DownArrow', 'Space', 'Esc', 'far', 'TypeTris', 'Tris1', 'Tris2', 'Tris3', 'Tris4', 'Tris5', 'Tris6', 'BColor', 'No_Tris', 'NumTris', 'OldNumTris', 'ArrayTris', 'ColorTris'], [(43, 'ptr0', 'FirstAdr[page] + 1', 'ptr0 = FirstAdr[page] + 1;'), (44, 'ptr1', 'FirstAdr[3] + 1', 'ptr1 = FirstAdr[3] + 1;'), (80, 'ptr', 'TypeTris[num] + (n << 3)', 'ptr = TypeTris[num] + (n << 3);'), (92, 'ptr', 'TypeTris[num] + (NumTris << 3)', 'ptr = TypeTris[num] + (NumTris << 3);'), (104, 'ptr', 'TypeTris[num] + (NumTris << 3)', 'ptr = TypeTris[num] + (NumTris << 3);'), (107, 'Y', 'YTris + *(ptr + 1)', 'Y = YTris + *(ptr + 1);'), (119, 'pl1', '48+(sin(k / 30) * 47.0 + 256 * (int)(47 * cos(k / 40)))', 'pl1 = 48+(sin(k / 30) * 47.0 + 256 * (int)(47 * cos(k / 40)));'), (120, 'pl2', '48+(sin(k / 14) * 47.0 + 256 * (int)(47 * sin(k / 32))) - pl1', 'pl2 = 48+(sin(k / 14) * 47.0 + 256 * (int)(47 * sin(k / 32))) - pl1;'), (121, 'ptr0', 'BKdata + pl1', 'ptr0 = BKdata + pl1;'), (126, 'color', '((*ptr0++) + pl2)', 'color = ((*ptr0++) + pl2);')]), ('tc', 'tc/TC/S33/BOMBER.C', 40, ['RightArrow', 'LeftArrow', 'UpArrow', 'DownArrow', 'Space', 'Esc', 'ch', 'ScanCode', 'BitImage', 'i', 'ptr', 'j', 'memtmp', 'width', 'height', 'ptr1', 'Map', 'Skip', 'MAXGOST1', 'MAXBOOM1'], [(219, 'width', '*ptr1++', 'width = *ptr1++; height = *ptr1++;'), (226, 'width', '*ptr++', 'width = *ptr++; height = *ptr++;'), (243, 'width', '*ptr++', 'width = *ptr++;'), (244, 'height', '*ptr++', 'height = *ptr++;'), (245, 'BitImage[num]', 'malloc((width << 1) * height + 2)', 'BitImage[num] = malloc((width << 1) * height + 2);'), (264, 'width', '*ptr++', 'width = *ptr++; height = *ptr++;'), (265, 'BitImage[num1]', 'malloc(width * height + 2)', 'BitImage[num1] = malloc(width * height + 2);'), (322, 'i', '(x - 5) / 12', 'i = (x - 5) / 12; j = (y - 3) / 12;'), (362, 'Addx', 'Gxgost[i] + addmove[Gran[i]][0]', 'Addx = Gxgost[i] + addmove[Gran[i]][0];'), (363, 'Addy', 'Gygost[i] + addmove[Gran[i]][1]', 'Addy = Gygost[i] + addmove[Gran[i]][1];')]), ('tc', 'tc/TC/S34/CUTSPRIT.C', 40, ['far', 'int', 'i', 'j', 'x1', 'y1', 'MouseX', 'MouseY', 'oMouseX', 'oMouseY', 'mousebutt', 'StMouse', 'MouseT', 'MouseT1', 'Palette', 'Image', 'Back', 'namefile', 'Numi', 'Post'], [(20, 'LINE_Y[i]', 'i * 320', 'LINE_Y[i] = i * 320;'), (68, 'x1', 'x0 + *ptr++', 'x1 = x0 + *ptr++; y1 = y0 + *ptr++;'), (213, 'StMouse', '-1', 'StMouse = -1;'), (284, 'Membuf', 'malloc(WHeight * WWidth)', 'Membuf = malloc(WHeight * WWidth);'), (290, 'l', 'c - 192', 'l = c - 192;'), (365, 'oGx', 'FGx + 1', 'oGx  = FGx + 1;'), (367, 'oGy', 'FGy + 1', 'oGy  = FGy + 1;'), (398, 'width', '*ptr++', 'width  = *ptr++;'), (399, 'height', '*ptr++', 'height = *ptr++;'), (416, 'red', '*ptr++', 'red   = *ptr++;')]), ('tc', 'tc/TC/S35/JUPITER.C', 40, ['Radius', 'Diameter', 'Circum', 'Rah', 'image', 'ImgWidth', 'ImgHeight', 'TRFV', 'char', 'Palette', 'i', 'ptr', 'curr_size', 'navail_bytes', 'nbits_left', 'long', 'fc', 'oc', 'c', 'clear'], [(50, 'b1', '*pbytes++', 'b1 = *pbytes++;'), (54, 'ret', 'b1 >> (8 - nbits_left)', 'ret = b1 >> (8 - nbits_left);'), (61, 'b1', '*pbytes++', 'b1 = *pbytes++;'), (88, 'ImgWidth', '(buf[6] << 8) + buf[5]', 'ImgWidth  = (buf[6] << 8) + buf[5];'), (89, 'ImgHeight', '(buf[8] << 8) + buf[7]', 'ImgHeight = (buf[8] << 8) + buf[7];'), (90, 'buffer', 'malloc(ImgWidth * ImgHeight)', 'buffer = malloc(ImgWidth * ImgHeight);'), (97, 'stack', 'malloc(MAX_CODES + 1)', 'stack  = malloc(MAX_CODES + 1);'), (98, 'suffix', 'malloc(MAX_CODES + 1)', 'suffix = malloc(MAX_CODES + 1);'), (99, 'prefix', 'malloc(sizeof(int) * (MAX_CODES + 1))', 'prefix = malloc(sizeof(int) * (MAX_CODES + 1));'), (101, 'curr_size', 'size + 1', 'curr_size = size + 1;')]), ('tc', 'tc/TC/S36/VESA24.C', 40, ['width', 'height', 'pal', 'IMG', 'far', 'adrx', 'adry', 'banky', 'CUfont', 'initvesa24', 'i', 'curr_size', 'navail_bytes', 'nbits_left', 'long', 'fc', 'oc', 'c', 'clear', 'ending'], [(28, 'ptrscreen', 'vgamem + adrx[x] + adry[y]', 'ptrscreen = vgamem + adrx[x] + adry[y];'), (34, 'adrx[i]', 'i * 3', 'adrx[i] = i * 3; /* one pixel equ 3 byte */'), (75, 'b1', '*pbytes++', 'b1 = *pbytes++;'), (79, 'ret', 'b1 >> (8 - nbits_left)', 'ret = b1 >> (8 - nbits_left);'), (86, 'b1', '*pbytes++', 'b1 = *pbytes++;'), (119, 'ptr', 'img->IMG', 'ptr    = img->IMG;'), (124, 'stack', 'malloc(MAX_CODES + 1)', 'stack  = malloc(MAX_CODES + 1);'), (125, 'suffix', 'malloc(MAX_CODES + 1)', 'suffix = malloc(MAX_CODES + 1);'), (126, 'prefix', 'malloc(sizeof(int) * (MAX_CODES + 1))', 'prefix = malloc(sizeof(int) * (MAX_CODES + 1));'), (128, 'curr_size', 'size + 1', 'curr_size = size + 1;')]), ('tc', 'tc/TC/S37/VESA24.C', 40, ['width', 'height', 'pal', 'IMG', 'far', 'adrx', 'adry', 'banky', 'CUfont', 'initvesa24', 'i', 'curr_size', 'navail_bytes', 'nbits_left', 'long', 'fc', 'oc', 'c', 'clear', 'ending'], [(28, 'ptrscreen', 'vgamem + adrx[x] + adry[y]', 'ptrscreen = vgamem + adrx[x] + adry[y];'), (34, 'adrx[i]', 'i * 3', 'adrx[i] = i * 3; /* one pixel equ 3 byte */'), (75, 'b1', '*pbytes++', 'b1 = *pbytes++;'), (79, 'ret', 'b1 >> (8 - nbits_left)', 'ret = b1 >> (8 - nbits_left);'), (86, 'b1', '*pbytes++', 'b1 = *pbytes++;'), (119, 'ptr', 'img->IMG', 'ptr    = img->IMG;'), (124, 'stack', 'malloc(MAX_CODES + 1)', 'stack  = malloc(MAX_CODES + 1);'), (125, 'suffix', 'malloc(MAX_CODES + 1)', 'suffix = malloc(MAX_CODES + 1);'), (126, 'prefix', 'malloc(sizeof(int) * (MAX_CODES + 1))', 'prefix = malloc(sizeof(int) * (MAX_CODES + 1));'), (128, 'curr_size', 'size + 1', 'curr_size = size + 1;')]), ('tc', 'tc/TC/S38/VESA.C', 40, ['PAGE', 'GX', 'GY', 'OGX', 'OGY', 'ADDX', 'ADDY', 'nBall', 'pal', 'Ball', 'Back', 'i', 'ptr', 'width', 'height', 'Length', 'j', 'k', 'loop'], [(99, 'width', '*ptr++', 'width = *ptr++;'), (100, 'height', '*ptr++', 'height = *ptr++;'), (101, 'Length', 'width * height', 'Length = width * height;'), (111, 'nBall[i]', 'random(4)', 'nBall[i] = random(4);'), (172, 'ADDY[i]', '(random(7) - 3) * 2', 'ADDY[i] = (random(7) - 3) * 2;'), (173, 'ADDX[i]', '-ADDX[i]', 'ADDX[i] = -ADDX[i];'), (176, 'ADDX[i]', '(random(7) - 3) * 2', 'ADDX[i] = (random(7) - 3) * 2 ;'), (177, 'ADDY[i]', '-ADDY[i]', 'ADDY[i] = -ADDY[i];'), (206, 'PAGE', '1 - PAGE', 'PAGE = 1 - PAGE;'), (213, 'ADDY[i]', '(random(4) - 2) * 4', 'ADDY[i] = (random(4) - 2) * 4;')]), ('tc', 'tc/TC/S39/DINOSTAR.C', 40, ['Dinosor', 'Ballon1', 'PAGE', 'MOVE', 'GX', 'GY', 'OGX', 'OGY', 'GXBallon', 'GYBallon', 'CBallon', 'AddBallon', 'OGXBallon', 'OGYBallon', 'GXStom', 'GYStom', 'AddStom', 'OGXStom', 'OGYStom', 'GXStar'], [(200, 'r', '*ptr++', 'r = *ptr++;'), (201, 'g', '*ptr++', 'g = *ptr++;'), (202, 'b', '*ptr++', 'b = *ptr++;'), (223, 'width', '2 * (*ptr++) + x', 'width  = 2 * (*ptr++) + x;'), (224, 'height', '2 * (*ptr++) + y', 'height = 2 * (*ptr++) + y;'), (227, 'color', '*ptr++', 'color = *ptr++;'), (243, 'width', '*ptr++', 'width = *ptr++;'), (244, 'height', '*ptr++', 'height = *ptr++;'), (258, 'k', 'random(4) + 4', 'k = random(4) + 4;'), (297, 'GXBallon[i]', 'random(20) * 40 + 60', 'GXBallon[i] = random(20) * 40 + 60;')]), ('tc', 'tc/TC/S40/FIREWORK.C', 40, ['tsin', 'tcos', 'X', 'Y', 'MAXY', 'GX', 'GY', 'DX', 'DY', 'GXTile', 'GYTile', 'cout', 'CC', 'color', 'TileU', 'SUBTile', 'LTile', 'BOOM', 'Boom1', 'Boom2'], [(249, 'x', 'GXTile[j] - 8', 'x = GXTile[j] - 8;'), (270, 'X[Num]', 'random(640) << 2', 'X[Num] = random(640) << 2;'), (271, 'Y[Num]', 'random(400) << 2', 'Y[Num] = random(400) << 2;'), (272, 'MAXY[Num]', 'random(MAXFIRE >> 1) + (MAXFIRE >> 1)', 'MAXY[Num] = random(MAXFIRE >> 1) + (MAXFIRE >> 1);'), (273, 'color[Num]', 'random(8)', 'color[Num] = random(8);'), (274, 'R', 'random(6)', 'R = random(6);'), (278, 'k', 'random(20) + 1', 'k = random(20) + 1;'), (279, 'th', 'random(360)', 'th = random(360);'), (298, 'SUBTile[Num]', 'random(8) + 8', 'SUBTile[Num] = random(8) + 8;'), (313, 'CC[i]', 'random(10) + 4', 'CC[i] = random(10) + 4;')]), ('tc', 'tc/TC/S41/MGRAPH.C', 40, ['PageStart', 'int', 'i', 'j', 'x1', 'y1', 'Right', 'Left', 'Up', 'Down', 'Space', 'Esc', 'ch', 'ScanCode', 'ptr', 'str', 'memtmp', 'width', 'height', 'BitImage'], [(21, 'LINE_Y[i]', 'i * 320', 'LINE_Y[i] = i * 320;'), (22, 'MemLength', '320 * 200', 'MemLength = 320 * 200;'), (79, 'x1', 'x0 + *ptr++', 'x1 = x0 + *ptr++; y1 = y0 + *ptr++;'), (89, 'x1', 'x0 + *ptr++', 'x1 = x0 + *ptr++; y1 = y0 + *ptr++;'), (161, 'width', '*ptr1++', 'width = *ptr1++; height = *ptr1++;'), (169, 'width', '*ptr++', 'width = *ptr++; height = *ptr++;'), (188, 'width', '*ptr++', 'width = *ptr++;'), (189, 'height', '*ptr++', 'height = *ptr++;'), (190, 'BitImage', 'malloc((width << 1) * height + 2)', 'BitImage = malloc((width << 1) * height + 2);'), (210, 'width', '*ptr++', 'width = *ptr++; height = *ptr++;')]), ('tc', 'tc/TC/S43/KILLYABA.C', 40, ['c_duration', 'c_octave', 'char', 'sp_on', 'sp_off', 'msb', 'c_note', 'Ya', 'Bitmap1', 'Bitmap2', 'Bitmap3', 'YaBa', 'Bitmap5', 'NewCo0', 'NewCo1', 'YaX', 'YaY', 'PosYA', 'Color0', 'Color1'], [(68, 'c_note', '*ptrsong', 'c_note = *ptrsong;'), (73, 'c_octave', '*ptrsong++', 'c_octave = *ptrsong++;'), (76, 'c_duration', '*ptrsong++', 'c_duration = *ptrsong++;'), (81, 'c_duration', '*ptrsong', 'c_duration = *ptrsong;'), (83, 'msb', 'notes[c_octave][c_note]/256', 'msb=notes[c_octave][c_note]/256;'), (195, 'x1', 'x0 + *ptr++', 'x1 = x0 + *ptr++; y1 = y0 + *ptr++;'), (216, 'Color0', 'random(7)', 'Color0 = random(7);'), (217, 'Color1', 'random(7)', 'Color1 = random(7);'), (218, 'NewCo0', 'random(7)', 'NewCo0 = random(7);'), (219, 'NewCo1', 'random(7)', 'NewCo1 = random(7);')])]
        state={'rec':None,'expr':None}
        box=self.card(b,'1 • SOURCE WITH EXTRACTABLE MATH EXPRESSIONS')
        tree=ttk.Treeview(box,columns=('archive','file','score','vars','exprs'),show='headings',height=11)
        for c,t,w in [('archive','Archive',80),('file','Source',300),('score','Score',60),('vars','Variables',330),('exprs','Expressions',90)]:
            tree.heading(c,text=t); tree.column(c,width=w)
        tree.pack(fill='both',expand=True,padx=12,pady=8)
        for rec in data:
            arc,fn,score,vars_,exprs=rec
            tree.insert('', 'end',values=(arc,fn,score,', '.join(vars_[:10]),len(exprs)))

        nb=ttk.Notebook(b); nb.pack(fill='both',expand=True,padx=28,pady=10)
        vt=tk.Frame(nb,bg='white'); et=tk.Frame(nb,bg='white'); mt=tk.Frame(nb,bg='white'); gt=tk.Frame(nb,bg='white')
        nb.add(vt,text='Variables'); nb.add(et,text='Source Expressions'); nb.add(mt,text='Mathematical Model'); nb.add(gt,text='Graph / Diagram')
        vtxt=tk.Text(vt,height=21,font=('Consolas',10),wrap='word'); vtxt.pack(fill='both',expand=True,padx=12,pady=10)
        etree=ttk.Treeview(et,columns=('line','lhs','rhs','source'),show='headings',height=16)
        for c,t,w in [('line','Line',60),('lhs','Variable',150),('rhs','Expression',420),('source','Original source line',500)]:
            etree.heading(c,text=t); etree.column(c,width=w)
        etree.pack(fill='both',expand=True,padx=12,pady=10)
        mtxt=tk.Text(mt,height=22,font=('Consolas',10),wrap='word'); mtxt.pack(fill='both',expand=True,padx=12,pady=10)
        cv=tk.Canvas(gt,height=430,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1); cv.pack(fill='both',expand=True,padx=12,pady=10)
        status=tk.StringVar(value='เลือก source เพื่อเริ่ม static extraction')
        tk.Label(b,textvariable=status,bg=BG,fg=MUTED,font=('Consolas',9),wraplength=1100).pack(anchor='w',padx=30,pady=(0,8))

        def normalize(rhs):
            x=rhs.replace('M_PI','π').replace('PI','π')
            x=re.sub(r'\bpow\s*\(([^,]+),\s*2\s*\)',r'(\1)²',x,flags=re.I)
            x=x.replace('sqrt','√').replace('sin','sin').replace('cos','cos').replace('tan','tan')
            x=x.replace('*','·')
            return x

        def classify(lhs,rhs):
            lo=rhs.lower()
            if 'sin(' in lo or 'cos(' in lo or 'tan(' in lo:return 'Trigonometric / Parametric Model'
            if 'sqrt(' in lo or 'pow(' in lo:return 'Distance / Power-Root Model'
            if 'random(' in lo or 'rand(' in lo:return 'Random Variable / Sampling Model'
            if any(op in rhs for op in ['+','-','*','/']):return 'Algebraic / Iterative Model'
            return 'General Assignment'

        def source_select(_=None):
            sel=tree.selection()
            if not sel:return
            vals=tree.item(sel[0],'values'); arc,fn=vals[0],vals[1]
            rec=next((r for r in data if r[0]==arc and r[1]==fn),None)
            if not rec:return
            state['rec']=rec
            vtxt.delete('1.0','end')
            vtxt.insert('end',f'SOURCE: {arc} / {fn}\n\nDECLARED VARIABLES EXTRACTED\n')
            for i,v in enumerate(rec[3],1):vtxt.insert('end',f'  {i:02d}. {v}\n')
            vtxt.insert('end','\nหมายเหตุ: extraction นี้เป็น lexical/static scan ไม่ใช่ full C/Pascal compiler parser.')
            for iid in etree.get_children():etree.delete(iid)
            for no,lhs,rhs,line in rec[4]:
                etree.insert('', 'end',values=(no,lhs,rhs,line))
            status.set(f'Extracted {len(rec[3])} variables and {len(rec[4])} math-like assignments from {fn}')
            nb.select(vt)

        def expression_select(_=None):
            sel=etree.selection()
            if not sel:return
            vals=etree.item(sel[0],'values'); no=int(vals[0]); lhs=str(vals[1]); rhs=str(vals[2])
            state['expr']=(no,lhs,rhs)
            model=classify(lhs,rhs); eq=f'{lhs} = {normalize(rhs)}'
            mtxt.delete('1.0','end')
            mtxt.insert('end',f'SOURCE LINE {no}\n  {lhs} = {rhs}\n\nNORMALIZED MATHEMATICAL EQUATION\n  {eq}\n\n')
            mtxt.insert('end',f'MODEL CLASSIFICATION\n  {model}\n\n')
            if model.startswith('Trigonometric'):
                mtxt.insert('end','REFERENCE MODEL\n  x = r cos θ, y = r sin θ\n  sin²θ + cos²θ = 1\n')
            elif model.startswith('Distance'):
                mtxt.insert('end','REFERENCE MODEL\n  d = √(Δx² + Δy²)\n  More generally, powers/roots can encode geometric magnitude.\n')
            elif model.startswith('Random'):
                mtxt.insert('end','REFERENCE MODEL\n  X = random outcome\n  P-hat(A)=count(A)/N\n  E-hat[X]=(1/N)ΣXᵢ\n')
            else:
                mtxt.insert('end','REFERENCE MODEL\n  y=f(x₁,x₂,...) or xₙ₊₁=F(xₙ) when the assignment occurs repeatedly in a loop.\n')
            mtxt.insert('end','\nCAUTION\n  Classification is based on the selected expression syntax. '
                              'It is a teaching model, not a proof of the original program author’s mathematical intent.')
            draw(lhs,rhs,model)
            nb.select(mt)

        def draw(lhs,rhs,model):
            cv.delete('all'); w=max(cv.winfo_width(),780); h=max(cv.winfo_height(),400)
            if model.startswith('Trigonometric'):
                cx,cy=w/2,h/2; r=125; pts=[]
                for d in range(361):
                    th=math.radians(d);pts += [cx+r*math.cos(th),cy-r*math.sin(th)]
                cv.create_line(*pts,fill=BLUE,width=3)
                cv.create_line(cx-r-30,cy,cx+r+30,cy,fill='#94a3b8');cv.create_line(cx,cy-r-30,cx,cy+r+30,fill='#94a3b8')
                cv.create_text(cx,25,text='Reference visualization: unit/parametric circle',fill=TEXT,font=('Segoe UI Semibold',10))
            elif model.startswith('Distance'):
                x1,y1=150,310;x2,y2=610,100
                cv.create_line(x1,y1,x2,y1,fill=GREEN,width=2);cv.create_line(x2,y1,x2,y2,fill=GREEN,width=2)
                cv.create_line(x1,y1,x2,y2,fill=BLUE,width=3)
                cv.create_text(w/2,25,text='Reference visualization: Pythagorean distance',fill=TEXT,font=('Segoe UI Semibold',10))
            elif model.startswith('Random'):
                hit=0;N=1200
                for i in range(N):
                    x=random.random();y=random.random();inside=x*x+y*y<=1
                    hit+=inside
                    if i<700:
                        px=80+x*300;py=350-y*300
                        cv.create_oval(px-1,py-1,px+1,py+1,outline=GREEN if inside else ORANGE)
                cv.create_text(500,100,anchor='w',text=f'Example Monte Carlo\nπ ≈ {4*hit/N:.6f}',fill=TEXT,font=('Consolas',10))
            else:
                cv.create_text(w/2,70,text='Algebraic / iterative expression',fill=TEXT,font=('Segoe UI Semibold',12))
                cv.create_text(w/2,125,text=f'{lhs} = {normalize(rhs)}',fill=BLUE,font=('Consolas',11))
                cv.create_text(w/2,175,text='Use source context/loop structure in the next stage to determine recurrence semantics.',fill=MUTED,font=('Segoe UI',9))
        tree.bind('<<TreeviewSelect>>',source_select)
        etree.bind('<<TreeviewSelect>>',expression_select)

        actions=tk.Frame(box,bg='white');actions.pack(fill='x',padx=12,pady=(0,10))
        def auto_pick():
            if not tree.get_children():return
            iid=tree.get_children()[0];tree.selection_set(iid);tree.see(iid);source_select()
            if etree.get_children():
                eid=etree.get_children()[0];etree.selection_set(eid);etree.see(eid);expression_select()
        ttk.Button(actions,text='🤖 AUTO EXTRACT BEST SOURCE',style='Primary.TButton',command=auto_pick).pack(side='left')
        ttk.Button(actions,text='V4.1 Math Model → Source',command=self.v41_math_model_source_lab).pack(side='left',padx=5)

        self.card(b,'V4.2 RESULT',
            'รุ่นนี้เริ่มจาก source จริงตามที่กำหนด: declared variables + assignment expressions → normalized equation → '
            'model classification → reference mathematical model → visualization. '
            'V4.3 ควรเพิ่ม expression parser/AST แบบปลอดภัย, dependency graph ของตัวแปร และ loop-context analysis '
            'เพื่อแยก recurrence, geometry และ probability models ได้แม่นยำขึ้น โดยยังไม่ execute legacy C/Pascal.')

    def v43_dependency_recurrence_lab(self):
        self.clear()
        self.header('🕸 V4.3 • Dependency Graph + Recurrence Analysis',
            'Mathematical rule: assignment is not automatically a recurrence')
        b=self.scrollbody()
        self.card(b,'MATHEMATICAL RULE',
            'สำหรับ y=f(x,z) สร้าง dependency x→y และ z→y. จะเป็น recurrence candidate เมื่อ state variable ด้านซ้าย '
            'ปรากฏใน RHS เช่น x=a*x+b; และจะเขียน xₙ₊₁=axₙ+b ได้เมื่อ assignment นั้นเกิดซ้ำโดยใช้ค่าที่ update จากรอบก่อน')
        data=[('tc', 'tc/TC/tp/EXAMPLES/TVFM/EQU.PAS', [], [(20, 'cmDosShell', 'cmNewWindow + 1', 'cmDosShell          = cmNewWindow + 1;'), (21, 'cmRun', 'cmDosShell + 1', 'cmRun               = cmDosShell + 1;'), (25, 'cmViewAsHex', 'cmExecute + 1', 'cmViewAsHex         = cmExecute + 1;'), (26, 'cmViewAsText', 'cmViewAsHex + 1', 'cmViewAsText        = cmViewAsHex + 1;'), (27, 'cmViewCustom', 'cmViewAsText + 1', 'cmViewCustom        = cmViewAsText + 1;'), (28, 'cmAssociate', 'cmViewCustom + 1', 'cmAssociate         = cmViewCustom + 1;'), (29, 'cmCopy', 'cmAssociate + 1', 'cmCopy              = cmAssociate + 1;'), (30, 'cmDelete', 'cmCopy + 1', 'cmDelete            = cmCopy + 1;'), (31, 'cmRename', 'cmDelete + 1', 'cmRename            = cmDelete + 1;'), (32, 'cmChangeAttr', 'cmRename + 1', 'cmChangeAttr        = cmRename + 1;')]), ('tc', 'tc/TC/caibinary/PROC.PAS', ['i', 'j', 'Old', 'Now', 'p'], [(24, 'x', 'x1 - size', 'x := x1 - size;'), (161, 'x1', 'x1 - 1', 'x1 := x1 - 1;'), (162, 'y1', 'y1 - 1', 'y1 := y1 - 1;'), (168, 'x1', 'x1 - 1', 'x1 := x1 - 1;'), (169, 'y1', 'y1 + 1', 'y1 := y1 + 1;'), (178, 'x1', 'x1 + 1', 'x1 := x1 + 1; y1 := y1 - 1;'), (184, 'x1', 'x1 + 1', 'x1 := x1 + 1;'), (185, 'y1', 'y1 + 1', 'y1 := y1 + 1;'), (228, 'a', 'a - 1', 'a := a - 1; b := b - 1;'), (237, 'a', 'a - 1', 'a := a - 1; b := b + 1;')]), ('tc', 'tc/TC/caitree/PROC.PAS', ['i', 'j', 'Old', 'Now', 'p'], [(24, 'x', 'x1 - size', 'x := x1 - size;'), (161, 'x1', 'x1 - 1', 'x1 := x1 - 1;'), (162, 'y1', 'y1 - 1', 'y1 := y1 - 1;'), (168, 'x1', 'x1 - 1', 'x1 := x1 - 1;'), (169, 'y1', 'y1 + 1', 'y1 := y1 + 1;'), (178, 'x1', 'x1 + 1', 'x1 := x1 + 1; y1 := y1 - 1;'), (184, 'x1', 'x1 + 1', 'x1 := x1 + 1;'), (185, 'y1', 'y1 + 1', 'y1 := y1 + 1;'), (228, 'a', 'a - 1', 'a := a - 1; b := b - 1;'), (237, 'a', 'a - 1', 'a := a - 1; b := b + 1;')]), ('tc', 'tc/TC/tp/caitree/PROC.PAS', ['i', 'j', 'Old', 'Now', 'p'], [(24, 'x', 'x1 - size', 'x := x1 - size;'), (161, 'x1', 'x1 - 1', 'x1 := x1 - 1;'), (162, 'y1', 'y1 - 1', 'y1 := y1 - 1;'), (168, 'x1', 'x1 - 1', 'x1 := x1 - 1;'), (169, 'y1', 'y1 + 1', 'y1 := y1 + 1;'), (178, 'x1', 'x1 + 1', 'x1 := x1 + 1; y1 := y1 - 1;'), (184, 'x1', 'x1 + 1', 'x1 := x1 + 1;'), (185, 'y1', 'y1 + 1', 'y1 := y1 + 1;'), (228, 'a', 'a - 1', 'a := a - 1; b := b - 1;'), (237, 'a', 'a - 1', 'a := a - 1; b := b + 1;')]), ('tc', 'tc/TC/caibinary/TESTNEW.PAS', ['Choose', 'no', 'Count', 'Ti', 'i', 'j', 'Old', 'Now', 'p'], [(96, 'x2', 'x1 + 20', 'x2 := x1 + 20;'), (97, 'y2', 'y1 + 20', 'y2 := y1 + 20;'), (99, 'x1', 'x1 + 22', 'x1 := x1 + 22;'), (101, 'y1', 'y1+22', 'y1 := y1+22;'), (119, 'x', '(x1-22) + 22*co', 'x  := (x1-22) + 22*co;'), (120, 'y', 'y1 + 22*(no)', 'y  := y1 + 22*(no);'), (121, 'x2', 'x + 20', 'x2 := x + 20;'), (122, 'y2', 'y + 20', 'y2 := y + 20;'), (135, 'Time', 'Timer[i] - sec', 'Time := Timer[i] - sec;'), (178, 'Now', 'Now-1', 'Now := Now-1;')]), ('tc', 'tc/TC/caitree/TESTNEW.PAS', ['Choose', 'no', 'Count', 'Ti', 'i', 'j', 'Old', 'Now', 'p'], [(96, 'x2', 'x1 + 20', 'x2 := x1 + 20;'), (97, 'y2', 'y1 + 20', 'y2 := y1 + 20;'), (99, 'x1', 'x1 + 22', 'x1 := x1 + 22;'), (101, 'y1', 'y1+22', 'y1 := y1+22;'), (119, 'x', '(x1-22) + 22*co', 'x  := (x1-22) + 22*co;'), (120, 'y', 'y1 + 22*(no)', 'y  := y1 + 22*(no);'), (121, 'x2', 'x + 20', 'x2 := x + 20;'), (122, 'y2', 'y + 20', 'y2 := y + 20;'), (135, 'Time', 'Timer[i] - sec', 'Time := Timer[i] - sec;'), (178, 'Now', 'Now-1', 'Now := Now-1;')]), ('tc', 'tc/TC/tp/caitree/TESTNEW.PAS', ['Choose', 'no', 'Count', 'Ti', 'i', 'j', 'Old', 'Now', 'p'], [(96, 'x2', 'x1 + 20', 'x2 := x1 + 20;'), (97, 'y2', 'y1 + 20', 'y2 := y1 + 20;'), (99, 'x1', 'x1 + 22', 'x1 := x1 + 22;'), (101, 'y1', 'y1+22', 'y1 := y1+22;'), (119, 'x', '(x1-22) + 22*co', 'x  := (x1-22) + 22*co;'), (120, 'y', 'y1 + 22*(no)', 'y  := y1 + 22*(no);'), (121, 'x2', 'x + 20', 'x2 := x + 20;'), (122, 'y2', 'y + 20', 'y2 := y + 20;'), (135, 'Time', 'Timer[i] - sec', 'Time := Timer[i] - sec;'), (178, 'Now', 'Now-1', 'Now := Now-1;')]), ('tc', 'tc/TC/tp/EXAMPLES/TVFM/TOOLS.PAS', ['i', 'ParamPos', 'I', 'TotalSize', 'R', 'C', 'L', 'Attr', 'Count', 'Command', 'Result', 'J'], [(245, 'GetExeBaseName', 'D + N', 'GetExeBaseName := D + N;'), (320, 's', "s + TwoDigit(t.Month, False) + '-' + TwoDigit(t.Day, True)", "s := s + TwoDigit(t.Month, False) + '-' + TwoDigit(t.Day, True);"), (321, 's', "s + '-' + Copy(FourDigit(t.Year),3,2)", "s := s + '-' + Copy(FourDigit(t.Year),3,2);"), (370, 'Name', 'Name + E', 'Name := Name + E;'), (392, 'Params', 'Copy(Command, ParamPos + 1, $FF)', 'Params := Copy(Command, ParamPos + 1, $FF);'), (394, 'Params', "Params + ' ' + FileName", "Params := Params + ' ' + FileName;"), (441, 'Params', "'/c ' + FileName + Params", "Params := '/c ' + FileName + Params;"), (527, 'Params', "'/c ' + Viewer + ' ' + FileName", "Params := '/c ' + Viewer + ' ' + FileName;"), (650, 'S', "Drive + ':'", "S := Drive + ':';"), (744, 'S', "Path + '\\' + F^.Name + F^.Ext", "S := Path + '\\' + F^.Name + F^.Ext;")]), ('caimath', 'caimath/PARAY.PAS', ['pyxa', 'pyc', 'pyx', 'pyy', 'pyya', 'bpyxa', 'pyh', 'pyk', 'pydatachoice', 'real_delay', 'real_delay2'], [(14, 'Xdelay', 'round((real_delay2*ms)/5000)', 'Xdelay := round((real_delay2*ms)/5000);'), (188, 'bpyxa', '-50', 'bpyxa := -50;'), (194, 'pyya', 'round((pyxa*pyxa)/(4*pyc))', 'pyya  := round((pyxa*pyxa)/(4*pyc));'), (197, 'pyy', 'round((pyxa*pyxa)/(4*pyc))', 'pyy := round((pyxa*pyxa)/(4*pyc));'), (222, 'bpyxa', '-100', 'bpyxa := -100;'), (228, 'pyya', 'round((pyxa*pyxa)/(4*pyc))', 'pyya  := round((pyxa*pyxa)/(4*pyc));'), (231, 'pyy', 'round((pyxa*pyxa)/(4*pyc))', 'pyy := round((pyxa*pyxa)/(4*pyc));'), (270, 'bpyxa', '-85', 'bpyxa := -85;'), (271, 'pyc', '-10', 'pyc   := -10;'), (276, 'pyya', 'round((pyxa*pyxa)/(4*pyc))', 'pyya  := round((pyxa*pyxa)/(4*pyc));')]), ('tc', 'tc/TC/caimath/PARAY.PAS', ['pyxa', 'pyc', 'pyx', 'pyy', 'pyya', 'bpyxa', 'pyh', 'pyk', 'pydatachoice', 'real_delay', 'real_delay2'], [(14, 'Xdelay', 'round((real_delay2*ms)/5000)', 'Xdelay := round((real_delay2*ms)/5000);'), (188, 'bpyxa', '-50', 'bpyxa := -50;'), (194, 'pyya', 'round((pyxa*pyxa)/(4*pyc))', 'pyya  := round((pyxa*pyxa)/(4*pyc));'), (197, 'pyy', 'round((pyxa*pyxa)/(4*pyc))', 'pyy := round((pyxa*pyxa)/(4*pyc));'), (222, 'bpyxa', '-100', 'bpyxa := -100;'), (228, 'pyya', 'round((pyxa*pyxa)/(4*pyc))', 'pyya  := round((pyxa*pyxa)/(4*pyc));'), (231, 'pyy', 'round((pyxa*pyxa)/(4*pyc))', 'pyy := round((pyxa*pyxa)/(4*pyc));'), (270, 'bpyxa', '-85', 'bpyxa := -85;'), (271, 'pyc', '-10', 'pyc   := -10;'), (276, 'pyya', 'round((pyxa*pyxa)/(4*pyc))', 'pyya  := round((pyxa*pyxa)/(4*pyc));')]), ('caimath', 'caimath/PARAX.PAS', ['pxxa', 'pxc', 'pxx', 'pxy', 'pxya', 'bpxxa', 'pxh', 'pxk', 'pxdatachoice', 'real_delay', 'real_delay2'], [(14, 'Xdelay', 'round((real_delay2*ms)/5000)', 'Xdelay := round((real_delay2*ms)/5000);'), (190, 'bpxya', '-50', 'bpxya := -50;'), (196, 'pxxa', 'round((pxya*pxya)/(4*pxc))', 'pxxa  := round((pxya*pxya)/(4*pxc));'), (199, 'pxx', 'round((pxya*pxya)/(4*pxc))', 'pxx := round((pxya*pxya)/(4*pxc));'), (223, 'bpxya', '-100', 'bpxya := -100;'), (229, 'pxxa', 'round((pxya*pxya)/(4*pxc))', 'pxxa  := round((pxya*pxya)/(4*pxc));'), (232, 'pxx', 'round((pxya*pxya)/(4*pxc))', 'pxx := round((pxya*pxya)/(4*pxc));'), (270, 'bpxya', '-83', 'bpxya := -83;'), (276, 'pxxa', 'round((pxya*pxya)/(4*pxc))', 'pxxa  := round((pxya*pxya)/(4*pxc));'), (279, 'pxx', 'round((pxya*pxya)/(4*pxc))', 'pxx := round((pxya*pxya)/(4*pxc));')]), ('tc', 'tc/TC/caimath/PARAX.PAS', ['pxxa', 'pxc', 'pxx', 'pxy', 'pxya', 'bpxxa', 'pxh', 'pxk', 'pxdatachoice', 'real_delay', 'real_delay2'], [(14, 'Xdelay', 'round((real_delay2*ms)/5000)', 'Xdelay := round((real_delay2*ms)/5000);'), (190, 'bpxya', '-50', 'bpxya := -50;'), (196, 'pxxa', 'round((pxya*pxya)/(4*pxc))', 'pxxa  := round((pxya*pxya)/(4*pxc));'), (199, 'pxx', 'round((pxya*pxya)/(4*pxc))', 'pxx := round((pxya*pxya)/(4*pxc));'), (223, 'bpxya', '-100', 'bpxya := -100;'), (229, 'pxxa', 'round((pxya*pxya)/(4*pxc))', 'pxxa  := round((pxya*pxya)/(4*pxc));'), (232, 'pxx', 'round((pxya*pxya)/(4*pxc))', 'pxx := round((pxya*pxya)/(4*pxc));'), (270, 'bpxya', '-83', 'bpxya := -83;'), (276, 'pxxa', 'round((pxya*pxya)/(4*pxc))', 'pxxa  := round((pxya*pxya)/(4*pxc));'), (279, 'pxx', 'round((pxya*pxya)/(4*pxc))', 'pxx := round((pxya*pxya)/(4*pxc));')]), ('caimath', 'caimath/MAIN.PAS', ['real_delay', 'real_delay2', 'valout', 'x', 'y', 'err', 'a', 'w', 'row', 'col'], [(15, 'Xdelay', 'round((real_delay2*ms)/5000)', 'Xdelay := round((real_delay2*ms)/5000);'), (211, 'Ya', '-74', 'Ya := -74;'), (212, 'Xa', 'round((Ya*Ya)/(4*C))', 'Xa := round((Ya*Ya)/(4*C));'), (213, 'Y', '-74', 'Y := -74;'), (216, 'X', 'round((Y*Y)/(4*C))', 'X := round((Y*Y)/(4*C));'), (244, 'xa', '-64', 'xa := -64;'), (245, 'ya', 'round((xa*xa)/(4*c))', 'ya := round((xa*xa)/(4*c));'), (246, 'X', '-64', 'X := -64;'), (248, 'Y', 'round((X*X)/(4*C))', 'Y := round((X*X)/(4*C));'), (362, 'xa', '-64', 'xa := -64;')]), ('tc', 'tc/TC/caimath/MAIN.PAS', ['real_delay', 'real_delay2', 'valout', 'x', 'y', 'err', 'a', 'w', 'row', 'col'], [(15, 'Xdelay', 'round((real_delay2*ms)/5000)', 'Xdelay := round((real_delay2*ms)/5000);'), (211, 'Ya', '-74', 'Ya := -74;'), (212, 'Xa', 'round((Ya*Ya)/(4*C))', 'Xa := round((Ya*Ya)/(4*C));'), (213, 'Y', '-74', 'Y := -74;'), (216, 'X', 'round((Y*Y)/(4*C))', 'X := round((Y*Y)/(4*C));'), (244, 'xa', '-64', 'xa := -64;'), (245, 'ya', 'round((xa*xa)/(4*c))', 'ya := round((xa*xa)/(4*c));'), (246, 'X', '-64', 'X := -64;'), (248, 'Y', 'round((X*X)/(4*C))', 'Y := round((X*X)/(4*C));'), (362, 'xa', '-64', 'xa := -64;')]), ('tc', 'tc/TC/c_grapic/2D.C', ['a', 'b', 'c', 'd', 'e', 'f', 'curcolor', 'gdriver', 'gmode', 'r', 'sa', 'ea'], [(59, 'a', 'getmaxx() / 2', 'a = getmaxx() / 2;'), (60, 'b', 'getmaxy() / 2', 'b = getmaxy() / 2;'), (79, 'd', 'b-1', 'd=b-1;'), (88, 'd', 'b+1', 'd=b+1;'), (96, 'c', 'a+1', 'c=a+1;'), (105, 'c', 'a-1', 'c=a-1;'), (114, 'c', 'a+1', 'c=a+1;'), (115, 'd', 'b+1', 'd=b+1;'), (123, 'c', 'a-1', 'c=a-1;'), (124, 'd', 'b-1', 'd=b-1;')]), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', [], [(64, 'next', 'p->next', 'next = p->next;'), (211, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (240, 'current', 'current->next', 'current = current->next;'), (257, 'cur', 'cur->next', 'cur = cur->next;'), (271, 'cur', 'cur->next', 'cur = cur->next;'), (285, 'res', '&(cur->data)', 'res = &(cur->data);'), (286, 'cur', 'cur->next', 'cur = cur->next;'), (337, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (359, 'cur', 'list->head.next', 'cur = list->head.next;'), (376, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', [], [(68, 'next', 'p->next', 'next = p->next;'), (201, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (224, 'current', 'current->next', 'current = current->next;'), (241, 'cur', 'cur->next', 'cur = cur->next;'), (255, 'cur', 'cur->next', 'cur = cur->next;'), (269, 'res', '&(cur->data)', 'res = &(cur->data);'), (270, 'cur', 'cur->next', 'cur = cur->next;'), (318, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (339, 'cur', 'list->head.next', 'cur = list->head.next;'), (355, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', [], [(64, 'next', 'p->next', 'next = p->next;'), (211, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (240, 'current', 'current->next', 'current = current->next;'), (257, 'cur', 'cur->next', 'cur = cur->next;'), (271, 'cur', 'cur->next', 'cur = cur->next;'), (285, 'res', '&(cur->data)', 'res = &(cur->data);'), (286, 'cur', 'cur->next', 'cur = cur->next;'), (337, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (359, 'cur', 'list->head.next', 'cur = list->head.next;'), (376, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/LISTIMP.H', [], [(68, 'next', 'p->next', 'next = p->next;'), (201, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (224, 'current', 'current->next', 'current = current->next;'), (241, 'cur', 'cur->next', 'cur = cur->next;'), (255, 'cur', 'cur->next', 'cur = cur->next;'), (269, 'res', '&(cur->data)', 'res = &(cur->data);'), (270, 'cur', 'cur->next', 'cur = cur->next;'), (318, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (339, 'cur', 'list->head.next', 'cur = list->head.next;'), (355, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/DLISTIMP.H', [], [(64, 'next', 'p->next', 'next = p->next;'), (211, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (240, 'current', 'current->next', 'current = current->next;'), (257, 'cur', 'cur->next', 'cur = cur->next;'), (271, 'cur', 'cur->next', 'cur = cur->next;'), (285, 'res', '&(cur->data)', 'res = &(cur->data);'), (286, 'cur', 'cur->next', 'cur = cur->next;'), (337, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (359, 'cur', 'list->head.next', 'cur = list->head.next;'), (376, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/LISTIMP.H', [], [(68, 'next', 'p->next', 'next = p->next;'), (201, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (224, 'current', 'current->next', 'current = current->next;'), (241, 'cur', 'cur->next', 'cur = cur->next;'), (255, 'cur', 'cur->next', 'cur = cur->next;'), (269, 'res', '&(cur->data)', 'res = &(cur->data);'), (270, 'cur', 'cur->next', 'cur = cur->next;'), (318, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (339, 'cur', 'list->head.next', 'cur = list->head.next;'), (355, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', [], [(64, 'next', 'p->next', 'next = p->next;'), (211, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (240, 'current', 'current->next', 'current = current->next;'), (257, 'cur', 'cur->next', 'cur = cur->next;'), (271, 'cur', 'cur->next', 'cur = cur->next;'), (285, 'res', '&(cur->data)', 'res = &(cur->data);'), (286, 'cur', 'cur->next', 'cur = cur->next;'), (337, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (359, 'cur', 'list->head.next', 'cur = list->head.next;'), (376, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', [], [(68, 'next', 'p->next', 'next = p->next;'), (201, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (224, 'current', 'current->next', 'current = current->next;'), (241, 'cur', 'cur->next', 'cur = cur->next;'), (255, 'cur', 'cur->next', 'cur = cur->next;'), (269, 'res', '&(cur->data)', 'res = &(cur->data);'), (270, 'cur', 'cur->next', 'cur = cur->next;'), (318, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (339, 'cur', 'list->head.next', 'cur = list->head.next;'), (355, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', [], [(64, 'next', 'p->next', 'next = p->next;'), (211, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (240, 'current', 'current->next', 'current = current->next;'), (257, 'cur', 'cur->next', 'cur = cur->next;'), (271, 'cur', 'cur->next', 'cur = cur->next;'), (285, 'res', '&(cur->data)', 'res = &(cur->data);'), (286, 'cur', 'cur->next', 'cur = cur->next;'), (337, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (359, 'cur', 'list->head.next', 'cur = list->head.next;'), (376, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/Project/Roof/TC/CLASSLIB/INCLUDE/LISTIMP.H', [], [(68, 'next', 'p->next', 'next = p->next;'), (201, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (224, 'current', 'current->next', 'current = current->next;'), (241, 'cur', 'cur->next', 'cur = cur->next;'), (255, 'cur', 'cur->next', 'cur = cur->next;'), (269, 'res', '&(cur->data)', 'res = &(cur->data);'), (270, 'cur', 'cur->next', 'cur = cur->next;'), (318, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (339, 'cur', 'list->head.next', 'cur = list->head.next;'), (355, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/TC/CLASSLIB/INCLUDE/DLISTIMP.H', [], [(64, 'next', 'p->next', 'next = p->next;'), (211, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (240, 'current', 'current->next', 'current = current->next;'), (257, 'cur', 'cur->next', 'cur = cur->next;'), (271, 'cur', 'cur->next', 'cur = cur->next;'), (285, 'res', '&(cur->data)', 'res = &(cur->data);'), (286, 'cur', 'cur->next', 'cur = cur->next;'), (337, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (359, 'cur', 'list->head.next', 'cur = list->head.next;'), (376, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/TC/CLASSLIB/INCLUDE/LISTIMP.H', [], [(68, 'next', 'p->next', 'next = p->next;'), (201, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (224, 'current', 'current->next', 'current = current->next;'), (241, 'cur', 'cur->next', 'cur = cur->next;'), (255, 'cur', 'cur->next', 'cur = cur->next;'), (269, 'res', '&(cur->data)', 'res = &(cur->data);'), (270, 'cur', 'cur->next', 'cur = cur->next;'), (318, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (339, 'cur', 'list->head.next', 'cur = list->head.next;'), (355, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/TC/OUTPUT/RoofAndCurtain/TC/CLASSLIB/INCLUDE/DLISTIMP.H', [], [(64, 'next', 'p->next', 'next = p->next;'), (211, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (240, 'current', 'current->next', 'current = current->next;'), (257, 'cur', 'cur->next', 'cur = cur->next;'), (271, 'cur', 'cur->next', 'cur = cur->next;'), (285, 'res', '&(cur->data)', 'res = &(cur->data);'), (286, 'cur', 'cur->next', 'cur = cur->next;'), (337, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (359, 'cur', 'list->head.next', 'cur = list->head.next;'), (376, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/TC/TC/OUTPUT/RoofAndCurtain/TC/CLASSLIB/INCLUDE/LISTIMP.H', [], [(68, 'next', 'p->next', 'next = p->next;'), (201, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (224, 'current', 'current->next', 'current = current->next;'), (241, 'cur', 'cur->next', 'cur = cur->next;'), (255, 'cur', 'cur->next', 'cur = cur->next;'), (269, 'res', '&(cur->data)', 'res = &(cur->data);'), (270, 'cur', 'cur->next', 'cur = cur->next;'), (318, 'cursor', 'cursor->next', 'cursor = cursor->next;'), (339, 'cur', 'list->head.next', 'cur = list->head.next;'), (355, 'cur', 'cur->next', 'cur = cur->next;')]), ('tc', 'tc/SORT/COVERRED.PAS', ['curx', 'cury', 'tarx', 'tary', 'col', 'stepx', 'stepy', 'totalpixel', 'color', 'colorcount', 'fadecount'], [(11, 'picturexofs', '(639-picturewidth) div 2', 'picturexofs = (639-picturewidth) div 2;'), (12, 'pictureyofs', '(479-pictureheight) div 2', 'pictureyofs = (479-pictureheight) div 2;'), (74, 'curx', 'random(639+1) shl step', 'curx:=random(639+1) shl step;'), (75, 'cury', 'random(479+1) shl step', 'cury:=random(479+1) shl step;'), (76, 'tarx', '(picturexofs+xc-1) shl step', 'tarx:=(picturexofs+xc-1) shl step;'), (77, 'tary', '(pictureyofs+yc-1) shl step', 'tary:=(pictureyofs+yc-1) shl step;'), (78, 'stepx', '(tarx-curx) div 64', 'stepx:=(tarx-curx) div 64;'), (79, 'stepy', '(tary-cury) div 64', 'stepy:=(tary-cury) div 64;'), (174, 'memw[$a000:(((y-1) shl 1)*320+(x shl 1))]', '(c shl 8) + c', 'memw[$a000:(((y-1) shl 1)*320+(x shl 1))] := (c shl 8) + c;'), (175, 'memw[$a000:(((y shl 1)-1)*320+(x shl 1))]', '(c shl 8) + c', 'memw[$a000:(((y shl 1)-1)*320+(x shl 1))] := (c shl 8) + c;')]), ('tc', 'tc/TC/sort/COVERRED.PAS', ['curx', 'cury', 'tarx', 'tary', 'col', 'stepx', 'stepy', 'totalpixel', 'color', 'colorcount', 'fadecount'], [(11, 'picturexofs', '(639-picturewidth) div 2', 'picturexofs = (639-picturewidth) div 2;'), (12, 'pictureyofs', '(479-pictureheight) div 2', 'pictureyofs = (479-pictureheight) div 2;'), (74, 'curx', 'random(639+1) shl step', 'curx:=random(639+1) shl step;'), (75, 'cury', 'random(479+1) shl step', 'cury:=random(479+1) shl step;'), (76, 'tarx', '(picturexofs+xc-1) shl step', 'tarx:=(picturexofs+xc-1) shl step;'), (77, 'tary', '(pictureyofs+yc-1) shl step', 'tary:=(pictureyofs+yc-1) shl step;'), (78, 'stepx', '(tarx-curx) div 64', 'stepx:=(tarx-curx) div 64;'), (79, 'stepy', '(tary-cury) div 64', 'stepy:=(tary-cury) div 64;'), (174, 'memw[$a000:(((y-1) shl 1)*320+(x shl 1))]', '(c shl 8) + c', 'memw[$a000:(((y-1) shl 1)*320+(x shl 1))] := (c shl 8) + c;'), (175, 'memw[$a000:(((y shl 1)-1)*320+(x shl 1))]', '(c shl 8) + c', 'memw[$a000:(((y shl 1)-1)*320+(x shl 1))] := (c shl 8) + c;')]), ('tc', 'tc/TC/sort/sort/COVERRED.PAS', ['curx', 'cury', 'tarx', 'tary', 'col', 'stepx', 'stepy', 'totalpixel', 'color', 'colorcount', 'fadecount'], [(11, 'picturexofs', '(639-picturewidth) div 2', 'picturexofs = (639-picturewidth) div 2;'), (12, 'pictureyofs', '(479-pictureheight) div 2', 'pictureyofs = (479-pictureheight) div 2;'), (74, 'curx', 'random(639+1) shl step', 'curx:=random(639+1) shl step;'), (75, 'cury', 'random(479+1) shl step', 'cury:=random(479+1) shl step;'), (76, 'tarx', '(picturexofs+xc-1) shl step', 'tarx:=(picturexofs+xc-1) shl step;'), (77, 'tary', '(pictureyofs+yc-1) shl step', 'tary:=(pictureyofs+yc-1) shl step;'), (78, 'stepx', '(tarx-curx) div 64', 'stepx:=(tarx-curx) div 64;'), (79, 'stepy', '(tary-cury) div 64', 'stepy:=(tary-cury) div 64;'), (174, 'memw[$a000:(((y-1) shl 1)*320+(x shl 1))]', '(c shl 8) + c', 'memw[$a000:(((y-1) shl 1)*320+(x shl 1))] := (c shl 8) + c;'), (175, 'memw[$a000:(((y shl 1)-1)*320+(x shl 1))]', '(c shl 8) + c', 'memw[$a000:(((y shl 1)-1)*320+(x shl 1))] := (c shl 8) + c;')]), ('tc', 'tc/SORT/ALLSORT.PAS', ['i', 'status'], [(62, 'tmp', 'a[i-1]', 'tmp:=a[i-1];'), (65, 'child', '(i)*2', 'child:=(i)*2;'), (71, 'a[i-1]', 'a[child-1]', 'a[i-1]:=a[child-1];'), (154, 'num', 'abs(right-left)+1', 'num:=abs(right-left)+1;'), (155, 'leftend', 'center-1', 'leftend:=center-1;'), (156, 'tmp', 'left+1', 'tmp:=left+1;'), (183, 'x[right]', 'temp[right+1]', 'x[right]:=temp[right+1];'), (204, 'num', 'abs(right-left)+1', 'num:=abs(right-left)+1;'), (207, 'leftend', 'center-1', 'leftend:=center-1;'), (210, 'tmp', 'left+1', 'tmp:=left+1;')]), ('tc', 'tc/TC/sort/ALLSORT.PAS', ['i', 'status'], [(62, 'tmp', 'a[i-1]', 'tmp:=a[i-1];'), (65, 'child', '(i)*2', 'child:=(i)*2;'), (71, 'a[i-1]', 'a[child-1]', 'a[i-1]:=a[child-1];'), (154, 'num', 'abs(right-left)+1', 'num:=abs(right-left)+1;'), (155, 'leftend', 'center-1', 'leftend:=center-1;'), (156, 'tmp', 'left+1', 'tmp:=left+1;'), (183, 'x[right]', 'temp[right+1]', 'x[right]:=temp[right+1];'), (204, 'num', 'abs(right-left)+1', 'num:=abs(right-left)+1;'), (207, 'leftend', 'center-1', 'leftend:=center-1;'), (210, 'tmp', 'left+1', 'tmp:=left+1;')]), ('tc', 'tc/TC/sort/sort/ALLSORT.PAS', ['i', 'status'], [(62, 'tmp', 'a[i-1]', 'tmp:=a[i-1];'), (65, 'child', '(i)*2', 'child:=(i)*2;'), (71, 'a[i-1]', 'a[child-1]', 'a[i-1]:=a[child-1];'), (154, 'num', 'abs(right-left)+1', 'num:=abs(right-left)+1;'), (155, 'leftend', 'center-1', 'leftend:=center-1;'), (156, 'tmp', 'left+1', 'tmp:=left+1;'), (183, 'x[right]', 'temp[right+1]', 'x[right]:=temp[right+1];'), (204, 'num', 'abs(right-left)+1', 'num:=abs(right-left)+1;'), (207, 'leftend', 'center-1', 'leftend:=center-1;'), (210, 'tmp', 'left+1', 'tmp:=left+1;')]), ('tc', 'tc/EXAMPLES/MCUTIL.C', ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/Project/Children/TC3/EXAMPLES/TCALC/TCUTIL.C', ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/Project/Roof/TC/EXAMPLES/TCALC/TCUTIL.C', ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/TC/MCUTIL.C', ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/TC/Project/Children/TC3/EXAMPLES/TCALC/TCUTIL.C', ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/TC/Project/Roof/TC/EXAMPLES/TCALC/TCUTIL.C', ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/TC/TC/EXAMPLES/TCALC/TCUTIL.C', ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/TC/TC/MCUTIL.C', ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/TC/TC/OUTPUT/RoofAndCurtain/TC/EXAMPLES/TCALC/TCUTIL.C', ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/TC/TCUTIL.C', ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/TC/port/control2/MCUTIL.C', ['size', 'len', 'maxlen', 'start', 'numstring', 'fcol', 'frow', 'value', 's', 'spaces1', 'spaces2', 'total', 'col'], [(22, 'cellptr', '(CELLPTR)(malloc(strlen(s) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + 2));'), (37, 'cellptr', '(CELLPTR)(malloc(sizeof(double) + 1))', 'cellptr = (CELLPTR)(malloc(sizeof(double) + 1));'), (53, 'cellptr', '(CELLPTR)(malloc(strlen(s) + sizeof(double) + 2))', 'cellptr = (CELLPTR)(malloc(strlen(s) + sizeof(double) + 2));'), (122, 'start', '*input', 'start = *input;'), (166, 'rowstart', 'curpos - rowwidth(frow)', 'rowstart = curpos - rowwidth(frow);'), (167, 'colstart', 'rowstart - ((fcol > 25) ? 2 : 1)', 'colstart = rowstart - ((fcol > 25) ? 2 : 1);'), (225, 'value', 'cellptr->v.f.fvalue', 'value = cellptr->v.f.fvalue;'), (238, 'colstr[0]', "col + 'A'", "colstr[0] = col + 'A';"), (241, 'colstr[0]', "(col / 26) - 1 + 'A'", "colstr[0] = (col / 26) - 1 + 'A';"), (242, 'colstr[1]', "(col % 26) + 'A'", "colstr[1] = (col % 26) + 'A';")]), ('tc', 'tc/INCLUDE/GRAPHICS.H', ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(45, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page\t*/'), (46, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page\t*/'), (48, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page\t*/'), (50, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page\t*/'), (51, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page\t*/'), (52, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page\t*/'), (53, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page\t*/'), (62, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page\t*/'), (63, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page\t*/'), (64, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page\t*/')]), ('tc', 'tc/Project/Bin/Tc3/INCLUDE/GRAPHICS.H', ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(43, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page   */'), (44, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page   */'), (46, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page   */'), (48, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page   */'), (49, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page   */'), (50, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page   */'), (51, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page   */'), (60, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page   */'), (61, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page   */'), (62, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page   */')]), ('tc', 'tc/Project/Children/TC3/INCLUDE/GRAPHICS.H', ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(43, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page   */'), (44, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page   */'), (46, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page   */'), (48, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page   */'), (49, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page   */'), (50, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page   */'), (51, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page   */'), (60, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page   */'), (61, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page   */'), (62, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page   */')]), ('tc', 'tc/Project/Roof/TC/INCLUDE/GRAPHICS.H', ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(43, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page   */'), (44, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page   */'), (46, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page   */'), (48, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page   */'), (49, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page   */'), (50, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page   */'), (51, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page   */'), (60, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page   */'), (61, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page   */'), (62, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page   */')]), ('tc', 'tc/TC/GRAPHICS.H', ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(45, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page\t*/'), (46, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page\t*/'), (48, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page\t*/'), (50, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page\t*/'), (51, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page\t*/'), (52, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page\t*/'), (53, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page\t*/'), (62, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page\t*/'), (63, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page\t*/'), (64, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page\t*/')]), ('tc', 'tc/TC/INCLUDE/GRAPHICS.H', ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(45, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page\t*/'), (46, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page\t*/'), (48, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page\t*/'), (50, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page\t*/'), (51, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page\t*/'), (52, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page\t*/'), (53, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page\t*/'), (62, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page\t*/'), (63, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page\t*/'), (64, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page\t*/')]), ('tc', 'tc/TC/Project/Bin/Tc3/INCLUDE/GRAPHICS.H', ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(43, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page   */'), (44, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page   */'), (46, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page   */'), (48, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page   */'), (49, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page   */'), (50, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page   */'), (51, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page   */'), (60, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page   */'), (61, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page   */'), (62, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page   */')]), ('tc', 'tc/TC/Project/Children/TC3/INCLUDE/GRAPHICS.H', ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(43, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page   */'), (44, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page   */'), (46, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page   */'), (48, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page   */'), (49, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page   */'), (50, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page   */'), (51, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page   */'), (60, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page   */'), (61, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page   */'), (62, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page   */')]), ('tc', 'tc/TC/Project/Roof/TC/INCLUDE/GRAPHICS.H', ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(43, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page   */'), (44, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page   */'), (46, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page   */'), (48, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page   */'), (49, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page   */'), (50, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page   */'), (51, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page   */'), (60, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page   */'), (61, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page   */'), (62, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page   */')]), ('tc', 'tc/TC/TC/GRAPHICS.H', ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(43, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page   */'), (44, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page   */'), (46, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page   */'), (48, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page   */'), (49, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page   */'), (50, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page   */'), (51, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page   */'), (60, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page   */'), (61, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page   */'), (62, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page   */')]), ('tc', 'tc/TC/TC/INCLUDE/GRAPHICS.H', ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(43, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page   */'), (44, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page   */'), (46, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page   */'), (48, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page   */'), (49, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page   */'), (50, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page   */'), (51, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page   */'), (60, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page   */'), (61, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page   */'), (62, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page   */')]), ('tc', 'tc/TC/TC/OUTPUT/RoofAndCurtain/TC/INCLUDE/GRAPHICS.H', ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(43, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page   */'), (44, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page   */'), (46, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page   */'), (48, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page   */'), (49, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page   */'), (50, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page   */'), (51, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page   */'), (60, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page   */'), (61, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page   */'), (62, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page   */')]), ('tc', 'tc/TC/genetic/GRAPHICS.H', ['char', 'linestyle', 'upattern', 'thickness', 'font', 'direction', 'charsize', 'horiz', 'vert', 'pattern', 'color', 'x', 'y'], [(45, 'CGAC0', '0,  /* 320x200 palette 0', 'CGAC0      = 0,  /* 320x200 palette 0; 1 page\t*/'), (46, 'CGAC1', '1,  /* 320x200 palette 1', 'CGAC1      = 1,  /* 320x200 palette 1; 1 page\t*/'), (48, 'CGAC3', '3,  /* 320x200 palette 3', 'CGAC3      = 3,  /* 320x200 palette 3; 1 page\t*/'), (50, 'MCGAC0', '0,  /* 320x200 palette 0', 'MCGAC0     = 0,  /* 320x200 palette 0; 1 page\t*/'), (51, 'MCGAC1', '1,  /* 320x200 palette 1', 'MCGAC1     = 1,  /* 320x200 palette 1; 1 page\t*/'), (52, 'MCGAC2', '2,  /* 320x200 palette 2', 'MCGAC2     = 2,  /* 320x200 palette 2; 1 page\t*/'), (53, 'MCGAC3', '3,  /* 320x200 palette 3', 'MCGAC3     = 3,  /* 320x200 palette 3; 1 page\t*/'), (62, 'ATT400C0', '0,  /* 320x200 palette 0', 'ATT400C0   = 0,  /* 320x200 palette 0; 1 page\t*/'), (63, 'ATT400C1', '1,  /* 320x200 palette 1', 'ATT400C1   = 1,  /* 320x200 palette 1; 1 page\t*/'), (64, 'ATT400C2', '2,  /* 320x200 palette 2', 'ATT400C2   = 2,  /* 320x200 palette 2; 1 page\t*/')]), ('caimath', 'caimath/START.PAS', ['x', 'y', 'c', 'ya', 'xa', 'i', 'd', 'co', 'l', 'p', 'xx', 'yy'], [(11, 'Ya', '-88', 'Ya := -88;'), (12, 'Xa', 'round((Ya*Ya)/(4*C))', 'Xa := round((Ya*Ya)/(4*C));'), (16, 'X', 'round((Y*Y)/(4*C))', 'X := round((Y*Y)/(4*C));'), (30, 'xa', '-88', 'xa := -88;'), (31, 'ya', 'round((xa*xa)/(4*c))', 'ya := round((xa*xa)/(4*c));'), (34, 'Y', 'round((X*X)/(4*C))', 'Y := round((X*X)/(4*C));'), (47, 'Xa', '-105', 'Xa := -105;'), (48, 'Ya', 'round((Xa*Xa)/(4*C))', 'Ya := round((Xa*Xa)/(4*C));'), (51, 'Y', 'round((X*X)/(4*C))', 'Y := round((X*X)/(4*C));'), (63, 'Xa', '-125', 'Xa := -125;')]), ('tc', 'tc/EXAMPLES/BGIDEMO.C', ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(160, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (166, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (254, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (305, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (316, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (317, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (318, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (332, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (338, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (359, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/EXAMPLES/CBAR.C', ['xdelta', 'ydelta', 'xstep', 'ystep', 'change', 'count', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4', 'wfactor', 'hfactor'], [(31, 'xdelta', 'x2 - x1', 'xdelta = x2 - x1;               /* Calculate the change in x coordinates */'), (32, 'ydelta', 'y2 - y1', 'ydelta = y2 - y1;               /* Calculate the change in y coordinates */'), (35, 'xdelta', '-xdelta', 'xdelta = -xdelta;'), (36, 'xstep', '-1', 'xstep = -1;'), (42, 'ydelta', '-ydelta', 'ydelta = -ydelta;'), (43, 'ystep', '-1', 'ystep = -1;'), (107, 'wfactor', 'width / 5', 'wfactor = width / 5;     /* figure out wfactor and hfactor */'), (108, 'hfactor', 'height / 12', 'hfactor = height / 12;'), (109, 'x2', 'x1 + wfactor', 'x2 = x1 + wfactor;       /* compute the location of the points on the bar */'), (110, 'x3', 'x1 + width', 'x3 = x1 + width;')]), ('tc', 'tc/Project/Bin/BGI/BGIDEMO.C', ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/Project/Children/BGI/BGIDEMO.C', ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/Project/Children/TC3/BGI/BGIDEMO.C', ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/Project/Children/TC3/BIN/HOME.C', ['up', 'down', 'ph', 'pr', 'y', 'use', 'hour', 'min', 't', 'sensor', 'chk_choice', 'int', 'chk_pos_home', 'chk_pos_auto', 'a', 'n', 'press', 'b', 'choice', 'm'], [(376, 'a', 'a-5', 'a=a-5;'), (380, 'a', 'a-10', 'a=a-10;'), (383, 'a', 'a-14', 'a=a-14;'), (406, 'a', 'y-130', 'a=y-130;\ta=a/20;'), (410, 'a', 'y-130', 'a=y-130;\ta=a/20;'), (414, 'a', 'y-260', 'a=y-260;\ta=a/20;'), (418, 'a', 'y-260', 'a=y-260;\ta=a/20;'), (429, 'a', 'y-130', 'a=y-130;\ta=a/20;'), (433, 'a', 'y-130', 'a=y-130;\ta=a/20;'), (867, 'a', 'area->tm_mday', 'a = area->tm_mday;')]), ('tc', 'tc/Project/ClothLine/BGI/BGIDEMO.C', ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/Project/Roof/BGI/BGIDEMO.C', ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/Project/Roof/TC/BGI/BGIDEMO.C', ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/Project/Roof/TC/BIN/ASSIGN1.CPP', ['list', 'any1', 'a', 'b', 'v', 'temp', 'm', 't', 'i', 'j', 'q', 'k', 'min', 'max1', 'any2'], [(33, 'list[b]', 'list[b-1]', 'list[b] = list[b-1];'), (34, 'b', 'b - 1', 'b = b - 1;'), (75, 'm', '(max2-min2+1)/2', 'm = (max2-min2+1)/2;'), (77, 'max2', 'max2-1', 'max2=max2-1;'), (83, 'i', 'min2+1', 'i = min2+1;'), (84, 'j', 'max2-1', 'j = max2-1;'), (89, 'i', 'i+1', 'i=i+1;'), (93, 'j', 'j-1', 'j=j-1;'), (126, 'k', 'rand()', 'k = rand();'), (137, 'i', 'i + 1', 'i = i + 1;')]), ('tc', 'tc/Project/Roof/TC/BIN/SU.CPP', ['objlength', 'start_loc', 'add_length', 'plus_minus', 'csect', 'ascii', 'locctr', 'proglength', 'progstart', 'textstart', 'textaddr', 'textlength', 'textarray', 'pc', 'base', 'current_mod', 'litpool', 'litpool1', 'litpool2', 'linenum'], [(306, 'tempo', 'optab[i+1].opcode', 'tempo = optab[i+1].opcode;'), (397, 'hash', 'hash + (unsigned char)(symbol[i])', 'hash = hash + (unsigned char)(symbol[i]);'), (398, 'hash', 'hash % (SYMTABLIMIT + 1)', 'hash = hash % (SYMTABLIMIT + 1);'), (419, 'ptr', '(ptr + 1) % (SYMTABLIMIT + 1)', 'ptr = (ptr + 1) % (SYMTABLIMIT + 1);'), (450, 'ptr', '(ptr + 1) % (SYMTABLIMIT + 1)', 'ptr = (ptr + 1) % (SYMTABLIMIT + 1);'), (469, 'hash', 'hash + (unsigned char)(literal[i])', 'hash = hash + (unsigned char)(literal[i]);'), (470, 'hash', 'hash % (SYMTABLIMIT + 1)', 'hash = hash % (SYMTABLIMIT + 1);'), (491, 'ptr', '(ptr + 1) % (SYMTABLIMIT + 1)', 'ptr = (ptr + 1) % (SYMTABLIMIT + 1);'), (509, 'textlength', 'textlength + littab[i].length', 'textlength = textlength + littab[i].length;'), (510, 'textaddr', 'locctr + littab[i].length / 2', 'textaddr = locctr + littab[i].length / 2;')]), ('tc', 'tc/SORT/TEST.PAS', ['age', 'oldh', 'oldm', 'olds', 'oldTime', 'Timeuse', 'i', 'Tmp', 'a', 'k', 'b', 'line', 'code', 'g', 'x', 'y', 'oldTm', 'timecomfort', 'maxp'], [(16, 'Stoptopic', "'*'", "Stoptopic = '*';   {for stop each topic}"), (254, 'secondToForm', "s1+':'+s2", "secondToForm := s1+':'+s2;"), (296, 'st', 'secondToform(Round((time-oldtime)/18.2))', 'st := secondToform(Round((time-oldtime)/18.2));'), (432, 'topic[t]', 'random(21)', 'topic[t]:=random(21);'), (434, 'se', 'se+[topic[t]]', 'se := se+[topic[t]];'), (455, 'Timeuse', 'Round((Time-oldTm)/18.2)', 'Timeuse := Round((Time-oldTm)/18.2);'), (499, 'i', 'random(15)+1', 'i := random(15)+1;'), (578, 'countArea', 'CountArea+2', 'countArea := CountArea+2;'), (586, 'upscrollbox', '46+((countp-1)*(310 div maxp))', 'upscrollbox := 46+((countp-1)*(310 div maxp));'), (587, 'downscrollBox', '46+(countp*(310 div maxp))', 'downscrollBox :=46+(countp*(310 div maxp));')]), ('tc', 'tc/SORT/TESTA.PAS', ['attr', 'age', 'oldh', 'oldm', 'olds', 'oldTime', 'Timeuse', 'i', 'Tmp', 'a', 'k', 'b', 'line', 'code', 'g', 'x', 'y', 'oldTm', 'timecomfort', 'maxp'], [(19, 'Stoptopic', "'*'", "Stoptopic = '*';   {for stop each topic}"), (271, 'secondToForm', "s1+':'+s2", "secondToForm := s1+':'+s2;"), (311, 'st', 'secondToform(Round((time-oldtime)/18.2))', 'st := secondToform(Round((time-oldtime)/18.2));'), (445, 'topic[t]', 'random(21)', 'topic[t]:=random(21);'), (447, 'se', 'se+[topic[t]]', 'se := se+[topic[t]];'), (470, 'Timeuse', 'Round((Time-oldTm)/18.2)', 'Timeuse := Round((Time-oldTm)/18.2);'), (512, 'i', 'random(15)+1', 'i := random(15)+1;'), (591, 'countArea', 'CountArea+2', 'countArea := CountArea+2;'), (599, 'upscrollbox', '46+((countp-1)*(310 div maxp))', 'upscrollbox := 46+((countp-1)*(310 div maxp));'), (600, 'downscrollBox', '46+(countp*(310 div maxp))', 'downscrollBox :=46+(countp*(310 div maxp));')]), ('tc', 'tc/TC/BGIDEMO.C', ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(160, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (166, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (254, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (305, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (316, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (317, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (318, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (332, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (338, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (359, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/TC/CBAR.C', ['xdelta', 'ydelta', 'xstep', 'ystep', 'change', 'count', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4', 'wfactor', 'hfactor'], [(31, 'xdelta', 'x2 - x1', 'xdelta = x2 - x1;               /* Calculate the change in x coordinates */'), (32, 'ydelta', 'y2 - y1', 'ydelta = y2 - y1;               /* Calculate the change in y coordinates */'), (35, 'xdelta', '-xdelta', 'xdelta = -xdelta;'), (36, 'xstep', '-1', 'xstep = -1;'), (42, 'ydelta', '-ydelta', 'ydelta = -ydelta;'), (43, 'ystep', '-1', 'ystep = -1;'), (107, 'wfactor', 'width / 5', 'wfactor = width / 5;     /* figure out wfactor and hfactor */'), (108, 'hfactor', 'height / 12', 'hfactor = height / 12;'), (109, 'x2', 'x1 + wfactor', 'x2 = x1 + wfactor;       /* compute the location of the points on the bar */'), (110, 'x3', 'x1 + width', 'x3 = x1 + width;')]), ('tc', 'tc/TC/DOUBLE/DOUBBLE.PAS', ['code', 'Side1', 'A', 'B', 'Side2', 'C', 'D', 'Raduis', 'E', 'F', 'a', 'b', 'c', 'x', 'y', 'Meanweek', 'Maxweek', 'Minweek', 'i', 'j'], [(17, 's', 's+c', 's := s+c;'), (62, 'a', 'side1*side1', 'a := side1*side1;'), (63, 'b', '4*side1', 'b := 4*side1;'), (97, 'c', 'side1*side2', 'c := side1*side2;'), (98, 'd', '2*(side1+side2)', 'd := 2*(side1+side2);'), (130, 'e', 'pi * (raduis * raduis)', 'e := pi * (raduis * raduis);'), (131, 'f', '2 * pi * raduis', 'f := 2 * pi * raduis;'), (208, 'x', 'a*a', 'x := a*a;'), (209, 'y', '(b*b) + (c*c)', 'y := (b*b) + (c*c);'), (274, 'sumt', 'sumt+t[i,j]', 'sumt:=sumt+t[i,j];')]), ('tc', 'tc/TC/EXAMP/Project/BGI/BGIDEMO.C', ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/TC/EXAMP/Project/BLOCK.C', ['id', 'num', 'i', 'j', 'chk', 'a', 'b', 'c', 'd', 'str', 'press', 'x', 'y', 'k', 'l', 'm', 'sum', 'aa', 'w', 'sw'], [(720, 'data[j]', 'data[j+1]', 'data[j]=data[j+1];'), (737, 'data[j]', 'data[j+1]', 'data[j]=data[j+1];'), (3008, 'led_t[i]', 'z->b[i]', 'led_t[i]=z->b[i];'), (3010, 'speed[i]', 'z->c[i]', 'speed[i]=z->c[i];'), (3161, 'c_led[i]', 'z->a[i]', 'c_led[i]=z->a[i];'), (3303, 'i', 'z->i', 'i=z->i;'), (3304, 'j', 'z->j', 'j=z->j;'), (3347, 'j', 'j-6', 'j=j-6;'), (3435, 'i', 'z->i', 'i=z->i;'), (3559, 'sw[j]', 'z->a[j]', 'sw[j]=z->a[j];')]), ('tc', 'tc/TC/FACE.C', ['x', 'y', 'radius', 'mood', 'ch', 'i', 'color', 'r', 'imgsize', 'dif', 'x1', 'x2', 'y1', 'y2'], [(33, 'x', 'face1->position.x=320', 'x=face1->position.x=320;'), (34, 'y', 'face1->position.y=180', 'y=face1->position.y=180;'), (37, 'r', 'face1->radius', 'r=face1->radius;'), (52, 'x', 'face1->position.x', 'x=face1->position.x;'), (53, 'y', 'face1->position.y', 'y=face1->position.y;'), (54, 'r', 'face1->radius', 'r=face1->radius;'), (66, 'r', 'face1->radius', 'r=face1->radius;'), (67, 'x1', 'face1->position.x-r/2', 'x1=face1->position.x-r/2;'), (68, 'y1', 'face1->position.y-r/4', 'y1=face1->position.y-r/4;'), (69, 'x2', 'face1->position.x+r/2', 'x2=face1->position.x+r/2;')]), ('tc', 'tc/TC/LENSCAI/LENSCAI.PAS', ['Row', 'Col', 'MaxColumn', 'Maxmenu', 'CharNo', 'ByteNo', 'Ind', 'Len', 'xx', 'yy', 'x2', 'y2', 'c1', 'c2', 'x', 'y', 'd', 'yinc', 'i', 'f'], [(109, 'x2', 'x1+12*9+8', 'x2:=x1+12*9+8;'), (110, 'y2', 'y1+27', 'y2:=y1+27;'), (211, 'x', 'Random(GetMaxX)', 'x := Random(GetMaxX);'), (212, 'y', 'Random(GetMaxY)', 'y := Random(GetMaxY);'), (213, 'd', 'Random(7)', 'd := Random(7);'), (225, 'x', 'x + 1 * (d + 1)', 'x := x + 1 * (d + 1);'), (228, 'y', 'y + 0  * (d + 1)', 'y := y + 0  * (d + 1);'), (320, 'St', 'St+p', 'St:=St+p;'), (350, 'm', 'I/O', 'm :=I/O;'), (383, 'sdat', '(s*f)/(s-f)', 'sdat :=(s*f)/(s-f);')]), ('tc', 'tc/TC/Project/Bin/BGI/BGIDEMO.C', ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/TC/Project/Children/BGI/BGIDEMO.C', ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/TC/Project/Children/TC3/BGI/BGIDEMO.C', ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/TC/Project/Children/TC3/BIN/HOME.C', ['up', 'down', 'ph', 'pr', 'y', 'use', 'hour', 'min', 't', 'sensor', 'chk_choice', 'int', 'chk_pos_home', 'chk_pos_auto', 'a', 'n', 'press', 'b', 'choice', 'm'], [(376, 'a', 'a-5', 'a=a-5;'), (380, 'a', 'a-10', 'a=a-10;'), (383, 'a', 'a-14', 'a=a-14;'), (406, 'a', 'y-130', 'a=y-130;\ta=a/20;'), (410, 'a', 'y-130', 'a=y-130;\ta=a/20;'), (414, 'a', 'y-260', 'a=y-260;\ta=a/20;'), (418, 'a', 'y-260', 'a=y-260;\ta=a/20;'), (429, 'a', 'y-130', 'a=y-130;\ta=a/20;'), (433, 'a', 'y-130', 'a=y-130;\ta=a/20;'), (867, 'a', 'area->tm_mday', 'a = area->tm_mday;')]), ('tc', 'tc/TC/Project/ClothLine/BGI/BGIDEMO.C', ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/TC/Project/Roof/BGI/BGIDEMO.C', ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/TC/Project/Roof/TC/BGI/BGIDEMO.C', ['x', 'y', 'GraphDriver', 'GraphMode', 'AspectRatio', 'MaxX', 'MaxY', 'MaxColors', 'ErrorCode', 'gprintf', 'int', 'char', 'xasp', 'yasp', 'driver', 'mode', 'buffer', 'font', 'ch', 'wwidth'], [(163, 'MaxColors', 'getmaxcolor() + 1', 'MaxColors = getmaxcolor() + 1;\t/* Read maximum number of colors*/'), (169, 'AspectRatio', '(double)xasp / (double)yasp', 'AspectRatio = (double)xasp / (double)yasp; /* Get correction factor\t*/'), (257, 'wwidth', 'vp.right - vp.left', 'wwidth = vp.right - vp.left;\t/* Determine the window width\t*/'), (308, 'h', '3 * textheight( "H" )', 'h = 3 * textheight( "H" );'), (319, 'xstep', '((vp.right-vp.left) - (2*h)) / 10', 'xstep = ((vp.right-vp.left) - (2*h)) / 10;'), (320, 'ystep', '((vp.bottom-vp.top) - (2*h)) / 5', 'ystep = ((vp.bottom-vp.top) - (2*h)) / 5;'), (321, 'j', '(vp.bottom-vp.top) - h', 'j = (vp.bottom-vp.top) - h;'), (335, 'color', 'random( MaxColors )', 'color = random( MaxColors );'), (341, 'bheight', '(vp.bottom-vp.top) - h - 1', 'bheight = (vp.bottom-vp.top) - h - 1;'), (362, 'color', 'random( MaxColors-1 )+1', 'color = random( MaxColors-1 )+1;')]), ('tc', 'tc/TC/Project/Roof/TC/BIN/ASSIGN1.CPP', ['list', 'any1', 'a', 'b', 'v', 'temp', 'm', 't', 'i', 'j', 'q', 'k', 'min', 'max1', 'any2'], [(33, 'list[b]', 'list[b-1]', 'list[b] = list[b-1];'), (34, 'b', 'b - 1', 'b = b - 1;'), (75, 'm', '(max2-min2+1)/2', 'm = (max2-min2+1)/2;'), (77, 'max2', 'max2-1', 'max2=max2-1;'), (83, 'i', 'min2+1', 'i = min2+1;'), (84, 'j', 'max2-1', 'j = max2-1;'), (89, 'i', 'i+1', 'i=i+1;'), (93, 'j', 'j-1', 'j=j-1;'), (126, 'k', 'rand()', 'k = rand();'), (137, 'i', 'i + 1', 'i = i + 1;')]), ('tc', 'tc/TC/Project/Roof/TC/BIN/SU.CPP', ['objlength', 'start_loc', 'add_length', 'plus_minus', 'csect', 'ascii', 'locctr', 'proglength', 'progstart', 'textstart', 'textaddr', 'textlength', 'textarray', 'pc', 'base', 'current_mod', 'litpool', 'litpool1', 'litpool2', 'linenum'], [(306, 'tempo', 'optab[i+1].opcode', 'tempo = optab[i+1].opcode;'), (397, 'hash', 'hash + (unsigned char)(symbol[i])', 'hash = hash + (unsigned char)(symbol[i]);'), (398, 'hash', 'hash % (SYMTABLIMIT + 1)', 'hash = hash % (SYMTABLIMIT + 1);'), (419, 'ptr', '(ptr + 1) % (SYMTABLIMIT + 1)', 'ptr = (ptr + 1) % (SYMTABLIMIT + 1);'), (450, 'ptr', '(ptr + 1) % (SYMTABLIMIT + 1)', 'ptr = (ptr + 1) % (SYMTABLIMIT + 1);'), (469, 'hash', 'hash + (unsigned char)(literal[i])', 'hash = hash + (unsigned char)(literal[i]);'), (470, 'hash', 'hash % (SYMTABLIMIT + 1)', 'hash = hash % (SYMTABLIMIT + 1);'), (491, 'ptr', '(ptr + 1) % (SYMTABLIMIT + 1)', 'ptr = (ptr + 1) % (SYMTABLIMIT + 1);'), (509, 'textlength', 'textlength + littab[i].length', 'textlength = textlength + littab[i].length;'), (510, 'textaddr', 'locctr + littab[i].length / 2', 'textaddr = locctr + littab[i].length / 2;')]), ('tc', 'tc/TC/S26/TETRIS.C', ['RightArrow', 'LeftArrow', 'UpArrow', 'DownArrow', 'Space', 'Esc', 'far', 'TypeTris', 'Tris1', 'Tris2', 'Tris3', 'Tris4', 'Tris5', 'Tris6', 'BColor', 'No_Tris', 'NumTris', 'OldNumTris', 'ArrayTris', 'ColorTris'], [(43, 'ptr0', 'FirstAdr[page] + 1', 'ptr0 = FirstAdr[page] + 1;'), (44, 'ptr1', 'FirstAdr[3] + 1', 'ptr1 = FirstAdr[3] + 1;'), (80, 'ptr', 'TypeTris[num] + (n << 3)', 'ptr = TypeTris[num] + (n << 3);'), (92, 'ptr', 'TypeTris[num] + (NumTris << 3)', 'ptr = TypeTris[num] + (NumTris << 3);'), (104, 'ptr', 'TypeTris[num] + (NumTris << 3)', 'ptr = TypeTris[num] + (NumTris << 3);'), (107, 'Y', 'YTris + *(ptr + 1)', 'Y = YTris + *(ptr + 1);'), (119, 'pl1', '48+(sin(k / 30) * 47.0 + 256 * (int)(47 * cos(k / 40)))', 'pl1 = 48+(sin(k / 30) * 47.0 + 256 * (int)(47 * cos(k / 40)));'), (120, 'pl2', '48+(sin(k / 14) * 47.0 + 256 * (int)(47 * sin(k / 32))) - pl1', 'pl2 = 48+(sin(k / 14) * 47.0 + 256 * (int)(47 * sin(k / 32))) - pl1;'), (121, 'ptr0', 'BKdata + pl1', 'ptr0 = BKdata + pl1;'), (126, 'color', '((*ptr0++) + pl2)', 'color = ((*ptr0++) + pl2);')]), ('tc', 'tc/TC/S33/BOMBER.C', ['RightArrow', 'LeftArrow', 'UpArrow', 'DownArrow', 'Space', 'Esc', 'ch', 'ScanCode', 'BitImage', 'i', 'ptr', 'j', 'memtmp', 'width', 'height', 'ptr1', 'Map', 'Skip', 'MAXGOST1', 'MAXBOOM1'], [(219, 'width', '*ptr1++', 'width = *ptr1++; height = *ptr1++;'), (226, 'width', '*ptr++', 'width = *ptr++; height = *ptr++;'), (243, 'width', '*ptr++', 'width = *ptr++;'), (244, 'height', '*ptr++', 'height = *ptr++;'), (245, 'BitImage[num]', 'malloc((width << 1) * height + 2)', 'BitImage[num] = malloc((width << 1) * height + 2);'), (264, 'width', '*ptr++', 'width = *ptr++; height = *ptr++;'), (265, 'BitImage[num1]', 'malloc(width * height + 2)', 'BitImage[num1] = malloc(width * height + 2);'), (322, 'i', '(x - 5) / 12', 'i = (x - 5) / 12; j = (y - 3) / 12;'), (362, 'Addx', 'Gxgost[i] + addmove[Gran[i]][0]', 'Addx = Gxgost[i] + addmove[Gran[i]][0];'), (363, 'Addy', 'Gygost[i] + addmove[Gran[i]][1]', 'Addy = Gygost[i] + addmove[Gran[i]][1];')]), ('tc', 'tc/TC/S34/CUTSPRIT.C', ['far', 'int', 'i', 'j', 'x1', 'y1', 'MouseX', 'MouseY', 'oMouseX', 'oMouseY', 'mousebutt', 'StMouse', 'MouseT', 'MouseT1', 'Palette', 'Image', 'Back', 'namefile', 'Numi', 'Post'], [(20, 'LINE_Y[i]', 'i * 320', 'LINE_Y[i] = i * 320;'), (68, 'x1', 'x0 + *ptr++', 'x1 = x0 + *ptr++; y1 = y0 + *ptr++;'), (213, 'StMouse', '-1', 'StMouse = -1;'), (284, 'Membuf', 'malloc(WHeight * WWidth)', 'Membuf = malloc(WHeight * WWidth);'), (290, 'l', 'c - 192', 'l = c - 192;'), (365, 'oGx', 'FGx + 1', 'oGx  = FGx + 1;'), (367, 'oGy', 'FGy + 1', 'oGy  = FGy + 1;'), (398, 'width', '*ptr++', 'width  = *ptr++;'), (399, 'height', '*ptr++', 'height = *ptr++;'), (416, 'red', '*ptr++', 'red   = *ptr++;')]), ('tc', 'tc/TC/S35/JUPITER.C', ['Radius', 'Diameter', 'Circum', 'Rah', 'image', 'ImgWidth', 'ImgHeight', 'TRFV', 'char', 'Palette', 'i', 'ptr', 'curr_size', 'navail_bytes', 'nbits_left', 'long', 'fc', 'oc', 'c', 'clear'], [(50, 'b1', '*pbytes++', 'b1 = *pbytes++;'), (54, 'ret', 'b1 >> (8 - nbits_left)', 'ret = b1 >> (8 - nbits_left);'), (61, 'b1', '*pbytes++', 'b1 = *pbytes++;'), (88, 'ImgWidth', '(buf[6] << 8) + buf[5]', 'ImgWidth  = (buf[6] << 8) + buf[5];'), (89, 'ImgHeight', '(buf[8] << 8) + buf[7]', 'ImgHeight = (buf[8] << 8) + buf[7];'), (90, 'buffer', 'malloc(ImgWidth * ImgHeight)', 'buffer = malloc(ImgWidth * ImgHeight);'), (97, 'stack', 'malloc(MAX_CODES + 1)', 'stack  = malloc(MAX_CODES + 1);'), (98, 'suffix', 'malloc(MAX_CODES + 1)', 'suffix = malloc(MAX_CODES + 1);'), (99, 'prefix', 'malloc(sizeof(int) * (MAX_CODES + 1))', 'prefix = malloc(sizeof(int) * (MAX_CODES + 1));'), (101, 'curr_size', 'size + 1', 'curr_size = size + 1;')]), ('tc', 'tc/TC/S36/VESA24.C', ['width', 'height', 'pal', 'IMG', 'far', 'adrx', 'adry', 'banky', 'CUfont', 'initvesa24', 'i', 'curr_size', 'navail_bytes', 'nbits_left', 'long', 'fc', 'oc', 'c', 'clear', 'ending'], [(28, 'ptrscreen', 'vgamem + adrx[x] + adry[y]', 'ptrscreen = vgamem + adrx[x] + adry[y];'), (34, 'adrx[i]', 'i * 3', 'adrx[i] = i * 3; /* one pixel equ 3 byte */'), (75, 'b1', '*pbytes++', 'b1 = *pbytes++;'), (79, 'ret', 'b1 >> (8 - nbits_left)', 'ret = b1 >> (8 - nbits_left);'), (86, 'b1', '*pbytes++', 'b1 = *pbytes++;'), (119, 'ptr', 'img->IMG', 'ptr    = img->IMG;'), (124, 'stack', 'malloc(MAX_CODES + 1)', 'stack  = malloc(MAX_CODES + 1);'), (125, 'suffix', 'malloc(MAX_CODES + 1)', 'suffix = malloc(MAX_CODES + 1);'), (126, 'prefix', 'malloc(sizeof(int) * (MAX_CODES + 1))', 'prefix = malloc(sizeof(int) * (MAX_CODES + 1));'), (128, 'curr_size', 'size + 1', 'curr_size = size + 1;')]), ('tc', 'tc/TC/S37/VESA24.C', ['width', 'height', 'pal', 'IMG', 'far', 'adrx', 'adry', 'banky', 'CUfont', 'initvesa24', 'i', 'curr_size', 'navail_bytes', 'nbits_left', 'long', 'fc', 'oc', 'c', 'clear', 'ending'], [(28, 'ptrscreen', 'vgamem + adrx[x] + adry[y]', 'ptrscreen = vgamem + adrx[x] + adry[y];'), (34, 'adrx[i]', 'i * 3', 'adrx[i] = i * 3; /* one pixel equ 3 byte */'), (75, 'b1', '*pbytes++', 'b1 = *pbytes++;'), (79, 'ret', 'b1 >> (8 - nbits_left)', 'ret = b1 >> (8 - nbits_left);'), (86, 'b1', '*pbytes++', 'b1 = *pbytes++;'), (119, 'ptr', 'img->IMG', 'ptr    = img->IMG;'), (124, 'stack', 'malloc(MAX_CODES + 1)', 'stack  = malloc(MAX_CODES + 1);'), (125, 'suffix', 'malloc(MAX_CODES + 1)', 'suffix = malloc(MAX_CODES + 1);'), (126, 'prefix', 'malloc(sizeof(int) * (MAX_CODES + 1))', 'prefix = malloc(sizeof(int) * (MAX_CODES + 1));'), (128, 'curr_size', 'size + 1', 'curr_size = size + 1;')]), ('tc', 'tc/TC/S38/VESA.C', ['PAGE', 'GX', 'GY', 'OGX', 'OGY', 'ADDX', 'ADDY', 'nBall', 'pal', 'Ball', 'Back', 'i', 'ptr', 'width', 'height', 'Length', 'j', 'k', 'loop'], [(99, 'width', '*ptr++', 'width = *ptr++;'), (100, 'height', '*ptr++', 'height = *ptr++;'), (101, 'Length', 'width * height', 'Length = width * height;'), (111, 'nBall[i]', 'random(4)', 'nBall[i] = random(4);'), (172, 'ADDY[i]', '(random(7) - 3) * 2', 'ADDY[i] = (random(7) - 3) * 2;'), (173, 'ADDX[i]', '-ADDX[i]', 'ADDX[i] = -ADDX[i];'), (176, 'ADDX[i]', '(random(7) - 3) * 2', 'ADDX[i] = (random(7) - 3) * 2 ;'), (177, 'ADDY[i]', '-ADDY[i]', 'ADDY[i] = -ADDY[i];'), (206, 'PAGE', '1 - PAGE', 'PAGE = 1 - PAGE;'), (213, 'ADDY[i]', '(random(4) - 2) * 4', 'ADDY[i] = (random(4) - 2) * 4;')]), ('tc', 'tc/TC/S39/DINOSTAR.C', ['Dinosor', 'Ballon1', 'PAGE', 'MOVE', 'GX', 'GY', 'OGX', 'OGY', 'GXBallon', 'GYBallon', 'CBallon', 'AddBallon', 'OGXBallon', 'OGYBallon', 'GXStom', 'GYStom', 'AddStom', 'OGXStom', 'OGYStom', 'GXStar'], [(200, 'r', '*ptr++', 'r = *ptr++;'), (201, 'g', '*ptr++', 'g = *ptr++;'), (202, 'b', '*ptr++', 'b = *ptr++;'), (223, 'width', '2 * (*ptr++) + x', 'width  = 2 * (*ptr++) + x;'), (224, 'height', '2 * (*ptr++) + y', 'height = 2 * (*ptr++) + y;'), (227, 'color', '*ptr++', 'color = *ptr++;'), (243, 'width', '*ptr++', 'width = *ptr++;'), (244, 'height', '*ptr++', 'height = *ptr++;'), (258, 'k', 'random(4) + 4', 'k = random(4) + 4;'), (297, 'GXBallon[i]', 'random(20) * 40 + 60', 'GXBallon[i] = random(20) * 40 + 60;')]), ('tc', 'tc/TC/S40/FIREWORK.C', ['tsin', 'tcos', 'X', 'Y', 'MAXY', 'GX', 'GY', 'DX', 'DY', 'GXTile', 'GYTile', 'cout', 'CC', 'color', 'TileU', 'SUBTile', 'LTile', 'BOOM', 'Boom1', 'Boom2'], [(249, 'x', 'GXTile[j] - 8', 'x = GXTile[j] - 8;'), (270, 'X[Num]', 'random(640) << 2', 'X[Num] = random(640) << 2;'), (271, 'Y[Num]', 'random(400) << 2', 'Y[Num] = random(400) << 2;'), (272, 'MAXY[Num]', 'random(MAXFIRE >> 1) + (MAXFIRE >> 1)', 'MAXY[Num] = random(MAXFIRE >> 1) + (MAXFIRE >> 1);'), (273, 'color[Num]', 'random(8)', 'color[Num] = random(8);'), (274, 'R', 'random(6)', 'R = random(6);'), (278, 'k', 'random(20) + 1', 'k = random(20) + 1;'), (279, 'th', 'random(360)', 'th = random(360);'), (298, 'SUBTile[Num]', 'random(8) + 8', 'SUBTile[Num] = random(8) + 8;'), (313, 'CC[i]', 'random(10) + 4', 'CC[i] = random(10) + 4;')]), ('tc', 'tc/TC/S41/MGRAPH.C', ['PageStart', 'int', 'i', 'j', 'x1', 'y1', 'Right', 'Left', 'Up', 'Down', 'Space', 'Esc', 'ch', 'ScanCode', 'ptr', 'str', 'memtmp', 'width', 'height', 'BitImage'], [(21, 'LINE_Y[i]', 'i * 320', 'LINE_Y[i] = i * 320;'), (22, 'MemLength', '320 * 200', 'MemLength = 320 * 200;'), (79, 'x1', 'x0 + *ptr++', 'x1 = x0 + *ptr++; y1 = y0 + *ptr++;'), (89, 'x1', 'x0 + *ptr++', 'x1 = x0 + *ptr++; y1 = y0 + *ptr++;'), (161, 'width', '*ptr1++', 'width = *ptr1++; height = *ptr1++;'), (169, 'width', '*ptr++', 'width = *ptr++; height = *ptr++;'), (188, 'width', '*ptr++', 'width = *ptr++;'), (189, 'height', '*ptr++', 'height = *ptr++;'), (190, 'BitImage', 'malloc((width << 1) * height + 2)', 'BitImage = malloc((width << 1) * height + 2);'), (210, 'width', '*ptr++', 'width = *ptr++; height = *ptr++;')]), ('tc', 'tc/TC/S43/KILLYABA.C', ['c_duration', 'c_octave', 'char', 'sp_on', 'sp_off', 'msb', 'c_note', 'Ya', 'Bitmap1', 'Bitmap2', 'Bitmap3', 'YaBa', 'Bitmap5', 'NewCo0', 'NewCo1', 'YaX', 'YaY', 'PosYA', 'Color0', 'Color1'], [(68, 'c_note', '*ptrsong', 'c_note = *ptrsong;'), (73, 'c_octave', '*ptrsong++', 'c_octave = *ptrsong++;'), (76, 'c_duration', '*ptrsong++', 'c_duration = *ptrsong++;'), (81, 'c_duration', '*ptrsong', 'c_duration = *ptrsong;'), (83, 'msb', 'notes[c_octave][c_note]/256', 'msb=notes[c_octave][c_note]/256;'), (195, 'x1', 'x0 + *ptr++', 'x1 = x0 + *ptr++; y1 = y0 + *ptr++;'), (216, 'Color0', 'random(7)', 'Color0 = random(7);'), (217, 'Color1', 'random(7)', 'Color1 = random(7);'), (218, 'NewCo0', 'random(7)', 'NewCo0 = random(7);'), (219, 'NewCo1', 'random(7)', 'NewCo1 = random(7);')])]; state={'rec':None,'a':[]}
        box=self.card(b,'SOURCE')
        tree=ttk.Treeview(box,columns=('a','f','v','e'),show='headings',height=10)
        for c,t,w in [('a','Archive',80),('f','Source',430),('v','Variables',90),('e','Assignments',100)]:
            tree.heading(c,text=t);tree.column(c,width=w)
        tree.pack(fill='both',expand=True,padx=12,pady=8)
        for a,f,v,e in data:tree.insert('','end',values=(a,f,len(v),len(e)))
        nb=ttk.Notebook(b);nb.pack(fill='both',expand=True,padx=28,pady=10)
        p1=tk.Frame(nb,bg='white');p2=tk.Frame(nb,bg='white');p3=tk.Frame(nb,bg='white')
        nb.add(p1,text='Dependencies');nb.add(p2,text='Recurrence');nb.add(p3,text='Validation')
        at=ttk.Treeview(p1,columns=('l','eq','dep','type'),show='headings',height=17)
        for c,t,w in [('l','Line',55),('eq','Equation',430),('dep','RHS variables',300),('type','Type',220)]:
            at.heading(c,text=t);at.column(c,width=w)
        at.pack(fill='both',expand=True,padx=12,pady=10)
        rt=tk.Text(p2,height=23,font=('Consolas',10),wrap='word');rt.pack(fill='both',expand=True,padx=12,pady=10)
        vt=tk.Text(p3,height=23,font=('Consolas',10),wrap='word');vt.pack(fill='both',expand=True,padx=12,pady=10)
        status=tk.StringVar(value='เลือก source แล้วกด ANALYZE')
        tk.Label(b,textvariable=status,bg=BG,fg=MUTED).pack(anchor='w',padx=30,pady=8)
        reserved=set('sin cos tan sqrt pow random rand abs min max sizeof int float double long short char'.split())
        def base(x):return re.sub(r'\[.*?\]','',x).strip()
        def ids(rhs):
            z=[]
            for x in re.findall(r'\b[A-Za-z_]\w*\b',rhs):
                if x.lower() not in reserved and x not in z:z.append(x)
            return z
        def norm(x):return x.replace('M_PI','π').replace('PI','π').replace('*','·')
        def select(_=None):
            q=tree.selection()
            if q:
                v=tree.item(q[0],'values');state['rec']=next((r for r in data if r[0]==v[0] and r[1]==v[1]),None)
        def analyze():
            if not state['rec']:return
            ans=[]
            for no,lhs,rhs,line in state['rec'][3]:
                d=ids(rhs); selfdep=base(lhs) in d
                ans.append((no,lhs,rhs,d,selfdep))
            state['a']=ans
            for q in at.get_children():at.delete(q)
            for no,lhs,rhs,d,selfdep in ans:
                at.insert('','end',values=(no,f'{lhs} = {norm(rhs)}',', '.join(d) or 'constant',
                          'recurrence candidate' if selfdep else 'algebraic dependency'))
            rt.delete('1.0','end');rt.insert('end','RECURRENCE CANDIDATES\n\n')
            found=0
            for no,lhs,rhs,d,selfdep in ans:
                if selfdep:
                    found+=1;b0=base(lhs)
                    rr=re.sub(r'\b'+re.escape(b0)+r'\b',b0+'ₙ',rhs)
                    rt.insert('end',f'Line {no}: {lhs} = {rhs}\n  Sequence form (only under repeated state update): {b0}ₙ₊₁ = {norm(rr)}\n\n')
            if not found:rt.insert('end','No self-dependent extracted assignment. V4.3 therefore does not label these equations as recurrences.\n')
            vt.delete('1.0','end')
            vt.insert('end','VALIDATION RULES\n\n✓ RHS variable x in y=f(x) gives dependency x→y.\n'
                      '✓ A loop alone does not prove recurrence.\n'
                      '✓ Self-dependency is only a recurrence candidate until repeated update context is established.\n'
                      '✓ Function names are not variable nodes.\n'
                      '✓ Syntax alone does not prove convergence, independence, distribution, or a closed form.\n'
                      '✓ Array/pointer semantics need a fuller parser.\n\n'
                      'This is conservative static educational analysis; legacy source is not executed.')
            status.set(f'Assignments={len(ans)} • recurrence candidates={found}')
        tree.bind('<<TreeviewSelect>>',select)
        r=tk.Frame(box,bg='white');r.pack(fill='x',padx=12,pady=(0,10))
        ttk.Button(r,text='▶ ANALYZE MATHEMATICALLY',style='Primary.TButton',command=analyze).pack(side='left')
        ttk.Button(r,text='V4.2 Expression Lab',command=self.v42_source_expression_model_lab).pack(side='left',padx=5)
        self.card(b,'NEXT',
            'V4.4: safe expression AST + loop-context analysis แล้วจึงวิเคราะห์ linear recurrence xₙ₊₁=axₙ+b: fixed point, explicit form และ convergence.')

    # ==================== V4.4: SYMBOLIC PROOF FIRST -> SIMULATION ====================
    def v44_symbolic_proof_simulation_lab(self):
        self.clear()
        self.header('∴ V4.4 • Symbolic Proof → Simulation',
            'Linear affine recurrence: xₙ₊₁ = a xₙ + b • prove first, simulate second')
        b=self.scrollbody()
        self.card(b,'MATHEMATICAL SCOPE',
            'V4.4 วิเคราะห์ recurrence อันดับหนึ่งแบบ affine: xₙ₊₁ = a xₙ + b, x₀ กำหนด. '
            'ระบบแยกกรณี a≠1 และ a=1 อย่างชัดเจน แล้วพิสูจน์สูตรปิดด้วย induction ก่อนทำ simulation. '
            'Simulation เป็นการตรวจเชิงตัวเลข ไม่ใช่ตัวแทนของ proof.')

        ctl=self.card(b,'1 • PARAMETERS')
        av=tk.DoubleVar(value=.75); bv=tk.DoubleVar(value=1.0); x0v=tk.DoubleVar(value=0.0); nv=tk.IntVar(value=20)
        for label,var,lo,hi in [('a',av,-2.0,2.0),('b',bv,-5.0,5.0),('x₀',x0v,-10.0,10.0)]:
            r=tk.Frame(ctl,bg='white');r.pack(fill='x',padx=16,pady=3)
            tk.Label(r,text=label,width=8,bg='white',anchor='w').pack(side='left')
            ttk.Scale(r,from_=lo,to=hi,variable=var).pack(side='left',fill='x',expand=True,padx=8)
            labv=tk.Label(r,width=12,bg='white',fg=BLUE,font=('Consolas',9));labv.pack(side='left')
            var.trace_add('write',lambda *_args,v=var,l=labv:l.config(text=f'{v.get():.5g}'))
            labv.config(text=f'{var.get():.5g}')
        r=tk.Frame(ctl,bg='white');r.pack(fill='x',padx=16,pady=3)
        tk.Label(r,text='n steps',width=8,bg='white',anchor='w').pack(side='left')
        ttk.Spinbox(r,from_=1,to=100,textvariable=nv,width=8).pack(side='left',padx=8)

        nb=ttk.Notebook(b);nb.pack(fill='both',expand=True,padx=28,pady=10)
        proof=tk.Frame(nb,bg='white');ind=tk.Frame(nb,bg='white');conv=tk.Frame(nb,bg='white');sim=tk.Frame(nb,bg='white')
        nb.add(proof,text='Symbolic Derivation');nb.add(ind,text='Induction Proof');nb.add(conv,text='Convergence');nb.add(sim,text='Simulation')
        ptxt=tk.Text(proof,height=25,font=('Consolas',10),wrap='word');ptxt.pack(fill='both',expand=True,padx=12,pady=10)
        itxt=tk.Text(ind,height=25,font=('Consolas',10),wrap='word');itxt.pack(fill='both',expand=True,padx=12,pady=10)
        ctxt=tk.Text(conv,height=25,font=('Consolas',10),wrap='word');ctxt.pack(fill='both',expand=True,padx=12,pady=10)
        scv=tk.Canvas(sim,height=430,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1);scv.pack(fill='both',expand=True,padx=12,pady=10)
        stxt=tk.StringVar(value='กด PROVE SYMBOLICALLY ก่อน แล้วจึง SIMULATE')
        tk.Label(b,textvariable=stxt,bg=BG,fg=MUTED,font=('Consolas',9),wraplength=1100).pack(anchor='w',padx=30,pady=(0,8))
        state={'proved':False,'a':0,'b':0,'x0':0}

        def prove():
            a=float(av.get());bb=float(bv.get());x0=float(x0v.get())
            state.update(proved=True,a=a,b=bb,x0=x0)
            ptxt.delete('1.0','end');itxt.delete('1.0','end');ctxt.delete('1.0','end')
            ptxt.insert('end','RECURRENCE\n  xₙ₊₁ = a xₙ + b,   x₀ given\n\n')
            eps=1e-10
            if abs(a-1.0)>eps:
                L=bb/(1-a)
                ptxt.insert('end','STEP 1 — FIXED POINT\n')
                ptxt.insert('end','  Let L satisfy L = aL + b.\n  (1-a)L = b\n  L = b/(1-a), for a ≠ 1.\n\n')
                ptxt.insert('end','STEP 2 — CENTER THE RECURRENCE\n')
                ptxt.insert('end','  yₙ = xₙ - L.\n  yₙ₊₁ = xₙ₊₁-L = axₙ+b-L = a(xₙ-L) = ayₙ.\n\n')
                ptxt.insert('end','STEP 3 — SOLVE THE GEOMETRIC RECURRENCE\n')
                ptxt.insert('end','  yₙ = aⁿy₀ = aⁿ(x₀-L).\n')
                ptxt.insert('end','  Therefore:  xₙ = L + aⁿ(x₀-L).\n')
                ptxt.insert('end','  Equivalent: xₙ = aⁿx₀ + b(1-aⁿ)/(1-a).\n\n')
                ptxt.insert('end',f'For current parameters: L = {L:.10g}\n')
                itxt.insert('end','CLAIM\n  xₙ = L + aⁿ(x₀-L).\n\nBASE CASE n=0\n')
                itxt.insert('end','  RHS = L + a⁰(x₀-L) = L + x₀-L = x₀. ✓\n\nINDUCTIVE STEP\n')
                itxt.insert('end','  Assume xₖ = L + aᵏ(x₀-L).\n')
                itxt.insert('end','  xₖ₊₁ = axₖ+b\n          = a[L+aᵏ(x₀-L)] + b\n')
                itxt.insert('end','          = (aL+b) + aᵏ⁺¹(x₀-L)\n          = L + aᵏ⁺¹(x₀-L). ✓\n\n')
                itxt.insert('end','Thus the closed form holds for all n≥0 by mathematical induction.')
                ctxt.insert('end','CONVERGENCE FROM THE CLOSED FORM\n  xₙ-L = aⁿ(x₀-L).\n\n')
                if abs(a)<1:
                    ctxt.insert('end','Since |a|<1, aⁿ→0. Therefore xₙ→L for every finite x₀.\n')
                    ctxt.insert('end',f'  Limit L = b/(1-a) = {L:.10g}\n')
                elif abs(a)>1:
                    ctxt.insert('end','Since |a|>1, |a|ⁿ grows. In general the sequence does not converge.\n')
                    ctxt.insert('end','Exception: if x₀=L exactly, xₙ=L for every n.\n')
                else: # a=-1 because a=1 handled separately
                    ctxt.insert('end','Here a=-1. Then aⁿ alternates between ±1.\n')
                    ctxt.insert('end','The sequence generally oscillates and has no limit; if x₀=L it is constant.\n')
            else:
                ptxt.insert('end','SPECIAL CASE a=1\n  xₙ₊₁ = xₙ+b.\n')
                ptxt.insert('end','Repeated substitution gives xₙ = x₀ + nb.\n')
                ptxt.insert('end','The fixed-point formula b/(1-a) is not valid because 1-a=0.\n')
                itxt.insert('end','CLAIM\n  xₙ=x₀+nb.\n\nBASE n=0\n  x₀=x₀+0b. ✓\n\n')
                itxt.insert('end','INDUCTIVE STEP\n  Assume xₖ=x₀+kb.\n  xₖ₊₁=xₖ+b=x₀+(k+1)b. ✓\n')
                if abs(bb)<eps:
                    ctxt.insert('end','a=1 and b=0: xₙ=x₀ for all n, so the sequence converges to x₀.\n')
                else:
                    ctxt.insert('end','a=1 and b≠0: xₙ=x₀+nb is unbounded in magnitude, so it does not converge to a finite limit.\n')
            stxt.set('Symbolic derivation + induction completed. Simulation may now be used as a numerical check.')
            nb.select(proof)

        def closed(n,a,bb,x0):
            if abs(a-1.0)<1e-10:return x0+n*bb
            L=bb/(1-a);return L+(a**n)*(x0-L)

        def simulate():
            if not state['proved']: prove()
            a=state['a'];bb=state['b'];x0=state['x0'];N=max(1,min(100,int(nv.get())))
            xs=[x0]
            for _ in range(N):xs.append(a*xs[-1]+bb)
            cf=[closed(i,a,bb,x0) for i in range(N+1)]
            err=max(abs(x-y) for x,y in zip(xs,cf))
            scv.delete('all');w=max(scv.winfo_width(),800);h=max(scv.winfo_height(),400);pad=55
            vals=xs+cf;mn=min(vals);mx=max(vals)
            if abs(mx-mn)<1e-12:mx=mn+1
            def xy(i,y):
                return pad+i*(w-2*pad)/max(1,N), h-pad-(y-mn)/(mx-mn)*(h-2*pad)
            pts=[]
            for i,y in enumerate(xs):pts.extend(xy(i,y))
            scv.create_line(*pts,fill=BLUE,width=3)
            for i,y in enumerate(cf):
                x1,y1=xy(i,y);scv.create_oval(x1-3,y1-3,x1+3,y1+3,outline=ORANGE,width=2)
            scv.create_text(pad,18,anchor='w',text='Blue line: recurrence iteration   Orange circles: symbolic closed form',fill=TEXT,font=('Segoe UI Semibold',10))
            scv.create_text(pad,38,anchor='w',text=f'max |simulation - closed form| = {err:.3e}',fill=MUTED,font=('Consolas',9))
            stxt.set(f'Simulation checked n=0..{N}; maximum numerical discrepancy = {err:.3e}')
            nb.select(sim)

        act=tk.Frame(ctl,bg='white');act.pack(fill='x',padx=16,pady=(4,12))
        ttk.Button(act,text='1 ▶ PROVE SYMBOLICALLY',style='Primary.TButton',command=prove).pack(side='left')
        ttk.Button(act,text='2 ▶ SIMULATE + VERIFY',command=simulate).pack(side='left',padx=6)
        ttk.Button(act,text='V4.3 Dependency Lab',command=self.v43_dependency_recurrence_lab).pack(side='left')

        self.card(b,'CORRECT INTERPRETATION',
            'Proof establishes the formula for all n under the stated recurrence. Simulation checks selected numerical parameters only. '
            'Agreement with finitely many simulated terms does not prove the general formula. '
            'V4.5 can connect verified recurrence candidates from source context to this proof engine, but only after loop/update semantics are established.')

    def v45_source_to_proof_lab(self):
        self.clear()
        self.header('🔬 V4.5 • Source → Verified Recurrence → Proof',
            'Source C/Pascal → verify recurrence → symbolic proof → numerical simulation')
        b=self.scrollbody()
        self.card(b,'MATHEMATICAL PIPELINE',
            'Self-dependency alone is not enough. V4.5 requires nearby loop/update evidence and a simple affine form x=a*x+b. '
            'Only then does it pass the model to the proof stage. Legacy source is never executed.')
        data=[('tc', 'tc/TC/caibinary/PROC.PAS', 161, 'x1', 'x1 - 1', 'x1 := x1 - 1;'), ('tc', 'tc/TC/caibinary/PROC.PAS', 162, 'y1', 'y1 - 1', 'y1 := y1 - 1;'), ('tc', 'tc/TC/caibinary/PROC.PAS', 168, 'x1', 'x1 - 1', 'x1 := x1 - 1;'), ('tc', 'tc/TC/caibinary/PROC.PAS', 169, 'y1', 'y1 + 1', 'y1 := y1 + 1;'), ('tc', 'tc/TC/caibinary/PROC.PAS', 178, 'x1', 'x1 + 1', 'x1 := x1 + 1; y1 := y1 - 1;'), ('tc', 'tc/TC/caibinary/PROC.PAS', 184, 'x1', 'x1 + 1', 'x1 := x1 + 1;'), ('tc', 'tc/TC/caibinary/PROC.PAS', 185, 'y1', 'y1 + 1', 'y1 := y1 + 1;'), ('tc', 'tc/TC/caibinary/PROC.PAS', 228, 'a', 'a - 1', 'a := a - 1; b := b - 1;'), ('tc', 'tc/TC/caibinary/PROC.PAS', 237, 'a', 'a - 1', 'a := a - 1; b := b + 1;'), ('tc', 'tc/TC/caitree/PROC.PAS', 161, 'x1', 'x1 - 1', 'x1 := x1 - 1;'), ('tc', 'tc/TC/caitree/PROC.PAS', 162, 'y1', 'y1 - 1', 'y1 := y1 - 1;'), ('tc', 'tc/TC/caitree/PROC.PAS', 168, 'x1', 'x1 - 1', 'x1 := x1 - 1;'), ('tc', 'tc/TC/caitree/PROC.PAS', 169, 'y1', 'y1 + 1', 'y1 := y1 + 1;'), ('tc', 'tc/TC/caitree/PROC.PAS', 178, 'x1', 'x1 + 1', 'x1 := x1 + 1; y1 := y1 - 1;'), ('tc', 'tc/TC/caitree/PROC.PAS', 184, 'x1', 'x1 + 1', 'x1 := x1 + 1;'), ('tc', 'tc/TC/caitree/PROC.PAS', 185, 'y1', 'y1 + 1', 'y1 := y1 + 1;'), ('tc', 'tc/TC/caitree/PROC.PAS', 228, 'a', 'a - 1', 'a := a - 1; b := b - 1;'), ('tc', 'tc/TC/caitree/PROC.PAS', 237, 'a', 'a - 1', 'a := a - 1; b := b + 1;'), ('tc', 'tc/TC/tp/caitree/PROC.PAS', 161, 'x1', 'x1 - 1', 'x1 := x1 - 1;'), ('tc', 'tc/TC/tp/caitree/PROC.PAS', 162, 'y1', 'y1 - 1', 'y1 := y1 - 1;'), ('tc', 'tc/TC/tp/caitree/PROC.PAS', 168, 'x1', 'x1 - 1', 'x1 := x1 - 1;'), ('tc', 'tc/TC/tp/caitree/PROC.PAS', 169, 'y1', 'y1 + 1', 'y1 := y1 + 1;'), ('tc', 'tc/TC/tp/caitree/PROC.PAS', 178, 'x1', 'x1 + 1', 'x1 := x1 + 1; y1 := y1 - 1;'), ('tc', 'tc/TC/tp/caitree/PROC.PAS', 184, 'x1', 'x1 + 1', 'x1 := x1 + 1;'), ('tc', 'tc/TC/tp/caitree/PROC.PAS', 185, 'y1', 'y1 + 1', 'y1 := y1 + 1;'), ('tc', 'tc/TC/tp/caitree/PROC.PAS', 228, 'a', 'a - 1', 'a := a - 1; b := b - 1;'), ('tc', 'tc/TC/tp/caitree/PROC.PAS', 237, 'a', 'a - 1', 'a := a - 1; b := b + 1;'), ('tc', 'tc/TC/caibinary/TESTNEW.PAS', 99, 'x1', 'x1 + 22', 'x1 := x1 + 22;'), ('tc', 'tc/TC/caibinary/TESTNEW.PAS', 101, 'y1', 'y1+22', 'y1 := y1+22;'), ('tc', 'tc/TC/caibinary/TESTNEW.PAS', 178, 'Now', 'Now-1', 'Now := Now-1;'), ('tc', 'tc/TC/caitree/TESTNEW.PAS', 99, 'x1', 'x1 + 22', 'x1 := x1 + 22;'), ('tc', 'tc/TC/caitree/TESTNEW.PAS', 101, 'y1', 'y1+22', 'y1 := y1+22;'), ('tc', 'tc/TC/caitree/TESTNEW.PAS', 178, 'Now', 'Now-1', 'Now := Now-1;'), ('tc', 'tc/TC/tp/caitree/TESTNEW.PAS', 99, 'x1', 'x1 + 22', 'x1 := x1 + 22;'), ('tc', 'tc/TC/tp/caitree/TESTNEW.PAS', 101, 'y1', 'y1+22', 'y1 := y1+22;'), ('tc', 'tc/TC/tp/caitree/TESTNEW.PAS', 178, 'Now', 'Now-1', 'Now := Now-1;'), ('tc', 'tc/TC/tp/EXAMPLES/TVFM/TOOLS.PAS', 320, 's', "s + TwoDigit(t.Month, False) + '-' + TwoDigit(t.Day, True)", "s := s + TwoDigit(t.Month, False) + '-' + TwoDigit(t.Day, True);"), ('tc', 'tc/TC/tp/EXAMPLES/TVFM/TOOLS.PAS', 321, 's', "s + '-' + Copy(FourDigit(t.Year),3,2)", "s := s + '-' + Copy(FourDigit(t.Year),3,2);"), ('tc', 'tc/TC/tp/EXAMPLES/TVFM/TOOLS.PAS', 370, 'Name', 'Name + E', 'Name := Name + E;'), ('tc', 'tc/TC/tp/EXAMPLES/TVFM/TOOLS.PAS', 394, 'Params', "Params + ' ' + FileName", "Params := Params + ' ' + FileName;"), ('tc', 'tc/TC/tp/EXAMPLES/TVFM/TOOLS.PAS', 441, 'Params', "'/c ' + FileName + Params", "Params := '/c ' + FileName + Params;"), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', 64, 'next', 'p->next', 'next = p->next;'), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', 211, 'cursor', 'cursor->next', 'cursor = cursor->next;'), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', 240, 'current', 'current->next', 'current = current->next;'), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', 257, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', 271, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', 286, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', 337, 'cursor', 'cursor->next', 'cursor = cursor->next;'), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', 376, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', 68, 'next', 'p->next', 'next = p->next;'), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', 201, 'cursor', 'cursor->next', 'cursor = cursor->next;'), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', 224, 'current', 'current->next', 'current = current->next;'), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', 241, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', 255, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', 270, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', 318, 'cursor', 'cursor->next', 'cursor = cursor->next;'), ('tc', 'tc/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', 355, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 64, 'next', 'p->next', 'next = p->next;'), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 211, 'cursor', 'cursor->next', 'cursor = cursor->next;'), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 240, 'current', 'current->next', 'current = current->next;'), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 257, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 271, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 286, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 337, 'cursor', 'cursor->next', 'cursor = cursor->next;'), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 376, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/LISTIMP.H', 68, 'next', 'p->next', 'next = p->next;'), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/LISTIMP.H', 201, 'cursor', 'cursor->next', 'cursor = cursor->next;'), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/LISTIMP.H', 224, 'current', 'current->next', 'current = current->next;'), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/LISTIMP.H', 241, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/LISTIMP.H', 255, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/LISTIMP.H', 270, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/LISTIMP.H', 318, 'cursor', 'cursor->next', 'cursor = cursor->next;'), ('tc', 'tc/Project/Roof/TC/CLASSLIB/INCLUDE/LISTIMP.H', 355, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/DLISTIMP.H', 64, 'next', 'p->next', 'next = p->next;'), ('tc', 'tc/TC/DLISTIMP.H', 211, 'cursor', 'cursor->next', 'cursor = cursor->next;'), ('tc', 'tc/TC/DLISTIMP.H', 240, 'current', 'current->next', 'current = current->next;'), ('tc', 'tc/TC/DLISTIMP.H', 257, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/DLISTIMP.H', 271, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/DLISTIMP.H', 286, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/DLISTIMP.H', 337, 'cursor', 'cursor->next', 'cursor = cursor->next;'), ('tc', 'tc/TC/DLISTIMP.H', 376, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/LISTIMP.H', 68, 'next', 'p->next', 'next = p->next;'), ('tc', 'tc/TC/LISTIMP.H', 201, 'cursor', 'cursor->next', 'cursor = cursor->next;'), ('tc', 'tc/TC/LISTIMP.H', 224, 'current', 'current->next', 'current = current->next;'), ('tc', 'tc/TC/LISTIMP.H', 241, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/LISTIMP.H', 255, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/LISTIMP.H', 270, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/LISTIMP.H', 318, 'cursor', 'cursor->next', 'cursor = cursor->next;'), ('tc', 'tc/TC/LISTIMP.H', 355, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', 64, 'next', 'p->next', 'next = p->next;'), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', 211, 'cursor', 'cursor->next', 'cursor = cursor->next;'), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', 240, 'current', 'current->next', 'current = current->next;'), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', 257, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', 271, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', 286, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', 337, 'cursor', 'cursor->next', 'cursor = cursor->next;'), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/DLISTIMP.H', 376, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', 68, 'next', 'p->next', 'next = p->next;'), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', 201, 'cursor', 'cursor->next', 'cursor = cursor->next;'), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', 224, 'current', 'current->next', 'current = current->next;'), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', 241, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', 255, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', 270, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', 318, 'cursor', 'cursor->next', 'cursor = cursor->next;'), ('tc', 'tc/TC/Project/Children/TC3/CLASSLIB/INCLUDE/LISTIMP.H', 355, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 64, 'next', 'p->next', 'next = p->next;'), ('tc', 'tc/TC/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 211, 'cursor', 'cursor->next', 'cursor = cursor->next;'), ('tc', 'tc/TC/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 240, 'current', 'current->next', 'current = current->next;'), ('tc', 'tc/TC/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 257, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 271, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 286, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 337, 'cursor', 'cursor->next', 'cursor = cursor->next;'), ('tc', 'tc/TC/Project/Roof/TC/CLASSLIB/INCLUDE/DLISTIMP.H', 376, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/Project/Roof/TC/CLASSLIB/INCLUDE/LISTIMP.H', 68, 'next', 'p->next', 'next = p->next;'), ('tc', 'tc/TC/Project/Roof/TC/CLASSLIB/INCLUDE/LISTIMP.H', 201, 'cursor', 'cursor->next', 'cursor = cursor->next;'), ('tc', 'tc/TC/Project/Roof/TC/CLASSLIB/INCLUDE/LISTIMP.H', 224, 'current', 'current->next', 'current = current->next;'), ('tc', 'tc/TC/Project/Roof/TC/CLASSLIB/INCLUDE/LISTIMP.H', 241, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/Project/Roof/TC/CLASSLIB/INCLUDE/LISTIMP.H', 255, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/Project/Roof/TC/CLASSLIB/INCLUDE/LISTIMP.H', 270, 'cur', 'cur->next', 'cur = cur->next;'), ('tc', 'tc/TC/Project/Roof/TC/CLASSLIB/INCLUDE/LISTIMP.H', 318, 'cursor', 'cursor->next', 'cursor = cursor->next;')]
        state={'row':None,'ok':False,'a':None,'bb':None}
        box=self.card(b,'1 • SOURCE CANDIDATES')
        tr=ttk.Treeview(box,columns=('a','f','n','x','rhs'),show='headings',height=10)
        for c,t,w in [('a','Archive',75),('f','Source',330),('n','Line',55),('x','State',90),('rhs','RHS',390)]:
            tr.heading(c,text=t);tr.column(c,width=w)
        tr.pack(fill='both',expand=True,padx=12,pady=8)
        for a,f,n,x,rhs,line in data:tr.insert('','end',values=(a,f,n,x,rhs))
        nb=ttk.Notebook(b);nb.pack(fill='both',expand=True,padx=28,pady=10)
        e=tk.Frame(nb,bg='white');p=tk.Frame(nb,bg='white');q=tk.Frame(nb,bg='white')
        nb.add(e,text='Verification');nb.add(p,text='Symbolic Proof');nb.add(q,text='Simulation')
        et=tk.Text(e,height=24,font=('Consolas',10),wrap='word');et.pack(fill='both',expand=True,padx=12,pady=10)
        pt=tk.Text(p,height=24,font=('Consolas',10),wrap='word');pt.pack(fill='both',expand=True,padx=12,pady=10)
        cv=tk.Canvas(q,height=430,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1);cv.pack(fill='both',expand=True,padx=12,pady=10)
        msg=tk.StringVar(value='เลือก source candidate')
        tk.Label(b,textvariable=msg,bg=BG,fg=MUTED).pack(anchor='w',padx=30,pady=8)
        def spath(a,f):
            return Path(__file__).resolve().parent / ('caimath_sources' if a=='caimath' else 'tc_sources') / Path(f)
        def ctx(a,f,n):
            try:
                z=spath(a,f).read_bytes().decode('utf-8',errors='ignore').splitlines()
                lo=max(0,n-10);hi=min(len(z),n+5)
                return [(i+1,z[i]) for i in range(lo,hi)]
            except Exception:return []
        def affine(x,rhs):
            z=re.sub(r'\s+','',rhs); X=re.escape(x); num=r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)'
            m=re.match(r'^('+num+r')\*'+X+r'([+-](?:\d+(?:\.\d*)?|\.\d+))?$',z)
            if m:return float(m.group(1)),float(m.group(2) or 0)
            m=re.match(r'^'+X+r'\*('+num+r')([+-](?:\d+(?:\.\d*)?|\.\d+))?$',z)
            if m:return float(m.group(1)),float(m.group(2) or 0)
            m=re.match(r'^'+X+r'([+-](?:\d+(?:\.\d*)?|\.\d+))?$',z)
            if m:return 1.0,float(m.group(1) or 0)
            m=re.match(r'^('+num+r')\+('+num+r')\*'+X+r'$',z)
            if m:return float(m.group(2)),float(m.group(1))
            return None
        def choose(_=None):
            z=tr.selection()
            if z:
                v=tr.item(z[0],'values')
                state['row']=next((r for r in data if r[0]==v[0] and r[1]==v[1] and int(r[2])==int(v[2]) and r[3]==v[3]),None)
                state['ok']=False
        def verify():
            r=state['row']
            if not r:return
            a,f,n,x,rhs,line=r;c=ctx(a,f,int(n))
            before='\n'.join(t.lower() for no,t in c if no<=int(n))
            loop=bool(re.search(r'\b(for|while|repeat)\b',before)); ab=affine(x,rhs)
            et.delete('1.0','end');et.insert('end',f'SOURCE: {a}/{f}\nLINE {n}: {line}\n\nCONTEXT\n')
            for no,t in c:et.insert('end',f'{no:04d}  {t}\n')
            et.insert('end',f'\nSelf-dependency: YES\nLoop/update evidence: {"YES" if loop else "NOT ESTABLISHED"}\nAffine x=a*x+b: {"YES" if ab else "NOT PARSED"}\n')
            state['ok']=bool(loop and ab)
            if ab:state['a'],state['bb']=ab
            if state['ok']:
                et.insert('end',f'\nVERIFIED TEACHING MODEL: {x}ₙ₊₁ = {ab[0]:.8g}{x}ₙ + {ab[1]:.8g}\n')
                msg.set('Verified. Symbolic proof is now allowed.')
            else:
                et.insert('end','\nSTOP: insufficient evidence for automatic recurrence proof.\n')
                msg.set('Not verified; proof remains blocked.')
            nb.select(e)
        def prove():
            if not state['ok']:msg.set('Proof blocked until source verification succeeds.');return
            a=float(state['a']);bb=float(state['bb']);pt.delete('1.0','end')
            pt.insert('end',f'MODEL: xₙ₊₁={a:.8g}xₙ+{bb:.8g}\n\n')
            if abs(a-1)>1e-10:
                L=bb/(1-a)
                pt.insert('end','Let L=aL+b, so L=b/(1-a).\nLet yₙ=xₙ-L. Then yₙ₊₁=a yₙ, hence yₙ=aⁿy₀.\n')
                pt.insert('end','Therefore xₙ=L+aⁿ(x₀-L).\n\nINDUCTION\n')
                pt.insert('end','n=0: L+a⁰(x₀-L)=x₀. ✓\n')
                pt.insert('end','Assume xₖ=L+aᵏ(x₀-L). Then xₖ₊₁=axₖ+b=(aL+b)+aᵏ⁺¹(x₀-L)=L+aᵏ⁺¹(x₀-L). ✓\n\n')
                if abs(a)<1:pt.insert('end',f'|a|<1 ⇒ aⁿ→0 ⇒ xₙ→L={L:.8g}.\n')
                elif abs(a)>1:pt.insert('end','|a|>1 ⇒ generally divergent; x₀=L is the constant exception.\n')
                else:pt.insert('end','a=-1 ⇒ generally oscillatory; x₀=L is the constant exception.\n')
            else:
                pt.insert('end','a=1 ⇒ xₙ₊₁=xₙ+b ⇒ xₙ=x₀+nb.\nInduction: xₖ₊₁=(x₀+kb)+b=x₀+(k+1)b. ✓\n')
            msg.set('Symbolic proof completed.');nb.select(p)
        def simulate():
            if not state['ok']:msg.set('Simulation blocked until verification succeeds.');return
            a=float(state['a']);bb=float(state['bb']);N=25;x0=0.0;xs=[x0]
            for _ in range(N):xs.append(a*xs[-1]+bb)
            if abs(a-1)>1e-10:
                L=bb/(1-a);cf=[L+a**n*(x0-L) for n in range(N+1)]
            else:cf=[x0+n*bb for n in range(N+1)]
            err=max(abs(u-v) for u,v in zip(xs,cf));cv.delete('all')
            w=max(cv.winfo_width(),800);h=max(cv.winfo_height(),400);pad=55;vals=xs+cf;mn=min(vals);mx=max(vals)
            if abs(mx-mn)<1e-12:mx=mn+1
            def xy(i,y):return pad+i*(w-2*pad)/N,h-pad-(y-mn)/(mx-mn)*(h-2*pad)
            pts=[]
            for i,y in enumerate(xs):pts.extend(xy(i,y))
            cv.create_line(*pts,fill=BLUE,width=3)
            for i,y in enumerate(cf):
                xx,yy=xy(i,y);cv.create_oval(xx-3,yy-3,xx+3,yy+3,outline=ORANGE,width=2)
            cv.create_text(pad,20,anchor='w',text='Blue: iteration • Orange: closed form',fill=TEXT)
            cv.create_text(pad,42,anchor='w',text=f'max discrepancy={err:.3e}',fill=MUTED,font=('Consolas',9))
            msg.set(f'Numerical verification complete; max discrepancy={err:.3e}. Simulation is not the proof.');nb.select(q)
        tr.bind('<<TreeviewSelect>>',choose)
        a=tk.Frame(box,bg='white');a.pack(fill='x',padx=12,pady=(0,10))
        ttk.Button(a,text='1 ▶ VERIFY SOURCE',style='Primary.TButton',command=verify).pack(side='left')
        ttk.Button(a,text='2 ▶ SYMBOLIC PROOF',command=prove).pack(side='left',padx=5)
        ttk.Button(a,text='3 ▶ SIMULATION',command=simulate).pack(side='left')
        ttk.Button(a,text='V4.4 Proof Lab',command=self.v44_symbolic_proof_simulation_lab).pack(side='left',padx=5)
        self.card(b,'V4.5 RULE','Automatic proof is deliberately narrow: source evidence + repeated-update evidence + affine form. Unsupported expressions are not forced into a recurrence model.')

    def v46_math_model_classifier_lab(self):
        self.clear()
        self.header('🧭 V4.6 • Mathematical Model Classifier',
            'Evidence-based classification first; derivation/proof method depends on the mathematical class')
        b=self.scrollbody()
        self.card(b,'WHY V4.6',
            'Source หนึ่งไฟล์อาจมีคณิตศาสตร์มากกว่าหนึ่งชนิด จึงไม่บังคับให้ทุกอย่างเป็น recurrence. '
            'ระบบให้คะแนนจากหลักฐานใน expression/source แล้วแสดง Primary class + supporting classes. '
            'จากนั้นใช้ derivation ที่เหมาะกับ Algebra, Geometry, Trigonometry, Probability, Statistics หรือ Sequence/Recurrence.')

        # Reuse the grounded V4.2 catalog packaged with the Studio.
        catalog_path=Path(__file__).resolve().parent/'V42_EXPRESSION_CATALOG.json'
        try:
            raw=json.loads(catalog_path.read_text(encoding='utf-8'))
        except Exception:
            raw=[]

        def classify(rec):
            text=' '.join([e.get('rhs','')+' '+e.get('source','') for e in rec.get('expressions',[])]).lower()
            vars_=[v.lower() for v in rec.get('variables',[])]
            scores={'Algebra':0,'Geometry':0,'Trigonometry':0,'Probability':0,'Statistics':0,'Sequence / Recurrence':0}
            if re.search(r'[+\-*/]',text): scores['Algebra']+=2
            if any(k in text for k in ['sqrt(','pow(','circle(','line(','ellipse(','putpixel']): scores['Geometry']+=4
            if any(k in text for k in ['sin(','cos(','tan(']): scores['Trigonometry']+=6
            if any(k in text for k in ['random(','rand(']): scores['Probability']+=6
            if any(k in text for k in ['sum','mean','avg','average','count','frequency']): scores['Statistics']+=4
            # recurrence requires direct self-dependency evidence in an extracted assignment
            for e in rec.get('expressions',[]):
                lhs=re.sub(r'\[.*?\]','',e.get('lhs','')).strip()
                if lhs and re.search(r'\b'+re.escape(lhs)+r'\b',e.get('rhs','')):
                    scores['Sequence / Recurrence']+=6
            ranked=sorted(scores.items(),key=lambda z:(-z[1],z[0]))
            positive=[x for x in ranked if x[1]>0]
            return scores,(positive[0][0] if positive else 'Algebra'),positive

        box=self.card(b,'1 • CLASSIFY GROUNDED SOURCE')
        tree=ttk.Treeview(box,columns=('archive','file','primary','support'),show='headings',height=13)
        for c,t,w in [('archive','Archive',80),('file','Source',350),('primary','Primary math class',190),('support','Supporting evidence/classes',460)]:
            tree.heading(c,text=t);tree.column(c,width=w)
        tree.pack(fill='both',expand=True,padx=12,pady=8)
        rows=[]
        for rec in raw[:250]:
            scores,primary,positive=classify(rec)
            support=', '.join(f'{k}:{v}' for k,v in positive[:4])
            rows.append((rec,primary,positive))
            tree.insert('','end',values=(rec.get('archive',''),rec.get('file',''),primary,support))

        nb=ttk.Notebook(b);nb.pack(fill='both',expand=True,padx=28,pady=10)
        evidence=tk.Frame(nb,bg='white');mathp=tk.Frame(nb,bg='white');method=tk.Frame(nb,bg='white')
        nb.add(evidence,text='Evidence');nb.add(mathp,text='Mathematical Model');nb.add(method,text='Correct Method')
        et=tk.Text(evidence,height=23,font=('Consolas',10),wrap='word');et.pack(fill='both',expand=True,padx=12,pady=10)
        mt=tk.Text(mathp,height=23,font=('Consolas',10),wrap='word');mt.pack(fill='both',expand=True,padx=12,pady=10)
        ct=tk.Text(method,height=23,font=('Consolas',10),wrap='word');ct.pack(fill='both',expand=True,padx=12,pady=10)

        def explain(primary):
            if primary=='Trigonometry':
                return ('MODEL\n  Trigonometric function / coordinate relation\n\n'
                        'REFERENCE IDENTITIES\n  sin²θ+cos²θ=1\n  x=r cosθ, y=r sinθ\n\n'
                        'METHOD\n  Derive from definitions/identities; verify numerically or geometrically afterward.')
            if primary=='Geometry':
                return ('MODEL\n  Coordinate / metric geometry\n\n'
                        'REFERENCE\n  d=√((x₂-x₁)²+(y₂-y₁)²)\n\n'
                        'METHOD\n  Identify coordinates and geometric invariants; derive with Pythagorean/analytic geometry.')
            if primary=='Probability':
                return ('MODEL\n  Random experiment and random variable\n\n'
                        'REFERENCE\n  P-hat(A)=count(A)/N\n  E[X]=ΣxP(X=x) for discrete X\n\n'
                        'METHOD\n  Define sample space/event/distribution first; Monte Carlo estimates do not replace probability theory.')
            if primary=='Statistics':
                return ('MODEL\n  Observed sample x₁,…,xₙ\n\n'
                        'REFERENCE\n  x̄=(1/n)Σxᵢ\n  population-style variance=(1/n)Σ(xᵢ-x̄)²\n\n'
                        'METHOD\n  State whether data are population/sample and distinguish descriptive statistics from probability claims.')
            if primary=='Sequence / Recurrence':
                return ('MODEL\n  State sequence xₙ\n\n'
                        'REFERENCE\n  xₙ₊₁=F(xₙ) only when repeated state-update semantics are established.\n\n'
                        'METHOD\n  Verify update context → derive recurrence → symbolic proof/induction → simulation.')
            return ('MODEL\n  Algebraic relation y=f(x₁,…,xₖ)\n\n'
                    'METHOD\n  Normalize expression, state domain/constraints, simplify or solve by valid algebraic transformations; '
                    'do not infer recurrence or probability without extra evidence.')

        def pick(_=None):
            q=tree.selection()
            if not q:return
            vals=tree.item(q[0],'values');arc,fn=vals[0],vals[1]
            item=next((z for z in rows if z[0].get('archive','')==arc and z[0].get('file','')==fn),None)
            if not item:return
            rec,primary,positive=item
            et.delete('1.0','end');mt.delete('1.0','end');ct.delete('1.0','end')
            et.insert('end',f'SOURCE: {arc}/{fn}\n\nVARIABLES\n  '+', '.join(rec.get('variables',[])[:20])+'\n\nEXTRACTED EXPRESSIONS\n')
            for e in rec.get('expressions',[])[:10]:
                et.insert('end',f'  L{e.get("line")}: {e.get("lhs")} = {e.get("rhs")}\n')
            et.insert('end','\nCLASS SCORES\n')
            for k,v in positive:et.insert('end',f'  {k}: {v}\n')
            mt.insert('end',f'PRIMARY CLASS: {primary}\n\n'+explain(primary))
            ct.insert('end','CORRECTNESS POLICY\n\n')
            ct.insert('end','• Classification is evidence-based and may have multiple supporting classes.\n')
            ct.insert('end','• A high score is not a mathematical proof of the original author’s intent.\n')
            ct.insert('end','• Algebra uses algebraic derivation; geometry uses geometric relations; trigonometry uses identities/definitions.\n')
            ct.insert('end','• Probability requires a defined random experiment; statistics requires defined observations/sample interpretation.\n')
            ct.insert('end','• Recurrence requires repeated state-update semantics before induction/closed-form analysis.\n')
            ct.insert('end','• Simulation comes after the mathematical model and does not replace proof.')
            nb.select(mathp)
        tree.bind('<<TreeviewSelect>>',pick)

        actions=tk.Frame(box,bg='white');actions.pack(fill='x',padx=12,pady=(0,10))
        ttk.Button(actions,text='V4.5 Source → Proof',command=self.v45_source_to_proof_lab).pack(side='left')
        ttk.Button(actions,text='V4.4 Symbolic Proof',command=self.v44_symbolic_proof_simulation_lab).pack(side='left',padx=5)

        self.card(b,'MENU IMPROVEMENT',
            'V4.6 เปลี่ยน navigation ด้านซ้ายเป็น scrollable sidebar เพื่อให้เมนูรุ่นเก่าและรุ่นใหม่ทั้งหมดเข้าถึงได้ '
            'โดยไม่ต้องลบหรือซ่อนบทเรียนเดิม. ใช้ mouse wheel หรือ scrollbar เพื่อเลื่อนรายการ.')

    def v47_math_knowledge_map_lab(self):
        self.clear()
        self.header('🗺 V4.7 • Mathematical Knowledge Map',
            'Concept → prerequisite → definition/formula → source evidence → correct derivation/proof → simulation')
        b=self.scrollbody()
        self.card(b,'LEARNING PRINCIPLE',
            'V4.7 จัดความรู้เป็นลำดับก่อน-หลัง ไม่เริ่มจาก code อย่างเดียว: ผู้เรียนเลือกแนวคิดคณิตศาสตร์ก่อน '
            'แล้วดูนิยาม/สมการ ความรู้พื้นฐานที่ต้องมี หลักฐานจาก C/Pascal และวิธีพิสูจน์หรือทดลองที่เหมาะสม.')

        knowledge={
          'Algebra':[
            ('Variable & Expression','Arithmetic','y=f(x)','ตัวแปรแทนค่าที่เปลี่ยนได้; expression สร้างค่าจากตัวแปรและตัวดำเนินการ.','algebra'),
            ('Equation','Variable & Expression','LHS = RHS','สมการเป็นข้อความว่าปริมาณสองด้านเท่ากันภายใต้เงื่อนไขที่กำหนด.','algebra'),
            ('Function','Variable & Expression','y=f(x)','ฟังก์ชันกำหนด output หนึ่งค่าต่อ input แต่ละค่าภายใน domain.','algebra')],
          'Geometry':[
            ('Coordinate Point','Algebra','P=(x,y)','ตำแหน่งบนระนาบคาร์ทีเซียนแทนด้วยคู่อันดับ.','geometry'),
            ('Distance','Coordinate Point','d=√((x₂-x₁)²+(y₂-y₁)²)','ระยะยุคลิดได้จากทฤษฎีพีทาโกรัส.','geometry'),
            ('Circle','Distance','(x-h)²+(y-k)²=r²','จุดบนวงกลมอยู่ห่างจากศูนย์กลางเป็นระยะ r คงที่.','geometry')],
          'Trigonometry':[
            ('Sine / Cosine','Circle','sin²θ+cos²θ=1','อัตราส่วนตรีโกณมิติและพิกัดบน unit circle.','trig'),
            ('Parametric Circle','Sine / Cosine','x=r cosθ,  y=r sinθ','ใช้ parameter θ สร้างพิกัดจุดบนวงกลม.','trig')],
          'Probability':[
            ('Random Experiment','Set / Event','0≤P(A)≤1','การทดลองสุ่มต้องกำหนดผลลัพธ์และ event ก่อนคำนวณ probability.','probability'),
            ('Empirical Probability','Random Experiment','P̂(A)=count(A)/N','ความถี่สัมพัทธ์จากการทดลอง N ครั้งเป็นค่าประมาณ probability.','probability'),
            ('Random Variable','Random Experiment','X: Ω→ℝ','random variable เป็นฟังก์ชันจากผลลัพธ์สุ่มไปยังจำนวนจริง.','probability')],
          'Statistics':[
            ('Sample Mean','Observed Data','x̄=(1/n)Σxᵢ','ค่าเฉลี่ยสรุปตำแหน่งกึ่งกลางของข้อมูลตัวเลข.','statistics'),
            ('Variance','Sample Mean','σ²=(1/n)Σ(xᵢ-μ)²','variance วัดการกระจายรอบ mean; ต้องระบุว่าใช้ population หรือ sample convention.','statistics'),
            ('Standard Deviation','Variance','σ=√σ²','standard deviation อยู่ในหน่วยเดียวกับตัวแปรเดิม.','statistics')],
          'Sequence / Recurrence':[
            ('Sequence','Function','x₀,x₁,x₂,…','ลำดับคือฟังก์ชันที่มีดัชนีจำนวนเต็มไม่ลบเป็น input.','recurrence'),
            ('Recurrence Relation','Sequence','xₙ₊₁=F(xₙ)','recurrence กำหนดพจน์ถัดไปจากพจน์ก่อนหน้าและต้องมี initial condition.','recurrence'),
            ('Affine Recurrence','Recurrence Relation','xₙ₊₁=axₙ+b','กรณีอันดับหนึ่งแบบ affine ที่ V4.4–V4.5 มี symbolic proof engine.','recurrence'),
            ('Closed Form','Affine Recurrence','xₙ=L+aⁿ(x₀-L), L=b/(1-a)','สำหรับ a≠1; กรณี a=1 ต้องใช้ xₙ=x₀+nb แยกต่างหาก.','recurrence'),
            ('Convergence','Closed Form','|a|<1 ⇒ xₙ→L','สรุปจาก closed form; simulation ไม่ใช่ proof.','recurrence')]
        }

        # Ground source evidence in the V4.2 catalog.
        try:
            catalog=json.loads((Path(__file__).resolve().parent/'V42_EXPRESSION_CATALOG.json').read_text(encoding='utf-8'))
        except Exception:
            catalog=[]

        top=tk.Frame(b,bg=BG);top.pack(fill='both',expand=True,padx=28,pady=8)
        left=self.card(top,'2 • KNOWLEDGE TREE');left.pack(side='left',fill='y',padx=(0,8))
        kt=ttk.Treeview(left,show='tree',height=24)
        kt.pack(fill='both',expand=True,padx=10,pady=10)
        node_info={}
        for cat,items in knowledge.items():
            pid=kt.insert('','end',text=cat,open=True)
            for title,pre,formula,definition,kind in items:
                iid=kt.insert(pid,'end',text=title)
                node_info[iid]=(cat,title,pre,formula,definition,kind)

        right=tk.Frame(top,bg=BG);right.pack(side='left',fill='both',expand=True)
        nb=ttk.Notebook(right);nb.pack(fill='both',expand=True)
        concept=tk.Frame(nb,bg='white');source=tk.Frame(nb,bg='white');path=tk.Frame(nb,bg='white')
        nb.add(concept,text='Concept + Formula');nb.add(source,text='Source Evidence');nb.add(path,text='Learning Path')
        ct=tk.Text(concept,height=25,font=('Consolas',10),wrap='word');ct.pack(fill='both',expand=True,padx=12,pady=10)
        st=tk.Text(source,height=25,font=('Consolas',10),wrap='word');st.pack(fill='both',expand=True,padx=12,pady=10)
        pc=tk.Canvas(path,height=450,bg='#fbfdff',highlightbackground=BORDER,highlightthickness=1);pc.pack(fill='both',expand=True,padx=12,pady=10)

        def evidence(kind):
            found=[]
            for rec in catalog:
                txt=' '.join(e.get('rhs','')+' '+e.get('source','') for e in rec.get('expressions',[])).lower()
                ok=False
                if kind=='trig':ok=any(k in txt for k in ['sin(','cos(','tan('])
                elif kind=='geometry':ok=any(k in txt for k in ['sqrt(','pow(','circle(','ellipse(','line(','putpixel'])
                elif kind=='probability':ok=any(k in txt for k in ['random(','rand('])
                elif kind=='statistics':ok=any(k in txt for k in ['sum','mean','avg','count','frequency'])
                elif kind=='recurrence':
                    for e in rec.get('expressions',[]):
                        lhs=re.sub(r'\[.*?\]','',e.get('lhs','')).strip()
                        if lhs and re.search(r'\b'+re.escape(lhs)+r'\b',e.get('rhs','')):ok=True;break
                elif kind=='algebra':ok=bool(re.search(r'[+\-*/]',txt))
                if ok:
                    found.append(rec)
                    if len(found)>=5:break
            return found

        def draw_path(pre,title):
            pc.delete('all');w=max(pc.winfo_width(),760);y=120
            steps=[pre,title,'Source Evidence','Derivation / Proof','Simulation / Visualization']
            xs=[70+i*(w-140)/(len(steps)-1) for i in range(len(steps))]
            for i in range(len(xs)-1):
                pc.create_line(xs[i]+45,y,xs[i+1]-45,y,fill='#94a3b8',width=3,arrow='last')
            for x,t in zip(xs,steps):
                pc.create_rectangle(x-58,y-30,x+58,y+30,fill='#e0f2fe',outline=BLUE,width=2)
                pc.create_text(x,y,text=t,width=105,fill=TEXT,font=('Segoe UI',9))
            pc.create_text(30,35,anchor='w',text='Mathematics first: prerequisite → concept → evidence → proof/derivation → experiment',
                           fill=TEXT,font=('Segoe UI Semibold',10))

        def choose(_=None):
            q=kt.selection()
            if not q or q[0] not in node_info:return
            cat,title,pre,formula,definition,kind=node_info[q[0]]
            ct.delete('1.0','end');st.delete('1.0','end')
            ct.insert('end',f'CATEGORY: {cat}\nCONCEPT: {title}\n\nPREREQUISITE\n  {pre}\n\nDEFINITION\n  {definition}\n\nFORMULA / MODEL\n  {formula}\n\n')
            if kind=='recurrence':
                ct.insert('end','CORRECT METHOD\n  Verify repeated state update → define initial condition → derive model → prove symbolically → simulate.\n')
            elif kind=='probability':
                ct.insert('end','CORRECT METHOD\n  Define sample space/event/random variable first → derive probability model → estimate by simulation only afterward.\n')
            elif kind=='statistics':
                ct.insert('end','CORRECT METHOD\n  Define observations and population/sample interpretation → compute statistic → interpret without turning it into an unsupported probability claim.\n')
            else:
                ct.insert('end','CORRECT METHOD\n  State definitions/domain → derive with valid identities/algebra/geometry → use graph or numerical experiment afterward.\n')
            ev=evidence(kind)
            st.insert('end','SOURCE EVIDENCE FROM THE PACKAGED C/PASCAL CATALOG\n\n')
            if not ev:
                st.insert('end','No matching evidence was found in the current catalog. V4.7 does not invent a source link.\n')
            for rec in ev:
                st.insert('end',f'[{rec.get("archive","")}] {rec.get("file","")}\n')
                for e in rec.get('expressions',[])[:3]:
                    st.insert('end',f'  L{e.get("line")}: {e.get("lhs")} = {e.get("rhs")}\n')
                st.insert('end','\n')
            draw_path(pre,title)
            nb.select(concept)
        kt.bind('<<TreeviewSelect>>',choose)

        actions=self.card(b,'3 • CONNECT TO EXISTING LABS')
        ttk.Button(actions,text='V4.6 Classifier',command=self.v46_math_model_classifier_lab).pack(side='left',padx=12,pady=10)
        ttk.Button(actions,text='V4.5 Source → Proof',command=self.v45_source_to_proof_lab).pack(side='left',padx=5,pady=10)
        ttk.Button(actions,text='V4.4 Symbolic Proof',command=self.v44_symbolic_proof_simulation_lab).pack(side='left',padx=5,pady=10)

        self.card(b,'V4.7 CORRECTNESS',
            'Knowledge Map distinguishes mathematical definitions/formulas from source evidence. '
            'A source match shows syntactic evidence only; it does not prove the original author intended that mathematical topic. '
            'Proof and simulation remain separate stages.')
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
