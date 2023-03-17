import enum
from win32com import client
from ff_draw.plugins import FFDrawPlugin
import imgui


class TTSType(enum.Enum):
    NULL = 0
    System = 1


def system_tts(msg: str, lang=804, flag=0):
    speak = client.Dispatch("SAPI.SpVoice")
    speak.Voice = speak.GetVoices("", f"language={lang}")[0]
    speak.Speak(msg, flag)


class TTS(FFDrawPlugin):
    def __init__(self, main):
        super().__init__(main)
        self.use_type = self.data.setdefault('use_type', TTSType.System.value)

    def set_use_type(self, use_type: TTSType | int | str):
        if isinstance(use_type, str):
            use_type = TTSType[use_type].value
        elif isinstance(use_type, TTSType):
            use_type = use_type.value
        self.use_type = use_type
        self.data['use_type'] = use_type
        self.storage.save()

    def draw_panel(self):
        imgui.text('use_type: ')
        imgui.same_line()
        imgui.push_id('tts_use_type')
        try:
            selected_key = next(e.name for e in TTSType if e.value == self.use_type)
        except StopIteration:
            self.set_use_type(selected_key := TTSType.NULL.name)
        if imgui.button(selected_key):
            imgui.open_popup("select")
        if imgui.begin_popup("select"):
            imgui.push_id('select')
            for e in TTSType:
                if imgui.selectable(e.name)[1]:
                    self.set_use_type(e.value)
            imgui.pop_id()
            imgui.end_popup()
        imgui.pop_id()

    def speak(self, msg: str, do_async=True):
        self.logger.debug(f'speak: {msg}')
        if self.use_type == TTSType.System.value:
            call = system_tts
        else:
            return
        if do_async:
            self.create_mission(call, msg)
        else:
            call(msg)
