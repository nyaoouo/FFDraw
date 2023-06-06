import typing
import sqlite3

import imgui
import requests
from .utils import TTsImplBase

if typing.TYPE_CHECKING:
    from . import TTS
api_url = r'https://tts.xivcdn.com/api/say'
Voice = [
    'huihui',
    'yaoyao',
    'kangkang',
    'yating',
    'hanhan',
    'tracy',
    'danny',
]


class CafeTTS(TTsImplBase):
    def __init__(self, main: 'TTS'):
        super().__init__(main)
        self.cache_db = main.storage.path / 'cafe_tts_cache.db'
        self.cfg = main.data.get('cafe tts', {})
        self.voice = self.cfg.get('voice', 0)  # hui hui
        self.rate = self.cfg.get('rate', 0)
        main.storage.save()

    def get_content(self, text: str, voice: int = None, rate: int = None):
        if voice is None:
            voice = self.voice
        if rate is None:
            rate = self.rate
        (res := requests.get(api_url, params={
            'text': text,
            'voice': Voice[voice],
            'rate': rate,
        })).raise_for_status()
        return res.content

    def connect_cache_db(self):
        db = sqlite3.connect(self.cache_db)
        db.execute('CREATE TABLE IF NOT EXISTS cache (text TEXT, voice INTEGER, rate INTEGER, content BLOB)')
        return db

    def check_cache(self, text: str, voice: int = None, rate: int = None):
        if voice is None:
            voice = self.voice
        if rate is None:
            rate = self.rate
        db = self.connect_cache_db()
        try:
            res = db.execute('SELECT content FROM cache WHERE text=? AND voice=? AND rate=?', (text, voice, rate)).fetchone()
            if res: return res[0]
        finally:
            db.close()

    def clear_cache(self):
        db = self.connect_cache_db()
        try:
            db.execute('DELETE FROM cache WHERE 1=1')
            db.commit()
        finally:
            db.close()

    def save_cache(self, text: str, content: bytes, voice: int, rate: int):
        db = self.connect_cache_db()
        try:
            db.execute('INSERT INTO cache VALUES (?, ?, ?, ?)', (text, voice, rate, content))
            db.commit()
        finally:
            db.close()

    def tts(self, text: str) -> bytes:
        voice = self.voice
        rate = self.rate
        if (res := self.check_cache(text)) is not None: return res
        res = self.get_content(text, voice, rate)
        self.save_cache(text, res, voice, rate)
        return res

    def render(self):
        imgui.text('voice: ')
        imgui.same_line()
        imgui.push_id('cafe_tts_voice')
        if imgui.button(Voice[self.voice]):
            imgui.open_popup("select")
        if imgui.begin_popup("select"):
            imgui.push_id('select')
            for i, e in enumerate(Voice):
                if imgui.selectable(e)[1]:
                    self.voice = i
                    self.cfg['voice'] = i
                    self.main.storage.save()
            imgui.pop_id()
            imgui.end_popup()
        imgui.pop_id()

        imgui.text('rate: ')
        imgui.same_line()
        changed, new_val = imgui.slider_int('##cafe_tts_rate', self.rate, -10, 10)
        if changed:
            self.rate = new_val
            self.cfg['rate'] = new_val
            self.main.storage.save()

        if imgui.button('clear cache'):
            self.clear_cache()
