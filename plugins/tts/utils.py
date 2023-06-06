import logging
import os
import pathlib
import queue
import subprocess
import tempfile
import tarfile
import gzip
import threading
import time
import typing

import requests

if typing.TYPE_CHECKING:
    from . import TTS

local_ffmpeg = pathlib.Path(os.environ['ExcPath']) / 'res' / 'ffmpeg'
logger = logging.getLogger('OnlineTTS')
_is_init = False


def check(cmd):
    try:
        return subprocess.check_output(cmd)
    except:
        return None


# ffmpeg https://registry.npmmirror.com/-/binary/ffmpeg-static/b5.0.1/win32-x64.gz win32-x64
# ffplay https://registry.npmmirror.com/ffplay-static/-/ffplay-static-3.2.2.tgz package/bin/win32/x64/ffplay.exe
# ffprobe https://registry.npmmirror.com/ffprobe-static/-/ffprobe-static-3.1.0.tgz package/bin/win32/x64/ffprobe.exe

def download_to_temp(url):
    r = requests.get(url, stream=True)
    r.raise_for_status()
    temp = tempfile.TemporaryFile(delete=False)
    start_time = time.time()
    content_length = int(r.headers.get('content-length', 0))
    for chunk in r.iter_content(chunk_size=8192):
        temp.write(chunk)
        if start_time + 5 < time.time():
            logger.debug(f'Downloading {url} {temp.tell()}/{content_length}')
            start_time = time.time()
    temp.seek(0)
    return temp


def download_and_save_ffmpeg(path: pathlib.Path):
    temp = download_to_temp('https://registry.npmmirror.com/-/binary/ffmpeg-static/b5.0.1/win32-x64.gz')
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(temp, 'rb') as f, open(path, 'wb') as f2:
        f2.write(f.read())
    temp.close()
    os.unlink(temp.name)


def download_and_save_ffplay(path: pathlib.Path):
    temp = download_to_temp('https://registry.npmmirror.com/ffplay-static/-/ffplay-static-3.2.2.tgz')
    path.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(temp.name, 'r:gz') as f, open(path, 'wb') as f2:
        f2.write(f.extractfile('package/bin/win32/x64/ffplay.exe').read())
    temp.close()
    os.unlink(temp.name)


def download_and_save_ffprobe(path: pathlib.Path):
    temp = download_to_temp('https://registry.npmmirror.com/ffprobe-static/-/ffprobe-static-3.1.0.tgz')
    path.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(temp.name, 'r:gz') as f, open(path, 'wb') as f2:
        f2.write(f.extractfile('package/bin/win32/x64/ffprobe.exe').read())
    temp.close()
    os.unlink(temp.name)


def init_env():
    global _is_init
    if _is_init: return
    _is_init = True
    # add local ffmpeg to path
    if str(local_ffmpeg) not in os.environ['PATH']:
        os.environ['PATH'] += os.pathsep + str(local_ffmpeg)

    if not check("ffmpeg -version"):
        download_and_save_ffmpeg(local_ffmpeg / 'ffmpeg.exe')
        assert check("ffmpeg -version")
    if not check("ffplay -version"):
        download_and_save_ffplay(local_ffmpeg / 'ffplay.exe')
        assert check("ffplay -version")
    if not check("ffprobe -version"):
        download_and_save_ffprobe(local_ffmpeg / 'ffprobe.exe')
        assert check("ffprobe -version")

    # fix pydub playback temp file issue
    from pydub import playback

    def _play_with_ffplay(seg):
        PLAYER = playback.get_player_name()
        f = tempfile.NamedTemporaryFile("w+b", suffix=".wav", delete=False)
        try:
            seg.export(f.name, "wav")
            subprocess.call([PLAYER, "-nodisp", "-autoexit", "-hide_banner", "-loglevel", "quiet", f.name])
        finally:
            f.close()
            os.unlink(f.name)

    playback._play_with_ffplay = _play_with_ffplay


def play(buffer: typing.IO):
    from pydub import playback, AudioSegment
    playback.play(AudioSegment.from_file(buffer))


class Player:
    def __init__(self):
        self.thread = None
        self.queue = queue.Queue()

    def run(self):
        init_env()
        from pydub import playback, AudioSegment
        while True:
            buf = self.queue.get()
            playback.play(AudioSegment.from_file(buf))

    def run_thread(self):
        if self.thread and self.thread.is_alive(): return self.thread
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
        return self.thread

    def play(self, buffer: typing.IO):
        self.queue.put(buffer)
        self.run_thread()


class TTsImplBase:
    def __init__(self, main: 'TTS'):
        self.main = main

    def tts(self, text: str) -> bytes:
        raise NotImplementedError()

    def render(self):
        pass
