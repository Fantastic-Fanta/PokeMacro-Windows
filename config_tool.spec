# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Config Tool
This file configures how PyInstaller builds the executable for the configuration tool
"""

import os
from pathlib import Path

block_cipher = None

# Get the project root directory (where the spec file is located)
project_root = Path(SPECPATH)

# Analysis for config tool - much simpler than main macro
a = Analysis(
    ['config_tool.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # Include configs.yaml in the executable (optional, user can specify different file)
        ('configs.yaml', '.'),
    ],
    hiddenimports=[
        # Core dependencies for config tool
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'yaml',
        'pathlib',
        'platform',
        # Windows-specific for transparency
        'ctypes',
        'ctypes.wintypes',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude heavy dependencies not needed for config tool
        'matplotlib',
        'pandas',
        'jupyter',
        'IPython',
        'notebook',
        'torch',
        'torchvision',
        'torchaudio',
        'easyocr',
        'cv2',
        'scipy',
        'scikit-image',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ConfigTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Windowed executable (no console window)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # You can add an icon file here if you have one
)

