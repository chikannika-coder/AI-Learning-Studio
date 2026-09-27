from pathlib import Path
import runpy, os, sys
base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
os.chdir(base)
runpy.run_path(str(base / "ai_learning_studio.py"), run_name="__main__")
