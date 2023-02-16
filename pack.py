import os
import shutil
import subprocess
import time
import zipfile

os.chdir('pack_assets')
os.system(
    r'..\venv\Scripts\pyinstaller --onefile --uac-admin ' +
    '--icon=sage.ico ' +
    '..\main.py'
)
os.chdir('../')
with zipfile.ZipFile(time.strftime("pack_assets/release/ffd_release_%Y_%m_%d_%H_%M_%S.zip"), 'w') as zf:
    zf.write(r'pack_assets/dist/main.exe', 'FFDraw/FFDraw.exe', compresslevel=9, compress_type=zipfile.ZIP_DEFLATED)
    for f in subprocess.check_output("git ls-files", shell=True).decode('utf-8').splitlines():
        zf.write(f, 'FFDraw/' + f, compresslevel=9,compress_type=zipfile.ZIP_DEFLATED)
