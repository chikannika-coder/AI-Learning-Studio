AI Learning Studio v5.9 — Windows Edition
============================================

เป้าหมาย
- สร้าง AI_Learning_Studio_v59.exe แบบ standalone
- สร้าง AI_Learning_Studio_v59_Setup.exe
- Setup สร้าง Desktop shortcut และ Start Menu shortcut
- ผู้ใช้ปลายทางไม่ต้องติดตั้ง Python

วิธีสร้าง Setup.exe (ทำครั้งเดียวบน Windows)
1. แตก ZIP นี้
2. ดับเบิลคลิก BUILD_SETUP_EXE.bat
3. Script จะสร้าง virtual environment และติดตั้ง PyInstaller อัตโนมัติ
4. จะได้ dist\AI_Learning_Studio_v59.exe
5. ถ้ามี Inno Setup 6 จะสร้าง installer\AI_Learning_Studio_v59_Setup.exe ด้วย

หมายเหตุสำคัญ
- ChatGPT runtime ปัจจุบันไม่ใช่ Windows จึงไม่สามารถ compile Windows bootloader/Setup.exe จริงจากที่นี่ได้อย่างน่าเชื่อถือ
- ชุดนี้เตรียม source, PyInstaller spec และ Inno Setup script ให้พร้อม build บน Windows
- หากยังไม่ต้องการ build EXE สามารถใช้ INSTALL_AND_RUN.bat / RUN_AI_STUDIO.bat ที่แนบไว้ได้
- data\tc_learning.zip เป็น TC ฉบับย่อที่คัดเฉพาะไฟล์บทเรียนที่จำเป็น
