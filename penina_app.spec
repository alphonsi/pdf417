# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['penina/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include test files for proven functionality
        ('tests/', 'tests/'),
    ],
    hiddenimports=[
        # Core dependencies
        'PIL',
        'zxingcpp',
        'pylibdmtx',
        'cv2',
        'numpy',
        'treepoem',
        'xml.etree.ElementTree',
        
        # AAMVA dependencies
        'aamva',
        
        # GUI dependencies
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        
        # Penina modules
        'penina.gui',
        'penina.scanner',
        'penina.encoder',
        'penina.converter',
        'penina.core',
        
        # Test modules (for proven functionality)
        'tests.decoder_xml',
        'tests.encoder_xml',
        'tests.xml_to_aamva_converter',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='penina',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
