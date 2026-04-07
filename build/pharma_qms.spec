# -*- mode: python ; coding: utf-8 -*-
import os

project_dir = os.path.abspath(os.path.join(SPECPATH, ".."))
backend_dir = os.path.join(project_dir, "backend")
frontend_dist = os.path.join(project_dir, "frontend", "dist")
data_dir = os.path.join(project_dir, "data")

a = Analysis(
    [os.path.join(backend_dir, "run.py")],
    pathex=[backend_dir],
    binaries=[],
    datas=[
        (frontend_dist, "frontend/dist"),
        (data_dir, "data"),
    ],
    hiddenimports=[
        "app",
        "app.change_management",
        "app.change_management.model",
        "app.change_management.controller",
        "app.change_management.view",
        "app.utils",
        "app.utils.const",
        "app.utils.logger",
        "app.utils.input_output",
        "config",
        "waitress",
        "sqlalchemy.dialects.sqlite",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib", "numpy", "PIL"],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="PharmaQMS",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="PharmaQMS",
)
