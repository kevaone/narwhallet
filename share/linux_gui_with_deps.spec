# -*- mode: python ; coding: utf-8 -*-
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks
from kivy.utils import platform

block_cipher = None

kivy_deps = get_deps_minimal(video=None, audio=None)

if platform == 'win':
    kivy_deps['hiddenimports'].append('win32timezone')

a = Analysis(['../main.py'],
             pathex=[],
             binaries=kivy_deps['binaries'],
             datas=[('../main.kv', '.'), ('../config', './config/'),('../narwhallet/core/kui/widgets/', './narwhallet/core/kui/widgets/'),('../narwhallet/core/kui/screens', './narwhallet/core/kui/screens/'),('../narwhallet/core/kui/assets', './narwhallet/core/kui/assets/'), ('../narwhallet/core/kui/fonts/', './narwhallet/core/kui/fonts/'),('../narwhallet/core/kcl/bip_utils/bip39/bip39_words/','./narwhallet/core/kcl/bip_utils/bip39/bip39_words/')],
             hiddenimports=kivy_deps['hiddenimports'],
             hookspath=hookspath(),
             hooksconfig={},
             runtime_hooks=runtime_hooks(),
             excludes=kivy_deps['excludes'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False,
             #**get_deps_minimal(video=None, audio=None)
             )

#splash = Splash('../narwhallet/core/kui/assets/narwhal.png',
#               binaries=a.binaries,
#                datas=a.datas,
#                text_pos=(10, 50),
#                text_size=12,
#                text_color='black')

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Narwhallet',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='../narwhallet/core/kui/assets/narwhal.png')