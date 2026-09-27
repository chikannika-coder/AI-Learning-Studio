AI Learning Studio v5.9 - Windows Edition / Auto Install Package
================================================

วิธีติดตั้งครั้งแรก
1. แตกไฟล์ ZIP นี้ออกเป็นโฟลเดอร์
2. ดับเบิลคลิก INSTALL_AND_RUN.bat
3. ระบบจะสร้าง .venv และติดตั้ง SymPy, Pillow, OpenCV, pySerial อัตโนมัติ
4. เมื่อติดตั้งเสร็จ โปรแกรมจะเปิดเอง

ครั้งต่อไป
- ดับเบิลคลิก RUN_AI_STUDIO.bat ได้ทันที

ข้อมูล TC
- ใช้ไฟล์ data\tc_learning.zip
- เป็นชุดย่อที่คัดเฉพาะ source ที่เกี่ยวข้องกับบทเรียน
- จากต้นฉบับ tc(3).zip จำนวน 10,943 entries
- ชุดย่อนี้มี 21 source files
- เน้น Circle, Parabola, Ellipse, Sorting, Statistics/MCALC และ Tree
- ไม่รวมไฟล์ compiler, OBJ, BGI, CHR และ binary ที่ไม่จำเป็นต่อระบบการเรียนรู้

Hardware
- ไม่จำเป็นต้องมี hardware เพื่อใช้ Robot Simulator
- Webcam ต้องมี OpenCV และกล้องที่ระบบมองเห็น
- Robot จริงต้องผ่าน Hardware Check ก่อน
- v5.8 Command Center ยังไม่ส่ง motor bytes โดยตรง

ไฟล์หลัก
- ai_learning_studio.py
- requirements.txt
- INSTALL_AND_RUN.bat
- RUN_AI_STUDIO.bat
- data\tc_learning.zip
