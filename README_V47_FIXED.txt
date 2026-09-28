AI Learning Studio V4.7 FIXED

Problem investigated:
The Python GUI itself passes syntax and startup smoke testing, but the old Windows installer used `py -3`,
which can select the newest installed Python rather than the project's expected Python 3.10.
It also aborted installation if any optional package failed, even though the program already handles
SymPy, Pillow, OpenCV and pyserial as optional imports. Finally, pythonw hid startup tracebacks.

Fixes:
1. Installer prefers Python 3.10, then 3.11/3.12.
2. Checks Tkinter before creating the environment.
3. Optional dependency installation failure no longer prevents the core GUI from launching.
4. Added DIAGNOSE_AND_RUN.bat to run in a visible console and show exact tracebacks.
5. RUN_AI_STUDIO.bat uses an absolute script path.
6. V4.6 scrollable menu/self.main fix and all V4.7 features are preserved.

Recommended Windows use:
- Extract the ZIP completely to a normal folder.
- Double-click INSTALL_AND_RUN.bat.
- If no window appears, double-click DIAGNOSE_AND_RUN.bat and keep the console visible.
