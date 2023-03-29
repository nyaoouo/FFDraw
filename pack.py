import os
import pathlib
import shutil
import subprocess
import time
import zipfile

os.chdir('pack_assets')
os.system(
    r'..\venv310\Scripts\pyinstaller --onefile --uac-admin ' +
    '--collect-all=nylib ' +
    '--collect-all=win32com ' +
    '--icon=sage.ico ' +
    '..\main.py'
)
os.system(
    r'..\venv310\Scripts\pyinstaller --onefile --uac-admin ' +
    '--collect-all=nylib ' +
    '--collect-all=win32com ' +
    '--icon=sage.ico ' +
    '..\main_cn.py'
)
os.chdir('../')
shutil.copy(r'pack_assets/dist/main.exe', 'FFDraw.exe')
p = pathlib.Path(time.strftime("pack_assets/release/%Y_%m_%d_%H_%M_%S"))
p.mkdir(parents=True)
with zipfile.ZipFile(p / 'ffd_cn_release.zip', 'w') as zf_cn, zipfile.ZipFile(p / 'ffd_release.zip', 'w') as zf:
    zf_cn.write(r'pack_assets/dist/main_cn.exe', 'FFDraw/FFDraw.exe', compresslevel=9, compress_type=zipfile.ZIP_DEFLATED)
    zf.write(r'pack_assets/dist/main.exe', 'FFDraw/FFDraw.exe', compresslevel=9, compress_type=zipfile.ZIP_DEFLATED)
    for f in subprocess.check_output("git ls-files", shell=True).decode('utf-8').splitlines():
        zf.write(f, 'FFDraw/' + f, compresslevel=9, compress_type=zipfile.ZIP_DEFLATED)
        zf_cn.write(f, 'FFDraw/' + f, compresslevel=9, compress_type=zipfile.ZIP_DEFLATED)

import tkinter as tk
import tkinter.messagebox as msg_box

tk.Tk().withdraw()
if msg_box.askyesno(None, 'open directory?'):
    subprocess.Popen(f'explorer "{p}"')
