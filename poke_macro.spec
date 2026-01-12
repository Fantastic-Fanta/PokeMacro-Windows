# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Pokemon Macro
This file configures how PyInstaller builds the executable
"""

import os
from pathlib import Path

block_cipher = None

# Get the project root directory (where the spec file is located)
project_root = Path(SPECPATH)

# Collect all Python files from src/auto_resetter
# Use the wrapper script that uses absolute imports
a = Analysis(
    ['poke_macro_main.py'],
    pathex=[str(project_root), str(project_root / "src")],
    binaries=[],
    datas=[
        # Include configs.yaml in the executable
        ('configs.yaml', '.'),
    ],
    hiddenimports=[
        # Core dependencies
        'pyautogui',
        'easyocr',
        'numpy',
        'PIL',
        'PIL.Image',
        'PIL.ImageEnhance',
        'PIL.ImageFilter',
        'yaml',
        'mss',
        'keyboard',
        'mouse',
        'pynput',
        'pywinauto',
        'pyperclip',
        'pytweening',
        'requests',
        'scipy',
        'scikit-image',
        'tqdm',
        # PyTorch and related (for EasyOCR)
        'torch',
        'torchvision',
        'torchaudio',
        # EasyOCR dependencies
        'easyocr',
        'easyocr.model',
        'easyocr.detection',
        'easyocr.recognition',
        'easyocr.utils',
        # Additional hidden imports that might be needed
        'cv2',
        'skimage',
        'skimage.io',
        'skimage.transform',
        'skimage.filters',
        'skimage.color',
        'skimage.morphology',
        'skimage.measure',
        'skimage.segmentation',
        'skimage.feature',
        'skimage.restoration',
        'skimage.util',
        'skimage.exposure',
        'skimage.draw',
        'skimage.graph',
        'skimage.registration',
        'skimage.metrics',
        'skimage.future',
        'skimage.viewer',
        'skimage.data',
        'skimage._shared',
        'skimage._shared.utils',
        'skimage._shared.filters',
        'skimage._shared.transform',
        'skimage._shared.geometry',
        'skimage._shared.coord',
        'skimage._shared.interpolation',
        'skimage._shared.version_requirements',
        # Windows-specific
        'win32api',
        'win32con',
        'win32gui',
        'win32process',
        'win32clipboard',
        'pywintypes',
        'pythoncom',
        'comtypes',
        'comtypes.client',
        'comtypes.gen',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'matplotlib',
        'tkinter',
        'pandas',
        'jupyter',
        'IPython',
        'notebook',
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
    name='PokeMacro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False if you want a windowless executable
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # You can add an icon file here if you have one
)

