# AI Learning Studio

**AI Learning Studio** is an educational project that connects legacy Pascal/C source code, mathematics, visualization, Python, AI, webcam input, robot simulation, and hardware learning.

> Thai: โครงการเรียนรู้จากโค้ด → คณิตศาสตร์ → ภาพ/แอนิเมชัน → Python → AI → Webcam → Robot Simulator → Hardware

## Learning path

```text
TC / Pascal / C source
        ↓
Code Reading
        ↓
Mathematical Formula
        ↓
Graph & Animation
        ↓
Modern Python
        ↓
Exercises & Adaptive Learning
        ↓
Image AI / Webcam
        ↓
Decision + Safety Gate
        ↓
Robot Simulator
        ↓
Hardware Check
        ↓
Real Robot
```

## Main learning modules

- TC Math Museum and Visual Math Laboratory
- Automatic equation reading and Equation Atlas
- Parabola, Circle, Vector, Matrix and Derivative animations
- Four-panel learning: Source | Formula | Graph | Python
- Line-by-line lesson generation
- Student exercises and teacher dashboard
- Adaptive learning/remediation
- Image AI and webcam output mapping
- Robot Command Center
- Hardware-free robot simulator
- Webcam / Serial / COM hardware checks
- Accessibility-oriented visual learning materials

## Accessibility

The project is designed so that important learning information is available visually and as text. Sound is not required as the only communication channel. This is especially useful for learners who are deaf or hard of hearing and for classrooms without robotics hardware.

## Hardware-free mode

A physical robot is **not required**. Students can learn the complete AI decision loop using the computer Robot Simulator:

```text
AI Output → Decision → Safety → Command → Simulated Robot → Feedback
```

## Installation

Python development setup:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
python src/ai_learning_studio.py
```

Windows installer/build documentation will be kept under `installer/` and `docs/`.

## Legacy TC/Pascal/C material

This public repository does **not** redistribute legacy TC/Turbo Pascal/Turbo C files whose redistribution rights have not been verified. Users may import their own legally obtained Pascal/C source files into the learning tools.

This separation is intentional: the open-source application code can be developed publicly without assuming redistribution rights for third-party legacy material.

## Safety

Robot commands should be tested in the simulator first. A successful simulation does not prove that physical hardware is safe or correctly wired. Check power, motor direction, emergency-stop procedure, serial connection and speed limits before physical operation.

## Contributing

Teachers, students and developers are welcome to contribute lessons, visualizations, accessibility improvements, simulations and hardware adapters. See `CONTRIBUTING.md`.

## License

Project-owned source code and documentation in this repository are released under the MIT License unless a file states otherwise. Third-party source/data remain subject to their own licenses.
