# AI Learning Studio v5.9

**Code → Math → Visualization → Python → AI → Robot**

AI Learning Studio is an open-source educational environment for learning mathematics, programming, artificial intelligence, computer vision, and robotics from one integrated Windows/Python application.

ภาษาไทย: โครงการนี้ออกแบบให้นักเรียนเรียนรู้จาก **โค้ด → สูตรคณิตศาสตร์ → กราฟ/แอนิเมชัน → Python → AI → Webcam → Robot Simulator → Hardware** โดยเน้นการเรียนรู้ด้วยภาพและข้อความ รวมถึงผู้เรียนที่หูหนวกหรือมีความบกพร่องทางการได้ยิน

## What students can learn

- TC/Pascal/C source-code reading and mathematical interpretation
- Circle, parabola, ellipse, trigonometry, vectors, matrices, statistics, probability and calculus
- Formula-to-graph and animated mathematics
- Source | Formula | Graph | Modern Python four-panel learning
- Automatic exercises, Teacher Mode and adaptive tutoring
- Image AI and webcam experiments
- AI decision → safety gate → robot command
- Robot Simulator / Digital Twin without physical hardware
- Webcam, Serial/COM and hardware checks

## Quick start on Windows

### Automatic setup
Run:

```text
INSTALL_AND_RUN.bat
```

The script creates a virtual environment, installs dependencies and launches AI Learning Studio.

### Manual Python setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python ai_learning_studio.py
```

Python 3.10+ is recommended.

## Windows executable / installer

Development files for PyInstaller and Inno Setup are included:

```text
BUILD_SETUP_EXE.bat
AI_Learning_Studio.spec
AI_Learning_Studio_v59.iss
launcher.py
```

Run `BUILD_SETUP_EXE.bat` on Windows to build the application. Inno Setup can then create the Windows installer when installed.

## Learning architecture

```text
Pascal / C / Math Source
          ↓
     Code Reader
          ↓
 Mathematical Formula
          ↓
 Graph + Animation
          ↓
   Modern Python
          ↓
 Exercise / Adaptive AI
          ↓
 Image AI / Webcam
          ↓
 AI Decision + Safety
          ↓
   Robot Simulator
          ↓
   Hardware Check
          ↓
     Real Robot
```

## Accessibility

Core learning information is presented visually and in text. Audio is not the only communication channel. The project is intended to support visual classroom instruction and learning activities for deaf and hard-of-hearing students as well as other learners.

This statement describes the project's design goal; it is not a claim of formal accessibility certification.

## Robot safety

Use the Robot Simulator before connecting physical hardware. Verify wiring, power supply, motor direction, serial port, speed limits and an emergency-stop procedure before real-world operation.

The current Robot Command Center is designed around a safety gate and simulation-first workflow. Hardware integrations should default to **STOP** when confidence or system state is uncertain.

## Legacy Turbo C / Turbo Pascal source

**Legacy TC/Turbo C/Turbo Pascal archives are not distributed in this public repository.**

Redistribution rights for legacy third-party source files may differ. Users should import only source files that they are legally permitted to use. The MIT License for this repository does not grant rights to unrelated third-party material.

## Repository hygiene

Python virtual environments (`.venv/`, `.buildvenv/`), build outputs, local ZIP archives and private legacy TC folders are intentionally excluded from version control. Recreate dependencies from `requirements.txt`.

## Contributing

Teachers, students and developers are welcome to contribute:

- new mathematics lessons and visualizations
- Python/AI learning activities
- accessibility improvements
- robot simulation environments
- safe hardware adapters
- Thai and English documentation

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.

## License

Project-owned source code and documentation are released under the [MIT License](LICENSE), unless a file states otherwise.

Third-party code, datasets and learning material remain subject to their respective licenses.

---

**AI Learning Studio v5.9 — Open learning from mathematics to AI and robotics.**
