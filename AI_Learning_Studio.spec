# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hidden = []
for pkg in ("sympy", "PIL", "cv2", "serial"):
    try:
        hidden += collect_submodules(pkg)
    except Exception:
        pass

a = Analysis(
    ["launcher.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("ai_learning_studio.py", "."),
        ("data/tc_learning.zip", "data"),
        ("data/manifest.json", "data"),
        ("README_TH.txt", "."),
    ],
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name="AI_Learning_Studio_v59",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
)
