import os
import shutil

os.chdir('pack_assets')
os.system(
    r'..\venv\Scripts\pyinstaller --onefile --uac-admin ' +
    '--icon=sage.ico ' +
    '..\main.py'
)
shutil.copy(r'dist/main.exe', '../FFDraw.exe')
